"""
Hybrid Weighted Risk Ensemble Scorer
--------------------------------------
Fuses 4 detection layers into a unified 0-100 risk score.

Layer weights (calibrated by layer-by-layer ablation study):
  - Rules      : 20%  (high precision, low recall)
  - Statistical: 10%  (z-score anomaly baseline)
  - ML         : 40%  (highest single-layer F1: 98.8%)
  - Graph      : 30%  (community + motif topology signals)

Hard Rule Overrides:
  If a high-confidence compliance rule fires (e.g., rapid_cashout OR structuring
  AND ML prob >= 0.4), the score receives a minimum floor of 40.0 regardless of
  the weighted combination. This mirrors real-world bank policy: certain
  rule violations are always escalated to at least MEDIUM review.
"""

import numpy as np


class EnsembleScorer:
    # Calibrated weights based on layer ablation results
    def __init__(
        self,
        rule_weight:  float = 0.20,
        stat_weight:  float = 0.10,
        ml_weight:    float = 0.40,
        graph_weight: float = 0.30,
    ):
        self.w_rule  = rule_weight
        self.w_stat  = stat_weight
        self.w_ml    = ml_weight
        self.w_graph = graph_weight

    def compute_graph_score(self, row) -> float:
        """
        Normalised graph risk score (0.0-1.0).
        Combines PageRank, Louvain community risk, and structural motif flags.
        """
        pr        = float(row.get("pagerank_score",        0.0))
        comm_risk = float(row.get("community_risk_score",  0.0))

        is_cycle   = int(row.get("is_cycle_edge",   0))
        is_fan_out = int(row.get("is_fan_out_edge", 0))
        is_fan_in  = int(row.get("is_fan_in_edge",  0))
        is_chain   = int(row.get("is_chain_edge",   0))

        # Scale PageRank — typical values in our graph are 0.00005-0.005
        pr_score = min(pr * 20.0, 1.0)

        # Motif signal — prioritised by severity
        if is_fan_out or is_fan_in:
            motif_val = 0.95   # smurfing / aggregation — highest severity
        elif is_chain:
            motif_val = 0.85   # layering chain
        elif is_cycle:
            motif_val = 0.75   # round-tripping cycle
        else:
            motif_val = 0.0

        # Weighted combination of three independent graph signals
        graph_risk = (
            0.25 * pr_score +
            0.40 * comm_risk +    # strongest signal: community contamination
            0.35 * motif_val      # strong signal: topological pattern
        )
        return min(graph_risk, 1.0)

    def calculate_score(self, row, ml_prob: float) -> tuple:
        """
        Returns (final_score: float 0-100, risk_category: str LOW/MEDIUM/HIGH).

        Scoring logic:
          1. Compute weighted sum of all four layers.
          2. Apply hard floor overrides for high-confidence rule violations
             that the model confirms (ML prob >= 0.4).
          3. Map to risk category.
        """
        rule_score  = float(row.get("rule_score",        0.0))
        stat_score  = float(row.get("statistical_score", 0.0))
        ml_score    = float(ml_prob)
        graph_score = self.compute_graph_score(row)

        # ── Weighted combination ───────────────────────────────────────────
        combined = (
            self.w_rule  * rule_score +
            self.w_stat  * stat_score +
            self.w_ml    * ml_score   +
            self.w_graph * graph_score
        )
        final_score = round(combined * 100.0, 1)

        # ── Hard rule overrides (bank policy floors) ───────────────────────
        # These mirror real AML policies: certain rule violations are ALWAYS
        # escalated to at least MEDIUM review when ML supports the signal.
        is_rapid_cashout      = int(row.get("is_rapid_cashout",      0))
        is_structuring        = int(row.get("is_structuring_amount",  0))
        structuring_flag      = int(row.get("structuring_flag",       0))
        rapid_cashout_flag    = int(row.get("rapid_cashout_flag",     0))
        velocity_flag         = int(row.get("velocity_flag",          0))

        # Rapid cashout override: always at least MEDIUM when ML is suspicious
        if (is_rapid_cashout == 1 or rapid_cashout_flag == 1) and ml_score >= 0.35:
            final_score = max(final_score, 42.0)

        # Structuring override: near-threshold amounts with velocity
        if (is_structuring == 1 or structuring_flag == 1) and ml_score >= 0.35:
            final_score = max(final_score, 40.0)

        # High-velocity + ML confirmation
        if velocity_flag == 1 and ml_score >= 0.5:
            final_score = max(final_score, 38.0)

        final_score = min(final_score, 100.0)

        # ── Risk category ──────────────────────────────────────────────────
        if final_score >= 70.0:
            category = "HIGH"
        elif final_score >= 38.0:
            category = "MEDIUM"
        else:
            category = "LOW"

        return final_score, category

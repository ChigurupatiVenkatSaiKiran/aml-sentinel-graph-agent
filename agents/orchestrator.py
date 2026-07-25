"""
Master Agent Orchestrator & Deterministic Intent Parser
---------------------------------------------------------
Parses natural language queries from the compliance dashboard.
Routes each query to the correct detection engine combination --
no live LLM dependency, fully deterministic and demo-safe.
"""

import re
import pandas as pd
from detection.rule_engine import ComplianceRuleEngine
from detection.statistical import StatisticalAnomalyDetector
from detection.ml_models import MLModelManager
from detection.ensemble_scorer import EnsembleScorer
from explainability.counterfactual import generate_counterfactuals
from explainability.sar_generator import generate_sar_narrative
from graph.visualizer import generate_interactive_graph


class AMLOrchestrator:
    def __init__(
        self,
        full_df: pd.DataFrame,
        graph,
        ml_manager: MLModelManager,
        n_train: int = None,
    ):
        self.df         = full_df
        self.graph      = graph
        self.ml_manager = ml_manager

        self.rule_engine   = ComplianceRuleEngine()
        self.stat_detector = StatisticalAnomalyDetector()
        self.ensemble      = EnsembleScorer()

        # Fit statistical baselines on training portion only (no leakage)
        # n_train is the exact boundary from the loader; fall back to 80%
        split = n_train if n_train is not None else int(len(full_df) * 0.8)
        self.stat_detector.fit(full_df.iloc[:split])

    # -- Intent Parser ----------------------------------------------------------

    def parse_intent(self, query: str) -> dict:
        """
        Fast keyword/regex router -- no network calls, never fails in demo.
        Returns a plan dict with: intent, filters, components, reasoning.

        Dynamically selects which tools/components to invoke based on query intent.
        Not every query invokes every tool -- selection is query-driven (per PS1 requirements).
        """
        q = query.lower()
        plan = {"intent": "general", "filters": {}, "components": [], "reasoning": ""}

        # 0. Extract date/time filter if present (e.g. "last 30 days", "last week")
        date_match = re.search(r"last\s+(\d+)\s+(day|days|week|weeks|month|months)", q)
        if date_match:
            num = int(date_match.group(1))
            unit = date_match.group(2)
            if "month" in unit:
                num *= 30
            elif "week" in unit:
                num *= 7
            plan["filters"]["date_days"] = num

        # 1. Aggregation / count queries - checked FIRST to avoid collision
        # e.g. "Which customers made 10+ transactions under $10,000?" -> rules only, no ML
        if re.search(r"\d+\+?\s*transaction|how many|count\b|frequen|velocity", q):
            plan.update(
                intent="aggregation",
                components=["rule_engine", "statistical"],
                reasoning=(
                    "Detected AGGREGATION / COUNT query -> running rule-based threshold aggregation "
                    "and statistical frequency profiling only. "
                    "ML model and graph traversal not required for this query type."
                ),
            )
            return plan

        # 2. Structuring / threshold queries
        if any(w in q for w in ["structur", "threshold", "under $10", "8000", "9000", "ctr"]):
            plan.update(
                intent="structuring",
                components=["rule_engine", "graph_detector"],
                reasoning=(
                    "Detected STRUCTURING query -> activating rule engine threshold checks "
                    "and graph fan-out pattern matching. "
                    + (f"Applying date filter: last {plan['filters'].get('date_days', 'N/A')} days. " if "date_days" in plan["filters"] else "")
                    + "Bypassing broad statistical profiling and full-dataset ML sweep."
                ),
            )
            return plan

        # 3. Single entity lookup (customer ID in query)
        acc_match = re.search(r"\b(acc\d{4,6})\b", q)
        cust_match = re.search(r"customer\s+#?([a-z0-9]+)", q)
        target = None
        if acc_match:
            target = acc_match.group(1).upper()
        elif cust_match:
            target = cust_match.group(1).upper()

        if target:
            plan.update(
                intent="entity",
                filters={**plan["filters"], "account_id": target},
                components=["entity_lookup", "ml_model", "graph_detector", "explainer"],
                reasoning=(
                    f"Detected ENTITY query for account [{target}] -> "
                    "running single-entity ML risk scoring, graph neighbourhood analysis, "
                    "counterfactual explainer, and auto-SAR generation. "
                    "Skipped full-dataset sweep."
                ),
            )
            return plan

        # 4. Network / community / mule ring
        if any(w in q for w in ["network", "ring", "cluster", "community", "mule", "connect", "graph"]):
            plan.update(
                intent="network",
                components=["graph_detector", "visualizer"],
                reasoning=(
                    "Detected NETWORK query -> activating graph community traversal "
                    "and PyVis ring visualisation. Bypassing numerical rule engine."
                ),
            )
            return plan

        # 5. Broad / full dataset sweep
        if any(w in q for w in ["analyse", "analyze", "overview", "all", "broad", "whole", "full", "suspicious activity"]):
            plan.update(
                intent="broad",
                components=["rule_engine", "statistical", "ml_model", "graph_detector"],
                reasoning=(
                    "Detected BROAD ANALYSIS query -> running all four detection layers "
                    "across sampled dataset. This may take a few seconds."
                ),
            )
            return plan

        # Default
        plan.update(
            intent="general",
            components=["rule_engine", "ml_model"],
            reasoning="General query -> invoking compliance rules and RandomForest classifier.",
        )
        return plan


    # -- Execution Engine -------------------------------------------------------

    def _score_rows(self, subset: pd.DataFrame):
        """Score a subset DataFrame with all four layers. Returns subset with risk columns."""
        if subset.empty:
            return subset

        subset = subset.copy().reset_index(drop=True)
        ml_probs = self.ml_manager.predict_probabilities(subset)

        risk_scores, risk_cats = [], []
        rule_scores_all, stat_scores_all = [], []

        for pos, (_, row) in enumerate(subset.iterrows()):
            r_flags = self.rule_engine.evaluate_transaction(row)
            s_flags = self.stat_detector.evaluate_transaction(row)
            row_dict = {**row.to_dict(), **r_flags, **s_flags}
            score, cat = self.ensemble.calculate_score(row_dict, float(ml_probs[pos]))
            risk_scores.append(score)
            risk_cats.append(cat)
            rule_scores_all.append(r_flags["rule_score"])
            stat_scores_all.append(s_flags["statistical_score"])

        subset["risk_score"]    = risk_scores
        subset["risk_category"] = risk_cats
        subset["rule_score"]    = rule_scores_all
        subset["statistical_score"] = stat_scores_all
        return subset

    def execute_plan(self, plan: dict) -> dict:
        """Executes the parsed plan and returns results dict."""
        results = {
            "execution_log":         plan["reasoning"],
            "intent":                plan["intent"],
            "flagged_transactions":  pd.DataFrame(),
            "selected_row":          None,
            "sar_narrative":         "",
            "counterfactuals":       [],
            "graph_html_path":       "",
        }

        intent     = plan["intent"]
        account_id = plan["filters"].get("account_id")
        date_days  = plan["filters"].get("date_days")

        # Apply date filter to working dataframe if specified
        working_df = self.df
        if date_days:
            cutoff = working_df["timestamp"].max() - pd.Timedelta(days=date_days)
            working_df = working_df[working_df["timestamp"] >= cutoff]

        # -- ENTITY intent --------------------------------------------------
        if intent == "entity":
            subset = self.df[
                (self.df["sender_id"] == account_id)
                | (self.df["receiver_id"] == account_id)
            ]

            if subset.empty:
                results["execution_log"] = (
                    f"Account {account_id} not found in transaction database. "
                    "Try a different account ID."
                )
                return results

            scored = self._score_rows(subset)
            results["flagged_transactions"] = scored.sort_values("risk_score", ascending=False)

            best = scored.loc[scored["risk_score"].idxmax()]
            results["selected_row"] = best

            cfs = generate_counterfactuals(best)
            results["counterfactuals"] = cfs
            results["sar_narrative"]   = generate_sar_narrative(
                best, best["risk_score"], best["risk_category"], cfs
            )

            node_scores = {}
            for _, r in scored.iterrows():
                node_scores[r["sender_id"]]   = max(node_scores.get(r["sender_id"],   0.0), r["risk_score"])
                node_scores[r["receiver_id"]] = max(node_scores.get(r["receiver_id"], 0.0), r["risk_score"])

            results["graph_html_path"] = generate_interactive_graph(
                self.graph.G, center_node=account_id, scores_dict=node_scores
            )

        # -- STRUCTURING intent ---------------------------------------------
        elif intent == "structuring":
            subset = working_df[working_df["is_structuring_amount"] == 1]
            node_scores = {}
            if not subset.empty:
                scored = self._score_rows(subset)
                results["flagged_transactions"] = scored.sort_values("risk_score", ascending=False)

                best = scored.loc[scored["risk_score"].idxmax()]
                results["selected_row"] = best
                cfs = generate_counterfactuals(best)
                results["counterfactuals"] = cfs
                results["sar_narrative"]   = generate_sar_narrative(
                    best, best["risk_score"], best["risk_category"], cfs
                )
                
                for _, r in scored.iterrows():
                    node_scores[r["sender_id"]]   = max(node_scores.get(r["sender_id"],   0.0), r["risk_score"])
                    node_scores[r["receiver_id"]] = max(node_scores.get(r["receiver_id"], 0.0), r["risk_score"])

            results["graph_html_path"] = generate_interactive_graph(
                self.graph.G, max_nodes=40, scores_dict=node_scores
            )

        # -- AGGREGATION intent (e.g. "which customers made 10+ transactions under $10k")
        # Only invokes rule_engine + statistical. Skips ML model and graph traversal.
        elif intent == "aggregation":
            rule_flagged = working_df[
                (working_df["is_structuring_amount"] == 1)
                | (working_df.get("tx_count_7d", 0) >= 10)
            ] if "tx_count_7d" in working_df.columns else working_df[
                working_df["is_structuring_amount"] == 1
            ]
            if not rule_flagged.empty:
                # Score with rules + statistical only (no ML inference)
                subset = rule_flagged.copy().reset_index(drop=True)
                rule_s, stat_s, risk_s, risk_c = [], [], [], []
                for _, row in subset.iterrows():
                    r_flags = self.rule_engine.evaluate_transaction(row)
                    s_flags = self.stat_detector.evaluate_transaction(row)
                    rule_s.append(r_flags["rule_score"])
                    stat_s.append(s_flags["statistical_score"])
                    combined = r_flags["rule_score"] * 0.5 + s_flags["statistical_score"] * 0.5
                    risk_s.append(combined)
                    risk_c.append("HIGH" if combined >= 50 else "MEDIUM" if combined >= 25 else "LOW")
                subset["risk_score"]        = risk_s
                subset["risk_category"]     = risk_c
                subset["rule_score"]        = rule_s
                subset["statistical_score"] = stat_s
                results["flagged_transactions"] = subset.sort_values("risk_score", ascending=False)

                node_scores = {}
                for _, r in subset.iterrows():
                    node_scores[r["sender_id"]]   = max(node_scores.get(r["sender_id"],   0.0), r["risk_score"])
                    node_scores[r["receiver_id"]] = max(node_scores.get(r["receiver_id"], 0.0), r["risk_score"])

                results["graph_html_path"] = generate_interactive_graph(
                    self.graph.G, max_nodes=40, scores_dict=node_scores
                )

        # -- NETWORK intent -------------------------------------------------
        elif intent == "network":
            motif_sub = self.df[
                (self.df["is_cycle_edge"]   == 1)
                | (self.df["is_fan_out_edge"] == 1)
                | (self.df["is_fan_in_edge"]  == 1)
                | (self.df["is_chain_edge"]   == 1)
            ]
            node_scores = {}
            if not motif_sub.empty:
                scored = self._score_rows(motif_sub)
                results["flagged_transactions"] = scored.sort_values("risk_score", ascending=False)
                for _, r in scored.iterrows():
                    node_scores[r["sender_id"]]   = max(node_scores.get(r["sender_id"],   0.0), r["risk_score"])
                    node_scores[r["receiver_id"]] = max(node_scores.get(r["receiver_id"], 0.0), r["risk_score"])

            results["graph_html_path"] = generate_interactive_graph(
                self.graph.G, max_nodes=50, scores_dict=node_scores
            )

        # -- BROAD / GENERAL intent -----------------------------------------
        else:
            sample = self.df.sample(n=min(500, len(self.df)), random_state=42)
            scored = self._score_rows(sample)
            results["flagged_transactions"] = scored.sort_values("risk_score", ascending=False)

            node_scores = {}
            for _, r in scored.iterrows():
                node_scores[r["sender_id"]]   = max(node_scores.get(r["sender_id"],   0.0), r["risk_score"])
                node_scores[r["receiver_id"]] = max(node_scores.get(r["receiver_id"], 0.0), r["risk_score"])

            results["graph_html_path"] = generate_interactive_graph(
                self.graph.G, max_nodes=40, scores_dict=node_scores
            )

        return results

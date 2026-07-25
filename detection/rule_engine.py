"""
Compliance Rule Engine
----------------------
Deterministic heuristic engine implementing core anti-money laundering patterns:
1. Structuring (smurfing/transactions just under threshold)
2. Rapid Cash-out
3. High transaction frequency (velocity)
"""

import pandas as pd

class ComplianceRuleEngine:
    def __init__(self):
        # standard AML parameters
        self.structuring_min = 8000.0
        self.structuring_max = 9999.99
        self.velocity_count_threshold = 8
        self.rapid_cashout_hours = 2.0

    def evaluate_transaction(self, row) -> dict:
        """
        Evaluates a single transaction row against compliance rules.
        Returns a dict of flags and rule scores.
        """
        flags = {
            "structuring_flag": 0,
            "velocity_flag": 0,
            "rapid_cashout_flag": 0,
            "rule_score": 0.0
        }
        
        # 1. Structuring Check
        amount = float(row.get("amount", 0.0))
        if self.structuring_min <= amount <= self.structuring_max:
            flags["structuring_flag"] = 1
            
        # 2. High Frequency/Velocity Check
        # Uses pre-computed tx_count_1d
        tx_count_1d = int(row.get("tx_count_1d", 0))
        if tx_count_1d >= self.velocity_count_threshold:
            flags["velocity_flag"] = 1
            
        # 3. Rapid Cashout Check
        is_rapid_cashout = int(row.get("is_rapid_cashout", 0))
        if is_rapid_cashout == 1:
            flags["rapid_cashout_flag"] = 1
            
        # Compute dynamic rule score (0.0 to 1.0)
        active_rules = sum([flags["structuring_flag"], flags["velocity_flag"], flags["rapid_cashout_flag"]])
        flags["rule_score"] = float(active_rules / 3.0)
        
        return flags
        
    def evaluate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies rule checks across a full DataFrame."""
        results = []
        for _, row in df.iterrows():
            results.append(self.evaluate_transaction(row))
        return pd.concat([df.reset_index(drop=True), pd.DataFrame(results)], axis=1)

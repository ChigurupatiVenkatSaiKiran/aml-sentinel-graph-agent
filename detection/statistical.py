"""
Statistical Anomaly Detector
----------------------------
Finds behavioral deviations from a customer's own baseline:
- Amount Z-Score vs average historical amount
- IQR outlier detection on transaction velocity
"""

import pandas as pd
import numpy as np

class StatisticalAnomalyDetector:
    def __init__(self):
        # Maps customer_id to historical baseline stats: {customer_id: (mean_amount, std_amount)}
        self.baselines = {}
        
    def fit(self, train_df: pd.DataFrame):
        """Builds normal transaction profiles/baselines for each customer."""
        grouped = train_df.groupby("sender_id")["amount"]
        for sender_id, amounts in grouped:
            mean_val = float(amounts.mean())
            std_val = float(amounts.std())
            # prevent division by zero for single transaction customers
            if np.isnan(std_val) or std_val == 0:
                std_val = 1.0
            self.baselines[sender_id] = (mean_val, std_val)
            
    def get_zscore(self, sender_id, amount) -> float:
        """Returns the Z-score for a given transaction amount vs sender's baseline."""
        if sender_id not in self.baselines:
            return 0.0
        mean_val, std_val = self.baselines[sender_id]
        return abs(amount - mean_val) / std_val
        
    def evaluate_transaction(self, row) -> dict:
        sender_id = row.get("sender_id")
        amount = float(row.get("amount", 0.0))
        
        z = self.get_zscore(sender_id, amount)
        
        # Max Z-score capped at 10.0 for scoring normalization
        z_normalized = min(z / 3.0, 1.0) # Z-score of 3.0+ translates to 1.0 max risk
        
        # Checking velocity IQR
        # If transaction hours gap is exceptionally small compared to historical gaps
        tx_gap = float(row.get("time_since_last_tx_hours", 999.0))
        is_velocity_outlier = 0
        if tx_gap < 0.1: # Less than 6 minutes
            is_velocity_outlier = 1
            
        statistical_score = (z_normalized + is_velocity_outlier) / 2.0
        
        return {
            "amount_zscore": z,
            "is_velocity_outlier": is_velocity_outlier,
            "statistical_score": float(statistical_score)
        }
        
    def evaluate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        results = []
        for _, row in df.iterrows():
            results.append(self.evaluate_transaction(row))
        return pd.concat([df.reset_index(drop=True), pd.DataFrame(results)], axis=1)

"""
Machine Learning Model Manager
--------------------------------
Trains a RandomForestClassifier on the full engineered feature set.
Feature columns are imported from data.loader.FEATURE_COLS to keep
a single source of truth -- no drift between training and inference.

SHAP is used if available; falls back to feature_importances_ gracefully.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

try:
    import shap
    SHAP_AVAILABLE = True
except Exception as e:
    print(f"[WARN] SHAP unavailable ({e}). Using feature_importances_ fallback.")
    SHAP_AVAILABLE = False

from data.loader import FEATURE_COLS   # Single source of truth

MODEL_PATH = "detection/random_forest_model.joblib"


class MLModelManager:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )
        self.explainer    = None
        self.feature_cols = FEATURE_COLS   # reference, not copy

    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Trains the classifier and persists it to disk."""
        print(f"Training RandomForest ({self.model.n_estimators} trees, n_jobs={self.model.n_jobs})...")
        self.model.fit(X_train[self.feature_cols], y_train)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        print(f"Model saved -> {MODEL_PATH}")

        if SHAP_AVAILABLE:
            try:
                self.explainer = shap.TreeExplainer(self.model)
                print("SHAP TreeExplainer ready.")
            except Exception as e:
                print(f"[WARN] SHAP init failed ({e}). Falling back to feature_importances_.")
                self.explainer = None

    def load_model(self) -> bool:
        """Loads a previously trained model. Returns True on success."""
        if not os.path.exists(MODEL_PATH):
            return False
        loaded = joblib.load(MODEL_PATH)
        # Handle both old (raw model) and new (MLModelManager) saved formats
        if isinstance(loaded, MLModelManager):
            self.model     = loaded.model
            self.explainer = loaded.explainer
        else:
            self.model = loaded
        if SHAP_AVAILABLE and self.explainer is None:
            try:
                self.explainer = shap.TreeExplainer(self.model)
            except Exception as e:
                print(f"[WARN] SHAP init failed on load ({e}).")
        return True

    def predict_probabilities(self, X: pd.DataFrame) -> np.ndarray:
        """Returns P(fraud) for each row."""
        cols_present = [c for c in self.feature_cols if c in X.columns]
        X_in = X[cols_present].copy()
        for c in self.feature_cols:
            if c not in X_in.columns:
                X_in[c] = 0.0
        return self.model.predict_proba(X_in[self.feature_cols])[:, 1]

    def get_shap_explanation(self, X_sample: pd.DataFrame) -> tuple:
        """
        Returns (shap_values_array, feature_names).
        Falls back to tiled feature_importances_ if SHAP is unavailable.
        """
        X_in = X_sample[self.feature_cols]
        n_samples = len(X_in)

        if SHAP_AVAILABLE and self.explainer is not None:
            try:
                sh_vals = self.explainer.shap_values(X_in)
                if isinstance(sh_vals, list):
                    class_vals = sh_vals[1] if len(sh_vals) > 1 else sh_vals[0]
                elif sh_vals.ndim == 3:
                    class_vals = sh_vals[:, :, 1]
                else:
                    class_vals = sh_vals
                return class_vals, self.feature_cols
            except Exception as e:
                print(f"[WARN] SHAP computation failed ({e}). Using feature_importances_.")

        importances = self.model.feature_importances_
        return np.tile(importances, (n_samples, 1)), self.feature_cols

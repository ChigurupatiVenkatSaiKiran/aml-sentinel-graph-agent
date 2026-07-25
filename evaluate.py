"""
AML Sentinel Evaluation Harness & Ablation Study
--------------------------------------------------
Evaluates the hybrid detection system using two rigorous protocols:
1. Stratified 80/20 Train/Test Split:
   - Computes raw confusion matrices (TP, FP, FN, TN) per layer.
   - Calculates False Positive reduction.
   - Breaks down metrics per typology.
2. Stratified 5-Fold Cross-Validation:
   - Recalculates community risks inside each fold to prevent leakage.
   - Reports Mean and Standard Deviation of Recall, Precision, and F1.
"""

import os
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold

from data.loader import load_processed_data, FEATURE_COLS
from detection.rule_engine import ComplianceRuleEngine
from detection.statistical import StatisticalAnomalyDetector
from detection.ml_models import MLModelManager
from detection.ensemble_scorer import EnsembleScorer
from graph.network_builder import TransactionGraph


def run_evaluation():
    print("=" * 60)
    print("           AML SENTINEL -- EVALUATION HARNESS")
    print("=" * 60)

    # 1. Load baseline processed dataset (graph built, no community risks yet)
    df, main_graph, _ = load_processed_data()
    df = df.sort_values("timestamp").reset_index(drop=True)
    
    y = df["is_fraud"].copy()
    
    # ─── SECTION 1: 5-FOLD CROSS-VALIDATION (LEAKAGE-FREE) ────────────────────
    print("\nRunning Stratified 5-Fold Cross-Validation (re-calculating community risks per fold)...")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    cv_recalls, cv_precisions, cv_f1s = [], [], []
    
    for fold, (train_idx, test_idx) in enumerate(skf.split(df, y), 1):
        # 1. Fit community risk on training labels only
        train_df = df.iloc[train_idx]
        train_fraud_accounts = set(
            train_df.loc[train_df["is_fraud"] == 1, "sender_id"].tolist()
            + train_df.loc[train_df["is_fraud"] == 1, "receiver_id"].tolist()
        )
        fold_labels = {acc: 1 for acc in train_fraud_accounts}
        
        # Fresh graph to prevent cross-fold pollution
        fold_graph = TransactionGraph()
        fold_graph.build_graph(df)
        fold_graph.compute_community_risks(fold_labels)
        
        # Apply fold-specific community risk (sender only)
        fold_df = df.copy()
        fold_df["community_risk_score"] = [fold_graph.get_community_risk(sid) for sid in fold_df["sender_id"]]

        # Separate features
        X_fold = fold_df[FEATURE_COLS]
        X_train_fold, y_train_fold = X_fold.iloc[train_idx], y.iloc[train_idx]
        X_test_fold, y_test_fold = X_fold.iloc[test_idx], y.iloc[test_idx]
        
        # Fit models
        ml_fold = MLModelManager()
        ml_fold.train(X_train_fold, y_train_fold)
        
        rule_fold = ComplianceRuleEngine()
        stat_fold = StatisticalAnomalyDetector()
        stat_fold.fit(train_df)
        
        ensemble_fold = EnsembleScorer()
        
        # Predict on fold test set
        ml_probs_fold = ml_fold.predict_probabilities(X_test_fold)
        fold_test_df = fold_df.iloc[test_idx].reset_index(drop=True)

        preds = []
        for pos, (_, row) in enumerate(fold_test_df.iterrows()):
            r_flags = rule_fold.evaluate_transaction(row)
            s_flags = stat_fold.evaluate_transaction(row)
            ml_p = float(ml_probs_fold[pos])

            row_dict = {**row.to_dict(), **r_flags, **s_flags}
            score, _ = ensemble_fold.calculate_score(row_dict, ml_p)
            preds.append(1 if score >= 35.0 else 0)

        cv_recalls.append(recall_score(y_test_fold, preds, zero_division=0))
        cv_precisions.append(precision_score(y_test_fold, preds, zero_division=0))
        cv_f1s.append(f1_score(y_test_fold, preds, zero_division=0))
        print(f"  Fold {fold}: Recall={cv_recalls[-1]:.1%}, Precision={cv_precisions[-1]:.1%}, F1={cv_f1s[-1]:.1%}")

    print("\n------------------------------------------------------------")
    print("  CROSS-VALIDATION RESULTS (5-Fold Mean +/- Std)")
    print("------------------------------------------------------------")
    print(f"  Recall   : {np.mean(cv_recalls)*100:.2f}% +/- {np.std(cv_recalls)*100:.2f}%")
    print(f"  Precision: {np.mean(cv_precisions)*100:.2f}% +/- {np.std(cv_precisions)*100:.2f}%")
    print(f"  F1 Score : {np.mean(cv_f1s)*100:.2f}% +/- {np.std(cv_f1s)*100:.2f}%")
    print("------------------------------------------------------------")

    # ─── SECTION 2: HELD-OUT SPLIT FOR DEEP ABLATION STUDY ───────────────────
    print("\nEvaluating single held-out 80/20 stratified split...")
    from sklearn.model_selection import train_test_split
    train_idx, test_idx = train_test_split(df.index, test_size=0.2, random_state=42, stratify=y)
    
    train_df = df.iloc[train_idx].reset_index(drop=True)
    test_df = df.iloc[test_idx].reset_index(drop=True)
    
    # Calculate community risk on training labels
    train_fraud_accounts = set(
        train_df.loc[train_df["is_fraud"] == 1, "sender_id"].tolist()
        + train_df.loc[train_df["is_fraud"] == 1, "receiver_id"].tolist()
    )
    labels_dict = {acc: 1 for acc in train_fraud_accounts}
    main_graph.compute_community_risks(labels_dict)
    
    # Apply to train and test (sender community risk only)
    df_eval = df.copy()
    df_eval["community_risk_score"] = [main_graph.get_community_risk(sid) for sid in df_eval["sender_id"]]

    X_train = df_eval[FEATURE_COLS].iloc[train_idx].reset_index(drop=True)
    y_train = y.iloc[train_idx].reset_index(drop=True)
    X_test = df_eval[FEATURE_COLS].iloc[test_idx].reset_index(drop=True)
    y_test = y.iloc[test_idx].reset_index(drop=True)
    
    # Fit final models
    ml_manager = MLModelManager()
    ml_manager.train(X_train, y_train)
    
    rule_engine = ComplianceRuleEngine()
    stat_detector = StatisticalAnomalyDetector()
    stat_detector.fit(train_df)
    
    ensemble = EnsembleScorer()
    
    ml_probs = ml_manager.predict_probabilities(X_test)
    test_df_eval = df_eval.iloc[test_idx].reset_index(drop=True)

    pred_rules, pred_stats, pred_ml, pred_ensemble = [], [], [], []

    for pos, (_, row) in enumerate(test_df_eval.iterrows()):
        r_flags = rule_engine.evaluate_transaction(row)
        s_flags = stat_detector.evaluate_transaction(row)
        ml_p = float(ml_probs[pos])

        pred_rules.append(1 if r_flags["rule_score"] > 0.0 else 0)

        combined_stat = max(r_flags["rule_score"], s_flags["statistical_score"])
        pred_stats.append(1 if combined_stat >= 0.25 else 0)

        pred_ml.append(1 if ml_p >= 0.5 else 0)

        row_dict = {**row.to_dict(), **r_flags, **s_flags}
        score, _ = ensemble.calculate_score(row_dict, ml_p)
        pred_ensemble.append(1 if score >= 35.0 else 0)

    # Metrics helper extracting raw matrix elements
    def extract_metrics(y_true, y_pred):
        rec = recall_score(y_true, y_pred, zero_division=0)
        prec = precision_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return rec, prec, f1, int(tp), int(fp), int(fn), int(tn)

    r_r, r_p, r_f, r_tp, r_fp, r_fn, r_tn = extract_metrics(y_test, pred_rules)
    s_r, s_p, s_f, s_tp, s_fp, s_fn, s_tn = extract_metrics(y_test, pred_stats)
    m_r, m_p, m_f, m_tp, m_fp, m_fn, m_tn = extract_metrics(y_test, pred_ml)
    e_r, e_p, e_f, e_tp, e_fp, e_fn, e_tn = extract_metrics(y_test, pred_ensemble)

    # Reconciled False Positive Reduction: comparing Ensemble against ML baseline
    fp_reduction_ml_to_ens = (m_fp - e_fp) / m_fp * 100.0 if m_fp > 0 else 0.0

    print("\n------------------------------------------------------------")
    print("  LAYER-BY-LAYER ABLATION (Held-Out 80/20 Split)")
    print("------------------------------------------------------------")
    print(f"  Layer 1 (Rules Only)      | R={r_r:5.1%} P={r_p:5.1%} F1={r_f:5.1%} | TP={r_tp:3d} FP={r_fp:2d} FN={r_fn:3d} TN={r_tn:3d}")
    print(f"  Layer 2 (+ Statistical)   | R={s_r:5.1%} P={s_p:5.1%} F1={s_f:5.1%} | TP={s_tp:3d} FP={s_fp:2d} FN={s_fn:3d} TN={s_tn:3d}")
    print(f"  Layer 3 (+ RandomForest)  | R={m_r:5.1%} P={m_p:5.1%} F1={m_f:5.1%} | TP={m_tp:3d} FP={m_fp:2d} FN={m_fn:3d} TN={m_tn:3d}")
    print(f"  Layer 4 (+ Graph Network) | R={e_r:5.1%} P={e_p:5.1%} F1={e_f:5.1%} | TP={e_tp:3d} FP={e_fp:2d} FN={e_fn:3d} TN={e_tn:3d}")
    print("------------------------------------------------------------")
    print(f"  Ensemble False Positive Reduction (vs ML alone)  : {fp_reduction_ml_to_ens:.1f}%")
    print("------------------------------------------------------------")

    # ─── SECTION 3: PER-TYPOLOGY DETECTION RATE ──────────────────────────────
    test_df_eval = test_df_eval.copy()
    test_df_eval["pred"] = pred_ensemble
    fraud_only = test_df_eval[test_df_eval["is_fraud"] == 1]

    print("\n  DETECTION RATE BY TYPOLOGY (Ensemble):")
    print("-" * 60)
    typology_results = {}
    for typology, grp in fraud_only.groupby("typology"):
        detected = int(grp["pred"].sum())
        total = len(grp)
        pct = detected / total if total > 0 else 0.0
        bar = "#" * int(pct * 20) + "." * (20 - int(pct * 20))
        print(f"  {typology:<20} [{bar}] {pct:>6.1%}  ({detected}/{total})")
        typology_results[typology] = {"detected": detected, "total": total, "pct": pct}
    print("-" * 60)

    # ─── SECTION 4: SAVE SUMMARY METRICS FOR DASHBOARD ────────────────────────
    pd.DataFrame([{
        "recall": e_r,
        "precision": e_p,
        "f1": e_f,
        "fp_reduction": fp_reduction_ml_to_ens,
        "cv_recall_mean": np.mean(cv_recalls),
        "cv_recall_std": np.std(cv_recalls),
        "cv_precision_mean": np.mean(cv_precisions),
        "cv_precision_std": np.std(cv_precisions),
        "cv_f1_mean": np.mean(cv_f1s),
        "cv_f1_std": np.std(cv_f1s),
        
        # Raw Confusion Matrix elements
        "tp": e_tp,
        "fp": e_fp,
        "fn": e_fn,
        "tn": e_tn,
        
        # Ablation details
        "layer1_recall": r_r, "layer1_prec": r_p, "layer1_f1": r_f, "layer1_fp": r_fp,
        "layer2_recall": s_r, "layer2_prec": s_p, "layer2_f1": s_f, "layer2_fp": s_fp,
        "layer3_recall": m_r, "layer3_prec": m_p, "layer3_f1": m_f, "layer3_fp": m_fp,
        
        # Typology details (for dynamic dashboard reading)
        "typology_layering_pct": typology_results.get("layering", {}).get("pct", 0.0),
        "typology_rapid_cashout_pct": typology_results.get("rapid_cashout", {}).get("pct", 0.0),
        "typology_round_tripping_pct": typology_results.get("round_tripping", {}).get("pct", 0.0),
        "typology_smurfing_pct": typology_results.get("smurfing", {}).get("pct", 0.0),
        "typology_structuring_pct": typology_results.get("structuring", {}).get("pct", 0.0),
    }]).to_csv("data/metrics_summary.csv", index=False)
    print("\n  Metrics saved -> data/metrics_summary.csv")


if __name__ == "__main__":
    run_evaluation()

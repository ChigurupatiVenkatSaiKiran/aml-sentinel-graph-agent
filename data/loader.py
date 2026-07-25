"""
Dataset Loader and Preprocessor
---------------------------------
Orchestrates data generation, feature engineering, graph construction,
and produces aligned 80/20 stratified train/test splits with zero leakage.
Specifically, community risk scores are calculated using ONLY training set labels.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from data.synthetic_generator import build_dataset
from data.feature_engineering import compute_transaction_features, compute_rolling_features
from graph.network_builder import TransactionGraph
from graph.motif_detector import MotifDetector

DATA_FILE      = "data/transactions.csv"
CACHED_FILE    = "data/processed_cache.parquet"

# Feature columns used for modelling — single source of truth
FEATURE_COLS = [
    # ── Transaction-level ─────────────────────────────────────────────────────
    "amount",
    "is_round_amount",
    "is_structuring_amount",
    "hour_of_day",
    # ── Behavioral rolling windows (sender) ───────────────────────────────────
    "tx_count_1d",
    "tx_count_7d",
    "tx_sum_1d",
    "tx_sum_7d",
    "unique_recipients_7d",
    "time_since_last_tx_hours",
    "is_rapid_cashout",
    # ── Sender graph features ─────────────────────────────────────────────────
    "pagerank_score",
    "in_degree",
    "out_degree",
    "clustering_coefficient",
    "community_risk_score",
    # ── Motif flags ───────────────────────────────────────────────────────────────
    "is_cycle_edge",
    "is_fan_out_edge",
    "is_fan_in_edge",
    "is_chain_edge",
]


def load_processed_data() -> tuple:
    """
    Loads raw transactions, engineers static & rolling features, builds the
    graph, and extracts purely structural (leakage-free) graph metrics and motifs.
    Label-based graph metrics (like community_risk_score) are deferred.

    Speed: On first run builds everything and caches to parquet (~1s on reload).
    Cache is invalidated when transactions.csv mtime changes.
    """
    if not os.path.exists(DATA_FILE):
        build_dataset(DATA_FILE)

    src_mtime = os.path.getmtime(DATA_FILE)

    # ── Always rebuild graph & motifs (in-memory objects, not cached) ──────────
    # The parquet cache stores the feature columns so we skip the slow pipeline.
    if os.path.exists(CACHED_FILE):
        try:
            cache_meta_file = CACHED_FILE + ".mtime"
            cached_mtime = float(open(cache_meta_file).read()) if os.path.exists(cache_meta_file) else 0.0
            if abs(cached_mtime - src_mtime) < 1.0:   # same source file
                df = pd.read_parquet(CACHED_FILE)
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                # Rebuild graph & motifs from raw CSV (fast, ~0.5s)
                raw = pd.read_csv(DATA_FILE)
                raw["timestamp"] = pd.to_datetime(raw["timestamp"])
                graph = TransactionGraph()
                graph.build_graph(raw)
                motifs = MotifDetector(graph.G)
                motifs.find_all_motifs()
                print("[loader] Cache hit — feature pipeline skipped.")
                return df, graph, motifs
        except Exception as e:
            print(f"[loader] Cache read failed ({e}), rebuilding...")

    # ── Full pipeline (runs once, ~15-25s) ─────────────────────────────────────
    df = pd.read_csv(DATA_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 1. Static transactional features
    df = compute_transaction_features(df)

    # 2. Vectorized rolling behavioral features
    df = compute_rolling_features(df)

    # 3. Build directed transaction graph
    graph = TransactionGraph()
    graph.build_graph(df)

    # 4. Vectorized structural graph feature extraction (no labels used)
    sender_ids = df["sender_id"].values
    graph_rows = [graph.get_node_features(sid) for sid in sender_ids]
    graph_df = pd.DataFrame(graph_rows)

    df["pagerank_score"]         = graph_df["pagerank_score"].values
    df["in_degree"]              = graph_df["in_degree"].values
    df["out_degree"]             = graph_df["out_degree"].values
    df["clustering_coefficient"] = graph_df["clustering_coefficient"].values
    df["community_id"]           = graph_df["community_id"].values

    # 5. Motif detection — vectorized set-membership (O(1) per edge vs iterrows)
    motifs = MotifDetector(graph.G)
    motifs.find_all_motifs()

    senders   = df["sender_id"].values
    receivers = df["receiver_id"].values
    edges     = list(zip(senders, receivers))

    df["is_cycle_edge"]   = [int(e in motifs._cycle_edges)   for e in edges]
    df["is_fan_out_edge"] = [int(e in motifs._fan_out_edges) for e in edges]
    df["is_fan_in_edge"]  = [int(e in motifs._fan_in_edges)  for e in edges]
    df["is_chain_edge"]   = [int(e in motifs._chain_edges)   for e in edges]

    def _typology(e):
        if e in motifs._fan_out_edges: return "smurfing_fan_out"
        if e in motifs._fan_in_edges:  return "smurfing_fan_in"
        if e in motifs._chain_edges:   return "layering_chain"
        if e in motifs._cycle_edges:   return "round_tripping_cycle"
        return "none"

    df["motif_typology"] = [_typology(e) for e in edges]

    # 6. Receiver-side graph features (leakage-free — structural only, no labels)
    receiver_ids = df["receiver_id"].values
    df["receiver_pagerank"]          = [graph.pagerank.get(r, 0.0) for r in receiver_ids]
    df["receiver_out_degree"]        = [graph.out_degree.get(r, 0)  for r in receiver_ids]
    df["receiver_community_risk"]    = 0.0
    df["flagged_counterparty_count"] = 0

    # ── Save cache ─────────────────────────────────────────────────────────────
    try:
        df.to_parquet(CACHED_FILE, index=False)
        open(CACHED_FILE + ".mtime", "w").write(str(src_mtime))
        print("[loader] Feature cache saved.")
    except Exception as e:
        print(f"[loader] Cache save failed ({e}).")

    return df, graph, motifs


def get_train_test_splits():
    """
    Returns aligned 80/20 stratified splits with zero leakage.
    Guarantees community_risk_score is fitted using ONLY training set labels.
    
    Returns: X_train, y_train, X_test, y_test, ordered_df, graph, n_train
    """
    df, graph, _ = load_processed_data()
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Stratified split based on target 'is_fraud'
    y = df["is_fraud"].copy()
    train_idx, test_idx = train_test_split(
        df.index, test_size=0.2, random_state=42, stratify=y
    )

    # Calculate community risks using ONLY training data labels to prevent leakage
    train_df = df.loc[train_idx]
    train_fraud_accounts = set(
        train_df.loc[train_df["is_fraud"] == 1, "sender_id"].tolist()
        + train_df.loc[train_df["is_fraud"] == 1, "receiver_id"].tolist()
    )
    labels_dict = {acc: 1 for acc in train_fraud_accounts}
    
    # Update graph risks based on training labels only
    graph.compute_community_risks(labels_dict)

    # Assign sender community risk scores to all rows
    df["community_risk_score"] = [graph.get_community_risk(sid) for sid in df["sender_id"]]

    # Assign receiver community risk scores (label-based, still leakage-free)
    df["receiver_community_risk"] = [graph.get_community_risk(rid) for rid in df["receiver_id"]]

    # Flagged counterparty count: how many of sender's all-time tx partners are known fraud accounts?
    # Build sender→receivers adjacency from full graph (structural), then count fraud-account hits
    import networkx as nx
    sender_neighbors = {node: set(graph.G.successors(node)) | set(graph.G.predecessors(node))
                        for node in graph.G.nodes()}
    df["flagged_counterparty_count"] = [
        sum(1 for nb in sender_neighbors.get(sid, set()) if nb in train_fraud_accounts)
        for sid in df["sender_id"]
    ]

    X = df[FEATURE_COLS].copy()
    
    X_train = X.loc[train_idx].reset_index(drop=True)
    y_train = y.loc[train_idx].reset_index(drop=True)
    X_test  = X.loc[test_idx].reset_index(drop=True)
    y_test  = y.loc[test_idx].reset_index(drop=True)

    # ordered_df: train rows first, test rows second — boundary = len(X_train)
    train_df_final = df.loc[train_idx].reset_index(drop=True)
    test_df_final  = df.loc[test_idx].reset_index(drop=True)
    ordered_df = pd.concat([train_df_final, test_df_final], ignore_index=True)

    n_train = len(X_train)

    return X_train, y_train, X_test, y_test, ordered_df, graph, n_train

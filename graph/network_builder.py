"""
Graph Network Builder and Centrality Estimator
-----------------------------------------------
Builds directed transaction graphs with NetworkX.
Computes per-node structural metrics:
  - Weighted PageRank
  - Louvain community detection (reproducible via random_state=42)
  - In/Out degree
  - Clustering coefficient
  - Guild-by-association community risk score
"""

import pandas as pd
import networkx as nx
import community as community_louvain


class TransactionGraph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.partition     = {}
        self.pagerank      = {}
        self.in_degree     = {}
        self.out_degree    = {}
        self.clustering_coef = {}
        self.community_risk  = {}

    def build_graph(self, df: pd.DataFrame):
        """Builds a weighted directed graph from transaction DataFrame using itertuples (fast)."""
        self.G = nx.DiGraph()

        for row in df.itertuples(index=False):
            sender   = row.sender_id
            receiver = row.receiver_id
            amount   = float(row.amount)

            if self.G.has_edge(sender, receiver):
                self.G[sender][receiver]["weight"]   += amount
                self.G[sender][receiver]["tx_count"] += 1
            else:
                self.G.add_edge(sender, receiver, weight=amount, tx_count=1)

        print(
            f"Graph: {self.G.number_of_nodes():,} nodes, "
            f"{self.G.number_of_edges():,} edges"
        )
        self._compute_metrics()

    def _compute_metrics(self):
        """Pre-computes graph structural metrics (called once after build)."""
        if len(self.G) == 0:
            return

        # 1. Weighted PageRank
        try:
            self.pagerank = nx.pagerank(self.G, weight="weight", max_iter=200)
        except nx.PowerIterationFailedConvergence:
            self.pagerank = nx.pagerank(self.G, max_iter=200)

        # 2. Degree centrality
        self.in_degree  = dict(self.G.in_degree())
        self.out_degree = dict(self.G.out_degree())

        # 3. Clustering coefficient (undirected)
        undirected_G = self.G.to_undirected()
        self.clustering_coef = nx.clustering(undirected_G)

        # 4. Louvain community detection -- random_state=42 for reproducibility
        try:
            self.partition = community_louvain.best_partition(
                undirected_G, random_state=42
            )
        except Exception as e:
            print(f"Louvain failed ({e}); defaulting all nodes to community 0.")
            self.partition = {node: 0 for node in self.G.nodes()}

    def get_node_features(self, node_id: str) -> dict:
        """Returns all pre-computed graph features for a node."""
        if not self.G.has_node(node_id):
            return {
                "pagerank_score":         0.0,
                "in_degree":              0,
                "out_degree":             0,
                "clustering_coefficient": 0.0,
                "community_id":           -1,
            }
        return {
            "pagerank_score":         self.pagerank.get(node_id, 0.0),
            "in_degree":              self.in_degree.get(node_id, 0),
            "out_degree":             self.out_degree.get(node_id, 0),
            "clustering_coefficient": self.clustering_coef.get(node_id, 0.0),
            "community_id":           self.partition.get(node_id, -1),
        }

    def compute_community_risks(self, labels_dict: dict):
        """
        Guilt-by-association: fraction of fraud-linked nodes in each community.
        labels_dict maps node_id -> 1 (fraud) or 0 (clean).
        """
        from collections import defaultdict
        members_by_community = defaultdict(list)
        for node, comm_id in self.partition.items():
            members_by_community[comm_id].append(node)

        self.community_risk = {}
        for comm_id, members in members_by_community.items():
            fraud_count = sum(labels_dict.get(m, 0) for m in members)
            self.community_risk[comm_id] = fraud_count / len(members) if members else 0.0

    def get_community_risk(self, node_id: str) -> float:
        comm_id = self.partition.get(node_id, -1)
        if comm_id == -1:
            return 0.0
        return self.community_risk.get(comm_id, 0.0)

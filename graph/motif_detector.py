"""
Network Motif Detector
-----------------------
Detects topological AML patterns in the transaction graph:
  1. Fan-Out (Smurfing)    -- one sender -> many receivers (>= 4)
  2. Fan-In  (Aggregation) -- many senders -> one receiver (>= 4)
  3. Layering Chains       -- multi-hop pass-through paths (depth >= 3)
  4. Round-Tripping Cycles -- directed cycles length 3-5

All motifs are pre-computed once and stored in lookup sets for O(1) edge query.
Cycle detection is capped at 5,000 to prevent unbounded computation on large graphs.
"""

import networkx as nx
from itertools import islice


MAX_CYCLES = 5_000   # Hard cap to prevent runaway simple_cycles on dense graphs


class MotifDetector:
    def __init__(self, G: nx.DiGraph):
        self.G = G
        # Pre-built edge-level lookup sets (sender, receiver) -> bool
        self._cycle_edges:    set = set()
        self._fan_out_edges:  set = set()
        self._fan_in_edges:   set = set()
        self._chain_edges:    set = set()

    def find_all_motifs(self):
        """Runs all four motif searches. Call once after graph is built."""
        self._detect_cycles()
        self._detect_fan_out_in()
        self._detect_chains()
        print(
            f"Motifs detected -- cycles: {len(self._cycle_edges)}, "
            f"fan-out edges: {len(self._fan_out_edges)}, "
            f"fan-in edges:  {len(self._fan_in_edges)}, "
            f"chain edges:   {len(self._chain_edges)}"
        )

    def _detect_cycles(self):
        """
        Finds directed cycles of length 3-5.
        Capped at MAX_CYCLES to stay fast on large graphs.
        """
        try:
            for cycle in islice(nx.simple_cycles(self.G), MAX_CYCLES):
                if 3 <= len(cycle) <= 5:
                    for i, node in enumerate(cycle):
                        nxt = cycle[(i + 1) % len(cycle)]
                        self._cycle_edges.add((node, nxt))
        except Exception as e:
            print(f"Cycle detection error: {e}")

    def _detect_fan_out_in(self, threshold: int = 4):
        """
        Fan-Out: a node with >= threshold distinct successors (smurfing source).
        Fan-In:  a node with >= threshold distinct predecessors (aggregation collector).
        Stores all edges that belong to such nodes.
        """
        for node in self.G.nodes():
            successors = list(self.G.successors(node))
            if len(successors) >= threshold:
                for s in successors:
                    self._fan_out_edges.add((node, s))

            predecessors = list(self.G.predecessors(node))
            if len(predecessors) >= threshold:
                for p in predecessors:
                    self._fan_in_edges.add((p, node))

    def _detect_chains(self, min_depth: int = 3):
        """
        Layering chains: sequences of pass-through nodes (in=1, out=1).
        Traces forward from each entry point, storing consecutive edges.
        """
        # Pass-through nodes: exactly 1 predecessor and 1 successor
        pass_through = {
            n for n in self.G.nodes()
            if self.G.in_degree(n) == 1 and self.G.out_degree(n) == 1
        }

        visited = set()
        for node in pass_through:
            if node in visited:
                continue

            # Build the full chain starting from current node
            path = [node]
            visited.add(node)

            # Trace backward to chain head
            curr = node
            while True:
                preds = list(self.G.predecessors(curr))
                if len(preds) == 1 and preds[0] not in path:
                    pred = preds[0]
                    path.insert(0, pred)
                    if pred in pass_through:
                        visited.add(pred)
                        curr = pred
                    else:
                        break
                else:
                    break

            # Trace forward to chain tail
            curr = node
            while True:
                succs = list(self.G.successors(curr))
                if len(succs) == 1 and succs[0] not in path:
                    succ = succs[0]
                    path.append(succ)
                    if succ in pass_through:
                        visited.add(succ)
                        curr = succ
                    else:
                        break
                else:
                    break

            # Only register chains meeting minimum depth
            if len(path) >= min_depth:
                for i in range(len(path) - 1):
                    self._chain_edges.add((path[i], path[i + 1]))

    def get_motif_features(self, sender_id: str, receiver_id: str) -> dict:
        """
        O(1) lookup for all motif flags on a specific directed edge.
        Returns dict with is_cycle_edge, is_fan_out_edge, is_fan_in_edge,
        is_chain_edge, and motif_typology label.
        """
        edge = (sender_id, receiver_id)
        in_cycle   = int(edge in self._cycle_edges)
        in_fan_out = int(edge in self._fan_out_edges)
        in_fan_in  = int(edge in self._fan_in_edges)
        in_chain   = int(edge in self._chain_edges)

        # Priority order: fan_out > fan_in > chain > cycle
        if in_fan_out:
            typology = "smurfing_fan_out"
        elif in_fan_in:
            typology = "smurfing_fan_in"
        elif in_chain:
            typology = "layering_chain"
        elif in_cycle:
            typology = "round_tripping_cycle"
        else:
            typology = "none"

        return {
            "is_cycle_edge":   in_cycle,
            "is_fan_out_edge": in_fan_out,
            "is_fan_in_edge":  in_fan_in,
            "is_chain_edge":   in_chain,
            "motif_typology":  typology,
        }

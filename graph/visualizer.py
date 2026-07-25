"""
PyVis Network Visualizer
------------------------
Generates interactive, color-coded HTML network graphs of transaction subgraphs.
High Risk nodes = Red, Medium = Orange, Low = Green.
Nodes and edges display hover metrics.
"""

import os
from pyvis.network import Network
import networkx as nx

def generate_interactive_graph(G: nx.DiGraph, center_node=None, max_nodes=50, save_path="data/network_viz.html", scores_dict=None) -> str:
    """
    Generates an interactive HTML representation of a transaction subgraph.
    Colors nodes dynamically based on risk scores:
    - Risk >= 70 -> Red
    - Risk >= 40 -> Orange
    - Risk < 40  -> Green
    """
    if scores_dict is None:
        scores_dict = {}
        
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # 1. Subgraph extraction
    if center_node and G.has_node(center_node):
        # Extract ego network (neighbors within 1 or 2 hops)
        neighbors = set(nx.single_source_shortest_path_length(G, center_node, cutoff=2).keys())
        # Add incoming neighbors as well
        reversed_G = G.reverse(copy=False)
        in_neighbors = set(nx.single_source_shortest_path_length(reversed_G, center_node, cutoff=2).keys())
        subgraph_nodes = list(neighbors.union(in_neighbors))[:max_nodes]
        subgraph = G.subgraph(subgraph_nodes)
    else:
        # Fallback to top nodes by degree
        degrees = dict(G.degree())
        sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)[:max_nodes]
        subgraph = G.subgraph(sorted_nodes)
        
    # 2. Build pyvis network representation
    # Initialize pyvis Network with clean dark background options
    net = Network(height="500px", width="100%", bgcolor="#0F172A", font_color="white", directed=True)
    
    # Configure physics engine
    net.set_options("""
    var options = {
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -15000,
          "centralGravity": 0.3,
          "springLength": 95,
          "springConstant": 0.04,
          "damping": 0.09,
          "avoidOverlap": 0.5
        },
        "minVelocity": 0.75
      }
    }
    """)
    
    # 3. Add nodes
    for node in subgraph.nodes():
        score = scores_dict.get(node, 15.0) # default low risk
        
        # Color schemes using robust Vis.js dictionary format
        if score >= 70.0:
            color_dict = {
                "background": "#EF4444", # Red
                "border": "#B91C1C",
                "highlight": {
                    "background": "#F87171",
                    "border": "#EF4444"
                }
            }
            size = 25
        elif score >= 40.0:
            color_dict = {
                "background": "#F59E0B", # Orange
                "border": "#D97706",
                "highlight": {
                    "background": "#FBBF24",
                    "border": "#F59E0B"
                }
            }
            size = 20
        else:
            color_dict = {
                "background": "#10B981", # Green
                "border": "#059669",
                "highlight": {
                    "background": "#34D399",
                    "border": "#10B981"
                }
            }
            size = 15
            
        # Hover info
        title_text = f"<b>Account:</b> {node}<br><b>Risk Score:</b> {score:.1f}/100"
        
        net.add_node(
            node, 
            label=node, 
            title=title_text, 
            color=color_dict, 
            size=size,
            borderWidth=2,
            borderWidthSelected=4
        )
        
    # 4. Add edges
    for u, v, data in subgraph.edges(data=True):
        weight = data.get("weight", 0.0)
        tx_count = data.get("tx_count", 1)
        net.add_edge(
            u, 
            v, 
            value=weight, 
            title=f"Total: ${weight:,.2f}<br>Count: {tx_count}",
            color="#64748B",
            arrowStrikethrough=False
        )
        
    # 5. Save HTML visual
    net.save_graph(save_path)
    return save_path

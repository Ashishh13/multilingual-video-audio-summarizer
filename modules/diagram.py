"""
Diagram generation module.

This module builds a simple keyword co‑occurrence graph from the
transcript. Each keyword is represented as a node and an edge is
created between two keywords when they appear within the same sentence.
Edge weights reflect the frequency of co‑occurrence. The graph is
rendered using ``networkx`` and ``matplotlib``.
"""

import os
from typing import List

import matplotlib.pyplot as plt
import networkx as nx

from .config import FIGURE_WIDTH, FIGURE_HEIGHT
from .cleaning import split_sentences


def build_keyword_graph(keywords: List[str], text: str, output_path: str) -> str:
    """Construct and save a keyword co‑occurrence graph.

    Parameters
    ----------
    keywords : List[str]
        Keywords extracted from the document.
    text : str
        The cleaned transcript used to compute co‑occurrences.
    output_path : str
        File path where the PNG image should be saved.

    Returns
    -------
    str
        The absolute path to the saved image.
    """
    # Build an undirected weighted graph
    G = nx.Graph()
    for kw in keywords:
        G.add_node(kw)

    sentences = split_sentences(text)
    for sentence in sentences:
        present = [kw for kw in keywords if kw in sentence]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                u, v = present[i], present[j]
                if G.has_edge(u, v):
                    G[u][v]["weight"] += 1
                else:
                    G.add_edge(u, v, weight=1)

    # Draw the graph
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    if len(G.edges()) > 0:
        weights = [G[u][v]["weight"] for u, v in G.edges()]
        pos = nx.spring_layout(G, k=0.5, seed=42)
        nx.draw_networkx(
            G,
            pos=pos,
            with_labels=True,
            node_size=1500,
            font_size=10,
            width=weights,
            edge_color="#888",
            node_color="#A0CBE2",
        )
    else:
        # No edges; draw nodes only
        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="#A0CBE2")
        nx.draw_networkx_labels(G, pos, font_size=10)

    plt.axis("off")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    return os.path.abspath(output_path)

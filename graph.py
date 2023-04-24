import networkx as nx
import matplotlib.pyplot as plt

# Create an empty weighted directed graph
G = nx.DiGraph()

# Add nodes for each word with their initial confidence scores
G.add_node('word1', confidence=0.8)
G.add_node('word2', confidence=0.6)
G.add_node('word3', confidence=0.9)

# Add edges between related words with their weights
G.add_edge('word1', 'word2', weight=0.7)
G.add_edge('word2', 'word3', weight=0.9)
G.add_edge('word1', 'word3', weight=0.6)

# Create a dictionary of node labels with confidence scores
labels = {node: f"{node} ({G.nodes[node]['confidence']})" for node in G.nodes}

# Create a dictionary of edge labels with weights
edge_labels = {(u, v): f"{G.edges[u, v]['weight']:.2f}" for u, v in G.edges}

# Draw the graph using spring layout algorithm and custom node and edge colors
# color of nodes indicate
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
nx.draw_networkx_edges(G, pos, edge_color='gray', width=2, arrowsize=20, arrowstyle='->')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_family='sans-serif')
nx.draw_networkx_labels(G, pos, labels, font_size=12, font_family='sans-serif')

# Display the graph
plt.axis('off')
plt.show()

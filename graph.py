import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import preProccess as fin
import random

# Create an empty weighted directed graph
G = nx.DiGraph()
fig, ax = plt.subplots(figsize=(8, 8))

# random_words = random.sample(list(fin.word_final_scores.items()), 10)
# for word, score in random_words:
#     print(f"{word}: {score}")

random_samples = random.sample(list(fin.word_final_scores.items()), 10)
for word, score in random_samples:
    G.add_node(word, weight = fin.word_final_scores[word])
    
# Add nodes for each word with their initial confidence scores
# word = "innocent"
# G.add_node(word, weight = fin.word_final_scores[word])

# Set the node label and size
# node_labels = {word: word + "\n" + str(fin.word_final_scores[word])}
node_labels = {word: word + "\n" for word, score in random_samples}
node_labels_weight = {word: str(fin.word_final_scores[word]) for word, score in random_samples}
node_sizes = [2000 * fin.word_final_scores[word] for word, score in random_samples]

# # Create a dictionary of edge labels with weights
# edge_labels = {(u, v): f"{G.edges[u, v]['weight']:.2f}" for u, v in G.edges}


# color of nodes indicate confidence level DO THIS LATER    
#///////////////
#Position of the string for the node
pos = nx.fruchterman_reingold_layout(G)
#Position of the weight value
label_pos_weight = {n: (x, y-0.04) for n, (x, y) in pos.items()}
#Displays the color and size of node
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
#Displays text inside node

nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_family='sans-serif')
nx.draw_networkx_labels(G, label_pos_weight, labels=node_labels_weight, font_size=9, font_family='sans-serif')
#///////////////////


# Display the graph
plt.axis('off')
plt.show()

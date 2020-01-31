# libraries
import matplotlib.pyplot as plt
import networkx as nx

# Build a dataframe with your connections

df = {'value': [1, 10, 5, 5]}

# Build your graph
G = nx.Graph()
G.add_node()

# Custom the nodes:
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_color=df['value'], width=10.0,
        edge_cmap=plt.cm.Blues)

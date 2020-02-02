# libraries
import json

import matplotlib.pyplot as plt
import networkx as nx

# Build a dataframe with your connections
from User import User


class NetworkGraph:

    def __init__(self, target, listFriends, famousColor="1", normalColor="2", privateColor="3"):
        self.target = target
        self.listFriends = listFriends
        self.color_map = {
            'famous': famousColor,
            'normal': normalColor,
            'private': privateColor,
        }

        def usersConfigured():
            fileTarget = open(f'Follows/{target}.txt', 'r')
            targetFollows = fileTarget.readlines()
            for userFollowing in targetFollows:
                infoFile = open(f"Info/{userFollowing}.txt", 'r')
                jsonInfo = json.load(infoFile)

                newUser = User(
                    jsonInfo['name'],
                    jsonInfo['username'],
                    jsonInfo['nPubs'],
                    jsonInfo['nFollowers'],
                    jsonInfo['nFollows'],
                    jsonInfo['description'])


v = 10
df = {'value': range(v)}

# Build your graph
G = nx.Graph()
colors = {
    'famous'
}

## assign a node attribute, which I am going to color according to
for node in G.nodes():
    G.node[node]['category'] = my_category_dict[node]
## put together a color map, one color for a category
color_map = {'type_A': 'b', 'type_B': '#FF0099', 'type_C': '#660066'}
## construct a list of colors then pass to node_color
nx.draw(G, node_color=[color_map[G.node[node]['category']] for node in G])
plt.show()

for x in range(1, v):
    G.add_node(str(x))
    G.add_edge(str(x), str(x + 1))
    colors.append(3.5)

colors.append(0)
# Custom the nodes:
nx.draw(G, with_labels=True, node_color=["#eee"], node_size=100, width=2.0)

plt.show()

# libraries
import json

import matplotlib.pyplot as plt
import networkx as nx

from BotInstagram import existFollowsFile
from User import User


class NetworkGraph:

    def __init__(self, target, famousColor=4, normalColor=7, principalColor=9, xColor=2):
        self.target = target
        self.color_map = {
            'famous': famousColor,
            'normal': normalColor,
            'principal': principalColor,
            'x': xColor
        }

        self.G = nx.Graph()

        self.G.add_node(target, tipo='principal')

        def usersConfigured():
            users = []
            fileTarget = open(f'Follows/{target}.txt', 'r')
            targetFollows = fileTarget.readlines()
            for userFollowing in targetFollows:
                userFollowing = userFollowing.replace("\n", '')
                try:
                    infoFile = open(f"Info/{userFollowing}.txt", 'r')
                    jsonInfo = dict(json.load(infoFile))
                except:
                    continue

                try:
                    newUser = User(
                        jsonInfo['name'],
                        jsonInfo['username'],
                        jsonInfo['nPubs'],
                        jsonInfo['nFollowers'],
                        jsonInfo['nFollows'],
                    )
                    newUser.descripcion = jsonInfo['description'] if jsonInfo['description'] else '',
                except:
                    pass
                try:
                    int(newUser.seguidores.replace('.', ''))
                    newUser.tipo = "normal"
                except:
                    newUser.tipo = "famous"
                users.append(newUser)

            return users

        def makeNodes(users):
            for u in users:
                self.G.add_node(u.usuario,
                                nombre=u.nombre,
                                publicaciones=u.publicaciones,
                                seguidores=u.seguidores,
                                seguidos=u.seguidos,
                                descripcion=u.descripcion,
                                tipo=u.tipo)

        def makeRelations(target, users):
            relations = {}
            relationsList = []
            _users = []

            # Quitar el "\n"
            for us in users:
                _users.append(us.usuario.replace('\n', ''))
            # Todos los usuarios
            for u in _users:
                self.G.add_edge(target, u)
                relationsList.append([target, u])
                if existFollowsFile(u):
                    with open(f"Follows/{u}.txt") as f:
                        follows = [uss.replace('\n', '') for uss in f.readlines()]
                        for _u in follows:
                            if relations.get(_u) != None:
                                relations[_u] = int(relations[_u]) + 1
                            else:
                                relations[_u] = 1
                            relationsList.append([u, _u])

            for k in relations.keys():
                # 3rd relations
                if relations[k] >= 15 and k not in _users:
                    for r, _r in relationsList:
                        if r != k and _r != k:
                            continue
                        if r not in self.G.nodes():
                            self.G.add_node(r, tipo='x')
                        if _r not in self.G.nodes():
                            self.G.add_node(_r, tipo='x')
                        self.G.add_edge(r, _r)

            # 2nd relations
            for r, _r in relationsList:
                if r in _users and _r in _users:
                    self.G.add_edge(r, _r)

        users = usersConfigured()
        makeNodes(users)
        makeRelations(target, users)
        self.show()

    def show(self):
        nx.draw(self.G,
                with_labels=True,
                node_color=[self.color_map[self.G.nodes[node]['tipo']] for node in self.G],
                node_size=100,
                # node_color='#A0CBE2',
                edge_color=range(len(self.G.edges)),
                width=.1)
        plt.show()

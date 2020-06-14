from random import randint
import networkx as nx

def Generate(numberOfNodes, density):
    Gs = nx.fast_gnp_random_graph(numberOfNodes, density, directed=True)

    for edge in Gs.edges():
        if Gs.has_edge(edge[1], edge[0]):
            Gs.remove_edge(edge[1], edge[0])
        Gs[edge[0]][edge[1]]['capacity'] = randint(0, 10)

    return Gs
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def PrintGraph(G, pos):
    labels = nx.get_edge_attributes(G, "capacity")
    nx.draw_networkx_edge_labels(G, pos, labels)
    nx.draw_networkx(G, pos)
    plt.show()

def extendedBFS(g, startingNode, finalNode):

    layer = {node: None for node in g.nodes}
    queue = []

    currentLayer = 0

    layeredNetwork = nx.DiGraph()
    layeredNetwork.add_nodes_from(g.nodes)
    layer[startingNode] = currentLayer

    queue.append(startingNode)

    foundFinalNode = False

    while queue:

        currentNode = queue.pop(0)
        currentLayer = layer[currentNode] + 1

        for neighbour in g.neighbors(currentNode):
            edge = g[currentNode][neighbour]

            if edge['capacity'] > 0 and (layer[neighbour] is None or layer[neighbour] == currentLayer):
                layer[neighbour] = currentLayer
                layeredNetwork.add_edge(currentNode, neighbour, capacity=edge['capacity'])

                if neighbour == finalNode:
                    foundFinalNode = True

                if neighbour not in queue:
                    queue.append(neighbour)

    return (layeredNetwork, foundFinalNode)


def BFS(g, startingNode, finalNode):

    visited = []
    queue = []

    layeredNetwork = nx.DiGraph()
    layeredNetwork.add_nodes_from(g.nodes)

    queue.append(startingNode)

    foundFinalNode = False

    while queue:
        currentNode = queue.pop(0)

        for neighbour in g.neighbors(currentNode):
            edge = g[currentNode][neighbour]

            if edge['capacity'] > 0 and neighbour not in visited:
                queue.append(neighbour)
                visited.append(neighbour)
                layeredNetwork.add_edge(currentNode, neighbour, capacity=edge['capacity'])

                if neighbour == finalNode:
                    foundFinalNode = True

    return (layeredNetwork, foundFinalNode)


def backwardsBFS(g, initialNode, finalNode):
    gReversed = nx.reverse(g)
    visited = []
    queue = []

    queue.append(finalNode)
    visited.append(finalNode)

    while queue:
        currentNode = queue.pop(0)

        for neighbour in gReversed.neighbors(currentNode):
            edge = gReversed[currentNode][neighbour]

            if edge['capacity'] > 0 and neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

    for notVisited in (set(g.nodes) - set(visited)):
        g.remove_node(notVisited)

def findAugmentingPath(L, initialNode, finalNode):

    augmentingPath = []
    currentNode = finalNode

    lReversed = nx.reverse(L)

    while currentNode is not initialNode:

        neighbors = list(lReversed.neighbors(currentNode))

        if not neighbors:

            if not augmentingPath:
                return augmentingPath

            edgeToRemove = augmentingPath.pop(0)
            L.remove_node(edgeToRemove[0])
            lReversed.remove_node(edgeToRemove[0])
            currentNode = edgeToRemove[1]

        else:
            neighbor = neighbors[0]
            augmentingPath.insert(0, (neighbor, currentNode))
            currentNode = neighbor

    return augmentingPath

def augmentFlow(L, path, Gs):

    maxFlow = min([L.get_edge_data(n[0], n[1])['capacity'] for n in path])

    for edgePos in path:
        edge = L[edgePos[0]][edgePos[1]]
        edge['capacity'] -= maxFlow

        if edge['capacity'] == 0:
            L.remove_edge(edgePos[0], edgePos[1])

        #Update the original Graph to maintain residual network
        originalEdge = Gs[edgePos[0]][edgePos[1]]
        originalEdge['capacity'] -= maxFlow

        if originalEdge['capacity'] == 0:
            Gs.remove_edge(edgePos[0], edgePos[1])

        if not Gs.has_edge(edgePos[1], edgePos[0]):
            Gs.add_edge(edgePos[1], edgePos[0], capacity=0)


        reverseEdge = Gs[edgePos[1]][edgePos[0]]

        reverseEdge['capacity'] += maxFlow


    return maxFlow
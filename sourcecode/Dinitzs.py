import utils

def DinitzsAlgorithm(Gs, initialNode, finalNode):
    flow = 0

    while True:
        L, existPathBetweenST = utils.extendedBFS(Gs, initialNode, finalNode)
        utils.backwardsBFS(L, initialNode, finalNode)

        if not existPathBetweenST: break

        while True:
            augmentingPath = utils.findAugmentingPath(L, initialNode, finalNode)
            if not augmentingPath: break
            flow += utils.augmentFlow(L, augmentingPath, Gs)

    return flow
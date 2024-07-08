

class OctreeNode:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.children = [None] * 8
        self.points = []  # list of leaves

class Octree:
    def __init__(self, center, size):
        self.root = OctreeNode(center, size)

    def new_node(self, point):
        self.new_node_calc(self.root, point)

    def new_node_calc(self, node, point):
        # Check if node is divisible, aka bigger than 1. if it's not then it's a leaf
        if node.size <= 1:
            node.points.append(point)
            return

        # Determine which child node the point belongs to
        position = 0
        for i in range(3):
            if point[i] > node.center[i]:
                position |= (1 << i)  # binary representation of where the point is placed in reference to the center node

        # If the child node doesn't exist, create it
        if not node.children[position]:
            offset = node.size / 4
            new_center = []
            for i in range(3):
                if (position & (1 << i)):
                    new_center_i = node.center[i] + offset
                else:
                    new_center_i = node.center[i] - offset
                new_center.append(new_center_i)

            # insert the new node to the list of existing nodes
            node.children[position] = OctreeNode(center=new_center, size=node.size / 2)

        self.new_node_calc(node.children[position], point)



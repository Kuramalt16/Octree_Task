
import numpy as np
import Octree as oc
import laspy


def get_las_data(path):
    return laspy.read(path)


def create_octree(data):
    points = data.points
    coordinate_list = np.vstack((points.x, points.y, points.z)).T

    coordinate_list =   [(11, 23, 38),
                        (30, 44, 57),
                         (-11, -22, 96),
                         (1, 2, 5),
                         (15, 64, 79)]

    min = np.min(coordinate_list, axis=0)
    max = np.max(coordinate_list, axis=0)

    center = (max + min) / 2

    size = np.max(max - min)
    octree = oc.Octree(center, size)  # root node

    for point in coordinate_list:  # child nodes
        octree.new_node(point)

data = get_las_data("Data/2743_1234.las")

create_octree(data)
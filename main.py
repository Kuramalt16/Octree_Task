
import numpy as np
import Octree as oc
import laspy

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def get_las_data(path):
    data = laspy.read(path)
    points = data.points
    coordinate_list = np.vstack((points.x, points.y, points.z)).T
    return coordinate_list


def create_octree(coordinate_list):

    min = np.min(coordinate_list, axis=0)
    max = np.max(coordinate_list, axis=0)

    center = (max + min) / 2

    size = np.max(max - min)
    octree = oc.Octree(center, size)  # root node

    for point in coordinate_list:  # child nodes
        octree.new_node(point)

    return octree

def downsample_las_random(file_path, fraction=1):
    las_file = laspy.read(file_path)
    points = np.vstack((las_file.x, las_file.y, las_file.z)).T

    # Calculate the number of points to sample
    num_points = len(points)
    sample_size = int(num_points * fraction)
    # Randomly select points
    indices = np.random.choice(num_points, size=sample_size, replace=False)
    sampled_points = points[indices]
    return sampled_points


def visualize_octree(octree):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    def draw_sphere(center, radius):
        u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x = center[0] + radius * np.cos(u) * np.sin(v)
        y = center[1] + radius * np.sin(u) * np.sin(v)
        z = center[2] + radius * np.cos(v)
        ax.plot_surface(x, y, z, color='red', alpha=0.1, edgecolor='r')

    def draw_cube(center, size):
        half_size = size / 2.0
        x, y, z = center
        r = [-half_size, half_size]
        vertices = [[(x+dx, y+dy, z+dz) for dz in r for dy in r for dx in r]]

        faces = [
            [vertices[0][0], vertices[0][1], vertices[0][3], vertices[0][2]],
            [vertices[0][4], vertices[0][5], vertices[0][7], vertices[0][6]],
            [vertices[0][0], vertices[0][1], vertices[0][5], vertices[0][4]],
            [vertices[0][2], vertices[0][3], vertices[0][7], vertices[0][6]],
            [vertices[0][0], vertices[0][2], vertices[0][6], vertices[0][4]],
            [vertices[0][1], vertices[0][3], vertices[0][7], vertices[0][5]],
        ]

        for face in faces:
            ax.add_collection3d(Poly3DCollection([face], facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
    def traverse_node(node):
        if node.size <= 1:
            return
        draw_sphere(node.center, node.size / 2)
        for child in node.children:
            if child is not None:
                draw_cube(child.center, child.size)
                traverse_node(child)

    # Draw the sphere and cube for the root node
    draw_sphere(octree.root.center, octree.root.size / 2)
    draw_cube(octree.root.center, octree.root.size)
    traverse_node(octree.root)

    # Plot points
    points = np.array(octree.root.points)
    if len(points) > 0:
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='black', marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


# coordinates = get_las_data("Data/2743_1234.las")

coordinates = downsample_las_random("Data/2743_1234.las", fraction=0.000001)

octree = create_octree(coordinates)

visualize_octree(octree)



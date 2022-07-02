# Import Packages
import numpy as np


# Open UIUC File
def extract_uiuc_data(filename):
    file = open(filename, 'r')
    file_lines = file.readlines()
    no_x_points = int(float(file_lines[1].split()[0]))
    no_y_points = int(float(file_lines[1].split()[1]))
    if no_y_points != no_x_points:
        return "Reformat File"

    # Extract Top Surface Points
    top_surface = np.zeros([no_x_points, 2])
    for n in range(no_x_points):
        top_surface[n][:] = [float(file_lines[n + 3].split()[0]), float(file_lines[n + 3].split()[1])]

    # Extract Bottom Surface Points
    bottom_surface = np.zeros([no_x_points, 2])
    for n in range(no_x_points):
        bottom_surface[n][:] = [float(file_lines[n + 4 + no_x_points].split()[0]),
                                float(file_lines[n + 4 + no_x_points].split()[1])]

    # Build Middle line, in between top and bottom points
    middle_surface = np.zeros([no_x_points, 2])
    for n in range(no_x_points):
        middle_surface[n][:] = [float(file_lines[n + 3].split()[0]), np.mean([top_surface[n][1], bottom_surface[n][1]])]

    file.close()
    return top_surface, bottom_surface, middle_surface

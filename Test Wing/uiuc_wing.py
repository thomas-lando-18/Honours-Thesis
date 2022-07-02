# Script for building a wing mesh

# Import Packages
from read_data import extract_uiuc_data
import matplotlib.pyplot as plt
import numpy as np
from write_data_to_file import write_2d_grid

filename = "UIUC Data/n0011sc.dat.txt"
# filename = "UIUC Data/whitcomb.dat"
top_surface, bottom_surface, middle_surface = extract_uiuc_data(filename)

# Write Nastran Geometry Card
total_points = len(top_surface) + len(bottom_surface) + len(middle_surface)
fid = open('nastran_geometry_input.dat', 'w')
for n in range(len(top_surface)):
    write_2d_grid(fid, point_id=n+1, x=top_surface[n][0], y=top_surface[n][1], z=0)
for n in range(len(middle_surface)):
    write_2d_grid(fid, point_id=n+1 + len(top_surface), x=middle_surface[n][0], y=middle_surface[n][1], z=0)
for n in range(len(bottom_surface)):
    write_2d_grid(fid, point_id=n + 1 + len(top_surface) + len(middle_surface), x=bottom_surface[n][0],
                  y=bottom_surface[n][1], z=0)
fid.close()


# Plot the points
plt.figure(1)
# Plot leading and trailing edge points
plt.scatter(middle_surface[0][0], middle_surface[0][1], color='red')
plt.scatter(middle_surface[len(middle_surface)-1][0], middle_surface[len(middle_surface)-1][1], color='red')

# Plot middle values
for n in range(len(top_surface)):
    plt.scatter(top_surface[n][0], top_surface[n][1], color='blue')
    plt.scatter(bottom_surface[n][0], bottom_surface[n][1], color='blue')
    plt.scatter(middle_surface[n][0], middle_surface[n][1], color='red')
plt.grid()
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.axis('equal')
plt.show()

# Script for building a wing mesh

# Import Packages
from read_data import extract_uiuc_data
import matplotlib.pyplot as plt
import numpy as np
from write_data_to_file import write_2d_grid, write_cquad4

filename = "UIUC Data/n0011sc.dat.txt"
# filename = "UIUC Data/whitcomb.dat"
top_surface, bottom_surface, middle_surface = extract_uiuc_data(filename)
chord = 1
top_surface = top_surface * chord
middle_surface = middle_surface * chord
bottom_surface = bottom_surface * chord
# Add Flap Angle
beta = np.deg2rad(0)
# set flap point at 60% of chord
flap_point = 0.6 * chord

# Rotate values past the flap point
rot_x = np.cos(beta)
rot_y = np.sin(beta)
for n in range(len(top_surface)):
    x = top_surface[n][0]
    y = top_surface[n][1]
    if x > flap_point:
        top_surface[n][:] = [rot_x*x + rot_y*y + 0.05*chord, -rot_y*x + rot_x*y + flap_point*rot_y]

for n in range(len(middle_surface)):
    x = middle_surface[n][0]
    y = middle_surface[n][1]
    if x > flap_point:
        middle_surface[n][:] = [rot_x*x + rot_y*y + 0.05*chord, -rot_y*x + rot_x*y + flap_point*rot_y]

for n in range(len(bottom_surface)):
    x = bottom_surface[n][0]
    y = bottom_surface[n][1]
    if x > flap_point:
        bottom_surface[n][:] = [rot_x*x + rot_y*y + 0.05*chord, -rot_y*x + rot_x*y + flap_point*rot_y]

# Write Geometry Card
fid = open('nastran_geometry_input.dat', 'w')

# Write Nastran Grid Card
for n in range(len(top_surface)):
    write_2d_grid(fid, point_id=n+1, x=top_surface[n][0], y=top_surface[n][1], z=0)
for n in range(len(middle_surface)):
    write_2d_grid(fid, point_id=n+1 + len(top_surface), x=middle_surface[n][0], y=middle_surface[n][1], z=0)
for n in range(len(bottom_surface)):
    write_2d_grid(fid, point_id=n + 1 + len(top_surface) + len(middle_surface), x=bottom_surface[n][0],
                  y=bottom_surface[n][1], z=0)

# Write Nastran Mesh Card
top_panels = np.zeros([len(middle_surface), 4])
bottom_panels = np.zeros([len(middle_surface), 4])

mid_count = len(top_surface)
bottom_count = len(middle_surface) + len(top_surface)

for n in range(len(middle_surface)):
    top_panels[n][:] = [mid_count+n+1, n+1, n+2, mid_count+n+2]
    bottom_panels[n][:] = [mid_count + n + 1, bottom_count + n + 1, bottom_count + n + 2, mid_count + n + 2]

thicknesses = 1.1 * np.ones([1, 4])
for n in range(len(middle_surface)):
    write_cquad4(fid, n + 1, top_panels[n][:], thicknesses[0][:])
    write_cquad4(fid, len(middle_surface) + n + 1, bottom_panels[n][:], thicknesses[:][0])

# Close Geometry Card
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

# -----------------------------------------------------------------------------------------------------------------
# Project     : Thomas Lando Thesis (Honours)
# Title       : Simulation 2: 2D NASTRAN
# Author      : Thomas Lando (SID: 490388538)
# Supervisor  : Gareth Vio
# Institution : The University of Sydney
# ------------------------------------------------------------------------------------------------------------------
#
# Description:
# This project is focused on the use of ... for the purposes of flutter suppression in a ... inspired rocket fin.
#
# Nomenclature:
#
# Code
# ------------------------------------------------------------------------------------------------------------------

# Import Packages
import numpy as np
import matplotlib.pyplot as plt


# Functions
def trap_fin_build(chord, le_l, flap_l, t_max, beta):
    le_point = [0, 0]
    te_point = [(chord - flap_l) + flap_l * np.cos(beta), flap_l * np.sin(beta)]

    if beta <= 0:
        top_surface = [[le_l, t_max / 2], [chord - flap_l, t_max / 2],
                       [chord - flap_l + 0.0001 - t_max * np.cos(np.pi / 2 - beta), t_max / 2]]
        bottom_surface = [[le_l, -t_max / 2], [chord - flap_l, -t_max / 2], [chord - flap_l + 0.0001, -t_max / 2]]
    else:
        top_surface = [[le_l, t_max / 2], [chord - flap_l, t_max / 2],
                       [chord - flap_l + 0.0001, t_max / 2]]
        bottom_surface = [[le_l, -t_max / 2], [chord - flap_l, -t_max / 2],
                          [chord - flap_l + 0.0001 + t_max * np.cos(np.pi / 2 - beta), -t_max / 2]]

    return le_point, te_point, top_surface, bottom_surface


def write_grid_card(x, y, z, n, file):
    file.write('GRID*%s' % empty_space(3))
    file.write(str(n + 1) + '%s' % empty_space(16 - len(str(n + 1))))
    file.write('%s' % empty_space(16))
    file.write(str(round(x[n], 3)) + '%s' % empty_space(16 - len(str(x[n]))))
    file.write(str(round(y[n], 3)) + '%s\n' % empty_space(16 - len(str(y[n]))))
    file.write('*%s' % empty_space(7))
    file.write(str(round(z[n], 3)) + '%s\n' % empty_space(16 - len(str(z[n]))))
    # file.write('0.0%s\n' % empty_space(13))
    return file


def write_cquad4_card(file, p1, p2, p3, p4, n, grid_z):
    file.write('CQUAD4%s' % empty_space(2))
    file.write(str(n + 1) + '%s' % empty_space(8 - len(str(n + 1))))
    file.write('1%s' % empty_space(7))
    file.write(str(int(p1[n])) + '%s' % empty_space(8 - len(str(int(p1[n])))))
    file.write(str(int(p2[n])) + '%s' % empty_space(8 - len(str(int(p2[n])))))
    file.write(str(int(p3[n])) + '%s' % empty_space(8 - len(str(int(p3[n])))))
    file.write(str(int(p4[n])) + '%s' % empty_space(8 - len(str(int(p4[n])))))
    file.write('%s%s' % (empty_space(8), empty_space(8)))
    file.write('+EL' + str(n + 1) + '\n')


def empty_space(n):
    prev_empty = ''
    empty = ''
    for i in range(n):
        add_on = ' '
        empty = prev_empty + add_on
        prev_empty = empty
    return empty


# Set up airfoil parameters
chord_length = 1
leading_edge_length = 0.25 * chord_length
flap_length = 0.3 * chord_length
max_thickness = 0.05 * chord_length
# flap_angle = np.deg2rad(-10)
flap_angle = np.deg2rad(float(input('Input Flap Angle: ')))

# Build Airfoil Points
[le, te, top, bottom] = trap_fin_build(chord_length, leading_edge_length, flap_length, max_thickness, flap_angle)

# Points for Patran Input
points = [[le[:]], [top[0][:]], [top[1][:]], [top[2][:]], [te[:]], [bottom[0][:]], [bottom[1][:]], [bottom[2][:]]]

# Plot Airfoil
plt.figure(1)
# Leading and Trailing Edge
plt.scatter(le[0], le[1], color="blue")
plt.scatter(te[0], te[1], color="blue")
# Top surface
plt.scatter(top[0][0], top[0][1], color="blue")
plt.scatter(top[1][0], top[1][1], color="blue")
plt.scatter(top[2][0], top[2][1], color="blue")

# Bottom surface
plt.scatter(bottom[0][0], bottom[0][1], color="blue")
plt.scatter(bottom[1][0], bottom[1][1], color="blue")
plt.scatter(bottom[2][0], bottom[2][1], color="blue")

# Show Plot
plt.grid()
plt.axis('equal')
# plt.show()

plt.figure(2)

# Top surface
plt.plot([le[0], top[0][0]], [le[1], top[0][1]], color="blue")
plt.plot([top[0][0], top[1][0]], [top[0][1], top[1][1]], color="blue")
plt.plot([top[1][0], top[2][0]], [top[1][1], top[2][1]], color="blue")
plt.plot([top[2][0], te[0]], [top[2][1], te[1]], color="blue")

# # Bottom surface
plt.plot([le[0], bottom[0][0]], [le[1], bottom[0][1]], color="blue")
plt.plot([bottom[0][0], bottom[1][0]], [bottom[0][1], bottom[1][1]], color="blue")
plt.plot([bottom[1][0], bottom[2][0]], [bottom[1][1], bottom[2][1]], color="blue")
plt.plot([bottom[2][0], te[0]], [bottom[2][1], te[1]], color="blue")

plt.grid()
plt.axis('equal')

# Mesh into Panels
check_divisions = input('Select division method: ')
if check_divisions == 'Default':
    le_divisions = 10
    mid_divisions = 10
    te_divisions = 10
else:
    le_divisions = int(input('Input Leading Edge Divisions: '))
    mid_divisions = int(input('Input Midspan Divisions: '))
    te_divisions = int(input('Input Trailing Edge Divisions: '))

# Build Leading Edge
# Grid Points
leading_edge_divisions = np.zeros([4, le_divisions])
leading_edge_divisions[0][:] = np.linspace(le[0], top[0][0], num=le_divisions)
leading_edge_divisions[1][:] = np.interp(xp=[le[0], top[0][0]], fp=[0, 0], x=leading_edge_divisions[0][:])
leading_edge_divisions[2][:] = np.interp(xp=[le[0], top[0][0]], fp=[le[0], top[0][1]], x=leading_edge_divisions[0][:])
leading_edge_divisions[3][:] = np.interp(xp=[le[0], bottom[0][0]], fp=[le[0], bottom[0][1]],
                                         x=leading_edge_divisions[0][:])

# Midspan
# Grid Points
midspan_divisions = np.zeros([4, mid_divisions])
midspan_divisions[0][:] = np.linspace(top[0][0], top[1][0], num=mid_divisions)
midspan_divisions[1][:] = np.interp(xp=[top[0][0], top[1][0]], fp=[0, 0], x=midspan_divisions[0][:])
midspan_divisions[2][:] = np.interp(xp=[top[0][0], top[1][0]], fp=[max_thickness / 2, max_thickness / 2],
                                    x=midspan_divisions[0][:])
midspan_divisions[3][:] = np.interp(xp=[top[0][0], top[1][0]], fp=[-max_thickness / 2, -max_thickness / 2],
                                    x=midspan_divisions[0][:])

# Mesh Panels


# Trailing Edge
# Grid Points
trailing_edge_divisions = np.zeros([4, te_divisions])
trailing_edge_divisions[0][:] = np.linspace(top[1][0], te[0], num=te_divisions)
trailing_edge_divisions[1][:] = np.interp(xp=[top[1][0], te[0]], fp=[0, te[1]], x=trailing_edge_divisions[0][:])
trailing_edge_divisions[2][:] = np.interp(xp=[top[1][0], te[0]], fp=[top[1][1], te[1]], x=trailing_edge_divisions[0][:])
trailing_edge_divisions[3][:] = np.interp(xp=[top[1][0], te[0]], fp=[bottom[1][1], te[1]],
                                          x=trailing_edge_divisions[0][:])

plt.figure(3)

plt.scatter(leading_edge_divisions[0][:], leading_edge_divisions[1][:], color="blue")
plt.scatter(leading_edge_divisions[0][:], leading_edge_divisions[2][:], color="red")
plt.scatter(leading_edge_divisions[0][:], leading_edge_divisions[3][:], color="red")

plt.scatter(midspan_divisions[0][:], midspan_divisions[1][:], color="blue")
plt.scatter(midspan_divisions[0][:], midspan_divisions[2][:], color="red")
plt.scatter(midspan_divisions[0][:], midspan_divisions[3][:], color="red")

plt.scatter(trailing_edge_divisions[0][:], trailing_edge_divisions[1][:], color="blue")
plt.scatter(trailing_edge_divisions[0][:], trailing_edge_divisions[2][:], color="red")
plt.scatter(trailing_edge_divisions[0][:], trailing_edge_divisions[3][:], color="red")

plt.grid()
plt.axis('equal')
# plt.show()

# Combine Grid Points
sum_of_divisions = le_divisions + te_divisions + mid_divisions - 2
total_grids = (le_divisions + te_divisions + mid_divisions - 2) * 3
x_points = np.zeros([1, total_grids])
y_points = np.zeros([1, total_grids])
z_points = np.zeros([1, total_grids])
print('Sum of divisions: %s' % str(sum_of_divisions))

# Top Surface
for n in range(le_divisions):
    x_points[0][n] = leading_edge_divisions[0][n]
    y_points[0][n] = leading_edge_divisions[2][n]

    x_points[0][n + sum_of_divisions] = leading_edge_divisions[0][n]
    y_points[0][n + sum_of_divisions] = leading_edge_divisions[1][n]

    x_points[0][n + 2 * sum_of_divisions] = leading_edge_divisions[0][n]
    y_points[0][n + 2 * sum_of_divisions] = leading_edge_divisions[3][n]

for n in range(mid_divisions - 1):
    x_points[0][n + le_divisions] = midspan_divisions[0][n + 1]
    y_points[0][n + le_divisions] = midspan_divisions[2][n + 1]

    x_points[0][n + le_divisions + sum_of_divisions] = midspan_divisions[0][n + 1]
    y_points[0][n + le_divisions + sum_of_divisions] = midspan_divisions[1][n + 1]

    x_points[0][n + le_divisions + 2 * sum_of_divisions] = midspan_divisions[0][n + 1]
    y_points[0][n + le_divisions + 2 * sum_of_divisions] = midspan_divisions[3][n + 1]

for n in range(te_divisions - 1):
    x_points[0][n + le_divisions + mid_divisions - 1] = trailing_edge_divisions[0][n + 1]
    y_points[0][n + le_divisions + mid_divisions - 1] = trailing_edge_divisions[2][n + 1]

    x_points[0][n + le_divisions + mid_divisions - 1 + sum_of_divisions] = trailing_edge_divisions[0][n + 1]
    y_points[0][n + le_divisions + mid_divisions - 1 + sum_of_divisions] = trailing_edge_divisions[1][n + 1]

    x_points[0][n + le_divisions + mid_divisions - 1 + 2 * sum_of_divisions] = trailing_edge_divisions[0][n + 1]
    y_points[0][n + le_divisions + mid_divisions - 1 + 2 * sum_of_divisions] = trailing_edge_divisions[3][n + 1]

# write out grid points
# look into panukl
fid = open('Grid_List.dat', 'w')
fid.write('Grid Points \n')
fid.write('No%s' % empty_space(6))
fid.write('X %s' % empty_space(6))
fid.write('Y %s' % empty_space(6))
fid.write('Z %s\n' % empty_space(6))

for n in range(len(x_points[0])):
    fid.write('%s%s' % (str(n+1), empty_space(8-len(str(n+1)))))
    fid.write('%s%s' % (str(round(x_points[0][n], 4)), empty_space(8-len(str(round(x_points[0][n], 4))))))
    fid.write('%s%s' % (str(round(y_points[0][n], 4)), empty_space(8 - len(str(round(y_points[0][n], 4))))))
    fid.write('%s%s\n' % (str(0.0), empty_space(8 - len(str(0.0)))))

fid.write('\n\nMesh Panels\n')
fid.write('No%s' % empty_space(6))
fid.write('P1%s' % empty_space(6))
fid.write('P2%s' % empty_space(6))
fid.write('P3%s' % empty_space(6))
fid.write('P4%s\n' % empty_space(6))


plt.figure(4)
plt.grid()
plt.scatter(x_points, y_points)
plt.axis('equal')

print(x_points)
fid.close()
plt.show()



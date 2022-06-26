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
from WingSpecs import trap_fin_build, add_points_trailing_edge, add_points_leading_edge, add_points_midspan


# Set up airfoil parameters
chord_length = 1
leading_edge_length = 0.25 * chord_length
flap_length = 0.3 * chord_length
max_thickness = 0.05 * chord_length
flap_angle = np.deg2rad(-10)
# flap_angle = np.deg2rad(float(input('Input Flap Angle: ')))

# Build Airfoil Points
[le, te, top, bottom] = trap_fin_build(chord_length, leading_edge_length, flap_length, max_thickness, flap_angle)

# Input division numbers
le_divisions = 2
mid_divisions = 2
te_divisions = 2

le_points = add_points_leading_edge(le, top, bottom, le_divisions)
mid_points = add_points_midspan(top, max_thickness, mid_divisions)
te_points = add_points_trailing_edge(te_divisions, top, te, bottom)


# # Combine Grid Points
# sum_of_divisions = le_divisions + te_divisions + mid_divisions - 2
# total_grids = (le_divisions + te_divisions + mid_divisions - 2) * 3
# x_points = np.zeros([1, total_grids])
# y_points = np.zeros([1, total_grids])
# z_points = np.zeros([1, total_grids])
# print('Sum of divisions: %s' % str(sum_of_divisions))
#
# # Top Surface
# for n in range(le_divisions):
#     x_points[0][n] = leading_edge_divisions[0][n]
#     y_points[0][n] = leading_edge_divisions[2][n]
#
#     x_points[0][n + sum_of_divisions] = leading_edge_divisions[0][n]
#     y_points[0][n + sum_of_divisions] = leading_edge_divisions[1][n]
#
#     x_points[0][n + 2 * sum_of_divisions] = leading_edge_divisions[0][n]
#     y_points[0][n + 2 * sum_of_divisions] = leading_edge_divisions[3][n]
#
# for n in range(mid_divisions - 1):
#     x_points[0][n + le_divisions] = midspan_divisions[0][n + 1]
#     y_points[0][n + le_divisions] = midspan_divisions[2][n + 1]
#
#     x_points[0][n + le_divisions + sum_of_divisions] = midspan_divisions[0][n + 1]
#     y_points[0][n + le_divisions + sum_of_divisions] = midspan_divisions[1][n + 1]
#
#     x_points[0][n + le_divisions + 2 * sum_of_divisions] = midspan_divisions[0][n + 1]
#     y_points[0][n + le_divisions + 2 * sum_of_divisions] = midspan_divisions[3][n + 1]
#
# for n in range(te_divisions - 1):
#     x_points[0][n + le_divisions + mid_divisions - 1] = trailing_edge_divisions[0][n + 1]
#     y_points[0][n + le_divisions + mid_divisions - 1] = trailing_edge_divisions[2][n + 1]
#
#     x_points[0][n + le_divisions + mid_divisions - 1 + sum_of_divisions] = trailing_edge_divisions[0][n + 1]
#     y_points[0][n + le_divisions + mid_divisions - 1 + sum_of_divisions] = trailing_edge_divisions[1][n + 1]
#
#     x_points[0][n + le_divisions + mid_divisions - 1 + 2 * sum_of_divisions] = trailing_edge_divisions[0][n + 1]
#     y_points[0][n + le_divisions + mid_divisions - 1 + 2 * sum_of_divisions] = trailing_edge_divisions[3][n + 1]
#
# # write out grid points
# # look into panukl
# fid = open('Grid_List.dat', 'w')
# fid.write('Grid Points \n')
# fid.write('No%s' % empty_space(6))
# fid.write('X %s' % empty_space(6))
# fid.write('Y %s' % empty_space(6))
# fid.write('Z %s\n' % empty_space(6))
#
# for n in range(len(x_points[0])):
#     fid.write('%s%s' % (str(n+1), empty_space(8-len(str(n+1)))))
#     fid.write('%s%s' % (str(round(x_points[0][n], 4)), empty_space(8-len(str(round(x_points[0][n], 4))))))
#     fid.write('%s%s' % (str(round(y_points[0][n], 4)), empty_space(8 - len(str(round(y_points[0][n], 4))))))
#     fid.write('%s%s\n' % (str(0.0), empty_space(8 - len(str(0.0)))))
#
# fid.write('\n\nMesh Panels\n')
# fid.write('No%s' % empty_space(6))
# fid.write('P1%s' % empty_space(6))
# fid.write('P2%s' % empty_space(6))
# fid.write('P3%s' % empty_space(6))
# fid.write('P4%s\n' % empty_space(6))
#
#
# plt.figure(4)
# plt.grid()
# plt.scatter(x_points, y_points)
# plt.axis('equal')
#
# print(x_points)
# fid.close()
# plt.show()



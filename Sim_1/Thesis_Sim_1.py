# -----------------------------------------------------------------------------------------------------------------
# Project     : Thomas Lando Thesis (Honours)
# Title       : Simulation 1: 2D Theory
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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Theodoreson_Constants import t_constants
from C_k_function import c_function
from simulation_tools import*

a = -0.5
c = 0.5
b = 1

h_num = 2
v_num = 2
h = np.linspace(10, 100e3, num=h_num)
v = np.linspace(2, 200, num=v_num)

# "Wow this is going to suck" - my computer
fid = open('Results.dat', 'w')

fid.write('2D 3DOF Simulation\n')
fid.write('\n\n')

plt.figure(1)
plt.grid()
plt.xlabel('Velocity (m/s)')
plt.ylabel('Real Eigenvalue')
for n1 in range(h_num):
    height = h[n1]
    fid.write('Altitude (m): %s\n' % str(height))
    for n2 in range(v_num):
        velocity = v[n2]
        fid.write('Velocity (m/s): %s\n' % str(velocity))
        A, B, C, D, E, F = iterate_frequency(v=velocity, w0=100, h=height, a=a, c=c, b=b)
        # Create System Matrix
        top_left = np.linalg.inv(A-D)*(E-B)
        top_right = np.linalg.inv(A-D)*(F-C)
        bot_left = np.identity(3)
        bot_right = np.zeros([3, 3])
        System = [[top_left, top_right], [bot_left, bot_right]]
        eigenvalues, eigenvectors = np.linalg.eig(System)

        fid.write('Eigenvalues : %s %s\n              %s %s\n\n' % (str(eigenvalues[0][0]), str(eigenvalues[0][1]),
                                                      str(eigenvalues[1][0]), str(eigenvalues[1][1])))

        plt.scatter(velocity, np.real(eigenvalues[0][0][0]), color='red')
        plt.scatter(velocity, np.real(eigenvalues[0][0][1]), color='blue')
        plt.scatter(velocity, np.real(eigenvalues[0][0][2]), color='black')

        plt.scatter(velocity, np.real(eigenvalues[0][1][0]), color='grey')
        plt.scatter(velocity, np.real(eigenvalues[0][1][1]), color='pink')
        plt.scatter(velocity, np.real(eigenvalues[0][1][2]), color='purple')
        if np.real(eigenvalues[0][0][2]) > 0:
            print(height)
            print(velocity)
            break

plt.show()

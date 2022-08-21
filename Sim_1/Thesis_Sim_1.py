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

a = -0.25
c = 0.5
b = 1

h_num = 5
v_num = 10000
w_num = 2
h = np.linspace(10, 100e3, num=h_num)
v = np.linspace(0.001, 10e3, num=v_num)
w = np.linspace(1.0001, 2, num=w_num)

# "Wow this is going to suck" - my computer
fid = open('Results.dat', 'w')

fid.write('2D 3DOF Simulation\n')
fid.write('\n\n')

plt.figure(1)
plt.grid()
plt.xlabel('Height (m)')
plt.ylabel('Velocity')
count = 0
for n1 in range(h_num):
    height = h[n1]

    for n2 in range(v_num):
        velocity = v[n2]
        check = False
        for n3 in range(w_num):
            count += 1
            # print(count)
            omega = w[n3]
            A, B, C, D, E, F = iterate_frequency(v=velocity, w=omega, h=height, a=a, c=c, b=b)
            A = -omega**2 * A
            D = -omega**2 * D
            B = complex(0, omega) * B
            E = complex(0, omega) * E
            system = A + B + C - (D + E + F)
            eigenvalues, eigenvectors = np.linalg.eig(system)

            if np.real(eigenvalues)[0] >= 0 or np.real(eigenvalues)[1] >= 0 or np.real(eigenvalues)[2] >= 0:
                print('Flutter at : %s' % str(count))
                fid.write('Altitude (m): %s\n' % str(height))
                fid.write('Velocity (m/s): %s\n' % str(velocity))
                fid.write('Circular Frequency (rad/s): %s\n' % str(omega))
                fid.write('Eigenvalues: %s\n\n' % str(eigenvalues))

                # Reset our frequency vector
                w_num = w_num - n3
                print(n3)
                w = np.linspace(omega, 1e6, w_num)

                plt.scatter(height, velocity, color='blue')

                check = True
                break

        if check:
            break

fid.close()
plt.show()

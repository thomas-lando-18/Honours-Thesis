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

import numpy as np
import pandas as pd
from Theodoreson_Constants import t_constants
from C_k_function import c_function
from simulation_tools import*

a = -0.5
c = 0.5
b = 1

h = np.linspace(10, 100e3, num=100)
v = np.linspace(200, 5000, num=20)

# "Wow this is going to suck" - my computer
fid = open('Results.dat', 'w')

fid.write('2D 3DOF Simulation\n')
fid.write('\n\n')


for n1 in range(100):
    height = h[n1]
    fid.write('Altitude (m): %s\n' % str(height))
    for n2 in range(20):
        velocity = v[n2]
        fid.write('Velocity (m/s): %s\n' % str(velocity))
        A, B, C, D, E, F = iterate_frequency(v=velocity, w0=0, h=height, a=a, c=c, b=b)
        # Create System Matrix
        top_left = np.linalg.inv(A-D)*(E-B)
        top_right = np.linalg.inv(A-D)*(F-C)
        bot_left = np.identity(3)
        bot_right = np.zeros([3, 3])
        System = [[top_left, top_right], [bot_left, bot_right]]

        eigenvalues = np.linalg.eig(System)
        fid.write('Eigenvalues : %s \n\n' % str(eigenvalues))



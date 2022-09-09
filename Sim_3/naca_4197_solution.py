# Imports
import numpy as np
import matplotlib.pyplot as plt
from Thesis_Sim_3 import density


# Script functions
def barometric_formula(height):
    p0 = 101325.0
    # rho0 = 1.125
    temp0 = 273+15.0
    g0 = 9.81
    h0 = 8500.0
    R = 287

    p = p0*np.exp((-g0*(height-h0))/(R * temp0))
    rho = density(height)
    temp = p/(rho*R)
    return temp, rho, p


# span = np.linspace(1.0, 4.0, num=10)
# taper = np.linspace(0.01, 1.0, num=10)
# root = np.linspace(0.15, 1, num=10)
#
# number_of_tests = 200
# height = np.linspace(0.0, 50000, number_of_tests)
# temperature = []
# rho = []
# pressure = []
#
# Ge = 4e6
# pa2lb = 0.000145038
# p0 = 101325*pa2lb
#
# for m in range(10):
#     aspect_ratio = span[m]**2 / (root[m]*span[m])
#     vf_a = []
#     for n in range(number_of_tests):
#         t, q, p = barometric_formula(height[n])
#         temperature.append(t)
#         rho.append(q)
#         pressure.append(p)


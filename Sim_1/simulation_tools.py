# Script holding tools used in Simulation 1

# Imports
import numpy as np
from wing_model.naca45 import*
from wing_model.inertial_properties import*
from C_k_function import*
from Theodoreson_Constants import*


# Functions
def aero_equations_of_motion():

    matrix_a = np.zeros([3, 3])
    matrix_b = np.zeros([3, 3])
    matrix_c = np.zeros([3, 3])

    yu, yl, xu, xl = naca_4_digit()
    area = foil_area_2d(yu, yl, xu, xl)
    m = mass_of_foil(area=area, density=1150, span=1)
    i_a = inertial_moment_alpha(m=m, xl=xl, xu=xu, yl=yl, yu=yu)
    i_b = inertial_moment_beta(yu, yl, xu, xl, [0.6, 0], m)

    c = 1
    a = 0.6


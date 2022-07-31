# This Script contains functions used in caluclating the properties of the wing

# Imports
import numpy as np
import scipy as sc
from naca45 import*


# Functions

# Find Area from trapezoidal rule

def foil_area_2d(yu, yl, xu, xl):

    area = 0
    for n in range(len(xl[:])-1):
        dx_upper = xu[n+1] - xu[n]
        dx_lower = xl[n+1] - xl[n]
        y_upper = yu[n+1] + yu[n]
        y_lower = yl[n+1] + yl[n]

        area_upper = 0.5 * y_upper * dx_upper
        area_lower = 0.5 * y_lower * dx_lower
        area = area + area_upper - area_lower

    return area


def mass_of_foil(density, span, area):
    mass = density * span * area
    return mass


def inertial_moment_alpha(yu, yl, xu, xl, m):
    # Need to do this calculation before the hinge is added
    ref_point = [xu[len(xu)-1], yu[len(yu)-1]]
    radius_vector = []
    for n in range(len(xu)-1):
        dxu = -xu[n] + ref_point[0]
        dxl = -xl[n] + ref_point[0]
        dyu = -yu[n] + ref_point[1]
        dyl = -yl[n] + ref_point[1]

        ru = np.sqrt(dxu**2 + dyu**2)
        rl = np.sqrt(dxl**2 + dyl**2)

        radius_vector.append(ru)
        radius_vector.append(rl)

    I = sum(radius_vector) * m

    return I


def inertial_moment_beta(yu, yl, xu, xl, hinge_point, m):
    radius_vector = []
    for n in range(len(xu) - 1):
        dxu = -xu[n] + hinge_point[0]
        dxl = -xl[n] + hinge_point[0]
        dyu = -yu[n] + hinge_point[1]
        dyl = -yl[n] + hinge_point[1]

        ru = np.sqrt(dxu ** 2 + dyu ** 2)
        rl = np.sqrt(dxl ** 2 + dyl ** 2)

        radius_vector.append(ru)
        radius_vector.append(rl)

    I = sum(radius_vector) * m

    return I


# Testing
# yu, yl, xu, xl = naca_4_digit(num=100, chord=0.1)
# area = foil_area_2d(yu, yl, xu, xl)
# m = mass_of_foil(density=1152, area=area, span=1)
# I_alpha = inertial_moment_alpha(yu, yl, xu, xl, m)
# print(I_alpha)
# I_beta = inertial_moment_beta(yu, yl, xu, xl, [0.075, 0], m)
# print(I_beta)


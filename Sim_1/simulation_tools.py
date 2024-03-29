# Script holding tools used in Simulation 1

# Imports
import numpy as np
from wing_model.naca45 import *
from wing_model.inertial_properties import *
from C_k_function import *
from Theodoreson_Constants import *


# Functions
def aero_equations_of_motion(a, c, b, w):
    matrix_a = np.zeros([3, 3])
    matrix_b = np.zeros([3, 3])
    matrix_c = np.zeros([3, 3])
    #  Need to ad flap angle to wing model, perhaps make a wing model build/ calculate functions for sim 1,
    #  sims 2 and 3 can use the main 3d one.
    w_a = 8
    w_b = 8
    w_h = 8
    yu, yl, xu, xl = naca_4_digit(m=2, p=4, xx=12, num=10, chord=0.5)
    area = foil_area_2d(yu, yl, xu, xl)
    m = mass_of_foil(area=area, density=1150/9, span=b)
    i_a = inertial_moment_alpha(m=m, xl=xl, xu=xu, yl=yl, yu=yu)
    i_b = inertial_moment_beta(yu, yl, xu, xl, [0.6, 0], m)
    d_a = i_a*w_a**2 * 9.81/w
    d_b = i_b*w_b**2*9.81/w
    d_h = m*w_h**2*9.81/w
    s_a = static_moment_alpha(yu, yl, xu, xl, m)
    s_b = static_moment_beta(yu, yl, xu, xl, [0.6, 0], m)
    c_a = torsional_stiffness_alpha(i_a, w_a)
    c_b = torsional_stiffness_beta(i_b, w_b)
    c_h = torsional_stiffness_span(m, w_h)

    A = np.zeros([3, 3])
    B = A
    C = A

    A[0, 0] = i_a
    A[0, 1] = i_b + b * (c - a) * s_b
    A[0, 2] = s_a

    A[1, 0] = i_b + b * (c - a) * s_b
    A[1, 1] = i_b
    A[1, 2] = s_b

    A[2, 0] = s_a
    A[2, 1] = s_b
    A[2, 2] = m

    B[0, 0] = d_a
    B[1, 1] = d_b
    B[2, 2] = d_h

    C[0, 0] = c_a
    C[1, 1] = c_b
    C[2, 2] = c_h

    return A, B, C


def density(h: float):
    rho0 = 1.225
    hs = 8500
    rho = rho0 * np.exp(-h / hs)
    return rho


def aero_forces(a, c, h, k, b, v):

    T = t_constants(a, c)
    rho = density(h)
    c = c_function(k)

    D = np.zeros([3, 3], dtype='complex_')
    E = np.zeros([3, 3], dtype='complex_')
    F = np.zeros([3, 3], dtype='complex_')

    # This is going to hurt
    D[0, 0] = -rho * b ** 4 * np.pi * (1 / 8 + a ** 2)
    D[0, 1] = rho * b ** 4 * (T[6] + (c - a) * T[0])
    D[0, 2] = rho * b ** 3 * a * np.pi

    D[1, 0] = -rho * b ** 4 * 2 * T[12]
    D[1, 1] = rho * b ** 4 * 1 / np.pi * T[2]
    D[1, 2] = rho * b ** 3 * T[0]

    D[2, 0] = rho * b ** 3 * np.pi * a
    D[2, 1] = -rho * b ** 3 * T[0]
    D[2, 2] = -rho * b ** 2 * np.pi

    E[0, 0] = -rho * b ** 3 * np.pi * (1 / 2 - a) * v + 2 * rho * v * b ** 3 * np.pi * (a ** 2 - 1 / 4) * c
    E[0, 1] = -rho * b ** 3 * (T[0] - T[7] - (c - a) * T[3] + 1 / 2 * T[10]) * v + rho * v * b ** 3 * (a + 1 / 2) * c * \
        T[10]
    E[0, 2] = 2 * rho * v * b ** 2 * np.pi * (a + 1 / 2) * c

    E[1, 0] = -rho * b ** 3 * (-2 * T[8] - T[0] + T[3] * (a - 1 / 2)) * v - rho * v * b ** 3 * T[11] * c * (1 / 2 - a)
    E[1, 1] = rho*b**3*1/(2*np.pi)*v*T[3]*T[10] - rho*v*b**3*T[11]*c*1/(2*np.pi)*T[10]
    E[1, 2] = -rho*v*b**2*T[11]*c

    E[2, 0] = -rho*b**2*v*np.pi - 2*np.pi*rho*v*b**2*c*(1/2-a)
    E[2, 1] = rho*b**2*v*T[3] - rho*v*b**2*c*T[10]
    E[2, 2] = -2*np.pi*rho*v*b*c

    F[0, 0] = 2*rho*v**2*b**2*np.pi*(a+1/2)*c
    F[0, 1] = -rho*b**2*(T[3]+T[9])*v**2 + 2*rho*v**2*b**2*(a+1/2)*c*T[9]

    F[1, 0] = -rho*v**2*b**2*T[11]*c
    F[1, 1] = -rho*b**2*1/np.pi*v**2*(T[4]-T[3]*T[9]) - rho*v**2*b**2*T[11]*c*1/np.pi*T[9]

    F[2, 0] = -2*np.pi*rho*v**2*b*c
    F[2, 1] = -2*rho*v**2*b*c*T[9]

    return D, E, F


def iterate_frequency(v, w, h, a, c, b):
    k = w*b/v
    A, B, C = aero_equations_of_motion(a=a, b=b, c=c, w=w)
    D, E, F = aero_forces(a=a, c=c, h=h, k=k, b=b, v=v)

    return A, B, C, D, E, F




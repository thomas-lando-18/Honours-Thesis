# Imports
import numpy
import numpy as np
from matplotlib import pyplot as plt
from inertial_properties import*
from sim_functions import *
from Theodoreson_Constants import t_constants
from C_k_function import c_function
from wing_model.wing_build import main as wing
import scipy as sc
from scipy import signal


def controller_system(geometry, inertial_properties, rho_air, rfreq, a, c, velocity, p):
    c_k = c_function(rfreq)
    T = t_constants(a, c)

    # Create the matrices
    A11 = inertial_properties["r_a"]**2 + inertial_properties["kappa"]*(1/8 + a**2)
    A21 = inertial_properties["r_b"]**2 + (c-a)*inertial_properties["x_b"] - inertial_properties["kappa"]*T[6]/np.pi- (c-a)*T[0]*inertial_properties["kappa"]/np.pi
    A31 = inertial_properties["x_a"] - inertial_properties["kappa"]*a

    A12 = inertial_properties["r_b"]**2 + (c-a)*inertial_properties["x_b"] - inertial_properties["kappa"]*T[6]/np.pi- (c-a)*T[0]*inertial_properties["kappa"]/np.pi
    A22 = inertial_properties["r_b"]**2 - 1/np.pi**2 * inertial_properties["kappa"]*T[2]
    A32 = inertial_properties["x_b"] - 1/np.pi*T[0]*inertial_properties["kappa"]

    A13 = inertial_properties["x_a"] - a*inertial_properties["kappa"]
    A23 = 1/geometry["Wing Properties"]["Span"]*(inertial_properties["x_b"]-1/np.pi*inertial_properties["kappa"]*T[0])
    A33 = 1/geometry["Wing Properties"]["Span"]*(1+inertial_properties["kappa"])

    A = np.matrix([[-A11, -A12, -A13], [-A21, -A22, -A23], [-A31, -A32, -A33]])

    B11 = velocity/geometry["Wing Properties"]["Span"] * inertial_properties["kappa"]* (0.5-a) - 2*inertial_properties["kappa"]*(a+0.5)*velocity*c_k/geometry["Wing Properties"]["Span"]*(0.5-a)
    B21 = velocity/geometry["Wing Properties"]["Span"]*inertial_properties["kappa"]/np.pi*(p-T[0] - 0.5*T[10]) + T[11]/np.pi * inertial_properties["kappa"]*velocity*c_k/geometry["Wing Properties"]["Span"]*(0.5 - a)
    B31 = velocity/geometry["Wing Properties"]["Span"]*inertial_properties["kappa"]+ 2*inertial_properties["kappa"]*velocity*c_k/geometry["Wing Properties"]["Span"]*(0.5-a)

    B12 = 1/np.pi * inertial_properties["kappa"]*velocity/geometry["Wing Properties"]["Span"]*(-2*p-(0.5-a)*T[3]) - 2*inertial_properties["kappa"]*(a+0.5)*velocity*c_k*T[10]/(geometry["Wing Properties"]["Span"]*2*np.pi)
    B22 = -1/(2*np.pi**2)*T[3]*T[10]*velocity/geometry["Wing Properties"]["Span"]*inertial_properties["kappa"]+T[11]/np.pi * inertial_properties["kappa"]*velocity*c_k*T[10]/(geometry["Wing Properties"]["Span"]*2*np.pi)
    B32 = velocity/c*T[3]*inertial_properties["kappa"]*1/np.pi + 2*inertial_properties["kappa"]*velocity*c_k*T[10]/(geometry["Wing Properties"]["Span"]*2*np.pi)

    B13 = -2 * inertial_properties["kappa"]*(a+0.5)*velocity*c_k/geometry["Wing Properties"]["Span"]**2
    B23 = T[11]/np.pi*inertial_properties["kappa"]*velocity*c_k/geometry["Wing Properties"]["Span"]**2
    B33 = 2*inertial_properties["kappa"]*velocity*c_k/geometry["Wing Properties"]["Span"]**2

    B = numpy.matrix([[B11, B12, B13], [B21, B22, B23], [B31, B32, B33]])

    C11 = inertial_properties["C_a"]/(inertial_properties["mass"]*geometry["Wing Properties"]["Span"]**2)-2*inertial_properties["kappa"]*(a+0.5)*velocity**2*c_k/geometry["Wing Properties"]["Span"]**2
    C21 = T[11]/np.pi * inertial_properties["kappa"]*velocity**2*c_k/geometry["Wing Properties"]["Span"]**2
    C31 = 2*inertial_properties["kappa"]*velocity**2*c_k/geometry["Wing Properties"]["Span"]**2

    C12 = inertial_properties["kappa"]*velocity**2/geometry["Wing Properties"]["Span"]**2*1/np.pi*(T[3]-T[9]-2*inertial_properties["kappa"]*(a+0.5)*velocity**2*c_k/geometry["Wing Properties"]["Span"]**2*T[9]/np.pi)
    C22 = inertial_properties["C_b"]/(inertial_properties["mass"]*geometry["Wing Properties"]["Span"]**2)  +1/np.pi**2 * velocity**2/geometry["Wing Properties"]["Span"]**2*inertial_properties["kappa"]*(T[4] - T[3]*T[9]) + T[11]/np.pi * inertial_properties["kappa"]*velocity**2*c_k/geometry["Wing Properties"]["Span"]**2*T[9]/np.pi
    C32 = 2*inertial_properties["kappa"]*velocity**2*c_k/geometry["Wing Properties"]["Span"]**2 * T[9]/np.pi

    C13 = 0
    C23 = 0
    C33 = inertial_properties["C_h"]/inertial_properties["mass"]*1/geometry["Wing Properties"]["Span"]

    C = numpy.matrix([[C11, C12, C13], [C21, C22, C23], [C31, C32, C33]])
    # print(C.shape)
    # print([C11, C12, C13])
    # print([C21, C22, C23])
    # print([C31, C32, C33])
    identity = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    zero = np.matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    # Create System Matrix
    system_top_left = np.matmul(np.linalg.inv(A), B)
    # print(system_top_left)
    system_top_right = np.matmul(np.linalg.inv(A), C)
    # print(system_top_right)
    system_bottom_left = identity
    system_bottom_right = zero

    system_top = np.hstack((system_top_left, system_top_right))
    system_bottom = np.hstack((system_bottom_left, system_bottom_right))
    system = np.matrix(np.vstack((system_top, system_bottom)))
    # print(system.shape)
    # print(system)
    eigenvalues = np.linalg.eigvals(system)
    return system, eigenvalues


def controller_gains(beta_control, foil, span, sweep, root_chord, taper, rho_air, velocity, rfreq, flutter_v):
    geometry0 = wing(foil=foil, semi_span=span, sweep=sweep, root_chord=root_chord, taper=taper, chord_num=15, num=15,
                     beta=np.deg2rad(0), plot=False, flap_point=0.4)
    geometry45 = wing(foil=foil, semi_span=span, sweep=sweep, root_chord=root_chord, taper=taper, chord_num=15, num=15,
                     beta=np.deg2rad(beta_control), plot=False, flap_point=0.4)

    # rho_air = 0.067
    # velocity = 1030.0
    # rfreq = 0.02
    # flutter_v = 1234.4

    inertial_properties = panel_inertial_calculations(geometry0, rho_air)
    inertial_properties45 = panel_inertial_calculations(geometry45, rho_air)

    a0 = inertial_properties["r_a"] - 0.5*geometry0["Wing Properties"]["Span"]
    a45 = inertial_properties45["r_a"] - 0.5 * geometry45["Wing Properties"]["Span"]

    c0 = geometry0["Wing Properties"]["Flap Point"] - 0.5*geometry0["Wing Properties"]["Span"]
    c45 = geometry45["Wing Properties"]["Flap Point"] - 0.5 * geometry45["Wing Properties"]["Span"]

    system0, eigenvalue0 = controller_system(a=a0, c=c0, geometry=geometry0, rfreq=rfreq, rho_air=rho_air, velocity=velocity, inertial_properties=inertial_properties, p=0.0)
    system45, eigenvalue45 = controller_system(a=a45, c=c45, geometry=geometry45, rfreq=rfreq, rho_air=rho_air, velocity=velocity, inertial_properties=inertial_properties45, p=0.0)

    K = eigenvalue45 - eigenvalue0
    b_k = np.matrix([[0, 0, 0, 0, 0, 0], K, [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    # C = np.matrix([[0, 1, 0, 0, 1, 0]])
    # kr1 = system0 - b_k
    # kr2 = np.linalg.inv(kr1)
    # kr3 = np.matmul(C, kr2)
    # kr4 = kr3[:, 1]
    # kr = -1/kr4
    # if flutter_v is not None:
    #     reference = (flutter_v - velocity) / flutter_v
    # theta = np.arctan(np.imag(kr) / np.real(kr))
    # # reference = 1
    return b_k, system0



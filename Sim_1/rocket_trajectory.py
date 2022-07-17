# Imports
import numpy as np
import matplotlib.pyplot as plt

# Functions


# Main run function
def main():
    # Conversion Factors
    deg = np.pi/180
    g0 = 9.81
    r_earth = 6378e3
    h_scale = 7.5e3
    rho0 = 1.225

    # Vehicle Features
    diam = 196.85/12 * 0.3048
    area = np.pi/4 * diam**2
    cd = 0.5
    m0 = 149912*0.4536
    n = 15
    t2w = 1.4
    isp = 390

    m_final = m0/n
    thrust = t2w*m0*g0
    m_dot = thrust/(isp*g0)
    m_propellent = m0 - m_final

    # Simulation Times
    t_burn = m_propellent/m_dot
    h_turn = 130
    t0 = 0
    tf = t_burn
    tspan = [t0, tf]

    # Initial conditions



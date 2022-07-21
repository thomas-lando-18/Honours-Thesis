# Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import RK45


# Functions
def rates(t, f):
    """
    Calculates the time rates df/dt of the variables f(t) in the equations of motion of a gravity turn trajectory
    :param t_burn:
    :param t:
    :param f:
    :return:
    """
    v = f[0]
    gamma = f[1]
    x = f[2]
    h = f[3]
    vd = f[4]
    vg = f[5]
    if t < t_burn:
        m = m0 - m_dot
        T = thrust
    else:
        m = m0 - m_dot * t_burn
        T = 0

    g = g0 / (1 + h / r_earth) ** 2

    rho = rho0 * np.exp((-h / h_scale))
    drag = 0.5 * rho * v ** 2 * area * cd

    # First derivatives

    # When h < hturn. start the gravity turn
    if h < h_turn or h == h_turn:
        gamma_dot = 0
        v_dot = T / m - drag / m - g
        x_dot = 0
        y_dot = v
        vg_dot = -g
    else:
        v_dot = T / m - drag / m - g * np.sin(gamma)
        gamma_dot = -1 / v * (g - v ** 2 / (r_earth + h)) * np.cos(gamma)
        x_dot = r_earth / (r_earth + h) * v * np.cos(gamma)
        h_dot = v * np.sin(gamma)
        vg_dot = -g * np.sin(gamma)

    vd_dot = -drag / m

    dfdt = [v_dot, gamma_dot, x_dot, h_dot, vd_dot, vg_dot]

    return dfdt


def rkf45(fun, tspan, y0, tolerance=1e-8):
    a = [0, 1 / 4, 3 / 8, 12 / 13, 1, 1 / 2]
    b = [[0, 0, 0, 0, 0], [1 / 4, 0, 0, 0, 0], [3 / 32, 9 / 32, 0, 0, 0],
         [1932 / 2197, -7200 / 2197, 7296 / 2197, 0, 0],
         [439 / 216, -8, 3680 / 513, -845 / 4104, 0], [-8 / 27, 2, -3544 / 2565, 1859 / 4104, -11 / 40]]

    c4 = [25/216, 0, 1408/2565, 2197/4104, -1/5, 0]
    c5 = [16/135, 0, 6656/12825, 28561/56430, -9/50, 2/55]

    t0 = tspan[0]
    tf = tspan[1]
    t = t0
    y = y0
    tout = t
    yout = np.transpose(y)
    h = (tf-t0)/100

    while t < tf:
        hmin = 16 * np.finfo(float).eps(t)
        ti = t
        yi = y
        for n in range(6):
            t_inner = ti + a[n]*h
            y_inner = yi
            for m in range(n-1):
                y_inner = y_inner + h*b[n][m]*f[:][m]

# Main run function
# Conversion Factors
deg = np.pi / 180
g0 = 9.81
r_earth = 6378e3
h_scale = 7.5e3
rho0 = 1.225

# Vehicle Features
diam = 196.85 / 12 * 0.3048
area = np.pi / 4 * diam ** 2
cd = 0.5
m0 = 149912 * 0.4536
n = 15
t2w = 1.4
isp = 390

m_final = m0 / n
thrust = t2w * m0 * g0
m_dot = thrust / (isp * g0)
m_propellent = m0 - m_final

# Simulation Times
t_burn = m_propellent / m_dot
h_turn = 130
t0 = 0
tf = t_burn
t_span = [t0, tf]

# Initial conditions
v0 = 0
gamma0 = 89.85 * deg
x0 = 0
h0 = 0
v_drag_loss0 = 0
v_gravity_loss0 = 0

# State Vector
f0 = [[v0], [gamma0], [x0], [h0], [v_drag_loss0], [v_gravity_loss0]]

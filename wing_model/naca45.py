
# Imports
import numpy as np
import matplotlib.pyplot as plt


def naca_4_digit(m=2, p=4, xx=12, num=10):
    """
    Creates a NACA 4 digit foil in the designated number of points
    :param M: First Digit
    :param P: Second Digit
    :param XX: Final Two Digits
    :param num: Number of points to be generated
    :return: 2 x num matrix of points
    """
    x = np.linspace(0, 1, num=num)

    # Create Camber line values
    yc = []
    camber = 0
    for n in range(len(x)):
        if x[n] <= p:
            camber = m/p**2 * (2*p*x[n] - x[n]**2)
        elif x[n] > p:
            camber = m/(1-p)**2 * ((1-2*p) + 2*p*x[n] - x[n]**2)

        yc.append(camber)


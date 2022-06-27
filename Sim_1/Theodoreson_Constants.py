# This script contains the function used to calculate the T constants

import numpy as np


def t_constants(a, c):
    T = np.zeros(14)
    T[0] = -1/3*np.sqrt(1-c**2)*(2+c**2)+c*np.arccos(c)
    T[1] = c*(1-c**2)-np.sqrt(1-c**2)*np.arccos(c)+c*(np.arccos(c))**2
    T[2] = -(1/8+c**2)*(np.arccos(c))**2+1/4*c*np.sqrt(1-c**2)*np.arccos(c)*(7+2*c**2) - 1/8*(1-c**2)*(5*c**2+4)
    T[3] = -np.arccos(c) + c*np.sqrt(1-c**2)
    T[4] = -(1-c**2)-(np.arccos(c))**2+2*c*np.sqrt(1-c**2)*np.arccos(c)
    T[5] = T[1]
    T[6] = -(1/8+c**2)*np.arccos(c)+1/8*c*np.sqrt(1-c**2)*(7+2*c**2)
    T[7] = -1/3*np.sqrt(1-c**2)*(2*c**2+1)+c*np.arccos(c)
    T[8] = 1/2*(1/3*(np.sqrt(1-c**2))+a*T[3])
    T[9] = np.sqrt(1-c**2)+np.arccos(c)
    T[10] = np.arccos(c)*(1-2*c)+np.sqrt(1-c**2)*(2-c)
    T[11] = np.sqrt(1-c**2)*(2+c)-np.arccos(c)*(2*c+1)
    T[12] = 1/2*(-T[6]-(c-a)*T[0])
    T[13] = 1/16+1/2*a*c

    return T

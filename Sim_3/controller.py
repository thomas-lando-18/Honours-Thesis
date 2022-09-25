# Imports
import numpy as np
from matplotlib import pyplot as plt
from sim_functions import *
from Theodoreson_Constants import t_constants
from C_k_function import c_function

# Get T Constants
a = 1.0
c = 2.0
T = t_constants(a, c)

rfreq = 1.0
c_k = c_function(rfreq)

# Create the matrices
A11 = 0
A12 = 0
A13 = 0

A21 = 0
A22 = 0
A23 = 0

A31 = 0
A32 = 0
A33 = 0

A = -1*[[A11, A12, A13], [A21, A22, A23], [A31, A32, A33]]

B11 = 0
B12 = 0
B13 = 0

B21 = 0
B22 = 0
B23 = 0

B31 = 0
B32 = 0
B33 = 0

B = [[B11, B12, B13], [B21, B22, B23], [B31, B32, B33]]

C11 = 0
C12 = 0
C13 = 0

C21 = 0
C22 = 0
C23 = 0

C31 = 0
C32 = 0
C33 = 0

C = [[C11, C12, C13], [C21, C22, C23], [C31, C32, C33]]

system = [[np.linalg.inv(A)*B, np.linalg.inv(A)*B], [np.identity(3), np.zeros([3, 3])]]


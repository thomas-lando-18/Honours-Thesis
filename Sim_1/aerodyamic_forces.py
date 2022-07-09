# This Script contains the funcitons that calculate the unstaedy aerodynamic forces

# Import
import numpy as np
import scipy as sc

from C_k_function import c_function
from Theodoreson_Constants import t_constants

def find_aero_force():
    p = -rho
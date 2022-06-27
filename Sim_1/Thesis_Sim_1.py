# -----------------------------------------------------------------------------------------------------------------
# Project     : Thomas Lando Thesis (Honours)
# Title       : Simulation 1: 2D Theory
# Author      : Thomas Lando (SID: 490388538)
# Supervisor  : Gareth Vio
# Institution : The University of Sydney
# ------------------------------------------------------------------------------------------------------------------
#
# Description:
# This project is focused on the use of ... for the purposes of flutter suppression in a ... inspired rocket fin.
#
# Nomenclature:
#
# Code

import numpy as np
from Theodoreson_Constants import t_constants
from C_k_function import c_function

I_a = 3.375
I_b = 2.1e-5
m = 5.12
c = 0.5
d_a = 0.02
k_a = 3.12
w_ac = 357.1
a = -0.5
rho = 6.42e-3
s_p = 1.159
k_h = 2542
s_ab = 7.1e-44
zeta_ac = 0.598
b = 0.799
d_h = 27.43
s_b = 8.6e-4

T = t_constants(a, c)
c = c_function(0)


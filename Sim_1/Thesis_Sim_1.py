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

a = -0.5
c = 0.5

T = t_constants(a, c)
c = c_function(0)  # Initial

# Make aerodynamic forces matrix

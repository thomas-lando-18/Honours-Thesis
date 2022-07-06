# -----------------------------------------------------------------------------------------------------------------
# Project     : Thomas Lando Thesis (Honours)
# Title       : Simulation 2: 2D NASTRAN
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
# ------------------------------------------------------------------------------------------------------------------

# Import Packages
import pyNastran

# Functions
from uiuc_wing import uiuc_wing_build


# Set Wing Specs
filename = "UIUC Data/n0011sc.dat.txt"
chord = 1  # chord length in metres
beta = 10  # flap angle in degrees
hinge = 0.6  # location of hinge point in %chord

# Build wing mesh file
mesh_file = uiuc_wing_build(filename, chord, beta, hinge, plot=False)

# Create BDF card (NASTRAN input file)


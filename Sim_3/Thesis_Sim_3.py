# -----------------------------------------------------------------------------------------------------------------
# Project     : Thomas Lando Thesis (Honours)
# Title       : Simulation 3: 3D NASTRAN
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
import numpy as np
import os
import subprocess
import matplotlib.pyplot as plt
from wing_model.wing_build import main as wing
from bdf_functions import*


# Script Functions
def density(h: float):
    rho0 = 1.225
    hs = 8500
    rho = rho0 * np.exp(-h / hs)
    return rho


def main():
    number_tests = 100
    velocity = np.linspace(10, 400, num=number_tests)
    height = np.linspace(10, 100e3, num=number_tests)
    rho = []
    mach = []

    for n in range(number_tests):
        rho_n = density(height[n])
        rho.append(rho_n)
        mach_n = velocity[n] / 343.3
        mach.append(mach_n)

    # Wing Structure
    foil = '2412'
    r_c = 0.2
    taper = 0.75
    span = 1
    span_num = 10
    chord_num = 15
    geometry = wing(foil=foil, root_chord=r_c, taper=taper, semi_span=span, chord_num=chord_num, num=span_num,
                    plot=False)

    # BDF Card Build
    model = bdf_setup()
    geometry_cards(model=model, geometry=geometry, chord_num=chord_num)
    aerodynamic_cards(model=model, geometry=geometry, span_num=span_num, root_chord=r_c, taper=taper, span=span)
    solution_cards(model=model, rho=rho[0], mach=mach[0])

    model.write_bdf('nastran_files/3d_6dof_card.bdf')

    executable_path = str("C:\\Program Files\\MSC.Software\\NaPa_SE\\20211\\Nastran\\bin\\nastran.exe")
    bdf_path = "C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3\\nastran_files\\3d_6dof_card.bdf"

    os.chdir("C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3\\nastran_files")
    os.remove('3d_6dof_card.f04')
    os.remove('3d_6dof_card.f06')
    os.remove('3d_6dof_card.log')
    subprocess.run([executable_path, bdf_path])

    plt.figure(1)
    # plt.plot(height, velocity)
    plt.plot(height, mach)
    plt.plot(height, rho)
    plt.show()


if __name__ == '__main__':
    main()

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
from sim_functions import *
import random


# Script Functions
def main():
    # Foil Shapes
    # foils1 = ['0106', '0108', '0110', '0112', '1106', '1108', '1110', '1112', '2106', '2108', '2110', '2112']
    # foils1 = ['0206', '0208', '0210', '0212', '1206', '1208', '1210', '1212', '2206', '2208', '2210', '2212']
    # foils1 = ['0406', '0408', '0410', '0412', '1406', '1408', '1410', '1412', '2406', '2408', '2410', '2412']
    foils1 = ['2412']

    # Spans
    span = np.linspace(1.0, 4.0, num=10)
    taper = np.linspace(0.01, 1.0, num=10)
    root = np.linspace(0.15, 1, num=10)
    number_of_tests = 10
    height = np.linspace(0.0, 50000, number_of_tests)
    velocity = [round(np.sqrt(0.1**2 + 2*(3*9.8)*(height[n] - height[0])), 3) for n in range(number_of_tests-1)]
    velocity.insert(0, 0.1)

    mach = []
    temperature = []
    rho = []
    pressure = []
    for n in range(number_of_tests):
        t, q, p = barometric_formula(height[n])
        temperature.append(t)
        rho.append(q)
        pressure.append(p)
        mach.append(round(velocity[n]/np.sqrt(1.4*287*t), 3))

    for m in range(2):
        beta = -45 + 45*m
        vf = []
        check = 0
        for n in range(number_of_tests):

            geometry = bdf_build(foil=foils1[0], chord_num=15, span_num=10, root_chord=root[5], span=span[6],
                                 taper=0.8, rho_input=rho[n], mach_input=mach[n], sweep=10, flap_point=0.4,
                                 beta=np.deg2rad(beta))
            run_nastran(plot=False)
            flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
            vf.append(find_flutter(flutter_results))
            if vf[n] is not None and not check:
                if vf[n] <= velocity[n]:
                    print(velocity[n])
                    print(height[n])
                    print(vf[n])
                    check = 1

        plt.figure(1)
        # plt.clf()
        if m == 0:
            plt.plot(height, velocity, label='Flight Velocity')
        plt.plot(height, vf, label='Flutter Speed (B = '+str(beta)+')')
        plt.xlabel('Height (m)')
        plt.ylabel('Velocity (m/s)')
        title = 'Span: ' + str(round(span[6], 2)) + ' Taper :' + str(round(taper[9], 2)) + ' Root Chord: ' \
                + str(round(root[5], 2))
        plt.title(title)
        plt.legend()
        plt.grid()
        # plot_save_name = 'nastran_plots/height_vs_vf/' + foils1[m] + '_' + str(k+1) + '.png'
        # plt.savefig(fname=plot_save_name)

        plt.figure(2)
        # plt.clf()
        plt.plot(mach, vf, label='Flutter Speed (B = '+str(beta)+')')
        plt.xlabel('Mach')
        plt.ylabel('Velocity (m/s)')
        title = 'Span: ' + str(round(span[6], 2)) + ' Taper :' + str(round(taper[9], 2)) + ' Root Chord: ' \
                + str(round(root[5], 2))
        plt.title(title)
        plt.legend()
        plt.grid()
        # plot_save_name = 'nastran_plots/mach_vs_vf/' + foils1[m] + '_' + str(k+1) + '.png'
        # plt.savefig(fname=plot_save_name)
    plt.show()


if __name__ == '__main__':
    main()

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
def density(h: float):
    rho0 = 1.225
    hs = 8500
    rho = rho0 * np.exp(-h / hs)
    return rho


def main():
    # Foil Shapes
    # foils1 = ['0106', '0108', '0110', '0112', '1106', '1108', '1110', '1112', '2106', '2108', '2110', '2112']
    foils1 = ['0206', '0208', '0210', '0212', '1206', '1208', '1210', '1212', '2206', '2208', '2210', '2212']
    # foils1 = ['0406', '0408', '0410', '0412', '1406', '1408', '1410', '1412', '2406', '2408', '2410', '2412']

    # Spans
    span = np.linspace(1.0, 4.0, num=10)
    taper = np.linspace(0.0, 1.0, num=10)
    root = np.linspace(0.15, 1, num=10)
    number_of_tests = 100
    height = np.linspace(0.0, 50000, number_of_tests)
    mach = [round(np.sqrt(height[n] / 3000), 2) for n in range(number_of_tests)]
    rho = [density(height[n]) for n in range(number_of_tests)]
    # temperature = [288 - 2.5 * height[n] / 10 for n in range(number_of_tests)]
    v = [mach[n]*np.sqrt(1.4*287*273) for n in range(number_of_tests)]

    for m in range(len(foils1)):
        for k in range(len(span)):
            vf = []
            for n in range(number_of_tests):

                geometry = bdf_build(foil=foils1[m], chord_num=15, span_num=10, root_chord=root[k], span=span[k],
                                     taper=taper[k], rho_input=rho[n], mach_input=mach[n], sweep=0.0)
                run_nastran(plot=False)
                flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
                vf.append(find_flutter(flutter_results))

            plt.figure(1)
            plt.clf()
            plt.plot(height, vf, label='Flutter Speed')
            plt.plot(height, v, label='Flight Velocity')
            plt.xlabel('Height (m)')
            plt.ylabel('Velocity (m/s)')
            title = 'Span: ' + str(round(span[k], 2)) + ' Taper :' + str(round(taper[k], 2)) + ' Root Chord: ' \
                    + str(round(root[k], 2))
            plt.title(title)
            plt.legend()
            plt.grid()
            plot_save_name = 'nastran_plots/height_vs_vf/' + foils1[m] + '_' + str(k+1) + '.png'
            plt.savefig(fname=plot_save_name)

            plt.figure(2)
            plt.clf()
            plt.plot(mach, vf, label='Flutter Speed')
            plt.xlabel('Mach')
            plt.ylabel('Velocity (m/s)')
            title = 'Span: ' + str(round(span[k], 2)) + ' Taper :' + str(round(taper[k], 2)) + ' Root Chord: ' \
                    + str(round(root[k], 2))
            plt.title(title)
            plt.legend()
            plt.grid()
            plot_save_name = 'nastran_plots/mach_vs_vf/' + foils1[m] + '_' + str(k+1) + '.png'
            plt.savefig(fname=plot_save_name)


if __name__ == '__main__':
    main()

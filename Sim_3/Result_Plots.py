# Imports
from graphing_tools import *
import matplotlib.pyplot as plt
import numpy as np
import pprint


# Internal Function
def plotting_function(x_vector, y_vector, fig_num, x_label, y_label, data_label, plot_title, fontsize, clear=False, show=False,
                      save=False, savename=None):
    plt.figure(fig_num)
    if clear:
        plt.clf()
    plt.grid()
    plt.plot(x_vector, y_vector, label=data_label)
    plt.xlabel(x_label, fontsize=fontsize)
    plt.ylabel(y_label, fontsize=fontsize)
    plt.legend(fontsize=fontsize)
    if save and savename:
        plt.title(plot_title)
        plt.savefig(savename)
    if show:
        plt.show()


number_of_tests = 50

# Extract Results

# Trajectory
trajectory_values = read_rocket_velocity('nastran_results/Rocket_Trajectory.dat')

# Foil Thickness
thickness_uncontrolled_labels, thickness_uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Foil_Thickness.dat', number_of_tests)
thickness_controlled_labels, thickness_controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Foil_Thickness.dat', number_of_tests)
thickness_gains, thickness_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Foil_Thickness.dat')

# Generate Velocity vs Height plots
for n in range(len(thickness_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Height'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Height (m)',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=thickness_uncontrolled_results[thickness_uncontrolled_labels[n]]['Height'],
                      y_vector=thickness_uncontrolled_results[thickness_uncontrolled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/Thick_' + str(n) + '_v_vs_h.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=thickness_controlled_results[thickness_controlled_labels[n]]['Height'],
                      y_vector=thickness_controlled_results[thickness_controlled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=thickness_uncontrolled_labels[n])

# Generate Velocity vs Mach plots
for n in range(len(thickness_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Mach'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Mach',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=thickness_uncontrolled_results[thickness_uncontrolled_labels[n]]['Mach'],
                      y_vector=thickness_uncontrolled_results[thickness_uncontrolled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/Thick_' + str(n) + '_v_vs_m.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=thickness_controlled_results[thickness_controlled_labels[n]]['Mach'],
                      y_vector=thickness_controlled_results[thickness_controlled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=thickness_uncontrolled_labels[n])

# Foil Camber
camber_uncontrolled_labels, camber_uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Foil_Camber.dat', number_of_tests)
camber_controlled_labels, camber_controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Foil_Camber.dat', number_of_tests)
camber_gains, camber_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Foil_Camber.dat')

# Generate Velocity vs Height plots
for n in range(len(camber_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Height'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Height (m)',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=camber_uncontrolled_results[camber_uncontrolled_labels[n]]['Height'],
                      y_vector=camber_uncontrolled_results[camber_uncontrolled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/Camber_' + str(n) + '_v_vs_h.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=camber_controlled_results[camber_controlled_labels[n]]['Height'],
                      y_vector=camber_controlled_results[camber_controlled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=camber_uncontrolled_labels[n])

# Generate Velocity vs Mach plots
for n in range(len(camber_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Mach'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Mach',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=camber_uncontrolled_results[camber_uncontrolled_labels[n]]['Mach'],
                      y_vector=camber_uncontrolled_results[camber_uncontrolled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/Camber_' + str(n) + '_v_vs_m.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=camber_controlled_results[camber_controlled_labels[n]]['Mach'],
                      y_vector=camber_controlled_results[camber_controlled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=camber_uncontrolled_labels[n])

# Foil Camber Position
camberPosition_uncontrolled_labels, camberPosition_uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Foil_Camber_Position.dat', number_of_tests)
camberPosition_controlled_labels, camberPosition_controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Foil_Camber_Position.dat', number_of_tests)
camberPosition_gains, camberPosition_gain_labels = extract_gains_from_file(
    'nastran_results/Flutter_Gains_Foil_Camber_Position.dat')

# Generate Velocity vs Height plots
for n in range(len(camberPosition_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Height'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Height (m)',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=camberPosition_uncontrolled_results[camberPosition_uncontrolled_labels[n]]['Height'],
                      y_vector=camberPosition_uncontrolled_results[camberPosition_uncontrolled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/CamberPosition_' + str(n) + '_v_vs_h.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=camberPosition_controlled_results[camberPosition_controlled_labels[n]]['Height'],
                      y_vector=camberPosition_controlled_results[camberPosition_controlled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=camberPosition_uncontrolled_labels[n])

# Generate Velocity vs Mach plots
for n in range(len(camberPosition_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Mach'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Mach',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=camberPosition_uncontrolled_results[camberPosition_uncontrolled_labels[n]]['Mach'],
                      y_vector=camberPosition_uncontrolled_results[camberPosition_uncontrolled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/CamberPosition_' + str(n) + '_v_vs_m.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=camberPosition_controlled_results[camberPosition_controlled_labels[n]]['Mach'],
                      y_vector=camberPosition_controlled_results[camberPosition_controlled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=camberPosition_uncontrolled_labels[n])

# Wing Span
span_uncontrolled_labels, span_uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Semi_Span.dat', number_of_tests)
span_controlled_labels, span_controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Semi_Span.dat', number_of_tests)
span_gains, span_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Semi_Span.dat')

# Generate Velocity vs Height plots
for n in range(len(span_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Height'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Height (m)',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=span_uncontrolled_results[span_uncontrolled_labels[n]]['Height'],
                      y_vector=span_uncontrolled_results[span_uncontrolled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/SemiSpan_' + str(n) + '_v_vs_h.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=span_controlled_results[span_controlled_labels[n]]['Height'],
                      y_vector=span_controlled_results[span_controlled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=span_uncontrolled_labels[n])

# Generate Velocity vs Mach plots
for n in range(len(span_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Mach'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Mach',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=span_uncontrolled_results[span_uncontrolled_labels[n]]['Mach'],
                      y_vector=span_uncontrolled_results[span_uncontrolled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/SemiSpan_' + str(n) + '_v_vs_m.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=span_controlled_results[span_controlled_labels[n]]['Mach'],
                      y_vector=span_controlled_results[span_controlled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=span_uncontrolled_labels[n])

# # Root Chord
# root_uncontrolled_labels, root_uncontrolled_results = extract_flutter_profile(
#     'nastran_results/Flutter_Velocity_Root_Chord.dat', number_of_tests)
# root_controlled_labels, root_controlled_results = extract_flutter_profile(
#     'nastran_results/Flutter_Velocity_Controlled_Root_Chord.dat', number_of_tests)
# root_gains, root_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Root_Chord.dat')

# # Generate Velocity vs Height plots
# for n in range(len(root_controlled_labels)):
#     # Rocket Trajectory
#     plotting_function(fig_num=1, x_vector=trajectory_values['Height'][0:number_of_tests],
#                       y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Height (m)',
#                       y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)
#
#     # Uncontrolled
#     plotting_function(fig_num=1, x_vector=root_uncontrolled_results[root_uncontrolled_labels[n]]['Height'],
#                       y_vector=root_uncontrolled_results[root_uncontrolled_labels[n]]['Velocity'],
#                       x_label='Height (m)', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
#                       fontsize=12, clear=False, show=False, plot_title=None)
#
#     # Plot name string
#     save_name = 'nastran_results/plots/RootChord_' + str(n) + '_v_vs_h.png'
#     # Controlled
#     plotting_function(fig_num=1, x_vector=root_controlled_results[root_controlled_labels[n]]['Height'],
#                       y_vector=root_controlled_results[root_controlled_labels[n]]['Velocity'],
#                       x_label='Height (m)', y_label='Velocity (m/s)', data_label='Controlled Wing',
#                       fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=root_uncontrolled_labels[n])

# # Generate Velocity vs Mach plots
# for n in range(len(root_controlled_labels)):
#     # Rocket Trajectory
#     plotting_function(fig_num=1, x_vector=trajectory_values['Mach'][0:number_of_tests],
#                       y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Mach',
#                       y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)
#
#     # Uncontrolled
#     plotting_function(fig_num=1, x_vector=root_uncontrolled_results[root_uncontrolled_labels[n]]['Mach'],
#                       y_vector=root_uncontrolled_results[root_uncontrolled_labels[n]]['Velocity'],
#                       x_label='Mach', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
#                       fontsize=12, clear=False, show=False, plot_title=None)
#
#     # Plot name string
#     save_name = 'nastran_results/plots/RootChord_' + str(n) + '_v_vs_m.png'
#     # Controlled
#     plotting_function(fig_num=1, x_vector=root_controlled_results[root_controlled_labels[n]]['Mach'],
#                       y_vector=root_controlled_results[root_controlled_labels[n]]['Velocity'],
#                       x_label='Mach', y_label='Velocity (m/s)', data_label='Controlled Wing',
#                       fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=root_uncontrolled_labels[n])

# Taper
# taper_uncontrolled_labels, taper_uncontrolled_results = extract_flutter_profile(
#     'nastran_results/Flutter_Velocity_Taper.dat', number_of_tests)
# taper_controlled_labels, taper_controlled_results = extract_flutter_profile(
#     'nastran_results/Flutter_Velocity_Controlled_Taper.dat', number_of_tests)
# taper_gains, taper_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Taper.dat')

# # Generate Velocity vs Height plots
# for n in range(len(taper_controlled_labels)):
#     # Rocket Trajectory
#     plotting_function(fig_num=1, x_vector=trajectory_values['Height'][0:number_of_tests],
#                       y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Height (m)',
#                       y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)
#
#     # Uncontrolled
#     plotting_function(fig_num=1, x_vector=taper_uncontrolled_results[taper_uncontrolled_labels[n]]['Height'],
#                       y_vector=taper_uncontrolled_results[taper_uncontrolled_labels[n]]['Velocity'],
#                       x_label='Height (m)', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
#                       fontsize=12, clear=False, show=False, plot_title=None)
#
#     # Plot name string
#     save_name = 'nastran_results/plots/TaperRatio_' + str(n) + '_v_vs_h.png'
#     # Controlled
#     plotting_function(fig_num=1, x_vector=taper_controlled_results[taper_controlled_labels[n]]['Height'],
#                       y_vector=taper_controlled_results[taper_controlled_labels[n]]['Velocity'],
#                       x_label='Height (m)', y_label='Velocity (m/s)', data_label='Controlled Wing',
#                       fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=taper_uncontrolled_labels[n])

# # Generate Velocity vs Mach plots
# for n in range(len(taper_controlled_labels)):
#     # Rocket Trajectory
#     plotting_function(fig_num=1, x_vector=trajectory_values['Mach'][0:number_of_tests],
#                       y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Mach',
#                       y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)
#
#     # Uncontrolled
#     plotting_function(fig_num=1, x_vector=taper_uncontrolled_results[taper_uncontrolled_labels[n]]['Mach'],
#                       y_vector=taper_uncontrolled_results[taper_uncontrolled_labels[n]]['Velocity'],
#                       x_label='Mach', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
#                       fontsize=12, clear=False, show=False, plot_title=None)
#
#     # Plot name string
#     save_name = 'nastran_results/plots/TaperRatio_' + str(n) + '_v_vs_m.png'
#     # Controlled
#     plotting_function(fig_num=1, x_vector=taper_controlled_results[taper_controlled_labels[n]]['Mach'],
#                       y_vector=taper_controlled_results[taper_controlled_labels[n]]['Velocity'],
#                       x_label='Mach', y_label='Velocity (m/s)', data_label='Controlled Wing',
#                       fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=taper_uncontrolled_labels[n])

# Sweep
sweep_uncontrolled_labels, sweep_uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Sweep.dat', number_of_tests)
sweep_controlled_labels, sweep_controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Sweep.dat', number_of_tests)
sweep_gains, sweep_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Sweep.dat')

# Generate Velocity vs Height plots
for n in range(len(sweep_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Height'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Height (m)',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=sweep_uncontrolled_results[sweep_uncontrolled_labels[n]]['Height'],
                      y_vector=sweep_uncontrolled_results[sweep_uncontrolled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/Sweep_' + str(n) + '_v_vs_h.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=sweep_controlled_results[sweep_controlled_labels[n]]['Height'],
                      y_vector=sweep_controlled_results[sweep_controlled_labels[n]]['Velocity'],
                      x_label='Height (m)', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=sweep_uncontrolled_labels[n])

# Generate Velocity vs Mach plots
for n in range(len(sweep_controlled_labels)):
    # Rocket Trajectory
    plotting_function(fig_num=1, x_vector=trajectory_values['Mach'][0:number_of_tests],
                      y_vector=trajectory_values['Velocity'][0:number_of_tests], x_label='Mach',
                      y_label='Velocity (m/s)', data_label='Rocket Trajectory', fontsize=12, clear=True, show=False, plot_title=None)

    # Uncontrolled
    plotting_function(fig_num=1, x_vector=sweep_uncontrolled_results[sweep_uncontrolled_labels[n]]['Mach'],
                      y_vector=sweep_uncontrolled_results[sweep_uncontrolled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Uncontrolled Wing',
                      fontsize=12, clear=False, show=False, plot_title=None)

    # Plot name string
    save_name = 'nastran_results/plots/Sweep_' + str(n) + '_v_vs_m.png'
    # Controlled
    plotting_function(fig_num=1, x_vector=sweep_controlled_results[sweep_controlled_labels[n]]['Mach'],
                      y_vector=sweep_controlled_results[sweep_controlled_labels[n]]['Velocity'],
                      x_label='Mach', y_label='Velocity (m/s)', data_label='Controlled Wing',
                      fontsize=12, clear=False, show=False, save=True, savename=save_name, plot_title=sweep_uncontrolled_labels[n])

# The next section will plot the gains against the foil parameters and create individual line of best fits for the
# final controller design

# As seen in Thesis_Final.py

# NACA 4 digit foil parameters
foil_thickness = ['1102', '1104', '1106', '1108', '1110']
foil_thickness_plot = [float(foil_thickness[n][2:4])/100 for n in range(len(thickness_gain_labels))]
thickness_gains_plot1 = [thickness_gains[thickness_gain_labels[n]][0] for n in range(len(thickness_gain_labels))]
thickness_gains_plot2 = [thickness_gains[thickness_gain_labels[n]][1] for n in range(len(thickness_gain_labels))]
thickness_gains_plot3 = [thickness_gains[thickness_gain_labels[n]][2] for n in range(len(thickness_gain_labels))]
thickness_gains_plot4 = [thickness_gains[thickness_gain_labels[n]][3] for n in range(len(thickness_gain_labels))]
thickness_gains_plot5 = [thickness_gains[thickness_gain_labels[n]][4] for n in range(len(thickness_gain_labels))]
thickness_gains_plot6 = [thickness_gains[thickness_gain_labels[n]][5] for n in range(len(thickness_gain_labels))]

plt.figure(1)
plt.clf()
plt.grid()
plt.xlabel('Foil Thickness (% chord)')
plt.ylabel('Gain')
plt.plot(foil_thickness_plot, thickness_gains_plot1, label='k1')
plt.plot(foil_thickness_plot, thickness_gains_plot2, label='k2')
plt.plot(foil_thickness_plot, thickness_gains_plot3, label='k3')
plt.legend()
plt.savefig('nastran_results/plots/Foil_Thickness_Gain1')

plt.figure(2)
plt.clf()
plt.grid()
plt.xlabel('Foil Thickness (% chord)')
plt.ylabel('Gain')
plt.plot(foil_thickness_plot, thickness_gains_plot4, label='k4')
plt.plot(foil_thickness_plot, thickness_gains_plot5, label='k5')
plt.plot(foil_thickness_plot, thickness_gains_plot6, label='k6')
plt.legend()
plt.savefig('nastran_results/plots/Foil_Thickness_Gain2')

foil_camber = ['1110', '2110', '3110', '4110', '5110']
foil_camber_plot = [float(foil_camber[n][0])/10 for n in range(len(camber_gain_labels))]
camber_gains_plot1 = [camber_gains[camber_gain_labels[n]][0] for n in range(len(camber_gain_labels))]
camber_gains_plot2 = [camber_gains[camber_gain_labels[n]][1] for n in range(len(camber_gain_labels))]
camber_gains_plot3 = [camber_gains[camber_gain_labels[n]][2] for n in range(len(camber_gain_labels))]
camber_gains_plot4 = [camber_gains[camber_gain_labels[n]][3] for n in range(len(camber_gain_labels))]
camber_gains_plot5 = [camber_gains[camber_gain_labels[n]][4] for n in range(len(camber_gain_labels))]
camber_gains_plot6 = [camber_gains[camber_gain_labels[n]][5] for n in range(len(camber_gain_labels))]

plt.figure(1)
plt.clf()
plt.grid()
plt.xlabel('Foil Camber (% chord)')
plt.ylabel('Gain')
plt.plot(foil_camber_plot, camber_gains_plot1, label='k1')
plt.plot(foil_camber_plot, camber_gains_plot2, label='k2')
plt.plot(foil_camber_plot, camber_gains_plot3, label='k3')
plt.legend()
plt.savefig('nastran_results/plots/Foil_Camber_Gain1')

plt.figure(2)
plt.clf()
plt.grid()
plt.xlabel('Foil Camber (% chord)')
plt.ylabel('Gain')
plt.plot(foil_camber_plot, camber_gains_plot4, label='k4')
plt.plot(foil_camber_plot, camber_gains_plot5, label='k5')
plt.plot(foil_camber_plot, camber_gains_plot6, label='k6')
plt.legend()
plt.savefig('nastran_results/plots/Foil_Camber_Gain2')

foil_camber_pos = ['1110', '1210', '1310', '1410', '1510']
foil_camber_pos_plot = [float(foil_camber_pos[n][1])/10 for n in range(len(camberPosition_gain_labels))]
camberPosition_gains_plot1 = [camberPosition_gains[camberPosition_gain_labels[n]][0] for n in range(len(camberPosition_gain_labels))]
camberPosition_gains_plot2 = [camberPosition_gains[camberPosition_gain_labels[n]][1] for n in range(len(camberPosition_gain_labels))]
camberPosition_gains_plot3 = [camberPosition_gains[camberPosition_gain_labels[n]][2] for n in range(len(camberPosition_gain_labels))]
camberPosition_gains_plot4 = [camberPosition_gains[camberPosition_gain_labels[n]][3] for n in range(len(camberPosition_gain_labels))]
camberPosition_gains_plot5 = [camberPosition_gains[camberPosition_gain_labels[n]][4] for n in range(len(camberPosition_gain_labels))]
camberPosition_gains_plot6 = [camberPosition_gains[camberPosition_gain_labels[n]][5] for n in range(len(camberPosition_gain_labels))]

plt.figure(1)
plt.clf()
plt.grid()
plt.xlabel('Foil Camber Position (% chord)')
plt.ylabel('Gain')
plt.plot(foil_camber_pos_plot, camberPosition_gains_plot1, label='k1')
plt.plot(foil_camber_pos_plot, camberPosition_gains_plot2, label='k2')
plt.plot(foil_camber_pos_plot, camberPosition_gains_plot3, label='k3')
plt.legend()
plt.savefig('nastran_results/plots/Foil_CamberPosition_Gain1')

plt.figure(2)
plt.clf()
plt.grid()
plt.xlabel('Foil Camber Position (% chord)')
plt.ylabel('Gain')
plt.plot(foil_camber_pos_plot, camberPosition_gains_plot4, label='k4')
plt.plot(foil_camber_pos_plot, camberPosition_gains_plot5, label='k5')
plt.plot(foil_camber_pos_plot, camberPosition_gains_plot6, label='k6')
plt.legend()
plt.savefig('nastran_results/plots/Foil_CamberPosition_Gain2')

# 3D effects
# taper_total = np.linspace(0.2, 0.6, num=5)
# taper = [taper_total[n] for n in range(len(taper_gain_labels))]
# taper_gains_plot1 = [taper_gains[taper_gain_labels[n]][0] for n in range(len(taper_gain_labels))]
# taper_gains_plot2 = [taper_gains[taper_gain_labels[n]][1] for n in range(len(taper_gain_labels))]
# taper_gains_plot3 = [taper_gains[taper_gain_labels[n]][2] for n in range(len(taper_gain_labels))]
# taper_gains_plot4 = [taper_gains[taper_gain_labels[n]][3] for n in range(len(taper_gain_labels))]
# taper_gains_plot5 = [taper_gains[taper_gain_labels[n]][4] for n in range(len(taper_gain_labels))]
# taper_gains_plot6 = [taper_gains[taper_gain_labels[n]][5] for n in range(len(taper_gain_labels))]

# plt.figure(1)
# plt.clf()
# plt.grid()
# plt.xlabel('Taper Ratio')
# plt.ylabel('Gain')
# plt.plot(taper, taper_gains_plot1, label='k1')
# plt.plot(taper, taper_gains_plot2, label='k2')
# plt.plot(taper, taper_gains_plot3, label='k3')
# plt.legend()
# plt.savefig('nastran_results/plots/TaperRatio_Gain1')
#
# plt.figure(2)
# plt.clf()
# plt.grid()
# plt.xlabel('Taper Ratio')
# plt.ylabel('Gain')
# plt.plot(taper, taper_gains_plot4, label='k4')
# plt.plot(taper, taper_gains_plot5, label='k5')
# plt.plot(taper, taper_gains_plot6, label='k6')
# plt.legend()
# plt.savefig('nastran_results/plots/TaperRatio_Gain2')

span_total = np.linspace(0.15, 0.7, num=5)
span = [span_total[n] for n in range(len(span_gain_labels))]
span_gains_plot1 = [span_gains[span_gain_labels[n]][0] for n in range(len(span_gain_labels))]
span_gains_plot2 = [span_gains[span_gain_labels[n]][1] for n in range(len(span_gain_labels))]
span_gains_plot3 = [span_gains[span_gain_labels[n]][2] for n in range(len(span_gain_labels))]
span_gains_plot4 = [span_gains[span_gain_labels[n]][3] for n in range(len(span_gain_labels))]
span_gains_plot5 = [span_gains[span_gain_labels[n]][4] for n in range(len(span_gain_labels))]
span_gains_plot6 = [span_gains[span_gain_labels[n]][5] for n in range(len(span_gain_labels))]

plt.figure(1)
plt.clf()
plt.grid()
plt.xlabel('Semi Span (m)')
plt.ylabel('Gain')
plt.plot(span, span_gains_plot1, label='k1')
plt.plot(span, span_gains_plot2, label='k2')
plt.plot(span, span_gains_plot3, label='k3')
plt.legend()
plt.savefig('nastran_results/plots/SemiSpan_Gain1')

plt.figure(2)
plt.clf()
plt.grid()
plt.xlabel('Semi Span (m)')
plt.ylabel('Gain')
plt.plot(span, span_gains_plot4, label='k4')
plt.plot(span, span_gains_plot5, label='k5')
plt.plot(span, span_gains_plot6, label='k6')
plt.legend()
plt.savefig('nastran_results/plots/SemiSpan_Gain2')

sweep_total = np.linspace(0.0, 30.0, num=5)
sweep = [sweep_total[n] for n in range(len(sweep_gain_labels))]
sweep_gains_plot1 = [sweep_gains[sweep_gain_labels[n]][0] for n in range(len(sweep_gain_labels))]
sweep_gains_plot2 = [sweep_gains[sweep_gain_labels[n]][1] for n in range(len(sweep_gain_labels))]
sweep_gains_plot3 = [sweep_gains[sweep_gain_labels[n]][2] for n in range(len(sweep_gain_labels))]
sweep_gains_plot4 = [sweep_gains[sweep_gain_labels[n]][3] for n in range(len(sweep_gain_labels))]
sweep_gains_plot5 = [sweep_gains[sweep_gain_labels[n]][4] for n in range(len(sweep_gain_labels))]
sweep_gains_plot6 = [sweep_gains[sweep_gain_labels[n]][5] for n in range(len(sweep_gain_labels))]

plt.figure(1)
plt.clf()
plt.grid()
plt.xlabel('Sweep Angle (deg)')
plt.ylabel('Gain')
plt.plot(sweep, sweep_gains_plot1, label='k1')
plt.plot(sweep, sweep_gains_plot2, label='k2')
plt.plot(sweep, sweep_gains_plot3, label='k3')
plt.legend()
plt.savefig('nastran_results/plots/Sweep_Gain1')

plt.figure(2)
plt.clf()
plt.grid()
plt.xlabel('Sweep Angle (deg)')
plt.ylabel('Gain')
plt.plot(sweep, sweep_gains_plot4, label='k4')
plt.plot(sweep, sweep_gains_plot5, label='k5')
plt.plot(sweep, sweep_gains_plot6, label='k6')
plt.legend()
plt.savefig('nastran_results/plots/Sweep_Gain2')

# root_total = np.linspace(0.15, 0.7, num=5)
# root = [root_total[n] for n in range(len(root_gain_labels))]
# root_gains_plot1 = [root_gains[root_gain_labels[n]][0] for n in range(len(root_gain_labels))]
# root_gains_plot2 = [root_gains[root_gain_labels[n]][1] for n in range(len(root_gain_labels))]
# root_gains_plot3 = [root_gains[root_gain_labels[n]][2] for n in range(len(root_gain_labels))]
# root_gains_plot4 = [root_gains[root_gain_labels[n]][3] for n in range(len(root_gain_labels))]
# root_gains_plot5 = [root_gains[root_gain_labels[n]][4] for n in range(len(root_gain_labels))]
# root_gains_plot6 = [root_gains[root_gain_labels[n]][5] for n in range(len(root_gain_labels))]

# plt.figure(1)
# plt.clf()
# plt.grid()
# plt.xlabel('Root Chord (m)')
# plt.ylabel('Gain')
# plt.plot(root, root_gains_plot1, label='k1')
# plt.plot(root, root_gains_plot2, label='k2')
# plt.plot(root, root_gains_plot3, label='k3')
# plt.legend()
# plt.savefig('nastran_results/plots/RootChord_Gain1')
#
# plt.figure(2)
# plt.clf()
# plt.grid()
# plt.xlabel('Root Chord (m)')
# plt.ylabel('Gain')
# plt.plot(root, root_gains_plot4, label='k4')
# plt.plot(root, root_gains_plot5, label='k5')
# plt.plot(root, root_gains_plot6, label='k6')
# plt.legend()
# plt.savefig('nastran_results/plots/RootChord_Gain2')


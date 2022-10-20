# Imports
from graphing_tools import *
import matplotlib.pyplot as plt
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

# Foil Camber
camber_uncontrolled_labels, camber_uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Foil_Camber.dat', number_of_tests)
camber_controlled_labels, camber_controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Foil_Camber.dat', number_of_tests)
camber_gains, camber_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Foil_Camber.dat')

# Foil Camber Position
camberPosition_uncontrolled_labels, camberPosition_uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Foil_Camber_Position.dat', number_of_tests)
camberPosition_controlled_labels, camberPosition_controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Foil_Camber_Position.dat', number_of_tests)
camberPosition_gains, camberPosition_gain_labels = extract_gains_from_file(
    'nastran_results/Flutter_Gains_Foil_Camber_Position.dat')

# Wing Span
span_uncontrolled_labels, span_uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Semi_Span.dat', number_of_tests)
span_controlled_labels, span_controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Semi_Span.dat', number_of_tests)
span_gains, span_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Semi_Span.dat')

# # Root Chord
# root_uncontrolled_labels, root_uncontrolled_results = extract_flutter_profile(
#     'nastran_results/Flutter_Velocity_Root_Chord.dat', number_of_tests)
# root_controlled_labels, root_controlled_results = extract_flutter_profile(
#     'nastran_results/Flutter_Velocity_Controlled_Root_Chord.dat', number_of_tests)
# root_gains, root_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Root_Chord.dat')

# Taper
# taper_uncontrolled_labels, taper_uncontrolled_results = extract_flutter_profile(
#     'nastran_results/Flutter_Velocity_Taper.dat', number_of_tests)
# taper_controlled_labels, taper_controlled_results = extract_flutter_profile(
#     'nastran_results/Flutter_Velocity_Controlled_Taper.dat', number_of_tests)
# taper_gains, taper_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Taper.dat')

# Sweep
sweep_uncontrolled_labels, sweep_uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Sweep.dat', number_of_tests)
sweep_controlled_labels, sweep_controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Sweep.dat', number_of_tests)
sweep_gains, sweep_gain_labels = extract_gains_from_file('nastran_results/Flutter_Gains_Sweep.dat')

# Presentation_labels = ['Uncontrolled 4% Thickness', 'Uncontrolled 6% Thickness']
# Presentation_labels1 = ['Controlled 4% Thickness', 'Controlled 6% Thickness']
#
# plt.figure(1)
# plt.clf()
# plt.grid()
# plt.plot(trajectory_values['Height'][0:number_of_tests], trajectory_values['Velocity'][0:number_of_tests], label='Rocket Trajectory')
#
#
# plt.figure(2)
# plt.clf()
# plt.grid()
#
# for n in range(2):
#     uncontrolled_header = uncontrolled_labels[n+1]
#     controlled_header = controlled_labels[n+1]
#
#     uncontrolled_velocity = uncontrolled_results[uncontrolled_header]['Velocity']
#     uncontrolled_height = uncontrolled_results[uncontrolled_header]['Height']
#     uncontrolled_mach = uncontrolled_results[uncontrolled_header]['Mach']
#
#     controlled_velocity = controlled_results[controlled_header]['Velocity']
#     controlled_height = controlled_results[controlled_header]['Height']
#     controlled_mach = controlled_results[controlled_header]['Mach']
#
#     plt.figure(1)
#     plt.plot(uncontrolled_height, uncontrolled_velocity, label=Presentation_labels[n])
#     plt.plot(controlled_height, controlled_velocity, label=Presentation_labels1[n])
#
#     plt.figure(2)
#     plt.plot(uncontrolled_mach, uncontrolled_velocity, label=uncontrolled_header)
#     plt.plot(controlled_mach, controlled_velocity, label=controlled_header)
#
# plt.figure(1)
# plt.xlabel('Height (m)', fontsize=14)
# plt.ylabel('Velocity (m/s)', fontsize=14)
#
# plt.legend(fontsize=14)
#
# plt.figure(2)
# plt.legend()
#
# plt.show()

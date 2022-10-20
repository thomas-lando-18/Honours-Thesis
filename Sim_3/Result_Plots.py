# Imports
from graphing_tools import*
import matplotlib.pyplot as plt
import pprint

number_of_tests = 50

# Trajectory
trajectory_values = read_rocket_velocity('nastran_results/Rocket_Trajectory.dat')
# pprint.pprint(trajectory_values)
# Foil Thickness Parameter

# Extract Results
uncontrolled_labels, uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Foil_Thickness.dat', number_of_tests)
controlled_labels, controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Foil_Thickness.dat', number_of_tests)

Presentation_labels = ['Uncontrolled 4% Thickness', 'Uncontrolled 6% Thickness']
Presentation_labels1 = ['Controlled 4% Thickness', 'Controlled 6% Thickness']

plt.figure(1)
plt.clf()
plt.grid()
plt.plot(trajectory_values['Height'][0:number_of_tests], trajectory_values['Velocity'][0:number_of_tests], label='Rocket Trajectory')


plt.figure(2)
plt.clf()
plt.grid()

for n in range(2):
    uncontrolled_header = uncontrolled_labels[n+1]
    controlled_header = controlled_labels[n+1]

    uncontrolled_velocity = uncontrolled_results[uncontrolled_header]['Velocity']
    uncontrolled_height = uncontrolled_results[uncontrolled_header]['Height']
    uncontrolled_mach = uncontrolled_results[uncontrolled_header]['Mach']

    controlled_velocity = controlled_results[controlled_header]['Velocity']
    controlled_height = controlled_results[controlled_header]['Height']
    controlled_mach = controlled_results[controlled_header]['Mach']

    plt.figure(1)
    plt.plot(uncontrolled_height, uncontrolled_velocity, label=Presentation_labels[n])
    plt.plot(controlled_height, controlled_velocity, label=Presentation_labels1[n])

    plt.figure(2)
    plt.plot(uncontrolled_mach, uncontrolled_velocity, label=uncontrolled_header)
    plt.plot(controlled_mach, controlled_velocity, label=controlled_header)

plt.figure(1)
plt.xlabel('Height (m)', fontsize=14)
plt.ylabel('Velocity (m/s)', fontsize=14)

plt.legend(fontsize=14)

plt.figure(2)
plt.legend()

plt.show()

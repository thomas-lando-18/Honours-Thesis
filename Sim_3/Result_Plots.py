# Imports
from graphing_tools import*
import matplotlib.pyplot as plt


number_of_tests = 75
# Foil Thickness Parameter

# Extract Results
uncontrolled_labels, uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Foil_Thickness.dat', number_of_tests)
controlled_labels, controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Controlled_Foil_Thickness.dat', number_of_tests)


plt.figure(1)
plt.clf()
plt.grid()

plt.figure(2)
plt.clf()
plt.grid()

for n in range(1):
    uncontrolled_header = uncontrolled_labels[n]
    controlled_header = controlled_labels[n]

    uncontrolled_velocity = uncontrolled_results[uncontrolled_header]['Velocity']
    uncontrolled_height = uncontrolled_results[uncontrolled_header]['Height']
    uncontrolled_mach = uncontrolled_results[uncontrolled_header]['Mach']

    controlled_velocity = controlled_results[controlled_header]['Velocity']
    controlled_height = controlled_results[controlled_header]['Height']
    controlled_mach = controlled_results[controlled_header]['Mach']

    plt.figure(1)
    plt.plot(uncontrolled_height, uncontrolled_velocity, label=uncontrolled_header)
    plt.plot(controlled_height, controlled_velocity, label=controlled_header)

    plt.figure(2)
    plt.plot(uncontrolled_mach, uncontrolled_velocity, label=uncontrolled_header)
    plt.plot(controlled_mach, controlled_velocity, label=controlled_header)

plt.figure(1)
plt.legend()

plt.figure(2)
plt.legend()

plt.show()


# Plotting Functions
import pprint
import matplotlib.pyplot as plt
import numpy as np


def extract_flutter_profile(filename, number_of_tests):
    label = []
    fid = open(filename, 'r')
    file_lines = fid.readlines()
    results_output = {}
    for n in range(len(file_lines)):
        if file_lines[n] != '\n':
            if file_lines[n].split()[0] == 'VELOCITY':
                label.append(file_lines[ n -1])
                velocity = []
                height = []
                mach = []
                for m in range(number_of_tests):
                    result_line = file_lines[n + m + 1]
                    velocity.append(float(result_line.split(' ' *8)[0]))
                    height.append(float(result_line.split(' ' *8)[1]))
                    mach.append(float(result_line.split(' ' *8)[2]))

                new_set = {file_lines[ n -1]: {'Velocity': velocity,
                                             'Height': height,
                                             'Mach': mach}}

                results_output.update(new_set)

    return label, results_output


def read_rocket_velocity(filename):
    fid = open(filename, 'r')

    file_lines = fid.readlines()
    velocity = []
    height = []
    mach = []
    temperature = []
    density = []
    for n in range(len(file_lines)):
        if n > 0:
            result_line = file_lines[n]
            velocity.append(float(result_line.split(' ' *8)[0]))
            height.append(float(result_line.split(' ' * 8)[1]))
            mach.append(float(result_line.split(' ' * 8)[2]))
            temperature.append(float(result_line.split(' ' * 8)[3]))
            density.append(float(result_line.split(' ' * 8)[4]))

    output = {
        "Velocity": velocity,
        "Height": height,
        "Mach": mach,
        "Temperature": temperature,
        "Density": density
    }
    return output


def extract_gains_from_file(filename):
    fid = open(filename, 'r')
    labels = []
    file_lines = fid.readlines()
    output = {}
    for n in range(len(file_lines)):
        line = file_lines[n]
        if line.split():
            if line.split()[0] == 'Controller':
                labels.append(file_lines[n-1])

                gain1 = file_lines[n+1]
                gain2 = file_lines[n+2]
                gain3 = file_lines[n+3]

                gain1 = gain1.replace('[', '')
                gain3 = gain3.replace(']', '')

                gain1 = gain1.split()
                gain2 = gain2.split()
                gain3 = gain3.split()

                gain1_vector = [abs(complex(gain1[n])) for n in range(2)]
                gain2_vector = [abs(complex(gain2[n])) for n in range(2)]
                gain3_vector = [abs(complex(gain3[n])) for n in range(2)]

                gains = [*gain1_vector, *gain2_vector, *gain3_vector]

                new_set = {file_lines[n-1]: gains}
                output.update(new_set)
    return output, labels



# Testing
# if __name__ == '__main__':
#     output_json = extract_gains_from_file('nastran_results/Flutter_Gains_Foil_Thickness.dat')
#     pprint.pprint(output_json)

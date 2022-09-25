# Imports
import pprint
import numpy as np
import matplotlib.pyplot as plt


# Script Functions
def extract_values(filename, start_line, mode):
    fid = open(filename, 'r')
    file_lines = fid.readlines()
    reduced_freq = []
    inverse_rfreq = []
    velocity = []
    damping = []
    frequency = []
    real_eig = []
    imag_eig = []
    for n in range(start_line - 1, start_line + 36):
        line = file_lines[n]
        if '**STUDENT' in line:
            break
        line_vector = line.split()
        reduced_freq.append(float(line_vector[0]))
        inverse_rfreq.append(float(line_vector[1]))
        velocity.append(float(line_vector[2]))
        damping.append(float(line_vector[3]))
        frequency.append(float(line_vector[4]))
        real_eig.append(float(line_vector[5]))
        imag_eig.append(float(line_vector[6]))

    output_json = {
        "Reduced Frequency": reduced_freq,
        "Inverse Rfreq": inverse_rfreq,
        "Velocity": velocity,
        "Damping": damping,
        "Frequency": frequency,
        "Real Eigenvalue": real_eig,
        "Imag Eigenvalue": imag_eig
    }
    return output_json

def read_f06_file(filename):
    fid = open(filename, 'r')
    file_lines = fid.readlines()
    mode = []
    for n in range(len(file_lines)):
        if 'FLUTTER  SUMMARY' in file_lines[n]:
            mode_line = file_lines[n+2].split()
            mode.append(int(mode_line[2]))

    flutter_json = {'mode': str(mode)}
    return flutter_json


# Run Configuration
if __name__ == '__main__':
    filename = 'nastran_files/3d_6dof_card.f06'
    flutter_json = read_f06_file(filename)
    pprint.pprint(flutter_json)

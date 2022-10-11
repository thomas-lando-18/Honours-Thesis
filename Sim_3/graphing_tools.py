

# Plotting Functions
def extract_flutter_profile(filename, number_of_tests):
    label = []
    fid = open(filename, 'r')
    file_lines = fid.readlines()
    results_output = {}
    for n in range(len(file_lines)):
        if file_lines[n] != '\n':
            if file_lines[n].split()[0] == 'VELOCITY':
                label.append(file_lines[n-1])
                velocity = []
                height = []
                mach = []
                for m in range(number_of_tests):
                    result_line = file_lines[n + m + 1]
                    velocity.append(float(result_line.split(' '*8)[0]))
                    height.append(float(result_line.split(' '*8)[1]))
                    mach.append(float(result_line.split(' '*8)[2]))

                new_set = {file_lines[n-1]: {'Velocity': velocity,
                                             'Height': height,
                                             'Mach': mach}}

                results_output.update(new_set)

    return label, results_output


# Testing
# if __name__ == '__main__':
#     output_json = extract_flutter_profile('nastran_results/Flutter_Velocity_Foil_Camber.dat', 50)
#     pprint.pprint(output_json)

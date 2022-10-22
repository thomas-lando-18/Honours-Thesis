from sim_functions import*
from graphing_tools import*
from controller import*
from wing_model.wing_build import main as wing
import matplotlib.pyplot as plt
import numpy as np
import pprint


# Internal Functions
def read_polyfit_file(filename):
    fid = open(filename, 'r')
    file_lines = fid.readlines()
    parameter = []
    output = {}
    for n in range(len(file_lines)):
        line = file_lines[n]
        polynomial_vector = []
        if line.split():
            if line.split()[0] == 'Correlation':
                parameter.append(file_lines[n-1].replace('\n', ''))
                polynomial = file_lines[n+1].replace('Coefficients', '')
                polynomial = polynomial.replace('[', '')
                polynomial = polynomial.replace(']', '')
                polynomial = polynomial.replace(':', '')
                polynomial = polynomial.split()
                polynomial_vector = [float(polynomial[n]) for n in range(len(polynomial))]

                residual = file_lines[n+2].replace('Residual:', '')
                residual = residual.replace('[', '')
                residual = residual.replace(']', '')
                residual = float(residual)

                new_set = {file_lines[n-1].replace('\n', ''): {'Polynomial': polynomial_vector,
                                                               'Residual': residual}}
                output.update(new_set)

    return output, parameter


def plotting_function_final(x_vector, y_vector, fig_num, x_label, y_label, data_label, plot_title, fontsize, clear=False, show=False,
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


def weighted_average(correlations, parameters):
    weights = []
    residuals = []
    for n in range(len(parameters)):
        if correlations[parameters[n]]['Residual'] < 1e6:
            residuals.append(correlations[parameters[n]]['Residual'])

    for n in range(len(parameters)):
        residual_p = correlations[parameters[n]]['Residual']
        if residual_p < 1e6:
            w_p = 1 - residual_p/sum(residuals)
        else:
            w_p = 0

        if len(residuals) == 1:
            w_p = 1.0
            weights.append(w_p)
            break

        weights.append(w_p)

    weights_sum = sum(weights)
    weights_vector = [weights[n]/weights_sum for n in range(len(weights))]

    return weights_vector


def gain_correlation_calculation(correlations, parameters, weights, foil, root, taper, sweep, span):
    # Break down the foil
    camber = int(foil[0])/10
    camber_pos = int(foil[1])/10
    thickness = int(foil[2:4])/100

    k = 0.0
    for n in range(len(weights)):
        if parameters[n].split()[1] == 'Thickness':
            k += weights[n] * np.polyval(correlations[parameters[n]]['Polynomial'], thickness)

        if parameters[n].split()[1] == 'Camber Position':
            k += weights[n] * np.polyval(correlations[parameters[n]]['Polynomial'], camber_pos)

        if parameters[n].split()[1] == 'Camber':
            k += weights[n] * np.polyval(correlations[parameters[n]]['Polynomial'], camber)

        if parameters[n].split()[1] == 'Span':
            k += weights[n] * np.polyval(correlations[parameters[n]]['Polynomial'], span)

        if parameters[n].split()[1] == 'Ratio':
            k += weights[n] * np.polyval(correlations[parameters[n]]['Polynomial'], taper)

        if parameters[n].split()[1] == 'Angle':
            k += weights[n] * np.polyval(correlations[parameters[n]]['Polynomial'], sweep)

        if parameters[n].split()[1] == 'Chord':
            k += weights[n] * np.polyval(correlations[parameters[n]]['Polynomial'], root)

    return k


# Build Final Controller
k1_correlations, k1_parameters = read_polyfit_file('nastran_results/Correlation_Polynomials_k1.dat')
k1_weights = weighted_average(k1_correlations, k1_parameters)

k2_correlations, k2_parameters = read_polyfit_file('nastran_results/Correlation_Polynomials_k2.dat')
k2_weights = weighted_average(k2_correlations, k2_parameters)

k3_correlations, k3_parameters = read_polyfit_file('nastran_results/Correlation_Polynomials_k3.dat')
k3_weights = weighted_average(k3_correlations, k3_parameters)

k4_correlations, k4_parameters = read_polyfit_file('nastran_results/Correlation_Polynomials_k4.dat')
k4_weights = weighted_average(k4_correlations, k4_parameters)

k5_correlations, k5_parameters = read_polyfit_file('nastran_results/Correlation_Polynomials_k5.dat')
k5_weights = weighted_average(k5_correlations, k5_parameters)

k6_correlations, k6_parameters = read_polyfit_file('nastran_results/Correlation_Polynomials_k6.dat')
k6_weights = weighted_average(k6_correlations, k6_parameters)

# Add final formula guess to file function

# Test the final controller

# Build Trajectory
number_of_tests = 5
t_max = 120
t0 = 0
t = np.linspace(t0, t_max, num=number_of_tests)
dt = t[1] - t[0]

# Rocket Trajectory
acceleration = 1.2 * 9.81
velocity = [t[n] * acceleration for n in range(number_of_tests)]
height = [velocity[n] * t[n] + acceleration / 2 * t[n] ** 2 for n in range(number_of_tests)]

# Atmospheric Conditions
mach = []
temperature = []
rho = []
pressure = []
for n in range(number_of_tests):
    t, q, p = barometric_formula(height[n])
    temperature.append(t)
    rho.append(round(q, 3) + 0.001)
    pressure.append(p)
    mach.append(round(velocity[n] / np.sqrt(1.4 * 287 * t), 3))


# Set Test Wing (Random Wing)

# Wing Properties
base_foil = '2106'
base_taper = 0.4
base_span = 0.6
base_sweep = 0.0
base_root = 0.3

k1 = gain_correlation_calculation(k1_correlations, k1_parameters, k1_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k2 = gain_correlation_calculation(k2_correlations, k2_parameters, k2_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k3 = gain_correlation_calculation(k3_correlations, k3_parameters, k3_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k4 = gain_correlation_calculation(k4_correlations, k4_parameters, k4_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k5 = gain_correlation_calculation(k5_correlations, k5_parameters, k5_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k6 = gain_correlation_calculation(k6_correlations, k6_parameters, k6_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)

BK = np.matrix([[0, 0, 0, 0, 0, 0],  [k1, k2, k3, k4, k5, k6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])

beta = 0
vf = []
h_plot = []
m_plot = []
rfreq = []
rocket_v_plot = []
for n in range(number_of_tests):

    # Create Flutter Analysis Card
    bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
              beta=np.deg2rad(beta),
              root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
              mkaero_freq=None)

    run_nastran(plot=False)
    flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
    flutter_v, k = find_flutter(flutter_results)
    if flutter_v is not None:
        vf.append(flutter_v)
        h_plot.append(height[n])
        m_plot.append(mach[n])
        rfreq.append(k)
        rocket_v_plot.append(velocity[n])

result_file_write(vf, h_plot, m_plot, 'Correlation_Test_Uncontrolled', wing_property_value='Base_Wing', new_file=True)

system = controller_gains(beta_control=beta, foil=base_foil, span=base_span, sweep=np.deg2rad(base_sweep),
                                      root_chord=base_root,
                                      taper=base_taper, rho_air=rho[0],
                                      velocity=velocity[0],
                                      flutter_v=0.0, rfreq=0.0)[1]

# Control System Stuff
x_prev = np.zeros([6, 1])
x_prev[1] += 0.001
xd_prev = x_prev

vf = []
h_plot = []
m_plot = []
rocket_v_plot = []
for n in range(number_of_tests):
    if n == 0:
        x = x_prev
    beta = abs(x[4])
    if beta > np.deg2rad(5):
        beta = np.deg2rad(5)

    bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
              beta=-beta,
              root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n])

    run_nastran(plot=False)
    flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
    flutter_v, k_controlled = find_flutter(flutter_results)

    if flutter_v is not None:
        vf.append(flutter_v)
        h_plot.append(height[n])
        m_plot.append(mach[n])
        rocket_v_plot.append(velocity[n])
        reference = (flutter_v - velocity[n]) / flutter_v
        if flutter_v > velocity[n] and reference > 0.3:
            system = controller_gains(beta_control=beta, foil=base_foil, span=base_span, sweep=np.deg2rad(base_sweep),
                                      root_chord=base_root,
                                      taper=base_taper, rho_air=rho[n],
                                      velocity=velocity[n],
                                      flutter_v=flutter_v, rfreq=k_controlled)[1]

    xd = system*x + BK*x
    x = dt/2 * (xd - xd_prev)
    xd_prev = xd

result_file_write(vf, h_plot, m_plot, 'Correlation_Test_Controlled', wing_property_value='Base_Wing', new_file=True)

# Graph Results
trajectory_values = read_rocket_velocity('nastran_results/Rocket_Trajectory.dat')

uncontrolled_labels, uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Correlation_Test_Uncontrolled.dat', number_of_tests)

controlled_labels, controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Correlation_Test_Controlled.dat', number_of_tests)

# Velocity vs Height
plotting_function_final(x_vector=trajectory_values['Height'], y_vector=trajectory_values['Velocity'], fig_num=1,
                        data_label='Rocket Trajectory', fontsize=12, plot_title=None, x_label='Height (m)', y_label='Velocity (m/s)', clear=True)

plotting_function_final(x_vector=uncontrolled_results[uncontrolled_labels[0]]['Height'], y_vector=uncontrolled_results[uncontrolled_labels[0]]['Velocity'], fig_num=1,
                        data_label='Uncontrolled Wing', fontsize=12, plot_title=None, x_label='Height (m)', y_label='Velocity (m/s)')

save_name = 'nastran_results/plots/Final_Test_Base_Wing_v_vs_h.png'

plotting_function_final(x_vector=controlled_results[controlled_labels[0]]['Height'], y_vector=controlled_results[controlled_labels[0]]['Velocity'], fig_num=1,
                        data_label='Controlled Wing', fontsize=12, plot_title='Final Test', x_label='Height (m)', y_label='Velocity (m/s)', save=True, savename=save_name)

# Velocity vs Mach
plotting_function_final(x_vector=trajectory_values['Mach'], y_vector=trajectory_values['Velocity'], fig_num=2,
                        data_label='Rocket Trajectory', fontsize=12, plot_title=None, x_label='Mach', y_label='Velocity (m/s)', clear=True)

plotting_function_final(x_vector=uncontrolled_results[uncontrolled_labels[0]]['Mach'], y_vector=uncontrolled_results[uncontrolled_labels[0]]['Velocity'], fig_num=2,
                        data_label='Uncontrolled Wing', fontsize=12, plot_title=None, x_label='Mach', y_label='Velocity (m/s)')

save_name = 'nastran_results/plots/Final_Test_Base_Wing_v_vs_m.png'

plotting_function_final(x_vector=controlled_results[controlled_labels[0]]['Mach'], y_vector=controlled_results[controlled_labels[0]]['Velocity'], fig_num=2,
                        data_label='Controlled Wing', fontsize=12, plot_title='Final Test', x_label='Mach', y_label='Velocity (m/s)', save=True, savename=save_name)

# Set Test Wing (Random Wing)

# Wing Properties
base_foil = '1104'
base_taper = 0.3
base_span = 0.6
base_sweep = 0.0
base_root = 0.4

k1 = gain_correlation_calculation(k1_correlations, k1_parameters, k1_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k2 = gain_correlation_calculation(k2_correlations, k2_parameters, k2_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k3 = gain_correlation_calculation(k3_correlations, k3_parameters, k3_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k4 = gain_correlation_calculation(k4_correlations, k4_parameters, k4_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k5 = gain_correlation_calculation(k5_correlations, k5_parameters, k5_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)
k6 = gain_correlation_calculation(k6_correlations, k6_parameters, k6_weights, base_foil, base_root, base_taper,
                                  base_sweep, base_span)

BK = np.matrix([[0, 0, 0, 0, 0, 0],  [k1, k2, k3, k4, k5, k6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])

beta = 0
vf = []
h_plot = []
m_plot = []
rfreq = []
rocket_v_plot = []
for n in range(number_of_tests):

    # Create Flutter Analysis Card
    bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
              beta=np.deg2rad(beta),
              root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
              mkaero_freq=None)

    run_nastran(plot=False)
    flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
    flutter_v, k = find_flutter(flutter_results)
    if flutter_v is not None:
        vf.append(flutter_v)
        h_plot.append(height[n])
        m_plot.append(mach[n])
        rfreq.append(k)
        rocket_v_plot.append(velocity[n])

result_file_write(vf, h_plot, m_plot, 'Correlation_Test_Uncontrolled2', wing_property_value='Base_Wing', new_file=True)

system = controller_gains(beta_control=beta, foil=base_foil, span=base_span, sweep=np.deg2rad(base_sweep),
                                      root_chord=base_root,
                                      taper=base_taper, rho_air=rho[0],
                                      velocity=velocity[0],
                                      flutter_v=0.0, rfreq=0.0)[1]

# Control System Stuff
x_prev = np.zeros([6, 1])
x_prev[1] += 0.001
xd_prev = x_prev

vf = []
h_plot = []
m_plot = []
rocket_v_plot = []
for n in range(number_of_tests):
    if n == 0:
        x = x_prev
    beta = abs(x[4])
    if beta > np.deg2rad(5):
        beta = np.deg2rad(5)

    bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
              beta=-beta,
              root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n])

    run_nastran(plot=False)
    flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
    flutter_v, k_controlled = find_flutter(flutter_results)

    if flutter_v is not None:
        vf.append(flutter_v)
        h_plot.append(height[n])
        m_plot.append(mach[n])
        rocket_v_plot.append(velocity[n])
        reference = (flutter_v - velocity[n]) / flutter_v
        if flutter_v > velocity[n] and reference > 0.3:
            system = controller_gains(beta_control=beta, foil=base_foil, span=base_span, sweep=np.deg2rad(base_sweep),
                                      root_chord=base_root,
                                      taper=base_taper, rho_air=rho[n],
                                      velocity=velocity[n],
                                      flutter_v=flutter_v, rfreq=k_controlled)[1]

    xd = system*x + BK*x
    x = dt/2 * (xd - xd_prev)
    xd_prev = xd

result_file_write(vf, h_plot, m_plot, 'Correlation_Test_Controlled2', wing_property_value='Base_Wing', new_file=True)

# Graph Results
trajectory_values = read_rocket_velocity('nastran_results/Rocket_Trajectory.dat')

uncontrolled_labels, uncontrolled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Correlation_Test_Uncontrolled2.dat', number_of_tests)

controlled_labels, controlled_results = extract_flutter_profile(
    'nastran_results/Flutter_Velocity_Correlation_Test_Controlled2.dat', number_of_tests)

# Velocity vs Height
plotting_function_final(x_vector=trajectory_values['Height'], y_vector=trajectory_values['Velocity'], fig_num=1,
                        data_label='Rocket Trajectory', fontsize=12, plot_title=None, x_label='Height (m)', y_label='Velocity (m/s)', clear=True)

plotting_function_final(x_vector=uncontrolled_results[uncontrolled_labels[0]]['Height'], y_vector=uncontrolled_results[uncontrolled_labels[0]]['Velocity'], fig_num=1,
                        data_label='Uncontrolled Wing', fontsize=12, plot_title=None, x_label='Height (m)', y_label='Velocity (m/s)')

save_name = 'nastran_results/plots/Final_Test_Base_Wing_v_vs_h2.png'

plotting_function_final(x_vector=controlled_results[controlled_labels[0]]['Height'], y_vector=controlled_results[controlled_labels[0]]['Velocity'], fig_num=1,
                        data_label='Controlled Wing', fontsize=12, plot_title='Final Test', x_label='Height (m)', y_label='Velocity (m/s)', save=True, savename=save_name)

# Velocity vs Mach
plotting_function_final(x_vector=trajectory_values['Mach'], y_vector=trajectory_values['Velocity'], fig_num=2,
                        data_label='Rocket Trajectory', fontsize=12, plot_title=None, x_label='Mach', y_label='Velocity (m/s)', clear=True)

plotting_function_final(x_vector=uncontrolled_results[uncontrolled_labels[0]]['Mach'], y_vector=uncontrolled_results[uncontrolled_labels[0]]['Velocity'], fig_num=2,
                        data_label='Uncontrolled Wing', fontsize=12, plot_title=None, x_label='Mach', y_label='Velocity (m/s)')

save_name = 'nastran_results/plots/Final_Test_Base_Wing_v_vs_m2.png'

plotting_function_final(x_vector=controlled_results[controlled_labels[0]]['Mach'], y_vector=controlled_results[controlled_labels[0]]['Velocity'], fig_num=2,
                        data_label='Controlled Wing', fontsize=12, plot_title='Final Test', x_label='Mach', y_label='Velocity (m/s)', save=True, savename=save_name)

# Grid Convergence

# To test the spanwise grid convergence of the wing
# Wing Properties
base_foil = '2106'
base_taper = 0.4
base_span = 0.6
base_sweep = 10.0
base_root = 0.3

spanwise_num = [5, 10, 20, 40, 80, 160]
grid_convergence_v = []
for n in range(len(spanwise_num)):
    bdf_build(foil=base_foil, chord_num=15, span_num=spanwise_num[n], span=base_span, sweep=base_sweep, flap_point=0.4,
                  beta=0,
                  root_chord=base_root, taper=base_taper, rho_input=rho[0], mach_input=mach[0])

    run_nastran(plot=False)
    flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
    flutter_v = find_flutter(flutter_results)[0]
    if flutter_v is not None:
        grid_convergence_v.append(flutter_v)

plt.figure(1)
plt.clf()
plt.grid()
plt.xlabel('Spanwise Number')
plt.ylabel('Flutter Velocity')
plt.plot(spanwise_num, grid_convergence_v)
plt.savefig('nastran_results/plots/Grid_Convergence_Study.png')

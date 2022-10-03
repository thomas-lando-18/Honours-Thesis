import numpy as np
from sim_functions import*
from controller import*
from wing_model.wing_build import main as wing
from matplotlib import pyplot as plt

# Simulation Parameters
number_of_tests = 5
t_max = 120
t0 = 0
t = np.linspace(t0, t_max, num=number_of_tests)

# Rocket Trajectory
acceleration = 1.2*9.81
velocity = [t[n]*acceleration for n in range(number_of_tests)]
height = [velocity[n]*t[n] + acceleration/2*t[n]**2 for n in range(number_of_tests)]

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
    mach.append(round(velocity[n]/np.sqrt(1.4*287*t), 3))

# Wing Properties
base_foil = '0110'
base_taper = 0.4
base_span = 0.6
base_sweep = 0.0
base_root = 0.3

foil_thickness = ['0102', '0104', '0106', '0108', '0110']
foil_camber = ['1110', '2110', '3110', '4110', '5110']
foil_camber_pos = ['1110', '1210', '1310', '1410', '1510']

taper = np.linspace(0.2, 0.6, num=5)
span = np.linspace(0.15, 1.5, num=5)
sweep = np.linspace(0.0, -5.0, num=5)
root_chord = np.linspace(0.15, 1.5, num=5)

# Uncontrolled Simulation (Foil Thickness)
for m in range(5):
    foil = foil_thickness[m]
    vf = []
    h_plot = []
    m_plot = []
    for n in range(number_of_tests):

        # Create Flutter Analysis Card
        bdf_build(foil=foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4, beta=0.0,
                  root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n])

        run_nastran(plot=False)
        flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
        flutter_v = find_flutter(flutter_results)
        if flutter_v is not None:
            vf.append(flutter_v)
            h_plot.append(height[n])
            m_plot.append(mach[n])

    if m == 0:
        result_file_write(vf, h_plot, m_plot, 'Foil_Thickness', wing_property_value=int(foil[2:4])/10, new_file=True)
    else:
        result_file_write(vf, h_plot, m_plot, 'Foil_Thickness', wing_property_value=int(foil[2:4])/10, new_file=False)

# Uncontrolled Simulation (Foil Camber)
for m in range(5):
    foil = foil_camber[m]
    vf = []
    h_plot = []
    m_plot = []
    for n in range(number_of_tests):

        # Create Flutter Analysis Card
        bdf_build(foil=foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4, beta=0.0,
                  root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n])

        run_nastran(plot=False)
        flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
        flutter_v = find_flutter(flutter_results)
        if flutter_v is not None:
            vf.append(flutter_v)
            h_plot.append(height[n])
            m_plot.append(mach[n])

    if m == 0:
        result_file_write(vf, h_plot, m_plot, 'Foil_Camber', wing_property_value=int(foil[0])/10, new_file=True)
    else:
        result_file_write(vf, h_plot, m_plot, 'Foil_Camber', wing_property_value=int(foil[0])/10, new_file=False)

# Uncontrolled Simulation (Foil Camber Position)
for m in range(5):
    foil = foil_camber_pos[m]
    vf = []
    h_plot = []
    m_plot = []
    for n in range(number_of_tests):

        # Create Flutter Analysis Card
        bdf_build(foil=foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4, beta=0.0,
                  root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n])

        run_nastran(plot=False)
        flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
        flutter_v = find_flutter(flutter_results)
        if flutter_v is not None:
            vf.append(flutter_v)
            h_plot.append(height[n])
            m_plot.append(mach[n])

    if m == 0:
        result_file_write(vf, h_plot, m_plot, 'Foil_Camber_Position', wing_property_value=int(foil[1])/10, new_file=True)
    else:
        result_file_write(vf, h_plot, m_plot, 'Foil_Camber_Position', wing_property_value=int(foil[1])/10, new_file=False)

# Uncontrolled Simulation (Taper)
for m in range(5):
    taper_n = taper[m]
    vf = []
    h_plot = []
    m_plot = []
    for n in range(number_of_tests):

        # Create Flutter Analysis Card
        bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4, beta=0.0,
                  root_chord=base_root, taper=taper_n, rho_input=rho[n], mach_input=mach[n])

        run_nastran(plot=False)
        flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
        flutter_v = find_flutter(flutter_results)
        if flutter_v is not None:
            vf.append(flutter_v)
            h_plot.append(height[n])
            m_plot.append(mach[n])

    if m == 0:
        result_file_write(vf, h_plot, m_plot, 'Taper', wing_property_value=taper_n, new_file=True)
    else:
        result_file_write(vf, h_plot, m_plot, 'Taper', wing_property_value=taper_n, new_file=False)

# Uncontrolled Simulation (Span)
for m in range(5):
    semi_span = span[m]
    vf = []
    h_plot = []
    m_plot = []
    for n in range(number_of_tests):

        # Create Flutter Analysis Card
        bdf_build(foil=base_foil, chord_num=15, span_num=15, span=semi_span, sweep=base_sweep, flap_point=0.4, beta=0.0,
                  root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n])

        run_nastran(plot=False)
        flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
        flutter_v = find_flutter(flutter_results)
        if flutter_v is not None:
            vf.append(flutter_v)
            h_plot.append(height[n])
            m_plot.append(mach[n])

    if m == 0:
        result_file_write(vf, h_plot, m_plot, 'Semi_Span', wing_property_value=semi_span, new_file=True)
    else:
        result_file_write(vf, h_plot, m_plot, 'Semi_Span', wing_property_value=semi_span, new_file=False)

# Uncontrolled Simulation (Wing Sweep)
for m in range(5):
    wing_sweep = sweep[m]
    vf = []
    h_plot = []
    m_plot = []
    for n in range(number_of_tests):

        # Create Flutter Analysis Card
        bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=wing_sweep, flap_point=0.4, beta=0.0,
                  root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n])

        run_nastran(plot=False)
        flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
        flutter_v = find_flutter(flutter_results)
        if flutter_v is not None:
            vf.append(flutter_v)
            h_plot.append(height[n])
            m_plot.append(mach[n])

    if m == 0:
        result_file_write(vf, h_plot, m_plot, 'Sweep', wing_property_value=wing_sweep, new_file=True)
    else:
        result_file_write(vf, h_plot, m_plot, 'Sweep', wing_property_value=wing_sweep, new_file=False)

# Uncontrolled Simulation (foil thickness)
for m in range(5):
    root = root_chord[m]
    vf = []
    h_plot = []
    m_plot = []
    for n in range(number_of_tests):

        # Create Flutter Analysis Card
        bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4, beta=0.0,
                  root_chord=root, taper=base_taper, rho_input=rho[n], mach_input=mach[n])

        run_nastran(plot=False)
        flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
        flutter_v = find_flutter(flutter_results)
        if flutter_v is not None:
            vf.append(flutter_v)
            h_plot.append(height[n])
            m_plot.append(mach[n])

    if m == 0:
        result_file_write(vf, h_plot, m_plot, 'Root_Chord', wing_property_value=root, new_file=True)
    else:
        result_file_write(vf, h_plot, m_plot, 'Root_Chord', wing_property_value=root, new_file=False)

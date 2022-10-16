import numpy as np
from sim_functions import *
from controller import *
from wing_model.wing_build import main as wing
from matplotlib import pyplot as plt

# Simulation Parameters
number_of_tests = 50
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

# Save Trajectory to File
trajectory_file_write(velocity, height, mach, rho, temperature)

# Wing Properties
base_foil = '1110'
base_taper = 0.4
base_span = 0.6
base_sweep = 0.0
base_root = 0.3

foil_thickness = ['1102', '1104', '1106', '1108', '1110']
foil_camber = ['1110', '2110', '3110', '4110', '5110']
foil_camber_pos = ['1110', '1210', '1310', '1410', '1510']

taper = np.linspace(0.2, 0.6, num=5)
span = np.linspace(0.15, 0.7, num=5)
sweep = np.linspace(0.0, -5.0, num=5)
root_chord = np.linspace(0.15, 0.7, num=5)

# Reduced Wing Frequencies 1x8 List
mk_freq_input = None
# Foil Thickness Complete Simulation
for m in range(5):
    foil = foil_thickness[m]
    beta = 0
    vf = []
    h_plot = []
    m_plot = []
    rfreq = []
    rocket_v_plot = []
    for n in range(number_of_tests):

        # Create Flutter Analysis Card
        bdf_build(foil=foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
                  beta=np.deg2rad(beta),
                  root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
                  mkaero_freq=mk_freq_input)

        run_nastran(plot=False)
        flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
        flutter_v, k = find_flutter(flutter_results)
        if flutter_v is not None:
            vf.append(flutter_v)
            h_plot.append(height[n])
            m_plot.append(mach[n])
            rfreq.append(k)
            rocket_v_plot.append(velocity[n])

    plt.figure(1)
    plt.grid()
    plt.xlabel('Height')
    plt.ylabel('Velocity')
    plt.plot(h_plot, vf, label=foil[2:4])

    if m == 0:
        result_file_write(vf, h_plot, m_plot, 'Foil_Thickness', wing_property_value=int(foil[2:4]) / 10, new_file=True)
    else:
        result_file_write(vf, h_plot, m_plot, 'Foil_Thickness', wing_property_value=int(foil[2:4]) / 10, new_file=False)

    # Find Equilibrium Point
    equilibrium_point = 0
    dif = 1e6
    for n in range(len(vf)):
        if (vf[n] - rocket_v_plot[n]) < dif:
            dif = vf[n] - rocket_v_plot[n]
            equilibrium_point = n
        elif vf[n] <= rocket_v_plot[n]:
            equilibrium_point = n
            break
    print(equilibrium_point)
    # Create Controller Gains
    BK, system = controller_gains(beta_control=5.0, foil=foil, span=base_span, sweep=base_sweep, root_chord=base_root,
                                  taper=base_taper, rho_air=rho[equilibrium_point-1],
                                  velocity=rocket_v_plot[equilibrium_point-1],
                                  flutter_v=vf[equilibrium_point-1], rfreq=rfreq[equilibrium_point-1])

    gain_vector = list(BK[1, :][0])
    if m == 0:
        gain_result_file_write(gain_vector, 'Foil_Thickness', foil[2:4], True)
    else:
        gain_result_file_write(gain_vector, 'Foil_Thickness', foil[2:4], False)

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

        bdf_build(foil=foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
                  beta=-beta,
                  root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
                  mkaero_freq=mk_freq_input)

        run_nastran(plot=False)
        flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
        flutter_v = find_flutter(flutter_results)[0]

        if flutter_v is not None:
            vf.append(flutter_v)
            h_plot.append(height[n])
            m_plot.append(mach[n])
            rocket_v_plot.append(velocity[n])
            reference = (flutter_v - velocity[n]) / flutter_v
            if flutter_v > velocity[n] and reference < 0.2:
                system = controller_gains(beta_control=beta, foil=foil, span=base_span, sweep=base_sweep,
                                          root_chord=base_root,
                                          taper=base_taper, rho_air=rho[n],
                                          velocity=velocity[n],
                                          flutter_v=flutter_v, rfreq=rfreq[equilibrium_point])[1]

        xd = system*x + BK*x
        x = dt/2 * (xd - xd_prev)
        xd_prev = xd
    if m == 0:
        controlled_result_file_write(vf, h_plot, m_plot, 'Foil_Thickness', foil[2:4], True)
    else:
        controlled_result_file_write(vf, h_plot, m_plot, 'Foil_Thickness', foil[2:4], False)

# # Foil Camber Complete Simulation
# for m in range(2):
#     foil = foil_camber[m]
#     beta = 0
#     vf = []
#     h_plot = []
#     m_plot = []
#     rfreq = []
#     rocket_v_plot = []
#     for n in range(number_of_tests):
#
#         # Create Flutter Analysis Card
#         bdf_build(foil=foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
#                   beta=np.deg2rad(beta),
#                   root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
#                   mkaero_freq=mk_freq_input)
#
#         run_nastran(plot=False)
#         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
#         flutter_v, k = find_flutter(flutter_results)
#         if flutter_v is not None:
#             vf.append(flutter_v)
#             h_plot.append(height[n])
#             m_plot.append(mach[n])
#             rfreq.append(k)
#             rocket_v_plot.append(velocity[n])
#
#     plt.figure(1)
#     plt.grid()
#     plt.xlabel('Height')
#     plt.ylabel('Velocity')
#     plt.plot(h_plot, vf, label=foil[2:4])
#
#     if m == 0:
#         result_file_write(vf, h_plot, m_plot, 'Foil_Camber', wing_property_value=int(foil[0]) / 10, new_file=True)
#     else:
#         result_file_write(vf, h_plot, m_plot, 'Foil_Camber', wing_property_value=int(foil[0]) / 10, new_file=False)
#
#     # Find Equilibrium Point
#     equilibrium_point = 0
#     dif = 1e6
#     for n in range(len(vf)):
#         if (vf[n] - rocket_v_plot[n]) < dif:
#             dif = vf[n] - rocket_v_plot[n]
#             equilibrium_point = n
#         elif vf[n] <= rocket_v_plot[n]:
#             equilibrium_point = n
#             break
#     print(equilibrium_point)
#     # Create Controller Gains
#     BK, system = controller_gains(beta_control=5.0, foil=foil, span=base_span, sweep=base_sweep, root_chord=base_root,
#                                   taper=base_taper, rho_air=rho[equilibrium_point-1],
#                                   velocity=rocket_v_plot[equilibrium_point-1],
#                                   flutter_v=vf[equilibrium_point-1], rfreq=rfreq[equilibrium_point-1])
#
#     gain_vector = list(BK[1, :][0])
#     if m == 0:
#         gain_result_file_write(gain_vector, 'Foil_Camber', foil[0], True)
#     else:
#         gain_result_file_write(gain_vector, 'Foil_Camber', foil[0], False)
#
#     # Control System Stuff
#     x_prev = np.zeros([6, 1])
#     x_prev[1] += 0.001
#     xd_prev = x_prev
#
#     vf = []
#     h_plot = []
#     m_plot = []
#     rocket_v_plot = []
#     for n in range(number_of_tests):
#         if n == 0:
#             x = x_prev
#         beta = abs(x[4])
#         if beta > np.deg2rad(5):
#             beta = np.deg2rad(5)
#
#         bdf_build(foil=foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
#                   beta=-beta,
#                   root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
#                   mkaero_freq=mk_freq_input)
#
#         run_nastran(plot=False)
#         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
#         flutter_v = find_flutter(flutter_results)[0]
#
#         if flutter_v is not None:
#             vf.append(flutter_v)
#             h_plot.append(height[n])
#             m_plot.append(mach[n])
#             rocket_v_plot.append(velocity[n])
#             reference = (flutter_v - velocity[n]) / flutter_v
#             if flutter_v > velocity[n] and reference > 0.3:
#                 system = controller_gains(beta_control=beta, foil=foil, span=base_span, sweep=base_sweep,
#                                           root_chord=base_root,
#                                           taper=base_taper, rho_air=rho[n],
#                                           velocity=velocity[n],
#                                           flutter_v=flutter_v, rfreq=rfreq[equilibrium_point])[1]
#
#         xd = system*x + BK*x
#         x = dt/2 * (xd - xd_prev)
#         xd_prev = xd
#     if m == 0:
#         controlled_result_file_write(vf, h_plot, m_plot, 'Foil_Camber', foil[0], True)
#     else:
#         controlled_result_file_write(vf, h_plot, m_plot, 'Foil_Camber', foil[0], False)
#
# # Foil Camber Position Complete Simulation
# for m in range(2):
#     foil = foil_camber_pos[m]
#     beta = 0
#     vf = []
#     h_plot = []
#     m_plot = []
#     rfreq = []
#     rocket_v_plot = []
#     for n in range(number_of_tests):
#
#         # Create Flutter Analysis Card
#         bdf_build(foil=foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
#                   beta=np.deg2rad(beta),
#                   root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
#                   mkaero_freq=mk_freq_input)
#
#         run_nastran(plot=False)
#         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
#         flutter_v, k = find_flutter(flutter_results)
#         if flutter_v is not None:
#             vf.append(flutter_v)
#             h_plot.append(height[n])
#             m_plot.append(mach[n])
#             rfreq.append(k)
#             rocket_v_plot.append(velocity[n])
#
#     plt.figure(1)
#     plt.grid()
#     plt.xlabel('Height')
#     plt.ylabel('Velocity')
#     plt.plot(h_plot, vf, label=foil[2:4])
#
#     if m == 0:
#         result_file_write(vf, h_plot, m_plot, 'Foil_Camber_Position', wing_property_value=int(foil[2]) / 10, new_file=True)
#     else:
#         result_file_write(vf, h_plot, m_plot, 'Foil_Camber_Position', wing_property_value=int(foil[2]) / 10, new_file=False)
#
#     # Find Equilibrium Point
#     equilibrium_point = 0
#     dif = 1e6
#     for n in range(len(vf)):
#         if (vf[n] - rocket_v_plot[n]) < dif:
#             dif = vf[n] - rocket_v_plot[n]
#             equilibrium_point = n
#         elif vf[n] <= rocket_v_plot[n]:
#             equilibrium_point = n
#             break
#     print(equilibrium_point)
#     # Create Controller Gains
#     BK, system = controller_gains(beta_control=5.0, foil=foil, span=base_span, sweep=base_sweep, root_chord=base_root,
#                                   taper=base_taper, rho_air=rho[equilibrium_point-1],
#                                   velocity=rocket_v_plot[equilibrium_point-1],
#                                   flutter_v=vf[equilibrium_point-1], rfreq=rfreq[equilibrium_point-1])
#
#     gain_vector = list(BK[1, :][0])
#     if m == 0:
#         gain_result_file_write(gain_vector, 'Foil_Camber_Position', foil[1], True)
#     else:
#         gain_result_file_write(gain_vector, 'Foil_Camber_Position', foil[1], False)
#
#     # Control System Stuff
#     x_prev = np.zeros([6, 1])
#     x_prev[1] += 0.001
#     xd_prev = x_prev
#
#     vf = []
#     h_plot = []
#     m_plot = []
#     rocket_v_plot = []
#     for n in range(number_of_tests):
#         if n == 0:
#             x = x_prev
#         beta = abs(x[4])
#         if beta > np.deg2rad(5):
#             beta = np.deg2rad(5)
#
#         bdf_build(foil=foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
#                   beta=-beta,
#                   root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
#                   mkaero_freq=mk_freq_input)
#
#         run_nastran(plot=False)
#         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
#         flutter_v = find_flutter(flutter_results)[0]
#
#         if flutter_v is not None:
#             vf.append(flutter_v)
#             h_plot.append(height[n])
#             m_plot.append(mach[n])
#             rocket_v_plot.append(velocity[n])
#             reference = (flutter_v - velocity[n]) / flutter_v
#             if flutter_v > velocity[n] and reference > 0.3:
#                 system = controller_gains(beta_control=beta, foil=foil, span=base_span, sweep=base_sweep,
#                                           root_chord=base_root,
#                                           taper=base_taper, rho_air=rho[n],
#                                           velocity=velocity[n],
#                                           flutter_v=flutter_v, rfreq=rfreq[equilibrium_point])[1]
#
#         xd = system*x + BK*x
#         x = dt/2 * (xd - xd_prev)
#         xd_prev = xd
#     if m == 0:
#         controlled_result_file_write(vf, h_plot, m_plot, 'Foil_Camber_Position', foil[1], True)
#     else:
#         controlled_result_file_write(vf, h_plot, m_plot, 'Foil_Camber_Position', foil[1], False)
#
# # Semi Span Complete Simulation
# for m in range(5):
#     beta = 0
#     vf = []
#     h_plot = []
#     m_plot = []
#     rfreq = []
#     rocket_v_plot = []
#     for n in range(number_of_tests):
#
#         # Create Flutter Analysis Card
#         bdf_build(foil=base_foil, chord_num=15, span_num=15, span=span[m], sweep=base_sweep, flap_point=0.4,
#                   beta=np.deg2rad(beta),
#                   root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
#                   mkaero_freq=mk_freq_input)
#
#         run_nastran(plot=False)
#         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
#         flutter_v, k = find_flutter(flutter_results)
#         if flutter_v is not None:
#             vf.append(flutter_v)
#             h_plot.append(height[n])
#             m_plot.append(mach[n])
#             rfreq.append(k)
#             rocket_v_plot.append(velocity[n])
#
#     plt.figure(1)
#     plt.grid()
#     plt.xlabel('Height')
#     plt.ylabel('Velocity')
#     plt.plot(h_plot, vf, label=foil[2:4])
#
#     if m == 0:
#         result_file_write(vf, h_plot, m_plot, 'Semi_Span', wing_property_value=span[m], new_file=True)
#     else:
#         result_file_write(vf, h_plot, m_plot, 'Semi_Span', wing_property_value=span[m], new_file=False)
#
#     # Find Equilibrium Point
#     equilibrium_point = 0
#     dif = 1e6
#     for n in range(len(vf)):
#         if (vf[n] - rocket_v_plot[n]) < dif:
#             dif = vf[n] - rocket_v_plot[n]
#             equilibrium_point = n
#         elif vf[n] <= rocket_v_plot[n]:
#             equilibrium_point = n
#             break
#     print(equilibrium_point)
#     # Create Controller Gains
#     BK, system = controller_gains(beta_control=5.0, foil=base_foil, span=span[m], sweep=base_sweep, root_chord=base_root,
#                                   taper=base_taper, rho_air=rho[equilibrium_point-1],
#                                   velocity=rocket_v_plot[equilibrium_point-1],
#                                   flutter_v=vf[equilibrium_point-1], rfreq=rfreq[equilibrium_point-1])
#
#     gain_vector = list(BK[1, :][0])
#     if m == 0:
#         gain_result_file_write(gain_vector, 'Semi_Span', span[m], True)
#     else:
#         gain_result_file_write(gain_vector, 'Semi_Span', span[m], False)
#
#     # Control System Stuff
#     x_prev = np.zeros([6, 1])
#     x_prev[1] += 0.001
#     xd_prev = x_prev
#
#     vf = []
#     h_plot = []
#     m_plot = []
#     rocket_v_plot = []
#     for n in range(number_of_tests):
#         if n == 0:
#             x = x_prev
#         beta = abs(x[4])
#         if beta > np.deg2rad(5):
#             beta = np.deg2rad(5)
#
#         bdf_build(foil=base_foil, chord_num=15, span_num=15, span=span[m], sweep=base_sweep, flap_point=0.4,
#                   beta=-beta,
#                   root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
#                   mkaero_freq=mk_freq_input)
#
#         run_nastran(plot=False)
#         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
#         flutter_v = find_flutter(flutter_results)[0]
#
#         if flutter_v is not None:
#             vf.append(flutter_v)
#             h_plot.append(height[n])
#             m_plot.append(mach[n])
#             rocket_v_plot.append(velocity[n])
#             reference = (flutter_v - velocity[n]) / flutter_v
#             if flutter_v > velocity[n] and reference > 0.3:
#                 system = controller_gains(beta_control=beta, foil=base_foil, span=span[m], sweep=base_sweep,
#                                           root_chord=base_root,
#                                           taper=base_taper, rho_air=rho[n],
#                                           velocity=velocity[n],
#                                           flutter_v=flutter_v, rfreq=rfreq[equilibrium_point])[1]
#
#         xd = system*x + BK*x
#         x = dt/2 * (xd - xd_prev)
#         xd_prev = xd
#     if m == 0:
#         controlled_result_file_write(vf, h_plot, m_plot, 'Semi_Span', span[m], True)
#     else:
#         controlled_result_file_write(vf, h_plot, m_plot, 'Semi_Span', span[m], False)
#
# # Root Chord Complete Simulation
#
# # for m in range(5):
# #     beta = 0
# #     vf = []
# #     h_plot = []
# #     m_plot = []
# #     rfreq = []
# #     rocket_v_plot = []
# #     for n in range(number_of_tests):
# #
# #         # Create Flutter Analysis Card
# #         bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
# #                   beta=np.deg2rad(beta),
# #                   root_chord=root_chord[m], taper=base_taper, rho_input=rho[n], mach_input=mach[n],
# #                   mkaero_freq=mk_freq_input)
# #
# #         run_nastran(plot=False)
# #         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
# #         flutter_v, k = find_flutter(flutter_results)
# #         if flutter_v is not None:
# #             vf.append(flutter_v)
# #             h_plot.append(height[n])
# #             m_plot.append(mach[n])
# #             rfreq.append(k)
# #             rocket_v_plot.append(velocity[n])
# #
# #     plt.figure(1)
# #     plt.grid()
# #     plt.xlabel('Height')
# #     plt.ylabel('Velocity')
# #     plt.plot(h_plot, vf, label=foil[2:4])
# #
# #     if m == 0:
# #         result_file_write(vf, h_plot, m_plot, 'Root_Chord', wing_property_value=root_chord[m], new_file=True)
# #     else:
# #         result_file_write(vf, h_plot, m_plot, 'Root_Chord', wing_property_value=root_chord[m], new_file=False)
# #
# #     # Find Equilibrium Point
# #     equilibrium_point = 0
# #     dif = 1e6
# #     for n in range(len(vf)):
# #         if (vf[n] - rocket_v_plot[n]) < dif:
# #             dif = vf[n] - rocket_v_plot[n]
# #             equilibrium_point = n
# #         elif vf[n] <= rocket_v_plot[n]:
# #             equilibrium_point = n
# #             break
# #     print(equilibrium_point)
# #     # Create Controller Gains
# #     BK, system = controller_gains(beta_control=5.0, foil=base_foil, span=base_span, sweep=base_sweep, root_chord=root_chord[m],
# #                                   taper=base_taper, rho_air=rho[equilibrium_point-1],
# #                                   velocity=rocket_v_plot[equilibrium_point-1],
# #                                   flutter_v=vf[equilibrium_point-1], rfreq=rfreq[equilibrium_point-1])
# #
# #     gain_vector = list(BK[1, :][0])
# #     if m == 0:
# #         gain_result_file_write(gain_vector, 'Root_Chord', root_chord[m], True)
# #     else:
# #         gain_result_file_write(gain_vector, 'Root_Chord', root_chord[m], False)
# #
# #     # Control System Stuff
# #     x_prev = np.zeros([6, 1])
# #     x_prev[1] += 0.001
# #     xd_prev = x_prev
# #
# #     vf = []
# #     h_plot = []
# #     m_plot = []
# #     rocket_v_plot = []
# #     for n in range(number_of_tests):
# #         if n == 0:
# #             x = x_prev
# #         beta = abs(x[4])
# #         if beta > np.deg2rad(5):
# #             beta = np.deg2rad(5)
# #
# #         bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
# #                   beta=-beta,
# #                   root_chord=root_chord[m], taper=base_taper, rho_input=rho[n], mach_input=mach[n],
# #                   mkaero_freq=mk_freq_input)
# #
# #         run_nastran(plot=False)
# #         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
# #         flutter_v = find_flutter(flutter_results)[0]
# #
# #         if flutter_v is not None:
# #             vf.append(flutter_v)
# #             h_plot.append(height[n])
# #             m_plot.append(mach[n])
# #             rocket_v_plot.append(velocity[n])
# #             reference = (flutter_v - velocity[n]) / flutter_v
# #             if flutter_v > velocity[n] and reference > 0.3:
# #                 system = controller_gains(beta_control=beta, foil=base_foil, span=base_span, sweep=base_sweep,
# #                                           root_chord=root_chord[m],
# #                                           taper=base_taper, rho_air=rho[n],
# #                                           velocity=velocity[n],
# #                                           flutter_v=flutter_v, rfreq=rfreq[equilibrium_point])[1]
# #
# #         xd = system*x + BK*x
# #         x = dt/2 * (xd - xd_prev)
# #         xd_prev = xd
# #     if m == 0:
# #         controlled_result_file_write(vf, h_plot, m_plot, 'Root_Chord', root_chord[m], True)
# #     else:
# #         controlled_result_file_write(vf, h_plot, m_plot, 'Root_Chord', root_chord[m], False)
#
# # # Taper Ratio Complete Simulation
# # for m in range(5):
# #     beta = 0
# #     vf = []
# #     h_plot = []
# #     m_plot = []
# #     rfreq = []
# #     rocket_v_plot = []
# #     for n in range(number_of_tests):
# #
# #         # Create Flutter Analysis Card
# #         bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
# #                   beta=np.deg2rad(beta),
# #                   root_chord=base_root, taper=taper[m], rho_input=rho[n], mach_input=mach[n],
# #                   mkaero_freq=mk_freq_input)
# #
# #         run_nastran(plot=False)
# #         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
# #         flutter_v, k = find_flutter(flutter_results)
# #         if flutter_v is not None:
# #             vf.append(flutter_v)
# #             h_plot.append(height[n])
# #             m_plot.append(mach[n])
# #             rfreq.append(k)
# #             rocket_v_plot.append(velocity[n])
# #
# #     plt.figure(1)
# #     plt.grid()
# #     plt.xlabel('Height')
# #     plt.ylabel('Velocity')
# #     plt.plot(h_plot, vf, label=foil[2:4])
# #
# #     if m == 0:
# #         result_file_write(vf, h_plot, m_plot, 'Taper', wing_property_value=taper[m], new_file=True)
# #     else:
# #         result_file_write(vf, h_plot, m_plot, 'Taper', wing_property_value=taper[m], new_file=False)
# #
# #     # Find Equilibrium Point
# #     equilibrium_point = 0
# #     dif = 1e6
# #     for n in range(len(vf)):
# #         if (vf[n] - rocket_v_plot[n]) < dif:
# #             dif = vf[n] - rocket_v_plot[n]
# #             equilibrium_point = n
# #         elif vf[n] <= rocket_v_plot[n]:
# #             equilibrium_point = n
# #             break
# #     print(equilibrium_point)
# #     # Create Controller Gains
# #     BK, system = controller_gains(beta_control=5.0, foil=base_foil, span=base_span, sweep=base_sweep, root_chord=base_root,
# #                                   taper=taper[m], rho_air=rho[equilibrium_point-1],
# #                                   velocity=rocket_v_plot[equilibrium_point-1],
# #                                   flutter_v=vf[equilibrium_point-1], rfreq=rfreq[equilibrium_point-1])
# #
# #     gain_vector = list(BK[1, :][0])
# #     if m == 0:
# #         gain_result_file_write(gain_vector, 'Taper', taper[m], True)
# #     else:
# #         gain_result_file_write(gain_vector, 'Taper', taper[m], False)
# #
# #     # Control System Stuff
# #     x_prev = np.zeros([6, 1])
# #     x_prev[1] += 0.001
# #     xd_prev = x_prev
# #
# #     vf = []
# #     h_plot = []
# #     m_plot = []
# #     rocket_v_plot = []
# #     for n in range(number_of_tests):
# #         if n == 0:
# #             x = x_prev
# #         beta = abs(x[4])
# #         if beta > np.deg2rad(5):
# #             beta = np.deg2rad(5)
# #
# #         bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=base_sweep, flap_point=0.4,
# #                   beta=-beta,
# #                   root_chord=base_root, taper=taper[m], rho_input=rho[n], mach_input=mach[n],
# #                   mkaero_freq=mk_freq_input)
# #
# #         run_nastran(plot=False)
# #         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
# #         flutter_v = find_flutter(flutter_results)[0]
# #
# #         if flutter_v is not None:
# #             vf.append(flutter_v)
# #             h_plot.append(height[n])
# #             m_plot.append(mach[n])
# #             rocket_v_plot.append(velocity[n])
# #             reference = (flutter_v - velocity[n]) / flutter_v
# #             if flutter_v > velocity[n] and reference > 0.3:
# #                 system = controller_gains(beta_control=beta, foil=base_foil, span=base_span, sweep=base_sweep,
# #                                           root_chord=base_root,
# #                                           taper=taper[m], rho_air=rho[n],
# #                                           velocity=velocity[n],
# #                                           flutter_v=flutter_v, rfreq=rfreq[equilibrium_point])[1]
# #
# #         xd = system*x + BK*x
# #         x = dt/2 * (xd - xd_prev)
# #         xd_prev = xd
# #     if m == 0:
# #         controlled_result_file_write(vf, h_plot, m_plot, 'Taper', taper[m], True)
# #     else:
# #         controlled_result_file_write(vf, h_plot, m_plot, 'Taper', taper[m], False)
#
# # Sweep Angle Complete Simulation
# for m in range(1):
#     beta = 0
#     vf = []
#     h_plot = []
#     m_plot = []
#     rfreq = []
#     rocket_v_plot = []
#     for n in range(number_of_tests):
#
#         # Create Flutter Analysis Card
#         bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=sweep[m], flap_point=0.4,
#                   beta=np.deg2rad(beta),
#                   root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
#                   mkaero_freq=mk_freq_input)
#
#         run_nastran(plot=False)
#         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
#         flutter_v, k = find_flutter(flutter_results)
#         if flutter_v is not None:
#             vf.append(flutter_v)
#             h_plot.append(height[n])
#             m_plot.append(mach[n])
#             rfreq.append(k)
#             rocket_v_plot.append(velocity[n])
#
#     plt.figure(1)
#     plt.grid()
#     plt.xlabel('Height')
#     plt.ylabel('Velocity')
#     plt.plot(h_plot, vf, label=foil[2:4])
#
#     if m == 0:
#         result_file_write(vf, h_plot, m_plot, 'Sweep', wing_property_value=sweep[m], new_file=True)
#     else:
#         result_file_write(vf, h_plot, m_plot, 'Sweep', wing_property_value=sweep[m], new_file=False)
#
#     # Find Equilibrium Point
#     equilibrium_point = 0
#     dif = 1e6
#     for n in range(len(vf)):
#         if (vf[n] - rocket_v_plot[n]) < dif:
#             dif = vf[n] - rocket_v_plot[n]
#             equilibrium_point = n
#         elif vf[n] <= rocket_v_plot[n]:
#             equilibrium_point = n
#             break
#     print(equilibrium_point)
#     # Create Controller Gains
#     BK, system = controller_gains(beta_control=5.0, foil=base_foil, span=base_span, sweep=sweep[m], root_chord=base_root,
#                                   taper=base_taper, rho_air=rho[equilibrium_point-1],
#                                   velocity=rocket_v_plot[equilibrium_point-1],
#                                   flutter_v=vf[equilibrium_point-1], rfreq=rfreq[equilibrium_point-1])
#
#     gain_vector = list(BK[1, :][0])
#     if m == 0:
#         gain_result_file_write(gain_vector, 'Sweep', sweep[m], True)
#     else:
#         gain_result_file_write(gain_vector, 'Sweep', sweep[m], False)
#
#     # Control System Stuff
#     x_prev = np.zeros([6, 1])
#     x_prev[1] += 0.001
#     xd_prev = x_prev
#
#     vf = []
#     h_plot = []
#     m_plot = []
#     rocket_v_plot = []
#     for n in range(number_of_tests):
#         if n == 0:
#             x = x_prev
#         beta = abs(x[4])
#         if beta > np.deg2rad(5):
#             beta = np.deg2rad(5)
#
#         bdf_build(foil=base_foil, chord_num=15, span_num=15, span=base_span, sweep=sweep[m], flap_point=0.4,
#                   beta=-beta,
#                   root_chord=base_root, taper=base_taper, rho_input=rho[n], mach_input=mach[n],
#                   mkaero_freq=mk_freq_input)
#
#         run_nastran(plot=False)
#         flutter_results = read_f06_file('nastran_files/3d_6dof_card.f06')
#         flutter_v = find_flutter(flutter_results)[0]
#
#         if flutter_v is not None:
#             vf.append(flutter_v)
#             h_plot.append(height[n])
#             m_plot.append(mach[n])
#             rocket_v_plot.append(velocity[n])
#             reference = (flutter_v - velocity[n]) / flutter_v
#             if flutter_v > velocity[n] and reference > 0.3:
#                 system = controller_gains(beta_control=beta, foil=base_foil, span=base_span, sweep=sweep[m],
#                                           root_chord=base_root,
#                                           taper=base_taper, rho_air=rho[n],
#                                           velocity=velocity[n],
#                                           flutter_v=flutter_v, rfreq=rfreq[equilibrium_point])[1]
#
#         xd = system*x + BK*x
#         x = dt/2 * (xd - xd_prev)
#         xd_prev = xd
#     if m == 0:
#         controlled_result_file_write(vf, h_plot, m_plot, 'Sweep', sweep[m], True)
#     else:
#         controlled_result_file_write(vf, h_plot, m_plot, 'Sweep', sweep[m], False)

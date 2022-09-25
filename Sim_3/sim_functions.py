# Imports
import numpy as np
import os
import subprocess
from pyNastran.bdf.bdf import BDF, CaseControlDeck
from pyNastran.f06.parse_flutter import plot_flutter_f06, make_flutter_plots
from pyNastran.f06.parse_flutter import make_flutter_response
from pyNastran.f06.flutter_response import FlutterResponse
import pprint
from wing_model.wing_build import main as wing


# Constants
def bdf_build(foil, span_num, chord_num, root_chord, taper, span, sweep, rho_input, mach_input, flap_point, beta):
    bdf_card_name = 'nastran_files/3d_6dof_card.bdf'

    flutter_sid = 100
    flfact_density_sid = 101
    flfact_mach_sid = 102
    flfact_velocity = 103

    eigrl_sid = 200

    spc_sid = 300

    pshell_pid = 100

    mat1_mid = 100
    youngs_modulus = 77.8e9
    poissons_ratio = 0.3
    shear_modulus = youngs_modulus / (2 * (1 + 2 * poissons_ratio))
    material_density = 2700.0
    damping_coef = 0.5

    caero5_eid = 101

    aefact_thickness_sid = 400
    aefact_alpha_sid = 401

    paero5_pid = 201

    spline1_eid = 201

    set1_sid = 500

    # Create model
    model = BDF()
    model.sol = 145

    case_control_list = [
        'ECHO=NONE',
        'FMETHOD=' + str(flutter_sid),
        'METHOD=' + str(eigrl_sid),
        'SPC=' + str(spc_sid),
        'RESVEC=NO',
        'DISP=ALL'
    ]

    case_ctrl = CaseControlDeck(case_control_list)
    model.case_control_deck = case_ctrl

    # Geometry
    # span_num = 10
    # chord_num = 15
    # root_chord = float(.1)
    # taper = float(0.5)
    # span = 1.0
    geometry = wing(foil=foil, semi_span=span, root_chord=root_chord, taper=taper, sweep=sweep, num=span_num,
                    chord_num=chord_num, beta=beta, flap_point=flap_point, plot=False)

    pid = 0
    for n1 in range(2):
        for n in range(span_num):
            for m in range(chord_num):
                pid += 1
                if n1 == 0:
                    y1 = geometry['Y-Mesh'][n][m]
                    z1 = geometry['Upper Surface'][n][m]
                    x1 = geometry['X-Mesh'][n][m]
                    model.add_grid(pid, [x1, y1, z1])

                if n1 == 1:
                    y2 = geometry['Y-Mesh'][n][m] + 0.001
                    z2 = geometry['Lower Surface'][n][m]
                    x2 = geometry['X-Mesh'][n][m] + 0.001
                    model.add_grid(pid, [x2, y2, z2])

    eid = 0
    for n1 in range(2):
        for n in range(span_num - 1):
            for m in range(chord_num - 1):
                eid += 1
                if n1 == 0:
                    p1 = m + 1 + n * chord_num
                    t1 = 0.015

                    p2 = m + 2 + n * chord_num
                    t2 = 0.015

                    p3 = m + 2 + (n + 1) * chord_num
                    t3 = 0.015

                    p4 = m + 1 + (n + 1) * chord_num
                    t4 = 0.015

                    model.add_cquad4(eid=eid, pid=pshell_pid, nids=[p1, p2, p3, p4], T1=t1, T2=t2, T3=t3, T4=t4)
                else:
                    p1 = (span_num)*(chord_num) + m + 1 + n * chord_num
                    t1 = 0.015

                    p2 = (span_num)*(chord_num) + m + 2 + n * chord_num
                    t2 = 0.015

                    p3 = (span_num)*(chord_num) + m + 2 + (n + 1) * chord_num
                    t3 = 0.015

                    p4 = (span_num)*(chord_num) + m + 1 + (n + 1) * chord_num
                    t4 = 0.015
                    model.add_cquad4(eid=eid, pid=pshell_pid, nids=[p1, p2, p3, p4], T1=t1, T2=t2, T3=t3, T4=t4)




    # Material
    model.add_mat1(mid=mat1_mid, E=youngs_modulus, rho=material_density, nu=0.3, G=None)

    # Material Property
    model.add_pshell(pid=pshell_pid, mid1=mat1_mid, t=0.015, mid2=mat1_mid)

    # CAERO5
    nspan = chord_num
    nthry = 0
    nthick = aefact_thickness_sid
    x12 = root_chord
    x43 = root_chord * taper

    x1 = geometry['X-Mesh'][0][0]
    y1 = geometry['Y-Mesh'][0][0]
    z1 = geometry['Upper Surface'][0][0]

    x4 = geometry['X-Mesh'][span_num - 1][0]
    y4 = geometry['Y-Mesh'][span_num - 1][0]
    z4 = geometry['Upper Surface'][span_num - 1][0]

    model.add_caero5(eid=caero5_eid, pid=paero5_pid, nspan=nspan, ntheory=nthry, nthick=nthick, p1=[x1, y1, z1],
                     p4=[x4, y4, z4], x12=x12, x43=x43, lspan=None)

    # PAERO5
    model.add_paero5(pid=paero5_pid, caoci=[0.0 for n in range(nspan)], nalpha=1, lalpha=aefact_alpha_sid, nxis=0,
                     ntaus=0, ltaus=0, lxis=0)

    # SPLINE1
    model.add_spline1(eid=spline1_eid, caero=caero5_eid, box1=caero5_eid, box2=110, setg=set1_sid)

    # SET1
    model.add_set1(sid=set1_sid, ids=[n + 1 for n in range(np.size(geometry['X-Mesh']))])

    # EIGRL
    v1 = -10000.0
    v2 = 10000.0
    no_roots = 4
    model.add_eigrl(sid=eigrl_sid, v1=v1, v2=v2, nd=no_roots, msglvl=None, maxset=None, shfscl=None, norm='MASS')

    # MKAERO1
    mkaero_machs = [0.5 * (n + 1) for n in range(8)]
    mkaero_freq = [0.001, 0.002, 0.01, 0.02, 0.6, 0.9, .1, 1.2]
    model.add_mkaero1(machs=mkaero_machs, reduced_freqs=mkaero_freq)

    # AEFACT

    # Thickness
    thickness_integrals = [0.0 for n in range(6)]
    model.add_aefact(sid=aefact_thickness_sid, fractions=thickness_integrals)

    # Alphas
    alphas_machs = []
    for n in range(8):
        alphas_machs.append(mkaero_machs[n])
        alphas_machs.append(0.0)
    model.add_aefact(sid=aefact_alpha_sid, fractions=alphas_machs)

    # AERO
    model.add_aero(velocity=None, cref=span, rho_ref=1.0, sym_xz=1)

    # FLUTTER
    model.add_flutter(sid=flutter_sid, method='PK', density=flfact_density_sid, mach=flfact_mach_sid,
                      reduced_freq_velocity=flfact_velocity, nvalue=no_roots)

    # FLFACT
    density_factor = [rho_input]
    model.add_flfact(sid=flfact_density_sid, factors=density_factor)

    velocity_factor = [10.0, 'THRU', 10000.0, 200]
    model.add_flfact(sid=flfact_velocity, factors=velocity_factor)

    mach_factor = [mach_input]
    model.add_flfact(sid=flfact_mach_sid, factors=mach_factor)

    # SPC1
    model.add_spc1(conid=spc_sid, components='123456', nodes=[n + 1 for n in range(chord_num)])
    model.write_bdf(bdf_card_name)

    return geometry


def run_nastran(plot=False):
    # Surface Pro
    executable_path = str("C:\\Program Files\\MSC.Software\\NaPa_SE\\20211\\Nastran\\bin\\nastran.exe")
    bdf_path = "C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3" + \
               "\\nastran_files\\3d_6dof_card.bdf"
    os.chdir(
        "C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3\\nastran_files")

    # HP
    # executable_path = "C:\\Program Files\\MSC.Software\\NaPa_SE\\20221\\Nastran\\bin\\nastran.exe"
    # bdf_path = "C:\\Users\\thoma\\Documents\\Honours-Thesis\\Sim_3\\nastran_files\\3d_6dof_card.bdf"
    # os.chdir("C:\\Users\\thoma\\Documents\\Honours-Thesis\\Sim_3\\nastran_files")

    os.remove('3d_6dof_card.f04')
    os.remove('3d_6dof_card.f06')
    os.remove('3d_6dof_card.log')
    subprocess.run([executable_path, bdf_path])
    # os.chdir("C:\\Users\\thoma\\Documents\\Honours-Thesis\\Sim_3")
    os.chdir("C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3")


def read_f06_file(filename):
    fid = open(filename, 'r')
    file_lines = fid.readlines()
    flutter_results = []
    for n in range(len(file_lines)):
        line = file_lines[n]

        if 'FLUTTER  SUMMARY' in line:
            results = extract_flutter_results(filename, n + 7)
            flutter_results.append(results)
    return flutter_results


def extract_flutter_results(filename, start_line):
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


def find_flutter(flutter_res):
    for m in range(len(flutter_res)):
        velocity = list(flutter_res[m]['Velocity'])
        eig = flutter_res[m]['Real Eigenvalue']
        check = 0
        for n in range(len(velocity)):
            if eig[n] == 0:
                vf = velocity[n]
                check = 1
                break
            elif eig[n] > 0 and n > 0:
                vf = velocity[n - 1] + (velocity[n] - velocity[n - 1]) / (eig[n] - eig[n - 1]) * (-eig[n])
                check = 1
                break
        if check:
            break

    if 'vf' not in locals():
        vf = None

    return vf


def barometric_formula(height):
    p0 = 101325.0
    # rho0 = 1.125
    temp0 = 273+15.0
    g0 = 9.81
    h0 = 8500.0
    R = 287

    p = p0*np.exp((-g0*(height-h0))/(R * temp0))
    rho = density(height)
    temp = p/(rho*R)
    return temp, rho, p


def density(h: float):
    rho0 = 1.225
    hs = 8500
    rho = rho0 * np.exp(-h / hs)
    return rho

# def temperature_calculation(height, density):

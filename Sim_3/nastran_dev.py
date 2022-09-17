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


# # Script Functions
# def read_sol144_f06_file(filename):
#     fid = open(filename, 'r')
#     file_lines = fid.readlines()
#     for n in range(len(file_lines)):
#         if file_lines[n]



def main():
    bdf_filename = 'nastran_files_sol144/dev_input_card.bdf'

    pshell_pid = 202
    paero5_pid = 301

    mat1_mid = 101

    spc_sid = 101
    aefact_thickness_sid = 201
    aefact_alpha_sid = 301
    set1_sid = 401
    trim_sid = 501

    caero5_eid = 101
    spline1_eid = 201

    model = BDF()
    model.sol = 144

    case_control_list = [
        'ECHO=NONE',
        'AEROF=ALL',
        'APRESSURE=ALL',
        'SPC=' + str(spc_sid),
        'FORCE=NONE',
        'STRESS=NONE',
        'DISP=NONE',
        'TRIM=' + str(trim_sid)
    ]

    case_ctrl = CaseControlDeck(case_control_list)
    model.case_control_deck = case_ctrl

    # Geometry
    span_num = 10
    chord_num = 15
    root_chord = float(.1)
    taper = float(0.5)
    span = 1.0
    beta = np.deg2rad(0)
    flap_point = 0.3
    sweep = 0.0
    foil = '2412'
    geometry = wing(foil=foil, semi_span=span, root_chord=root_chord, taper=taper, sweep=sweep, num=span_num,
                    chord_num=chord_num, beta=beta, flap_point=flap_point, plot=False)

    pid = 0
    for n in range(span_num):
        for m in range(chord_num):
            pid += 1

            y = geometry['Y-Mesh'][n][m]
            z = geometry['Upper Surface'][n][m] - geometry['Lower Surface'][n][m]
            x = geometry['X-Mesh'][n][m]
            # z = 0.0
            model.add_grid(pid, [x, y, z])

    eid = 0
    eid_top = 0

    for n in range(span_num - 1):
        for m in range(chord_num - 1):
            eid += 1
            p1 = m + 1 + n * chord_num
            t1 = 0.015  # (geometry['Upper Surface'][n][m] + geometry['Lower Surface'][n][m])/2

            p2 = m + 2 + n * chord_num
            t2 = 0.015  # (geometry['Upper Surface'][n][m+1] + geometry['Lower Surface'][n][m+1])/2

            p3 = m + 2 + (n + 1) * chord_num
            t3 = 0.015  # (geometry['Upper Surface'][n+1][m+1] + geometry['Lower Surface'][n+1][m+1])/2

            p4 = m + 1 + (n + 1) * chord_num
            t4 = 0.015  # (geometry['Upper Surface'][n+1][m] + geometry['Lower Surface'][n+1][m])/2

            model.add_cquad4(eid=eid, pid=pshell_pid, nids=[p1, p2, p3, p4], T1=t1, T2=t2, T3=t3, T4=t4)

    # Material
    youngs_modulus = 77e9
    material_density = 2700.0
    model.add_mat1(mid=mat1_mid, E=youngs_modulus, rho=material_density, nu=0.3, G=None)

    # Material Property
    model.add_pshell(pid=pshell_pid, mid1=mat1_mid, t=0.015, mid2=mat1_mid)

    # AEROS
    area = span * (taper * root_chord / 2 + root_chord / 2)
    model.add_aeros(cref=root_chord, bref=span, sref=area, sym_xz=1, sym_xy=0)

    # CAERO5
    nspan = chord_num
    nthry = 0
    nthick = aefact_thickness_sid
    x12 = root_chord
    x43 = root_chord * taper

    x1 = geometry['X-Mesh'][0][0]
    y1 = geometry['Y-Mesh'][0][0]
    z1 = 0.0

    x4 = geometry['X-Mesh'][span_num - 1][0]
    y4 = geometry['Y-Mesh'][span_num - 1][0]
    z4 = 0.0

    model.add_caero1(eid=caero5_eid, pid=paero5_pid, igroup=1, cp=0, nspan=nspan, nchord=chord_num, lspan=None,
                     lchord=None, p1=[x1, y1, z1], p4=[x4, y4, z4], x12=x12, x43=x43)


    # PAERO5
    model.add_paero1(pid=paero5_pid)

    # SPLINE1
    model.add_spline1(eid=spline1_eid, caero=caero5_eid, box1=caero5_eid, box2=110, setg=set1_sid)

    # SET1
    model.add_set1(sid=set1_sid, ids=[n + 1 for n in range(np.size(geometry['X-Mesh']))])

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

    model.add_param('BAILOUT', [-1])

    aestat_id = 732
    model.add_aestat(aestat_id, label='ANGLEA')

    model.add_trim(sid=trim_sid, mach=200 / 343, q=0.5 * 1.225 * 200 ** 2, aeqr=0.0, labels=['ANGLEA'], uxs=[1.0])
    # # AERO
    # model.add_aero(velocity=200.0, cref=span, rho_ref=1.0, sym_xz=1)

    model.write_bdf(bdf_filename)

    # Surface Pro
    executable_path = str("C:\\Program Files\\MSC.Software\\NaPa_SE\\20211\\Nastran\\bin\\nastran.exe")
    bdf_path = "C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3" + \
               "\\nastran_files_sol144\\dev_input_card.bdf"
    os.chdir(
        "C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3\\nastran_files_sol144")

    # HP
    # executable_path = "C:\\Program Files\\MSC.Software\\NaPa_SE\\20221\\Nastran\\bin\\nastran.exe"
    # bdf_path = "C:\\Users\\thoma\\Documents\\Honours-Thesis\\Sim_3\\nastran_files\\3d_6dof_card.bdf"
    # os.chdir("C:\\Users\\thoma\\Documents\\Honours-Thesis\\Sim_3\\nastran_files")

    os.remove('dev_input_card.f04')
    os.remove('dev_input_card.f06')
    os.remove('dev_input_card.log')
    subprocess.run([executable_path, bdf_path])
    # os.chdir("C:\\Users\\thoma\\Documents\\Honours-Thesis\\Sim_3")
    os.chdir("C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3")


if __name__ == '__main__':
    main()

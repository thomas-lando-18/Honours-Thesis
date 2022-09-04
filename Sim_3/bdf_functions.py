# Imports
import numpy as np
import os
import subprocess
from pyNastran.bdf.bdf import BDF, CaseControlDeck
from pyNastran.f06.parse_flutter import plot_flutter_f06
from pyNastran.f06.parse_flutter import make_flutter_response
from pyNastran.f06.flutter_response import FlutterResponse
from wing_model.wing_build import main as wing

# Constants
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
shear_modulus = youngs_modulus/(2*(1+2*poissons_ratio))
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
span_num = 5
chord_num = 15
root_chord = float(1)
taper = float(0.5)
span = 1.0
geometry = wing(foil='0104', semi_span=span, root_chord=root_chord, taper=taper, sweep=-10, num=span_num,
                chord_num=chord_num, plot=False)

pid = 0
for n in range(span_num):
    for m in range(chord_num):
        pid += 1
        x = geometry['X-Mesh'][n][m]
        y = geometry['Y-Mesh'][n][m]
        z = geometry['Upper Surface'][n][m] - geometry['Lower Surface'][n][m]
        model.add_grid(pid, [x, y, z])

eid = 0
for n in range(span_num-1):
    for m in range(chord_num-1):
        eid += 1

        p1 = m + 1 + n * chord_num
        t1 = 0.015  # geometry['Upper Surface'][n][m] - geometry['Lower Surface'][n][m]

        p2 = m + 2 + n * chord_num
        t2 = 0.015  # geometry['Upper Surface'][n][m+1] - geometry['Lower Surface'][n][m+1]

        p3 = m + 2 + (n+1) * chord_num
        t3 = .015  # geometry['Upper Surface'][n+1][m+1] - geometry['Lower Surface'][n+1][m+1]

        p4 = m + 1 + (n+1) * chord_num
        t4 = 0.015  # geometry['Upper Surface'][n+1][m] - geometry['Lower Surface'][n+1][m]

        model.add_cquad4(eid=eid, pid=pshell_pid, nids=[p1, p2, p3, p4], T1=t1, T2=t2, T3=t3, T4=t4)

# Material
# model.add_mat1(mid=mat1_mid, E=youngs_modulus, G=shear_modulus, rho=material_density, nu=0.3, ge=damping_coef)
model.add_mat1(mid=mat1_mid, E=8.108e10, nu=0.1219, rho=1521.61, G=None)
# Material Property
model.add_pshell(pid=pshell_pid, mid1=mat1_mid, t=0.015)

# CAERO5
nspan = chord_num
nthry = 0
nthick = aefact_thickness_sid
x12 = root_chord
x43 = root_chord * taper

x1 = geometry['X-Mesh'][0][0]
y1 = geometry['Y-Mesh'][0][0]
z1 = 0.0

x4 = geometry['X-Mesh'][span_num-1][0]
y4 = geometry['Y-Mesh'][span_num-1][0]
z4 = 0.0

model.add_caero5(eid=caero5_eid, pid=paero5_pid, nspan=nspan, ntheory=nthry, nthick=nthick, p1=[x1, y1, z1],
                 p4=[x4, y4, z4], x12=x12, x43=x43, lspan=None)

# PAERO5
model.add_paero5(pid=paero5_pid, caoci=[0.0 for n in range(nspan)], nalpha=1, lalpha=aefact_alpha_sid, nxis=0,
                 ntaus=0, ltaus=0, lxis=0)

# SPLINE1
model.add_spline1(eid=spline1_eid, caero=caero5_eid, box1=caero5_eid, box2=110, setg=set1_sid)

# SET1
model.add_set1(sid=set1_sid, ids=[n+1 for n in range(np.size(geometry['X-Mesh']))])

# EIGRL
v1 = -10000.0
v2 = 10000.0
no_roots = 4
model.add_eigrl(sid=eigrl_sid, v1=v1, v2=v2, nd=no_roots, msglvl=None, maxset=None, shfscl=None, norm='MASS')

# MKAERO1
mkaero_machs = [0.5*(n+1) for n in range(8)]
mkaero_freq = [0.5, 0.8, 1.0, 1.2, 1.3, 1.5, 2.1, 2.3]
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
density_factor = [0.001]
model.add_flfact(sid=flfact_density_sid, factors=density_factor)

velocity_factor = [10.0, 'THRU', 5000.0, 200]
model.add_flfact(sid=flfact_velocity, factors=velocity_factor)

mach_factor = [1.0]
model.add_flfact(sid=flfact_mach_sid, factors=mach_factor)

# SPC1
model.add_spc1(conid=spc_sid, components='123456', nodes=[n+1 for n in range(chord_num)])

model.write_bdf(bdf_card_name)

executable_path = str("C:\\Program Files\\MSC.Software\\NaPa_SE\\20211\\Nastran\\bin\\nastran.exe")
bdf_path = "C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3" + \
           "\\nastran_files\\3d_6dof_card.bdf"

os.chdir("C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3\\nastran_files")
os.remove('3d_6dof_card.f04')
os.remove('3d_6dof_card.f06')
os.remove('3d_6dof_card.log')
subprocess.run([executable_path, bdf_path])



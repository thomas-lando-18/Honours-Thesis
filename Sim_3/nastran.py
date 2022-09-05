import os
import subprocess
import pyNastran.utils.nastran_utils
from pyNastran.bdf.bdf import BDF, CaseControlDeck
from pyNastran.f06.parse_flutter import make_flutter_plots, plot_flutter_f06
from wing_model.wing_build import main as wing
import numpy as np
from sim_functions import*
import pprint
import sys

# BDF Functions

model = BDF()
CaseControlDeck(model.case_control_lines)
# Case Control
model.sol = 145
case_ctrl = CaseControlDeck([
    'ECHO=NONE',
    'FMETHOD=1',
    'METHOD=1',
    'SPC=1',
    'RESVEC=NO',
    'DISP=ALL'
])
model.case_control_deck = case_ctrl

# Add Geometry   dw
span_num = 5
chord_num = 10
root_chord = float(1)
taper = float(0.5)
span = 1.0
geometry = wing(foil='2412', semi_span=span, root_chord=root_chord, taper=taper, sweep=-10, num=span_num,
                chord_num=chord_num, plot=True)

geometry_cards(model, geometry, chord_num=chord_num)
aerodynamic_cards(model=model, geometry=geometry, span_num=span_num, root_chord=root_chord, taper=taper, span=span)

# Required Cards
# model.add_eigrl(sid=1, v1=-5e3, v2=5e3, norm='MASS', nd=6)
#
# model.add_aero(acsid=0, velocity=None, cref=1.0, rho_ref=1.0)
#
#
#
# model.add_flutter(sid=3, method='PK', density=420693, mach=420694, reduced_freq_velocity=420695)
#
# model.add_flfact(sid=420693, factors=list(np.linspace(1.5, 0.02, num=10)))
# model.add_flfact(sid=420694, factors=list(np.linspace(0.3, 1.5, num=10)))
# model.add_flfact(sid=420695, factors=list(np.linspace(10, 1000, num=100)))
#
# # model.add_mkaero2(machs=[0.8, 1.0, 1.2, 1.4], reduced_freqs=[0.3, 10.0, 43.0, 100.0])
#
# model.add_spc1(conid=1, nodes=[n+1 for n in range(chord_num)], components='123456')

# model.add_spline1(eid=420696, caero=101, box1=11, box2=17, dz=0, setg=420697)

# model.add_set1(sid=420697, ids=[n+1 for n in range(np.size(geometry['X-Mesh']))])



model.write_bdf('nastran_files/3d_6dof_card.bdf')

fid = open('nastran_files/3d_6dof_card.bdf', 'a')
fid.write('ENDDATA')
fid.close()
# executable_path = str("C:\\Program Files\\MSC.Software\\NaPa_SE\\20211\\Nastran\\bin\\nastran.exe")
# bdf_path = "C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3\\nastran_files\\3d_6dof_card.bdf"
# # bdf_path = 'nastran_files/3d_6dof_card.bdf'
#
# os.chdir("C:\\Users\\thoma\\OneDrive\\Documents\\University Work\\Fourth Year\\Honours-Thesis\\Sim_3\\nastran_files")
# os.remove('3d_6dof_card.f04')
# os.remove('3d_6dof_card.f06')
# os.remove('3d_6dof_card.log')
# subprocess.run([executable_path, bdf_path])

# plot_flutter_f06('bluewrennastran.f06.1', plot=True, plot_vg_vf=True, plot_root_locus=True)


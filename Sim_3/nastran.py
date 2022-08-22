from pyNastran.bdf.bdf import BDF, CaseControlDeck
from pyNastran.f06.parse_flutter import make_flutter_plots

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



# Required Cards
model.add_eigrl(sid=1, v1=-5e10, v2=5e10)

model.add_aero(acsid=3, velocity=1.4e4, cref=100, rho_ref=0.0001, sym_xy=-1, sym_xz=1)

model.add_flfact(sid=2, factors=[10, 50, 75, 100, 150, 200])

model.add_flutter(sid=3, method='PK', density=1, mach=1, reduced_freq_velocity=100)

model.add_mkaero2(machs=[0.8, 1, 1.2, 1.4], reduced_freqs=[80, 100, 110, 120])

# Additional Cards
# To cover both subsonic and supersonic regions and give accuracy in the transonic regions, use piston theory
# model.add_paero5()

# model.add_caero5()
#
# model.add_aefact()
#
# model.add_set1()
#
# model.add_spline1()

model.write_bdf('3d_6dof_card.bdf')


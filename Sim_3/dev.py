import pprint
from sim_functions import*


f = read_f06_file('nastran_files/3d_6dof_card.f06')
vf = find_flutter(f)
print(vf)

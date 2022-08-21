from simulation_tools import*

velocity = 50
height = 5e3
a = -0.5
c = 0.5
b = 1

A, B, C, D, E, F = iterate_frequency(v=velocity, w=0, h=height, a=a, c=c, b=b)

top_left = np.linalg.inv(A-D)*(E-B)
top_right = np.linalg.inv(A-D)*(F-C)
bot_left = np.identity(3)
bot_right = np.zeros([3, 3])
System = [[top_left, top_right], [bot_left, bot_right]]
eigenvalues, eigenvectors = np.linalg.eig(System)
print(eigenvalues)

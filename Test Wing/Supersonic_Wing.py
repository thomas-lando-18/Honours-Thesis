# Script for building a wing mesh

# Import Packages
from read_data import extract_uiuc_data
import matplotlib.pyplot as plt
import numpy as np

# filename = "UIUC Data/n0011sc.dat.txt"
filename = "UIUC Data/whitcomb.dat"
top_surface, bottom_surface, middle_surface = extract_uiuc_data(filename)
for n in range(len(top_surface)):
    plt.scatter(top_surface[n][0], top_surface[n][1], color='blue')
    plt.scatter(bottom_surface[n][0], bottom_surface[n][1], color='blue')
    plt.scatter(middle_surface[n][0], middle_surface[n][1], color='red')
plt.grid()
plt.axis('equal')
plt.show()

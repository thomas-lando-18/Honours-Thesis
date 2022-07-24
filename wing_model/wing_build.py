# Imports
import numpy as np
import matplotlib.pyplot as plt
from naca45 import*


# Functions
def main(semi_span=0.15, root_chord=0.30, taper=1.0, sweep=0, num=10, chord_num=10):
    """
    Completes the 3D model of the wing and calculates the mass properties.
    :param semi_span: semi span of wing (m)
    :param root_chord: root chord of wing (m)
    :param taper: Taper ratio
    :param sweep: quarter-chord sweep angle (rad)
    :param num: number of panels across the wingspan
    :param chord_num: number of panels across the chord
    :return: points in x-y-z frame of wing model and a dictionary of mass properties
    """

    # Create rectangular wing
    spanwise_x = np.linspace(0, semi_span, num=num)
    chordwise_x = np.linspace(0, root_chord, num=chord_num)
    taper_vector = np.linspace(1, taper, num=num)
    print(taper_vector)
    x_mesh, y_mesh = np.meshgrid(chordwise_x, spanwise_x)

# Bring values back to midchord
    x_mesh -= root_chord/2

    # Add Taper
    for n in range(num):
        chord = root_chord * taper_vector[n]
        x_mesh[n][:] = x_mesh[n][:] * chord

    x_mesh += root_chord/2

    # add sweep
    x_mesh -= root_chord/4

    for n in range(num):
        sweep_shift = spanwise_x[n] * np.sin(sweep)
        x_mesh[n][:] += sweep_shift

    x_mesh += root_chord/4
    z_mesh = np.zeros([chord_num, num])
    upper_mesh = x_mesh
    lower_mesh = x_mesh

    # Add Foil


    fig = plt.figure(2)
    ax = fig.add_subplot(projection='3d')
    ax.scatter(x_mesh, y_mesh, z_mesh)
    plt.grid()

    plt.show()


if __name__ == '__main__':
    main(taper=0.5, sweep=np.deg2rad(20))

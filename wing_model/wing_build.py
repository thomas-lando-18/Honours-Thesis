# Imports
import numpy as np
import matplotlib.pyplot as plt
from wing_model.naca45 import *
import pprint


# Functions
def main(foil='2412', semi_span=0.15, root_chord=0.30, taper=1.0, sweep=0.0, num=5, chord_num=10,
         beta=0.0, flap_point=0.2, plot=True):
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
    x_mesh, y_mesh = np.meshgrid(chordwise_x, spanwise_x)

    # Create Foil
    upper = np.zeros([num, chord_num])
    lower = np.zeros([num, chord_num])

    # Bring values back to midchord
    x_mesh -= root_chord / 2

    # Add Taper and foil
    for n in range(num):
        chord = root_chord * taper_vector[n]
        x_mesh[n][:] = x_mesh[n][:] * chord

    x_mesh += root_chord / 2

    # add sweep
    x_mesh -= root_chord / 4

    for n in range(num):
        sweep_shift = spanwise_x[n] * np.sin(sweep)
        x_mesh[n][:] += sweep_shift

    x_mesh += root_chord / 4

    # Unpack Foil Shape
    m = int(foil[0])
    # print(m)
    p = int(foil[1])
    # print(p)
    t = int(foil[2]) * 10 + int(foil[3])
    # print(t)

    # add foil
    area_vector = []
    for n in range(num):
        upper[n][:], lower[n][:], temp, temp1 = naca_4_digit(m=m, p=p, xx=t, num=chord_num,
                                                             chord=root_chord * taper_vector[n],
                                                             beta=beta, flap_length=flap_point)
        # area_vector.append(area)

    if plot:
        fig = plt.figure(2)
        ax = fig.add_subplot(projection='3d')
        ax.scatter(x_mesh, y_mesh, upper, label='Upper Surface')
        ax.scatter(x_mesh, y_mesh, lower, label='Lower Surface')
        ax.axes.set_zlim3d(bottom=-0.5, top=0.5)
        plt.xlabel('x (m)', fontsize=14)
        plt.ylabel('y (m)', fontsize=14)
        ax.set_zlabel('z(m)', fontsize=14)

        plt.legend()
        plt.grid()
        plt.show()

    # Create Return Variable
    output = {"X-Mesh": x_mesh,
              "Y-Mesh": y_mesh,
              "Upper Surface": upper,
              "Lower Surface": lower,
              "Wing Properties": {"Root Chord": root_chord,
                                  "Taper": taper,
                                  "Span Num": num,
                                  "Chord Num": chord_num,
                                  "Span": semi_span,
                                  "Flap Point": flap_point}}

    return output


# if __name__ == '__main__':
#     base_foil = '0110'
#     base_taper = 0.4
#     base_span = 0.6
#     base_sweep = 0.0
#     base_root = 0.3
#     output = main(foil=base_foil, root_chord=base_root, sweep=base_sweep, taper=base_taper, chord_num=15, num=15,
#                   plot=True, semi_span=base_span, beta=np.deg2rad(0.0), flap_point=0.4)



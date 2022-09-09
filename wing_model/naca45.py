# Imports
import numpy as np
import matplotlib.pyplot as plt


def naca_4_digit(m=2, p=4, xx=12, num=10, chord=1, beta=0.0, flap_length=0.2):
    """
    Creates a NACA 4 digit foil in the designated number of points
    :param m: First Digit
    :param p: Second Digit
    :param xx: Final Two Digits
    :param num: Number of points to be generated
    :return: 2 x num matrix of points
    """

    # Convert values into fractions
    m = m / 100
    p = p / 10
    xx = xx / 100

    x = np.linspace(0, 1, num=num)

    # Create Camber line values
    yc = []
    camber = 0
    for n in range(len(x)):
        if x[n] <= p:
            camber = m / p ** 2 * (2 * p * x[n] - x[n] ** 2)
        elif x[n] > p:
            camber = m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x[n] - x[n] ** 2)

        yc.append(camber)

    # Create Thickness Lines
    yt = []
    for n in range(len(x)):
        thickness = xx / 0.2 * (
                0.2969 * np.sqrt(x[n]) - 0.1260 * x[n] - 0.3516 * x[n] ** 2 + 0.2843 * x[n] ** 3 - 0.1015 * x[
            n] ** 4)
        yt.append(thickness)

    # Create upper and lower surface values
    xu = []
    yu = []
    xl = []
    yl = []
    theta = 0
    for n in range(len(x)):
        if x[n] <= p:

            dyc_dx = 2 * m / p * (1 - x[n] / p)
            theta = np.arctan(dyc_dx)

            xu.append(x[n] - yt[n] * np.sin(theta))
            yu.append(yc[n] + yt[n] * np.cos(theta))
            xl.append(x[n] + yt[n] * np.sin(theta))
            yl.append(yc[n] - yt[n] * np.cos(theta))
        else:

            dyc_dx = 2 * m * p / (1 - p) ** 2 * (p - x[n])
            theta = np.arctan(dyc_dx)

            xu.append(x[n] - yt[n] * np.sin(theta))
            yu.append(yc[n] + yt[n] * np.cos(theta))
            xl.append(x[n] + yt[n] * np.sin(theta))
            yl.append(yc[n] - yt[n] * np.cos(theta))

    for n in range(len(x)):
        if x[n] >= 1-flap_length:
            xu[n] -= 1-flap_length
            xl[n] -= 1-flap_length
            xu[n] = xu[n]*np.cos(beta) - yu[n]*np.sin(beta)
            yu[n] = xu[n]*np.sin(beta) + yu[n]*np.cos(beta)

            xl[n] = xl[n] * np.cos(beta) - yl[n] * np.sin(beta)
            yl[n] = xl[n] * np.sin(beta) + yl[n] * np.cos(beta)

            xu[n] += 1 - flap_length
            xl[n] += 1 - flap_length

    # Adjust for chord value
    xu = np.multiply(xu, chord)
    xl = np.multiply(xl, chord)
    yu = np.multiply(yu, chord)
    yl = np.multiply(yl, chord)

    return yu, yl, xu, xl


def naca_5_digit(cl_int=2, p=4, q=0, xx=12, num=10, chord=1):
    """
    This function returns a set of points for a naca 5 digit foil
    :param cl_int: First digit
    :param p: second digit
    :param q: third digit
    :param xx: final two digits
    :param num: number of points
    :param chord: chord length
    :return: matrix of x y values for the upper and lower surface
    """
    x = np.linspace(0, 1, num=num)
    if q == 0:
        m = [0.05, 0.1, 0.15, 0.2, 0.25]
        m = float(m[p - 1])
        r = [0.0580, 0.126, 0.2025, 0.29, 0.391]
        r = r[p - 1]
        k1 = [361.4, 51.64, 15.957, 6.543, 3.23]
        k1 = k1[p - 1]
        t = xx / 100

        yc = []
        for n in range(len(x)):
            if x[n] <= m:
                camber = k1 / 6 * (x[n] ** 3 - 3 * m * x[n] ** 2 + m ** 2 * (3 - m) * x[n])
                yc.append(camber)
            elif x[n] > m:
                camber = k1 * m ** 3 / 6 * (1 - x[n])
                yc.append(camber)

        # Create Thickness Lines
        yt = []
        for n in range(len(x)):
            thickness = t / 0.2 * (
                    0.2969 * np.sqrt(x[n]) - 0.1260 * x[n] - 0.3516 * x[n] ** 2 + 0.2843 * x[n] ** 3 - 0.1015 *
                    x[n] ** 4)
            yt.append(thickness)

        # Create upper and lower surface values
        xu = []
        yu = []
        xl = []
        yl = []
        theta = 0
        for n in range(len(x)):
            if x[n] <= p:

                dyc_dx = 2 * m / p * (1 - x[n] / p)
                theta = np.arctan(dyc_dx)

                xu.append(x[n] - yt[n] * np.sin(theta))
                yu.append(yc[n] + yt[n] * np.cos(theta))
                xl.append(x[n] + yt[n] * np.sin(theta))
                yl.append(yc[n] - yt[n] * np.cos(theta))
            else:

                dyc_dx = 2 * m * p / (1 - p) ** 2 * (p - x[n])
                theta = np.arctan(dyc_dx)

                xu.append(x[n] - yt[n] * np.sin(theta))
                yu.append(yc[n] + yt[n] * np.cos(theta))
                xl.append(x[n] + yt[n] * np.sin(theta))
                yl.append(yc[n] - yt[n] * np.cos(theta))

        # Adjust for chord value
        xu = np.multiply(xu, chord)
        xl = np.multiply(xl, chord)
        yu = np.multiply(yu, chord)
        yl = np.multiply(yl, chord)

    return yu, yl


# if __name__ == '__main__':
#     yu, yl, xu, xl = naca_4_digit(beta=np.deg2rad(-20))
#     plt.figure(1)
#     plt.scatter(xu, yu)
#     plt.scatter(xl, yl)
#     plt.grid()
#     plt.axis('equal')
#     plt.show()

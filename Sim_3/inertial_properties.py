# This Script contains functions used in caluclating the properties of the wing

# Imports
import numpy as np


def surface_area(geometry):
    """
    Uses the shoelace formula to estimate the surface area of the wing
    :param geometry: the JSON containing the mesh points
    :return: the surface area in m^2
    """

    # Root Foil
    area = 0
    for n in range(geometry["Wing Properties"]["Span Num"]-1):
        area_addition = 0.5 * (geometry['Upper Surface'][0][n] + geometry['Upper Surface'][0][n + 1]) * \
                        (geometry['X-Mesh'][0][n] - geometry['X-Mesh'][0][n + 1])
        area += area_addition

        area_addition = 0.5 * (geometry['Upper Surface'][geometry["Wing Properties"]["Span Num"]-1][n] +
                               geometry['Upper Surface'][geometry["Wing Properties"]["Span Num"]-1][n + 1]) * \
                        (geometry['X-Mesh'][geometry["Wing Properties"]["Span Num"]-1][n] -
                         geometry['X-Mesh'][geometry["Wing Properties"]["Span Num"]-1][n + 1])
        area += area_addition

        area_addition = 0.5 * (geometry['Lower Surface'][0][n] + geometry['Lower Surface'][0][n + 1]) * \
                        (geometry['X-Mesh'][0][n] - geometry['X-Mesh'][0][n + 1])
        area += area_addition

        area_addition = 0.5 * (geometry['Lower Surface'][geometry["Wing Properties"]["Span Num"] - 1][n] +
                               geometry['Lower Surface'][geometry["Wing Properties"]["Span Num"] - 1][n + 1]) * \
                        (geometry['X-Mesh'][geometry["Wing Properties"]["Span Num"] - 1][n] -
                         geometry['X-Mesh'][geometry["Wing Properties"]["Span Num"] - 1][n + 1])
        area += area_addition

    area += 0.5 * geometry["Wing Properties"]["Root Chord"] * (1 + geometry["Wing Properties"]["Taper"]) * \
            geometry["Wing Properties"]["Span"]

    return area


def get_volume_and_mass(area):
    volume = area * 0.015
    mass = volume * 2700
    return volume, mass


def panel_inertial_calculations(geometry, rho_air):
    volume, mass = get_volume_and_mass(surface_area(geometry))

    # Loop through each panel
    I_a = 0
    I_b = 0
    S_a = 0
    S_b = 0
    for n in range(geometry["Wing Properties"]["Span Num"] - 1):
        for m in range(geometry["Wing Properties"]["Chord Num"]-1):
            x1 = geometry["X-Mesh"][n][m]
            y1 = geometry["Upper Surface"][n][m]

            x2 = geometry["X-Mesh"][n][m + 1]
            y2 = geometry["Upper Surface"][n][m + 1]

            x3 = geometry["X-Mesh"][n + 1][m + 1]
            y3 = geometry["Upper Surface"][n + 1][m + 1]

            x4 = geometry["X-Mesh"][n + 1][m]
            y4 = geometry["Upper Surface"][n + 1][m]

            dx = x2 - x1
            dy = y3 - y1

            xc = x1 + dx / 2
            yc = y1 + dy / 2

            alpha = np.arctan2(dy, dx)
            mass_panel = 2700 * dx * dy * 0.015

            S_a += mass_panel * (geometry["Wing Properties"]["Root Chord"] - np.sqrt(xc ** 2 + yc ** 2))
            S_b += mass_panel * (geometry["Wing Properties"]["Root Chord"] * (1 - geometry["Wing Properties"]["Flap Point"])
                           - np.sqrt(xc ** 2 + yc ** 2))

            I_a += 1 / 12 * mass_panel * (0.015 ** 2 + dx ** 2) + \
                   mass_panel * (geometry["Wing Properties"]["Root Chord"] - np.sqrt(xc ** 2 + yc ** 2)) ** 2
            I_b += 1 / 12 * mass_panel * (0.015**2 + dx ** 2) + mass_panel * (geometry["Wing Properties"]["Root Chord"] *
                                        (1 - geometry["Wing Properties"]["Flap Point"])- np.sqrt(xc ** 2 + yc ** 2))

    kappa = np.pi*rho_air * geometry["Wing Properties"]["Span"]**2 / mass
    r_a = np.sqrt(I_a/(mass*geometry["Wing Properties"]["Span"]**2))
    r_b = np.sqrt(I_b/(mass*geometry["Wing Properties"]["Span"]**2))

    x_a = S_a/(mass*geometry["Wing Properties"]["Span"])
    x_b = S_b/(mass*geometry["Wing Properties"]["Span"])

    w_a = 2.0
    w_b = 10.0
    w_h = 5.0

    C_a = w_a**2 * I_a
    C_b = w_b**2 * I_b
    C_h = w_h**2 * mass
    inertial_properties = {"S_a": S_a,
                           "S_b": S_b,
                           "mass": mass,
                           "volume": volume,
                           "I_a": I_a,
                           "I_b": I_b,
                           "r_a": r_a,
                           "r_b": r_b,
                           "x_a": x_a,
                           "x_b": x_b,
                           "kappa": kappa,
                           "C_a": C_a,
                           "C_b": C_b,
                           "C_h": C_h}
    return inertial_properties

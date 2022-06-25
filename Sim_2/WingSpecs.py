# contains class used to design the trapezoidal wing used in all simulations.

# Import packages
import numpy as np


# Build Functions
def trap_fin_build(chord, le_l, flap_l, t_max, beta):
    le_point = [0, 0]
    te_point = [(chord - flap_l) + flap_l * np.cos(beta), flap_l * np.sin(beta)]

    if beta <= 0:
        top_surface = [[le_l, t_max / 2], [chord - flap_l, t_max / 2],
                       [chord - flap_l + 0.0001 - t_max * np.cos(np.pi / 2 - beta), t_max / 2]]
        bottom_surface = [[le_l, -t_max / 2], [chord - flap_l, -t_max / 2], [chord - flap_l + 0.0001, -t_max / 2]]
    else:
        top_surface = [[le_l, t_max / 2], [chord - flap_l, t_max / 2],
                       [chord - flap_l + 0.0001, t_max / 2]]
        bottom_surface = [[le_l, -t_max / 2], [chord - flap_l, -t_max / 2],
                          [chord - flap_l + 0.0001 + t_max * np.cos(np.pi / 2 - beta), -t_max / 2]]

    return le_point, te_point, top_surface, bottom_surface


def add_points_leading_edge(le, top, bottom, le_divisions):
    leading_edge_divisions = np.zeros([4, le_divisions])
    leading_edge_divisions[0][:] = np.linspace(le[0], top[0][0], num=le_divisions)
    leading_edge_divisions[1][:] = np.interp(xp=[le[0], top[0][0]], fp=[0, 0], x=leading_edge_divisions[0][:])
    leading_edge_divisions[2][:] = np.interp(xp=[le[0], top[0][0]], fp=[le[0], top[0][1]],
                                             x=leading_edge_divisions[0][:])
    leading_edge_divisions[3][:] = np.interp(xp=[le[0], bottom[0][0]], fp=[le[0], bottom[0][1]],
                                             x=leading_edge_divisions[0][:])
    return leading_edge_divisions


def add_points_midspan(top, max_thickness, mid_divisions):
    midspan_divisions = np.zeros([4, mid_divisions])
    midspan_divisions[0][:] = np.linspace(top[0][0], top[1][0], num=mid_divisions)
    midspan_divisions[1][:] = np.interp(xp=[top[0][0], top[1][0]], fp=[0, 0], x=midspan_divisions[0][:])
    midspan_divisions[2][:] = np.interp(xp=[top[0][0], top[1][0]], fp=[max_thickness / 2, max_thickness / 2],
                                        x=midspan_divisions[0][:])
    midspan_divisions[3][:] = np.interp(xp=[top[0][0], top[1][0]], fp=[-max_thickness / 2, -max_thickness / 2],
                                        x=midspan_divisions[0][:])
    return midspan_divisions


# def add_points_trailing_edge():

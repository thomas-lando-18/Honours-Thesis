# Used to calculate the C(k) function

import scipy.special as sc


def c_function(k):
    if k == 0:
        F = 1
        G = 0
    else:

        j0 = sc.j0(k)
        j1 = sc.j1(k)
        y0 = sc.y0(k)
        y1 = sc.y1(k)

        F = (j1*(j1+y0)+y1*(y1-j0))/((j1+y0)**2+(y1-j0)**2)
        G = -(y1*(j1+y0)-j1*(y1-j0))/((j1+y0)**2+(y1-j0)**2)

    c = complex(F, G)
    return c

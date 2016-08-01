# -*- coding: utf-8 -*-

"""Generate test files for `tecplot_writer.py`."""

import numpy as np


X = 10
Y = 6

radius = np.zeros([X, Y])
u = np.zeros([X, Y, 2])
for i in range(X):
    for j in range(Y):
        radius[i,j] = (i**2 + j**2)**0.5
        u[i,j,0] = 3-j
        u[i,j,1] = i-5

np.savez('npz_test.npz', radius=radius, u=u)

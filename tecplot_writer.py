# -*- coding: utf-8 -*-

"""This is a converter to Tecplot data format. It supports writing 2D and 3D
data aligned with the axes.
"""

import numpy as np

def tecplot_writer(filename, variables, X=[], Y=[], Z=[]):
    """
    X, Y, Z are the lists of xyz coordinates. If not provided, intergers
    from 0 will be used.

    `variables` is a dict of the variables to store with the variable names as
    the keys. Each variable should be 2 or 3 dimensional array using numpy's
    row-major order.

    Check the test function to see how to create input data structure.

    Notice that tecplot format use 'column-major order' as in Fortran, which is
    different from that of Numpy or C.
    """
    if filename[-4:] != '.dat':
        filename += '.dat'

    with open(filename, 'w') as f:
        ## 2D case
        if len(Z) == 0:
            f.write('Variables = "X", "Y"')
            for key in variables.keys():
                f.write(', "' + key + '"')
            f.write('\n\nZone I='+str(len(X))+', J='+str(len(Y))+', F=POINT\n')

            for j in range(len(Y)):
                for i in range(len(X)):
                    f.write(str(X[i]) + ' ' + str(Y[j]))
                    for var in variables.values():
                        f.write(' ' + str(var[i,j]))
                    f.write('\n')

        ## 3D case
        else:
            f.write('Variables = "X", "Y", "Z"')
            for key in variables.keys():
                f.write(', "' + key + '"')
            f.write('\n\nZone I=' + str(len(X)) + ', J=' + str(len(Y)) +
                    ', K=' + str(len(Z)) + ', F=POINT\n')

            for k in range(len(Z)):
                for j in range(len(Y)):
                    for i in range(len(X)):
                        f.write(str(X[i]) + ' ' + str(Y[j]) + ' ' + str(Z[k]))
                        for var in variables.values():
                            f.write(' ' + str(var[i,j,k]))
                        f.write('\n')

def npz2tecplot(input_file, filename=None):
    if filename == None:
        filename = input_file + '_.dat'
    npz = np.load(input_file)
    var_names = npz.keys()
    data = {var: npz[var] for var in var_names}

    ## sometimes the velocity is 3d but the data is actually 2d, so it's quite
    ## tricky to figure out the actual dimension.
    dims = [len(data[var].shape) for var in var_names]
    print('dims', dims)
    if min(dims) == 2:
        dim = 2
    elif len(dims) == 1 and ('u' in var_names[0]):  # only u stored
        dim = 2
    else:
        dim = 3

    xlen, ylen = data[var_names[0]].shape[:2]
    if dim == 3:
        zlen = data[var_names[0]].shape[2]
        tecplot_writer(filename, data, range(xlen), range(ylen), range(zlen))
        return
    else:
        ## handling the 3d arrays (velocity, etc) requires careful work
        if max(dims) == 2:
            tecplot_writer(filename, data, range(xlen), range(ylen))
            return
        else:
            data = {}
            for var in var_names:
                if len(npz[var].shape) == 3:
                    for i in range(npz[var].shape[2]):
                        ## this is very specific to my own custom
                        data[var+str(i)] = npz[var][:,:,i]
                else:
                    data[var] = npz[var]
            tecplot_writer(filename, data, range(xlen), range(ylen))
            return

def test_tecplot_writer():
    if input('Do you wish to create the test files? (y/n)\n') == 'y':
        X = [0, 0.5, 1, 1.5]
        Y = [0, 1, 2]
        Z = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        data2d = np.empty([4,3], dtype=np.float64)
        data3d = np.empty([4,3,6], dtype=np.float64)
        for i in range(4):
            for j in range(3):
                data2d[i,j] = (X[i]**2 + Y[j]**2) ** 0.5
                for k in range(6):
                    data3d[i,j,k] = (X[i]**2 + Y[j]**2 + Z[k]**2) ** 0.5
        tecplot_writer('test2d', {'rad': data2d}, X, Y)
        tecplot_writer('test3d', {'rad': data3d}, X, Y, Z)
    else:
        input('Exiting. Press ENTER to continue.')

def test_npz2tecplot():
    npz2tecplot('npz_test.npz')

if __name__ == "__main__":
    test_npz2tecplot()

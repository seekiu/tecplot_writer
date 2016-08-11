# tecplot_writer

A simple script for writing ASCII data file for the Tecplot.

`tecplot_writer` has the following functions:

1. `tecplot_writer`, which accepts a numpy array and writes it to a tec file.
2. `npz2tecplot`, which reads a `npz` file saved by numpy and writes it to a
   `tec` file.

Notice that this script is a very limited tecplot data writer in terms of
functionality, because it only recognizes 2d or 3d data on regular lattice.
Also the `npz2tecplot` function is created according to my own custom. Although
you can easily adapt it to your own use, too.

**Credit**

The tecplot data format is inspired from [visitusers.org](http://www.visitusers.org/index.php?title=Writing_Tecplot_Using_Python).

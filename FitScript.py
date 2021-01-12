#! /usr/bin/env python
#
#    FitScript.py: a python script to generate (modified) Arrhenius fits to T, k data
#    lightly modified from a script written by Franklin Goldsmith
#    Usage: $ FitScript.py data.txt [options]
#    Specify data file as output from MESS or TAMkin with options 'mess' or 'tamkin'
#    Default input format assumed to be two columns: temperature and rate
#    Default behavior is to print return modified Arrhenius fit
#    Specify 'Arr' as option for two-parameter fit
#    Copyright (C) 2020  Mark E. Fuller
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    Mark E. Fuller: mark.e.fuller@gmx.de


# setup terminal output later:
#    FitScript.py  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################

import sys
import numpy


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


####################################################################################################

data_T0 = 1.0
data_R = 1.987  # cal/mol-K.  Note that PLOG formalism requires Ea in cal/mol-K!
data_N_avo = (
    6.0221415e23  # convert bimolecular rate coefficients from cm^3/sec to cm^3/mol/s
)


command_line = sys.argv[1:]

datafile = command_line[0]

MESS = False
Tamkin = False
TwoFit = False
if len(command_line) > 1:
    for item in command_line[1:]:
        if item == "mess":
            MESS = True
        if item == "tamkin":
            Tamkin = True
        if item == "Arr":
            TwoFit = True

# results = open(datafile,'r')
with open(datafile, "r") as results:
    lines = results.readlines()
# results.close()

local_T = []
local_kfwd = []
# local_krev = []

# there's some header in the file, then columns of data, then more output after
InData = False
NotData = False
for q, line in enumerate(lines):
    if NotData and InData:
        break
    if line == "\n":  # empty line
        NotData = True
    else:
        bits = line.split()
        if is_number(bits[0]):
            NotData = False
            InData = True
            if Tamkin:
                local_T.append(bits[0])
                local_kfwd.append(bits[2])
            else:
                local_T.append(bits[0])
                local_kfwd.append(bits[1])
#    local_krev.append(bits[2])

T = numpy.array(local_T, dtype=numpy.float64)
k_fwd = numpy.array(local_kfwd, dtype=numpy.float64)
# k_rev = numpy.array(local_krev,dtype=numpy.float64)

# Avogadro number not used here since TAMkin output already on mole basis
if Tamkin:  # TAMkin m^3 vs. cm^3
    k_fwd = k_fwd * 1.0e6
    # k_rev = k_rev*1.0e6

# print("Forward rate:")
if TwoFit:
    X = numpy.array([numpy.ones(len(T)), -1.0 / data_R / T], dtype=numpy.float64)
    X = X.transpose()
    theta_fwd = numpy.linalg.lstsq(X, numpy.log(k_fwd), rcond=None)[0]
    A_fwd = numpy.exp(theta_fwd[0])
    n_fwd = 0.0
    Ea_fwd = theta_fwd[1]
    print("%s\t%5.2E    %2.1F\t\t" % (datafile, A_fwd, Ea_fwd))
else:
    X = numpy.array(
        [numpy.ones(len(T)), numpy.log(T / data_T0), -1.0 / data_R / T],
        dtype=numpy.float64,
    )
    X = X.transpose()
    theta_fwd = numpy.linalg.lstsq(X, numpy.log(k_fwd), rcond=None)[0]
    A_fwd = numpy.exp(theta_fwd[0])
    n_fwd = theta_fwd[1]
    Ea_fwd = theta_fwd[2]
    print("%s\t%5.2E    %8.2F    %2.1F\t\t" % (datafile, A_fwd, n_fwd, Ea_fwd))

# return A_fwd, n_fwd, Ea_fwd

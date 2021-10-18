#! /usr/bin/env python
#
#    writemess: a python script to generate MESS input files from g09/g16 output
#    copied from the function g09_to_paper.py written by Franklin Goldsmith
#    added functionality: prompts user for energy, rotor information during write
#    Usage: $ writemess file.log [options]
#    Options: include 'linear' for linear structures; an integer value for the number of hindered rotors
#    Default behavior writes output to terminal; specify 'yes' in optional arguments to write to file
#    Default behavior writes templates for energy and rotors;
#    specify 'interactive' in optional arguments to prompt for file locations to write energy and rotors
#    Copyright (C) 2020 - 2021 Mark E. Fuller
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    Mark E. Fuller: fuller@stossrohr.net


################################################################################

"""
writemess: a python script to generate MESS input files from g09/g16 output
copied from the function g09_to_paper.py written by Franklin Goldsmith
added functionality: prompts user for energy, rotor information during write
"""

import sys
import os

from FileParsers import MagicNo, is_number, get_cartesian, get_energy, get_frequencies, get_rotor

# ------------------------------------------------------------------------------------------------------------------------------------
# BEGIN HERE
# ------------------------------------------------------------------------------------------------------------------------------------
# SPE_ext = '_f12_tz.orca.out' #replaces '.log' on DFT file to get SPE file

command_line = sys.argv[1:]

method = command_line[0]
pwd = os.getcwd()

N_rotor = 0
linear = False
newout = False
prompt = False
if len(command_line) > 1:
    for item in command_line[1:]:
        if item == "linear":
            linear = True
        elif is_number(item):
            N_rotor = int(item)
        elif item == "yes":
            newout = True
        elif item == "interactive":
            prompt = True
        else:
            print(f"Command line argument not recognized: {item}")

# PART 1: GET THE GEOMETRIES
N_atoms, geom, multiplicity = get_cartesian(method)
geom = geom.replace("\n", "\n\t")  # add tabs to reformat
real, imaginary, freq = get_frequencies(method, linear, N_rotor)

# check that the freq. count is correct
N_counted = len(imaginary) + len(real)
if linear:
    N_total = 3 * N_atoms - 5
else:
    N_total = 3 * N_atoms - 6

if N_counted != N_total:
    print(
        f"Warning! Frequency count in file ({N_counted:d}) differs from expected {N_total:d}"
    )

if linear:
    N_freq = 3 * N_atoms - 5 - len(imaginary) - N_rotor
else:
    N_freq = 3 * N_atoms - 6 - len(imaginary) - N_rotor


newline = "\n"
newline = newline + "      ! Current data taken from:\n"
newline = newline + "      !" + pwd + "/" + method + "\n"

newline = newline + "      RRHO\n"
newline = newline + "        Geometry[angstrom]\t%d\n" % (N_atoms)
newline = newline + "\t" + geom + "\n"
newline = newline + "        Core    RigidRotor\n"
newline = (
    newline + "          SymmetryFactor\t1\n"
)  # write 1 as default - user can change this
newline = newline + "        End\n"


if N_rotor > 0:
    for rotor in range(int(N_rotor)):
        # default values - reset for each rotor
        grp1 = "X"
        grp2 = "X"
        ax1 = "X"
        ax2 = "X"
        sym = "1"
        stp = "36"
        potline = ""
        if prompt:
            print(f"Load rotor {rotor:d}:")
            grp = input("Specify rotor group name: ")
            scanf = method.replace(".log", f"_scan_{grp:s}.log")
            try:
                grp1, grp2, ax1, ax2, sym, stp, potline = get_rotor(scanf)
            except FileNotFoundError:
                print("Scan file not found. Writing template block.")
            except ValueError:
                print("Requested scan output not found. Writing template block.")

        # grp1 and grp2 are potential member of the group - but not both; will figure out later what do do here
        newline = newline + "        Rotor     Hindered\n"
        newline = (
            newline
            + "          Group                  X \t\t# atoms in rotating group excluding the atom on the axis\n"
        )
        newline = (
            newline
            + "          Axis                   %s %s \t\t# rotational axis\n"
            % (ax1, ax2)
        )
        newline = (
            newline
            + "          Symmetry               %s \t\t# 360/angle of rotation to recover the initial structure\n"
            % sym
        )
        newline = (
            newline
            + "          Potential[kcal/mol]    %s \t\t# number of equidistant point on the potential energy curve with respect to the rotational angle\n\t\t%s\n          End\n"
            % (stp, potline)
        )

newline = newline + "\n        Frequencies[1/cm]\t%d\n" % (N_freq)
newline = newline + freq
if len(imaginary) > 0:
    for i in imaginary:
        newline = newline + "\n        !Imaginary mode:  %6.1F\n" % (float(i))

if prompt:
    print("Calculate and write energy:")
    flog = method
    SPE_ext = (
        input(
            "Specify ORCA output file name extension (replaces '.log') [_f12_tz.orca.out]: "
        )
        or "_f12_tz.orca.out"
    )
    forc = method.replace(".log", SPE_ext)
    newzero = float(
        input("Baseline value for relative energies (kcal/mol)? [0]: ") or "0"
    )
    energy = MagicNo * get_energy(flog, forc)  # convert to kcal/mol
    newline = newline + f"\n        ZeroEnergy[kcal/mol]\t{(energy-newzero):.2f}\n"
else:
    if len(imaginary) > 0:
        newline = newline + "\n        ZeroEnergy[kcal/mol]\tTSENERGY\n"
    else:
        newline = newline + "\n        ZeroEnergy[kcal/mol]\t0.0\n"

newline = newline + "        ElectronicLevels[1/cm]\t1\n"
newline = newline + "            0    %d\n" % (int(multiplicity))

if len(imaginary) > 0:
    newline = newline + "        Tunneling\tEckart\n"
    newline = newline + "          ImaginaryFrequency[1/cm]  %6.1F\n" % -float(
        imaginary[0]
    )
    newline = newline + "          WellDepth[kcal/mol]\tXREACTANT\n"
    newline = newline + "          WellDepth[kcal/mol]\tXPRODUCT\n"
    newline = newline + "        End\n"
newline = newline + "      End\n"


if newout:
    newname = method.replace(".log", ".paper")
    newfile = open(newname, "w")
    newfile.write(newline)
    newfile.close()
else:
    print(newline)

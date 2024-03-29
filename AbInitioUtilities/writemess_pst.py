#! /usr/bin/env python
#
#    writemess_pst: a python script to generate MESS input from g09/g16 output
#    specifically takes two fragments and build a phase space theory block for barrierless reaction
#    copied from the function g09_to_paper.py written by Franklin Goldsmith
#    added functionality: prompts user for energy, rotor information during write
#    Usage: $ writemess_pst file0.log file1.log [options]
#    Options: specify 'yes' in optional arguments to write to file
#    Copyright (C) 2020  Mark E. Fuller
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
writemess_pst: a python script to generate MESS input from g09/g16 output
specifically takes two fragments and build a phase space theory block for barrierless reaction
copied from the function g09_to_paper.py written by Franklin Goldsmith
added functionality: prompts user for energy, rotor information during write
Usage: $ writemess_pst file0.log file1.log [options]
Options: specify 'yes' in optional arguments to write to file
"""

import sys

from FileParsers import get_cartesian, get_bondscan, get_frequencies
from PhaseSpaceFit import PhaseSpaceFit

# -------------------------------------------------------------------------------
# BEGIN HERE
# -------------------------------------------------------------------------------

# need to supply two fragments and potential
# (in that order)

command_line = sys.argv[1:]

frag0 = command_line[0]
frag1 = command_line[1]


N_rotor = 0
linear = False
newout = False
prompt = False
scantype = "none"
if len(command_line) > 2:  # additional arguments besides fragments passed
    for item in command_line[2:]:
        if item == "yes":
            newout = True
        elif item == "interactive":
            prompt = True
        elif (item == "relaxed") or (item == "rigid"):
            scantype = item
        else:
            print(f"Command line argument not recognized: {item}")

# PART 1: GET THE GEOMETRIES
N_atoms0, geom0, multiplicity0 = get_cartesian(frag0)
N_atoms1, geom1, multiplicity1 = get_cartesian(frag1)

stoich = ""  # empty string
for atom in ["H", "C", "N", "O"]:  # atoms currently in our reactive systems
    temp = geom0.count(atom) + geom1.count(atom)
    if temp > 0:
        stoich += f"{atom:s}{temp:d}"

geom0 = geom0.replace("\n", "\n\t")  # add tabs to reformat
geom1 = geom1.replace("\n", "\n\t")  # add tabs to reformat

newline = "\n"
newline += "  Barrier	BX by wz\n"
newline += "   RRHO\n"
newline += f"      Stoichiometry {stoich}\n"
newline += "      Core      PhaseSpaceTheory\n"

newline += "        FragmentGeometry[angstrom]\t%d\n" % (N_atoms0)
newline += "\t" + geom0 + "\n"

newline += "        FragmentGeometry[angstrom]\t%d\n" % (N_atoms1)
newline += "\t" + geom1 + "\n"

newline += "        SymmetryFactor\tX\n"

if prompt:
    scanf = input("Specify bond scan file: ")
    r, V = get_bondscan(scanf, scantype)
    A, n = PhaseSpaceFit(r, V)
    print("Warning! Check that scan reproduces expected barrier height!")
else:
    A = 0
    n = 0

newline += f"        PotentialPrefactor[au]          {A:.2e}\n"
newline += f"        PotentialPowerExponent          {n:.2f}\n"

newline += "        End\n"


# PART 2: GET THE FREQUENCIES
# temporary workaround - assume diatoms are linear, all else non-linear
real0, imaginary0, freq0 = get_frequencies(frag0, (N_atoms0 == 2), N_rotor)
real1, imaginary1, freq1 = get_frequencies(frag1, (N_atoms1 == 2), N_rotor)

# check for imaginary frequencies
if (len(imaginary0) | len(imaginary1)) != 0:
    print("Warning! Imaginary frequencies detected")

# check that the freq. count is correct
N_atoms_total = N_atoms0 + N_atoms1
N_freq_counted = len(imaginary0) + len(real0) + len(imaginary0) + len(real1)
N_freq_counted_real = len(real0) + len(real1)
N_freq_expect = 3 * N_atoms_total - (2 * 6)
if N_atoms0 == 2:
    N_freq_expect += 1
if N_atoms1 == 2:
    N_freq_expect += 1

if N_freq_counted_real != N_freq_expect:
    print(
        f"Warning! (Real) frequency count in files ({N_freq_counted_real:d}) differs from expected ({N_freq_expect:d})"
    )

newline += f"      Frequencies[1/cm]\t{N_freq_counted_real:d}\n"
newline += "\t" + freq0.strip() + "\n"
newline += "\t" + freq1.strip() + "\n"

if int(multiplicity0) == 2 and int(multiplicity1) == 2:
    print("Sum of two doublets is singlet")
else:
    print("Check multiplicity")
multiplicity_pst = 1

newline += "        ElectronicLevels[1/cm]\t1\n"
newline += f"            0    {multiplicity_pst:d}\n"
newline += "        ZeroEnergy[kcal/mol]\t0.0\n"
newline += "      End\n"

if newout:
    newname = "pst.paper"  # method.replace('.log','.paper')
    newfile = open(newname, "w")
    newfile.write(newline)
    newfile.close()
else:
    print(newline)

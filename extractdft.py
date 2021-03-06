#! /usr/bin/env python
#
#    extractdft: a python script to print the output energies from Gaussian optimizations from the command line
#    modified from the original function written by Aaron Danilack
#    Usage: $ extractdft file1.log file2.log ...
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
#    extractdft  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################


# Import stuff.
import sys
from FileParsers import get_energy_gaussian

print("\n")

for filename in sys.argv[1:]:

    q, w = get_energy_gaussian(filename)

    # Print the data we want.
    print(filename)
    print(f"E0+ZPE = {q:f}")
    print(f"ZPE = {w:f}")
    print("\n")

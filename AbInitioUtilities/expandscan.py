#! /usr/bin/env python
#
#    expandscan: a python script to update template g09/g16 scan input files
#    runs on output of writescan with rotors to update file name and chk file
#    also places dummy line where scan goes for easy find and replace
#    derived from the function g09_to_paper.py of written by Franklin Goldsmith
#    Usage: $ writescan file1.log file2.log ...
#    Copyright (C) 2020 - 2021  Mark E. Fuller
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
expandscan: a python script to update template g09/g16 scan input files
runs on output of writescan with rotors to update file name and chk file
also places dummy line where scan goes for easy find and replace
derived from the function g09_to_paper.py of written by Franklin Goldsmith
Usage: $ writescan file1.log file2.log ...
"""

# Import stuff.
import sys
import os

scanfilename = sys.argv[1]  # output of writescan: *scan_.gjf
if scanfilename.endswith("_scan_.gjf"):  # make sure this is the template file
    if len(sys.argv[2:]) > 1:
        for rotor in sys.argv[2:]:
            rotorstr = "_scan_{:s}.".format(rotor)
            ofilename = scanfilename.replace("_scan_.", rotorstr)

            with open(scanfilename, "r") as ifile:
                ifilelines = ifile.readlines()

            scanline = ""

            # copy input file information with req'd updates
            for (l, line) in enumerate(ifilelines):
                if line.startswith("%chk"):
                    line = line.replace("_scan_.", rotorstr)

                scanline += line

            # update for some of my most common rotors
            if rotor == "ch3":
                sym = 3
            elif rotor == "ch3_0":
                sym = 3
            elif rotor == "no2":
                sym = 2
            elif rotor == "ch2":
                sym = 2
            else:
                sym = 1

            scanline += f"\nW X Y Z S {(36/sym):n} 10.0"  # template dihedral scan

            with open(ofilename, "w") as sfile:
                sfile.write(scanline)

        os.remove(scanfilename)  # don't need template anymore
    else:  # when rotor list is empty
        print("No rotor list provided. Doing nothing.")
else:  # when filename doesn't match ouput of writescan
    print("Given file does not match expected naming pattern. Doing nothing.")

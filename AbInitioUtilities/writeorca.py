#! /usr/bin/env python
#
#    writeorca: a python script to generate ORCA input files from g09/g16 output
#    derived from the function g09_to_paper.py written by Franklin Goldsmith
#    Usage: $ writeorca file1.log file2.log ...
#    Copyright (C) 2020 - 2021 Mark E. Fuller
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
#    Mark E. Fuller:fuller@stossrohr.net 


################################################################################

"""
writeorca: a python script to generate ORCA input files from g09/g16 output
derived from the function g09_to_paper.py written by Franklin Goldsmith
Usage: $ writeorca file1.log file2.log ...
"""

# Import stuff.
import sys

from FileParsers import get_cartesian

# ------------------------------------------------------------------------------------------------------------------------------------
# BEGIN HERE
# ------------------------------------------------------------------------------------------------------------------------------------

for gfilename in sys.argv[1:]:

    N_atoms, geom, multiplicity = get_cartesian(gfilename)

    methods = {
        "! DLPNO-CCSD(T)-F12 cc-pVTZ-F12 cc-pVTZ/C cc-pVTZ-F12-CABS TightSCF\n": "_f12_tz.inp",
        "! DLPNO-CCSD(T) cc-pVTZ cc-pVTZ/c TightSCF\n": "_ccsdt_tz.inp",
        "! DLPNO-CCSD(T) cc-pVQZ cc-pVQZ/c TightSCF\n": "_ccsdt_qz.inp",
    }

    for newline, ext in methods.items():
        newline = newline + "%MaxCore 20000\n"
        newline = newline + "\n"
        newline = newline + "%pal nprocs 12\n"
        newline = newline + "end\n"
        newline = newline + "\n"
        newline = newline + "* xyz 0 %d\n" % (int(multiplicity))
        newline = newline + geom
        newline = newline + "*\n"

        ofilename = gfilename.replace(".log", ext)
        with open(ofilename, "w") as ofile:
            ofile.write(newline)

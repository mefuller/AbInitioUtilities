#! /usr/bin/env python
#
#    mergescan: a python script to combine fwd. and rev. g09/g16 rotor scans
#    sometimes those scan do weird things and running in reverse captures the
#    messed-up portion
#    currently assume the reverse scan is denoted by "-1" appended to name
#    Usage: $ mergescan scan.log
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
#    mergescan  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################

import sys

from FileParsers import get_rotor
import numpy as np
from collections import Counter


def compare(s, t):
    return Counter(s) == Counter(t)


command_line = sys.argv[1:]

scanf = command_line[0]
scanr = scanf.replace(".log", "-1.log")

fill = False  # logical for broken scans

if len(command_line) > 1:  # additional arguments besides fragments passed
    print('Only supply forward scan file. Append reverse with "-1"')

grp1f, grp2f, ax1f, ax2f, symf, stpf, potlinef = get_rotor(scanf)
grp1r, grp2r, ax1r, ax2r, symr, stpr, potliner = get_rotor(scanr)

if not compare([ax1f, ax2f], [ax1r, ax2r]):
    print("ERROR! Scans do not use consistent axis - terminating")
    exit()

if not compare([grp1f, grp2f], [grp1r, grp2r]):
    print("WARNING! Off-axis atoms do not match - manually verify scans are compatible")

if not (symf == symr):
    print("ERROR! Scans have inconsistent symmetry - terminating")
    exit()

if not (abs(stpf) == abs(stpr)):
    print("ERROR! Scans step sizes do not match - terminating")
    exit()

if not (len(potlinef) == len(potliner)):
    print("WARNING! Scans potential lengths do not match")
    next = (input("Merge two partial scans? [y]: ") or "y")
    if next == ("y" or "yes"):
        n_step = (input(f"Total number of scan steps? [{36 / symf}]: ") or (36 / symf))
        scan_template = np.full(int(n_step), np.inf)  # preset with very high value
        fill = True
    else:
        print("Unable to continue - terminating")
        exit()

# time to get down to business
if fill:
    fwdtmp = np.array(potlinef.split()).astype(float)
    fwdval = scan_template.copy()
    for q, pot in enumerate(fwdtmp):
        fwdval[q] = np.minimum(pot, fwdval[q])
    revtmp = np.array(potliner.split()).astype(float)
    revval = scan_template.copy()
    for q, pot in enumerate(fwdtmp):
        revval[q] = np.minimum(pot, revval[q])
else:
    fwdval = np.array(potlinef.split()).astype(float)
    revval = np.array(potliner.split()).astype(float)

# minimum energy at each scan point
minval = fwdval.copy()
minval[1:] = np.minimum(fwdval[1:], revval[:0:-1])


# make a string to replace potline
potline_merge = (
    np.array2string(minval, separator="  ")
    .replace(". ", ".0")
    .replace("[", " ")
    .replace("]", " ")
)

print(potline_merge)

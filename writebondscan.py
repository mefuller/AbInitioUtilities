#! /usr/bin/env python
# 
#    writescan: a python script to generate g09/g16 scan input files (templated) from g09/g16 output
#    derived from the function g09_to_paper.py of written by Franklin Goldsmith
#    Usage: $ writescan file1.log file2.log ...
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


#setup terminal output later:
#    writescan  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################

# Import stuff.
import re # regular expressions
import fileinput, sys, os
import time
import shutil


for gfilename in sys.argv[1:]:
    ifilename = gfilename.replace('.log','.gjf')

    with open(ifilename, 'r')as ifile:
        ifilelines = ifile.readlines()

    newline = ''

    #copy input file information with req'd updates
    for (l,line) in enumerate(ifilelines):
        if line.startswith('%chk'):
            line = line.replace('.chk','_scan_.chk')
        elif line.startswith("#p"):
            line = line.replace('internal','modredundant')
            if "calcall" in line:
                line = line.replace('calcall','calcfc') #don't want to waste time
        elif line.startswith('   B1'):
            break

        newline += line


    #get results of calculation
    with open(gfilename, 'r')as gfile:
        gfilelines = gfile.readlines()

    start_freq = False
    for (l,line) in enumerate(gfilelines):
        if line.startswith(" Optimization completed"):
            if gfilelines[l+1].startswith("    -- Stationary point found."):
                start_freq = True

        if (start_freq == True) and (line.startswith('                       !   Optimized Parameters')):
            geom = ''
            for i in range(1000):
                localline =  gfilelines[l+5+i]
                if localline.startswith(' ---------'):
                    break
                else:
                    bits = localline.split()
                    geom += '   ' + bits[1] + '\t' + bits[2] + '\n'
            break


    scanline = newline + geom    

    sfilename = gfilename.replace('.log','_scan_.gjf')
    with open(sfilename, 'w') as sfile:
        sfile.write(scanline)

#! /usr/bin/env python
# 
#    get_cartesian.py: a python function to read g09/g16 output and return the 
#    cartesian coordinates of the structure
#    developed (mostly copied)) from the function g09_to_paper.py written by
#    Franklin Goldsmith
#    Usage: []=get_cartesian(logfile)
#    logfile is Gaussian log (output) file
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
#    get_cartesian.py  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################

def get_cartesian(logfile):
    # start by parsing Gaussian log file
    with open (logfile, 'r') as log:
        loglines = log.readlines()

    start_freq = False
    geom_line = 'ERROR'
    charge = 0
    multiplicity = 0
    for (l,line) in enumerate(loglines):
        if line.startswith(" Charge = "):
            bits = line.split()
            charge = int(bits[2])
            multiplicity = int(bits[5])

        if line.startswith(" Optimization completed"):
            if loglines[l+1].startswith("    -- Stationary point found."):
                start_freq = True

        if (start_freq == True) and (line.startswith('                          Input orientation:')):
            geom_line = ''
            for i in range(1000):
                localline =  loglines[l+5+i]
                if localline.startswith(' ---------'):
                    break
                else:
                    bits = localline.split()
                    if len(bits)==6:
                        N_atoms = int(bits[0])
                        atom = bits[1]
                        x = bits[3]
                        y = bits[4]
                        z = bits[5]
                        if atom=='1':
                            geom_line = geom_line +"H\t%10.6F\t%10.6F\t%10.6F\n"%(float(x),float(y), float(z))
                        elif atom=='6':
                            geom_line = geom_line +"C\t%10.6F\t%10.6F\t%10.6F\n"%(float(x),float(y), float(z))
                        elif atom=='7':
                            geom_line = geom_line +"N\t%10.6F\t%10.6F\t%10.6F\n"%(float(x),float(y), float(z))
                        elif atom=='8':
                            geom_line = geom_line +"O\t%10.6F\t%10.6F\t%10.6F\n"%(float(x),float(y), float(z))

            break

    if geom_line == 'ERROR':
        print('ERROR: no geometry found for ' + logfile)
    return N_atoms, geom_line, multiplicity

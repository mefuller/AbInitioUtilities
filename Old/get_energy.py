# 
#    get_energy.py: a python function to read and return the optimized energy
#    Combines zero point energy from geometry/frequency calculation with single-point energy result
#    Usage: energy=get_energy(flog,forc,floc)
#    flog and forc are Gaussian and ORCA output files, respectively
#    floc is path to directory where files are located
#    Currently written assuming Gaussian and Orca 
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
#    get_energy.py  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################

def get_energy(flog,forc,floc):
    #input name is the identifier, e.g. ts_ch3o_no2_to_ch2o_hno2, ch3o, no2, &c.
    logf = (floc+flog) #this is my preferred method right now
    orcf = (floc+forc) #this is my preferred method right now

    #extract ZPE from log file
    ZPE = [] # Fill this list with ZPE lines. 

    # Get the data from the geometry optimization calculation.
    logfile = open(logf, 'r')
    loglines = logfile.readlines()
    logfile.close()

    for (l,line) in enumerate(loglines):
        if line.startswith(' Zero-point correction='):
            ZPE.append(line)

    #print (float(ZPE[-1].split()[-2]))


    #extract energy from orca output file
    E0 = [] # Fill this list with E0 lines.

    # Get the data from the single-point calculation.
    outfile = open(orcf,'r')
    outlines = outfile.readlines()
    outfile.close()

    for (l,line) in enumerate(outlines):
        if line.startswith('FINAL SINGLE POINT ENERGY'):
            E0.append(line)

    #print (float(E0[-1].split()[-1]))
    
    q = ((float(ZPE[-1].split()[-2])) + (float(E0[-1].split()[-1])))
    
    return q

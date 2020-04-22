# 
#    get_energy.py: a python function to read and return the optimized energy
#    Combines zero point energy from geometry/frequency calculation with single-point energy result
#    Usage: energy=get_energy(mol_name,mol_loc)
#    mol_loc is path to directory where files are located
#    mol_name is species identifier; files names are species followed by method and basis
#    Currently written assuming methods (b2plypd3-ccpvtz//f12-tz) with Gaussian and Orca 
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

"""
M. E. Fuller, 5 April 2020

A function to automatically read and return the optimized energy
Required files are Gaussian log and Orca output
Single-point energy is extracted form Orca and summed with the ZPE from Gaussian
Methods are currently assumed (b2plypd3-ccpvtz//f12-tz)
Intended application is for input to Tamkin and/or PAPR input preparation
"""
def get_energy(conformer,loc):
    #input name is the identifier, e.g. ts_ch3o_no2_to_ch2o_hno2, ch3o, no2, &c.
    logf = (loc+conformer+"_b2plypd3_ccpvtz.log") #this is my preferred method right now
    orcf = (loc+conformer+"_b2plypd3_ccpvtz_f12_tz.orca.out") #this is my preferred method right now

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

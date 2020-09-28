#! /usr/bin/env python
# 
#    refit.py: a python script to script to read in a double Arrhenius PLOG rate
#    in CHEMKIN format
#    evaluates rate and prints temperature and rate to file for refitting
#    
#    Usage: $ refit.py
#    Specify data file as output from MESS or TAMkin with options 'mess' or 'tamkin'
#    Default input format assumed to be two columns: temperature and rate
#    Default behavior is to print return modified Arrhenius fit
#    Specify 'Arr' as option for two-parameter fit
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
#    refit.py  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################


import numpy as np

for num in range(1,10):
    ratefile = 'oldfit_{}.txt'.format(num)

    with open(ratefile,'r') as oldfit:
        lines = oldfit.readlines()

    header=lines[0].split()
    ncase = int((len(lines)-1)/2)
        
    for PLOG in range(ncase):
        outfile = 'refit_{}_PLOG_{}.txt'.format(header[0],PLOG)
        with open(outfile, 'w') as outf:
            line0 = PLOG*2 + 1
            Abits = lines[line0].replace('/',' ').split()
            Bbits = lines[line0+1].replace('/',' ').split()
            Pname = Abits[1]
            outf.write('Rates for {}\n'.format(header[0]))
            outf.write('P = {}\n'.format(Pname))
            outf.write('T (K) \t k \n')
            #print('Rates for {}'.format(header[0]))
            #print('P = {}'.format(Pname))
            #print('T (K) \t k')
            for T in np.arange(200,2025,25):
                rateA = float(Abits[2])*(T**float(Abits[3]))*np.exp(-1*float(Abits[4])/(1.987*T))
                rateB = float(Bbits[2])*(T**float(Bbits[3]))*np.exp(-1*float(Bbits[4])/(1.9870*T))        
                outf.write('{:4f} \t {:6g} \n'.format(T, (rateA+rateB))) 
                #print('{:4f} \t {:6g}'.format(T, (rateA+rateB))) 

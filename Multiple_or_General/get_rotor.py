#! /usr/bin/env python
# 
#    get_rotor.py: a python function to read a rotor scan and return key values
#    Usage: []=get_rotor(fscan, floc)
#    fscan is Gaussian scan log (output) file
#    floc is path to directory where file is located
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
#    get_rotor.py  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################


#		    newline = newline + "        Rotor     Hindered\n"
#		    newline = newline + "          Group                  X \t\t# atoms in rotating group excluding the atom on the axis\n"
#		    newline = newline + "          Axis                   X \t\t# rotational axis\n"
#		    newline = newline + "          Symmetry               X \t\t# 360/angle of rotation to recover the initial structure\n"
#		    newline = newline + "          Potential[kcal/mol]    36 \t\t# number of equidistant point on the potetial energy curve with respect to the rotational angle\n\n          End\n"


def get_rotor(fscan,floc):

    logf = (floc+fscan) 

    scantext = open(logf, 'r')
    lines = scantext.readlines()
    scantext.close()

    raw_potential = []

    temp=''

    for q,line in enumerate(lines):
        if line.startswith(' The following ModRedundant input section has been read:'):
            bits = lines[q+1].split()
            ax1 = bits[2] #atom 1 on axis
            ax2 = bits[3] #atom 2 on axis
            grp1 = bits[1] #possible group member
            grp2 = bits[4] #other possible group member
            stp = int(bits[6]) #number of scan steps
            inc = float(bits[7]) #angular increment, degree

        if line.startswith(' E2(B2PLYPD3) ='):
	        #raw_potential.append(float(line.split()[5]))
	        temp = line.split()[5]
        if line.startswith(' Step number   1 out of a maximum of'):
            Escan = float(temp.replace('D','E'))
            raw_potential.append(Escan)

    #after the last line, add the last value
    Escan = float(temp.replace('D','E'))
    raw_potential.append(Escan)

    #
    mini = min(raw_potential)
    maxi = max(raw_potential)

    if raw_potential[0]!=mini:
	    print ("Warning: first entry is not minimum!")

    #print ("%.2F"%(627.5095*(maxi-mini)))

    potline = ''

    for V in raw_potential:
        potline = potline + " %.2F "%( 627.5095*(V-mini))


    sym = int(360.0/(stp*inc))

    #print(grp1, grp2, ax1, ax2, sym, stp, potline)
    return grp1, grp2, ax1, ax2, sym, stp, potline

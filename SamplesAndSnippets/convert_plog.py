#! /usr/bin/env python

#    convert_plog.py: a template for formatting MESS results
#    written by Franklin Goldsmith (Brown University)
#
#    see https://tcg.cse.anl.gov/papr/codes/mess.html
#    using the auxiliary codes to process the MESS output file returns PLOG output
#    this function converts Chemkin PLOG to Cantera cti format
#    fill in the dictionry below as needed
#    as usual:
#    goal is to be more systematic and less error-prone
#
#    All contents of this file:
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
#    convert_plog.py  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.
"""
open master equation results
"""
import sys,os
#import numpy
#import scipy
#import pylab


# read me.out file from the command line
command_line = sys.argv[1:]
oldplog = command_line[0]
results = open(oldplog,'r')
lines = results.readlines()
results.close()

prefix, suffix = oldplog.split('.')

cti = open(prefix+'.cti', 'w')

my_dict = {}

my_dict['roono'] = 'CH3OONO'
my_dict['no'] = 'CH3O2 + NO'
my_dict['no2'] = 'CH3O + NO2'


for (l,line) in enumerate(lines):
	if '=' in line and line[0]!='!':
		reactant, the_rest = line.split('=')
		product = the_rest.split()[0]
		print(reactant, product)
		if reactant in my_dict:
			new_reactant = my_dict[reactant]
		else:
			new_reactant = reactant
		if product in my_dict:
			new_product = my_dict[product]
		else:
			new_product = product

		newline = "pdep_arrhenius('%s <=> %s',\n"%(new_reactant,new_product)
		cti.write(newline)

	elif line.startswith("  PLOG/"):
		firstbits = line.split('!')
		print(line, firstbits)
		bits = firstbits[0].split()
		comment = firstbits[1]

		pressure = float(bits[0].split('/')[1])
		A = float(bits[1])
		n = float(bits[2])
		Ea = float(bits[3].split('/')[0])

		if lines[l+1]=='\n':
			print("oye")
			newline = "\t[(%.2E, 'atm'), %.2E,  %.2F,  %.1F])\t#%s\n"%(pressure, A, n, Ea, comment)
		else:
			newline = "\t[(%.2E, 'atm'), %.2E,  %.2F,  %.1F],\t#%s"%(pressure, A, n, Ea, comment)
		cti.write(newline)

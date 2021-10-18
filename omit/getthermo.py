#! /usr/bin/env python
#
#    getthermo: a python function utilizing TAMkin and g09/g16 results
#    to calculate and output thermodynamic data for inclusion in mechanismss
#    Usage: $ mergescan scan.log
#    Copyright (C) 2020  Mark E. Fuller
#    Based on a script developed by Heiko Minwegen
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


#    setup terminal output later:
#    getthermo  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.
#
#
################################################################################
import sys
from FileParsers import is_number, get_cartesian, get_energy, get_frequencies, get_rotor
from tamkin import *
from molmod import *
from nasafit import *
import numpy
import os
from datetime import date
from pybel import *  # generating smiles using openbabel


def parseChemForm(ChemString):
    elements = ["C", "H", "O", "N", "F", "S"]
    chars = list(ChemString)
    splitted = []
    elCount = 99
    for element in elements:
        for i in xrange(len(chars)):
            if chars[i] == element:
                if chars[i + 1].isdigit():
                    if chars[i + 1] < len(chars):
                        if chars[i + 2].isdigit():
                            elCount = int(chars[i + 1] + chars[i + 2])
                        else:
                            elCount = int(chars[i + 1])
                    else:
                        elCount = int(chars[i + 1])

                else:
                    elCount = 1
                splitted.append([element, elCount])
    # print splitted
    return splitted


# NpT is used when nothing else is specified (1bar)

# input files
command_line = sys.argv[1:]

input_file = command_line[0]
if not input_file.endswith(".fchk"):  # make sure this is the template file
    print("Formatted check file (.fchk) input required - terminating")
    quit()

thermo = load_molecule_g03fchk(input_file)

N_rotor = 0
prompt = True
if len(command_line) > 1:
    for item in command_line[1:]:
        if is_number(item):
            N_rotor = int(item)
        else:
            print(f"Command line argument not recognized: {item}")

# rotor objects
rotors = []
if N_rotor > 0:
    for rotor in range(int(N_rotor)):
        print(f"Load rotor {rotor:d}:")
        grp = input("Specify rotor group name: ")
        scanf = input_file.replace(".fchk", f"_scan_{grp:s}.log")
        thermo_scan = load_rotscan_g03log(scanf)
        grp1, grp2, ax1, ax2, sym, stp, potline = get_rotor(scanf)
        rotors[q] = Rotor(thermo_scan, thermo, rotsym=sym, cancel_freq="scan",
                          even=False, dofmax=3, num_levels=levels)

# input data
name = input_file.strip(".fchk")
IntRots = len(rotors)
extRotSym = 2
T1 = numpy.array(range(100, 950, 50))
T2 = numpy.array(range(1000, 5100, 100))
T3 = [273.15, 298.15, 1500, 2500, 3500]
T1 = numpy.sort(numpy.append(T1, T3))
T = numpy.append(T1, T2)
hf = -215.39  # enthalpy of formation from compound method calculation in kJ/mol

R = 8.3145  # gas constant [Joule / (mol*Kelvin)]

kcal = 4.184  # calculation factor Joule/ thermocalorie

levels = 1000  # Energylevels to be solved in SE
printlevels = 500  # Energylevels to be printed in plot
printTemp = 300  # Temperature [K] for printing occupation of energy levels

print "##################################################################"
print "##              Nasa Polynomial Resulting Values                ##"
print "##################################################################"

# normal modes
nma1 = NMA(thermo, ConstrainExt())


# partition functions
pfrrho = PartFun(nma1, [ExtTrans(), ExtRot(symmetry_number=extRotSym)])
pfHR = PartFun(nma1, [ExtTrans(), ExtRot(symmetry_number=extRotSym), rotor1, rotor2])

# thermo analysis
taHR = ThermoAnalysis(pfHR, T)
tarrho = ThermoAnalysis(pfrrho, T)

# export data
if not os.path.exists("plot"):
    os.mkdir("plot")

if not os.path.exists("dat"):
    os.mkdir("dat")

taHR.write_to_file("dat/thermorotor.csv")
tarrho.write_to_file("dat/rrho.csv")
pfHR.write_to_file("dat/partFun.csv")
rotor1.plot_levels("plot/RotorLevels1.png", printTemp, num=printlevels)
rotor2.plot_levels("plot/RotorLevels2.png", printTemp, num=printlevels)

enthalpy, coeffs, lagr_multi, errorfit = nasafit(pfHR, hf, T1, T2)
print "{:10} {:^44} {:^22} {:^22}".format(
    "Fit:", "Enthalpy", "Entropy", "Heat Capacity"
)
print "{:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(
    "T", "Nasa", "pf:", "Nasa*RT", "pf*RT", "S", "S_fit", "Cp", "CpNasa"
)
print "{:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(
    "[K]",
    "[]",
    "[]",
    "[kJ/mol]",
    "[kJ/mol]",
    "[J/molK]",
    "[J/molK]",
    "[J/molK]",
    "[J/molK]",
)
for i in xrange(len(enthalpy)):
    print "{:>10.2f} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.1f} {:>10.1f} {:>10.2f} {:>10.2f}".format(
        enthalpy[i, 0],
        enthalpy[i, 1],
        enthalpy[i, 2],
        enthalpy[i, 3],
        enthalpy[i, 4],
        enthalpy[i, 5],
        enthalpy[i, 6],
        enthalpy[i, 8],
        enthalpy[i, 7],
    )

enthalpy, coeffs, lagr_multi, errorfit = nasafit(pfHR, hf, T1, T2)
print "{:10} {:^44} {:^22} {:^22}".format(
    "Fit:", "Enthalpy", "Entropy", "Heat Capacity"
)
print "{:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(
    "T", "Nasa", "pf:", "Nasa*RT", "pf*RT", "S", "S_fit", "Cp", "CpNasa"
)
print "{:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(
    "[K]",
    "[]",
    "[]",
    "[kcal/mol]",
    "[kcal/mol]",
    "[cal/molK]",
    "[cal/molK]",
    "[cal/molK]",
    "[cal/molK]",
)
for i in xrange(len(enthalpy)):
    print "{:>10.2f} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.1f} {:>10.1f} {:>10.2f} {:>10.2f}".format(
        enthalpy[i, 0],
        enthalpy[i, 1],
        enthalpy[i, 2],
        enthalpy[i, 3] / kcal,
        enthalpy[i, 4] / kcal,
        enthalpy[i, 5] / kcal,
        enthalpy[i, 6] / kcal,
        enthalpy[i, 8] / kcal,
        enthalpy[i, 7] / kcal,
    )

print "\nChi-Squared:\n{:10}{:.8e}\n{:10}{:.8e}".format(
    "Enthalpy:", errorfit[0], "Entropy:", errorfit[1]
)

print "\nNasa Coefficients:\n"
head = ""
for i in xrange(7):
    print "a{}(T < 1000 K) = {:20.10e}".format(i, coeffs[i])
    head = head + "a{}(T < 1000 K),".format(i)
print ""
for i in xrange(7, 14):
    print "a{}(T > 1000 K) = {:20.10e}".format(i - 7, coeffs[i])
    head = head + "a{}(T > 1000 K),".format(i - 7)
numpy.savetxt(
    "dat/nasa_coefficients.csv",
    numpy.reshape(coeffs, (1, len(coeffs))),
    delimiter=",",
    header=head,
)

# generating SMILES with openbabel
# moleculeSmile = readfile("fchk", IN_FormCHK).next().write("smi").split()[0] # "can": canonical SMILES format, else choose "smi" works just with non radicals
moleculeSmile = (
    readstring("cml", readfile("fchk", IN_FormCHK).next().write("cml"))
    .write("smi")
    .split()[0]
)  # with transfer fchk to cml and read cml multplicity is assigned "smi" prints SMILES and title


# generating date string
today = date.today()
insertdate = str(today.day) + "/" + str(today.month) + "/" + str(today.year - 2000)

# Nasa polynomial datasheet needs some molecular informations
formula = pfHR.chemical_formula
parsedFormula = parseChemForm(formula)

O = " "
H = " "
C = " "
oxy = " "
hydro = " "
carb = " "
other = " "
oth = " "

for species in parsedFormula:
    if species[0] == "O":
        O = species[0]
        oxy = species[1]
    elif species[0] == "H":
        H = species[0]
        hydro = species[1]
    elif species[0] == "C":
        C = species[0]
        carb = species[1]
    else:
        other = species[0]
        oth = species[1]

identName = moleculeSmile
# instNameDate = insertdate + " PCFC"
instNameDate = "PCFC"


print ""
# print "Standard Format for Nasa-Polynomials (note high temperature coefficients coming first):"
# print "C2H5COCH3  29/4/15 THERMC   4H   8O   1    0G   300.000  5000.000 1380.000    31"
# print " 1.25141235E+01 1.84604475E-02-6.14816056E-06 9.37968198E-10-5.37721162E-14    2"
# print "-3.46118541E+04-3.82309512E+01 1.92048232E+00 4.00983271E-02-2.20686090E-05    3"
# print " 5.85110392E-09-5.66573305E-13-3.05908852E+04 1.98194682E+01                   4"
# print ""
print "THERMO"
print "{:10.3f}{:10.3f}{:10.3f}".format(min(T), 1000, max(T))
# print "! NASA Polynomial format for CHEMKIN-II"
print "!", name, formula, moleculeSmile, "provided by PCFC RWTH", insertdate
print "{:19}{:>5}{:1}{:4}{:1}{:4}{:1}{:4}{:1}{:4}{:4}{:<9.3f}{:<9.3f}{:<9.3f}{:>5}".format(
    identName,
    instNameDate,
    C,
    carb,
    H,
    hydro,
    O,
    oxy,
    other,
    oth,
    "G",
    min(T),
    max(T),
    1000,
    str(IntRots) + "1",
)
print "{: .8E}{: .8E}{: .8E}{: .8E}{: .8E}    2".format(
    coeffs[7], coeffs[8], coeffs[9], coeffs[10], coeffs[11]
)
print "{: .8E}{: .8E}{: .8E}{: .8E}{: .8E}    3".format(
    coeffs[12], coeffs[13], coeffs[0], coeffs[1], coeffs[2]
)
print "{: .8E}{: .8E}{: .8E}{: .8E}                   4".format(
    coeffs[3], coeffs[4], coeffs[5], coeffs[6]
)
print "END"
print ""
print "\n***************************************************************************************\n"
print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Successfully Done !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
print "The End."

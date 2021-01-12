#! /usr/bin/env python
#
#    FileParsers.py: Python functions for extracting data from g09/g16/orca output
#
#    is_number: a little helper function to evaluate a variable as a number (or not)
#    copied in its entirely from Franklin Goldsmith
#
#    get_energy: a python function to read and return the optimized energy
#    Combines zero point energy from geometry/frequency calculation with single-point energy result
#    Usage: energy=get_energy(logfile,orcafile)
#    logfile and orcafile are Gaussian and ORCA output files, respectively
#    Currently written assuming Gaussian and Orca
#
#    get_rotor: a python function to read a g09/g16 rotor scan and return key values
#    Usage: []=get_rotor(logfile)
#    logfile is Gaussian scan log (output) file
#
#    get_bondscan: a python function to read a g09/g16 bond scan and return distance and energy
#    Usage: []=get_bondscan(logfile)
#    logfile is Gaussian scan log (output) file
#
#    get_cartesian: a python function to read g09/g16 output and return the
#    cartesian coordinates of the structure for inclusion in new input files
#    developed (mostly copied)) from the function g09_to_paper.py written by
#    Franklin Goldsmith
#    Usage: [N_atoms, geom_block, multiplicity]=get_cartesian(logfile)
#    logfile is Gaussian log (output) file
#
#    get_frequencies: a python function to read g09/g16 output and return the
#    frequncies broken down as real and imaginary and a text block for writing
#    PAPR/MESS input
#    Usage: [real, imaginary, freq_block]=get_frequencies(logfile, linear, N_rotor)
#    logfile is Gaussian log (output) file
#
#    get_energy_orca: a python function to read and return the optimized energy
#    from ORCA output file
#    Usage: energy=get_energy(orcafile)
#    orcafile is an ORCA output file
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


# setup terminal output later:
#    FileParsers.py  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_energy(logf, orcf):
    # "the" energy after we have performed DFT and SPE calculations
    # extract ZPE from log file
    E0_ZPE, ZPE = get_energy_gaussian(logf)

    # Get the optimized energy from the single-point calculation.
    E0, T1 = get_energy_orca(orcf)

    return E0 + ZPE


def get_energy_CBS(logf, orcf_tz, orcf_qz):
    E0_ZPE, ZPE = get_energy_gaussian(logf)
    E0_TZ, T1_TZ = get_energy_orca(orcf_tz)
    E0_QZ, T1_QZ = get_energy_orca(orcf_qz)

    E0_CBS = (
        64.0 * E0_QZ - 27.0 * E0_TZ
    ) / 37.0  # 64 = 4**3, 27 = 3**3, 37 = 4**3 - 3**3

    return E0_CBS + ZPE


# -------------------------------------------------------------------------------


def get_rotor(logf):

    scantext = open(logf, "r")
    lines = scantext.readlines()
    scantext.close()

    raw_potential = []

    temp = ""

    for q, line in enumerate(lines):
        if line.startswith(" The following ModRedundant input section has been read:"):
            bits = lines[q + 1].split()
            ax1 = bits[2]  # atom 1 on axis
            ax2 = bits[3]  # atom 2 on axis
            grp1 = bits[1]  # possible group member
            grp2 = bits[4]  # other possible group member
            stp = int(bits[6])  # number of scan steps
            inc = abs(float(bits[7]))  # angular increment, degree

        if line.startswith(" E2("):
            # raw_potential.append(float(line.split()[5]))
            temp = line.split()[5]
        if line.startswith(" Step number   1 out of a maximum of"):
            Escan = float(temp.replace("D", "E"))
            raw_potential.append(Escan)

    # after the last line, append the last value
    Escan = float(temp.replace("D", "E"))
    raw_potential.append(Escan)

    #
    mini = min(raw_potential)
    maxi = max(raw_potential)  # noqa: F841

    if raw_potential[0] != mini:
        print("Warning: first entry is not minimum!")

    # print ("%.2F"%(627.5095*(maxi-mini)))

    potline = ""

    # output potential in kcal/mole
    # formatted like this to paste into MESS / PAPR input
    for q, V in enumerate(raw_potential):
        if q < stp:  # trim to correct/desired number of entries
            potline = potline + " %.2F " % (627.5095 * (V - mini))
        else:
            break

    sym = int(360.0 / (stp * inc))  # assumes writer of scan was correct

    # print(grp1, grp2, ax1, ax2, sym, stp, potline)
    return grp1, grp2, ax1, ax2, sym, stp, potline


# -------------------------------------------------------------------------------
def get_bondscan(logf, scantype):

    if scantype == "relaxed":
        relaxed = True
    elif scantype == "rigid":
        relaxed = False
    else:
        print("Only relaxed and rigid scans currently supported.")
        print("Fallback to rigid")
        relaxed = False

    scantext = open(logf, "r")
    lines = scantext.readlines()
    scantext.close()

    radius = []
    raw_potential = []

    if relaxed:
        for q, line in enumerate(lines):
            # relaxed scans
            if line.startswith(
                " The following ModRedundant input section has been read:"
            ):
                bits = lines[q + 1].split()
                grp1 = bits[1]  # noqa: F841  # side A
                grp2 = bits[2]  # noqa: F841  # side B
                stp = int(bits[4])  # number of scan steps
                inc = float(bits[5])  # increment, angstrom

            # find line with initial bond length
            if ("!" in line) and ("Scan" in line):
                # if (f'R({grp1},{grp2})' or f'R({grp2},{grp1})') and 'Scan' in line:
                bits = line.split()
                r0 = float(bits[3])  # initial bond distance, angstrom

            # extract potentials
            if line.startswith(" SCF Done:  E("):
                # not always final
                temp = line.split()[4]

            # relaxed / rigid scan
            if line.startswith(" Step number   1 out of a maximum of"):
                # starting new step, so last energy was final
                Escan = float(temp.replace("D", "E"))
                raw_potential.append(Escan)

            # after the last line, append the last value
            Escan = float(temp.replace("D", "E"))
            raw_potential.append(Escan)

        # return lists to pass to fitting routines
        for dx in range(max(stp, len(raw_potential))):
            radius.append(dx * inc + r0)

    # rigid scan
    else:
        FindScanVals = True
        for q, line in enumerate(lines):
            if ("B" in line) and ("Scan" in line) and FindScanVals:
                bits = line.replace("Scan", "").split()
                r0 = float(bits[1])  # initial bond distance, angstrom
                stp = int(bits[2])  # number of scan steps
                inc = float(bits[3])  # increment, angstrom
                FindScanVals = False
            if line.startswith(" Summary of the potential surface scan:"):
                for w in range(q + 3, q + 3 + stp + 1):
                    bits = lines[w].split()
                    radius.append(float(bits[1]))
                    raw_potential.append(float(bits[2]))

    # general checking and returning information
    mini = min(raw_potential)
    maxi = max(raw_potential)  # noqa: F841

    if raw_potential[0] != mini:
        print("Warning: first entry is not minimum!")

    if stp > len(raw_potential):
        print("Warning: scan appears to have terminated early")
    if len(radius) < len(raw_potential):
        print("Warning: scan potential list is too long - truncating")
        radius = radius[: len(radius)]
        raw_potential = raw_potential[: len(radius)]

    return radius, raw_potential


# -------------------------------------------------------------------------------
def get_cartesian(logfile):
    # start by parsing Gaussian log file
    with open(logfile, "r") as log:
        loglines = log.readlines()

    start_freq = False
    geom_line = "ERROR"
    charge = 0
    multiplicity = 0
    for (l, line) in enumerate(loglines):
        if line.startswith(" Charge = "):
            bits = line.split()
            charge = int(bits[2])  # noqa: F841
            multiplicity = int(bits[5])

        if line.startswith(" Optimization completed"):
            if loglines[l + 1].startswith("    -- Stationary point found."):
                start_freq = True

        if start_freq and line.startswith(
            "                          Input orientation:"
        ):
            geom_line = ""
            for i in range(1000):
                localline = loglines[l + 5 + i]
                if localline.startswith(" ---------"):
                    break
                else:
                    bits = localline.split()
                    if len(bits) == 6:
                        N_atoms = int(bits[0])
                        atom = bits[1]
                        x = bits[3]
                        y = bits[4]
                        z = bits[5]
                        if atom == "1":
                            geom_line = geom_line + "H\t%10.6F\t%10.6F\t%10.6F\n" % (
                                float(x),
                                float(y),
                                float(z),
                            )
                        elif atom == "6":
                            geom_line = geom_line + "C\t%10.6F\t%10.6F\t%10.6F\n" % (
                                float(x),
                                float(y),
                                float(z),
                            )
                        elif atom == "7":
                            geom_line = geom_line + "N\t%10.6F\t%10.6F\t%10.6F\n" % (
                                float(x),
                                float(y),
                                float(z),
                            )
                        elif atom == "8":
                            geom_line = geom_line + "O\t%10.6F\t%10.6F\t%10.6F\n" % (
                                float(x),
                                float(y),
                                float(z),
                            )

            break

    if geom_line == "ERROR":
        print("ERROR: no geometry found for " + logfile)
    return N_atoms, geom_line, multiplicity


# -------------------------------------------------------------------------------


def get_frequencies(logfile, linear, N_rotor):
    # start by parsing Gaussian log file
    log = open(logfile, "r")
    loglines = log.readlines()
    log.close()
    frequencies = []
    for (l, line) in enumerate(loglines):
        if line.startswith(" Frequencies"):
            bits = line.split()
            if len(bits) == 5:
                frequencies.append(bits[2])
                frequencies.append(bits[3])
                frequencies.append(bits[4])
            elif len(bits) == 3 and linear:
                frequencies.append(bits[2])
        if line.startswith(" - Thermochemistry -"):
            break

    imaginary = []
    real = []

    for freq in frequencies:
        if float(freq) < 0.0:
            imaginary.append(freq)
        else:
            real.append(freq)

    # checking for correct count moved out of function

    # format frequencies
    freq_line = ""
    tors_line = "        !Torsional frequencies:"
    for (f, freq) in enumerate(real):
        if (f + 1) <= int(N_rotor):
            tors_line = tors_line + "\t%6.1F" % (float(freq))
        else:
            freq_line = freq_line + "\t%6.1F" % (float(freq))
        if (f + 1) % 3 == 0 and f != 0:
            freq_line = freq_line + "\n"
    if int(N_rotor) > 0:
        freq_line = freq_line + "\n" + tors_line + "\n"
    return real, imaginary, freq_line


# -------------------------------------------------------------------------------


def get_energy_orca(orcf):

    # extract energy from orca output file
    E0 = []  # Fill this list with E0 lines.
    T1 = []  # Fill this list with T1 lines.

    # Get the data from the single-point calculation.
    outfile = open(orcf, "r")
    outlines = outfile.readlines()
    outfile.close()

    for (l, line) in enumerate(outlines):
        if line.startswith("FINAL SINGLE POINT ENERGY"):
            E0.append(line)
        elif line.startswith("T1 diagnostic"):
            T1.append(line)

    # print (float(E0[-1].split()[-1]))

    q = float(E0[-1].split()[-1])
    w = float(T1[-1].split()[-1])

    return q, w


# -------------------------------------------------------------------------------


def get_energy_gaussian(filename):

    E0 = []  # Fill this list with E0 lines.
    ZPE = []  # Fill this list with ZPE lines.

    # Get the data from the geometry optimization calculation.
    with open(filename, "r") as logfile:
        loglines = logfile.readlines()

    for (l, line) in enumerate(loglines):
        if line.startswith(" Sum of electronic and zero-point Energies="):
            E0.append(line)
        elif line.startswith(" Zero-point correction="):
            ZPE.append(line)

    Energy = float(E0[-1].split()[-1])
    ZeroPoint = float(ZPE[-1].split()[-2])

    return Energy, ZeroPoint

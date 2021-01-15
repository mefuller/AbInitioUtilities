#! /usr/bin/env python
#
#    messmanager: a python script to calculate energies related values for MESS
#    requires a driver script with necessary inputs (dictionaries, fiel extensions))
#    prints out energy and phase space theory parameters for system
#    relies on file naming conventions and is adapted to particular problems,
#    so this is really largely an example
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
#    messmanager  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


###############################################################################


from FileParsers import get_bondscan
from PhaseSpaceFit import PhaseSpaceFit

MagicNo = 627.5095  # (kcal/mol)/hartree


def messmanager(
    FragLocationDict,
    WellLocationDict,
    TSLocationDict,
    BimolecDict,
    EnergyDict,
    E0,
    toplevel,
    ext_dft_NO,
    ext_dft_NO2,
    scantype,
):

    print("\nZero Energy:")
    print(f"{E0:.2e} Hartree")
    print(f"{MagicNo*E0:.2f} kcal/mol\n")

    print("\n##### Bimoleculars #####\n")
    for A, B in BimolecDict.items():
        print(A + "+" + B)
        Etemp = EnergyDict[A] + EnergyDict[B] - E0
        print(f"{Etemp:.2e} Hartree")
        print(f"{MagicNo*Etemp:.2f} kcal/mol\n")

    print("\n##### Wells #####\n")
    for well in WellLocationDict:
        print(well)
        Etemp = EnergyDict[well] - E0
        print(f"{Etemp:.2e} Hartree")
        print(f"{MagicNo*Etemp:.2f} kcal/mol\n")

    print("\n##### Transition States #####\n")
    for TS in TSLocationDict:
        print(TS)
        bits = TS.split("_")
        R = bits[1]
        P1 = bits[2]
        if TSLocationDict[TS] == "pst":  # phase space theory
            print("Phase Space Theory")
            Ewell = EnergyDict[R]

            # PST products always bimolecular
            P2 = BimolecDict[P1]
            Edelta = EnergyDict[P1] + EnergyDict[P2] - Ewell

            loc = WellLocationDict[R]
            if BimolecDict[P1] == "no":
                ext = ext_dft_NO
            elif BimolecDict[P1] == "no2":
                ext = ext_dft_NO2
            else:
                print(f"malformed pst identifier: {TS}")
                continue

            rvals, Evals = get_bondscan(toplevel + loc + ext, scantype)
            # fit the scans
            A, n = PhaseSpaceFit(rvals, Evals)
            # rescale
            A = A * (Edelta) / (max(Evals) - min(Evals))

            print(f"\tPES Barrier: {MagicNo*Edelta:.2f} kcal/mol")
            print(f"\tScan Barrier: {MagicNo*(max(Evals)-min(Evals)):.2f} kcal/mol")
            print(f"\tPST fit (A, n): {A:.2f}, {n:.2f}")
            print("\n")

        else:
            Etemp = EnergyDict[TS] - E0
            print(f"{Etemp:.2e} Hartree")
            print(f"{MagicNo*Etemp:.2f} kcal/mol\n")
            # convention is that reactants are always wells
            print(f"\tBarrier to {R}")
            Etemp = EnergyDict[TS] - EnergyDict[R]
            print(f"\t{Etemp:.2e} Hartree")
            print(f"\t{MagicNo*Etemp:.2f} kcal/mol\n")
            try:
                # check if bimolecular
                P2 = BimolecDict[P1]
                Etemp = EnergyDict[TS] - (EnergyDict[P1] + EnergyDict[P2])
                name = P1 + " + " + P2
            except KeyError:
                # it's a well
                Etemp = EnergyDict[TS] - EnergyDict[P1]
                name = P1
            print(f"\tBarrier to {name}")
            print(f"\t{Etemp:.2e} Hartree")
            print(f"\t{MagicNo*Etemp:.2f} kcal/mol\n")

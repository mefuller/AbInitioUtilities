#    PhaseSpaceFit.py: curve fit bond scan results for use in phase-space theory
#
#    All contents of this file:
#    Copyright (C) 2020 - 2021  Mark E. Fuller
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    Mark E. Fuller: fuller@stossrohr.net

###############################################################################

"""
PhaseSpaceFit.py: curve fit bond scan results for use in phase-space theory
"""

import numpy as np
from scipy.optimize import curve_fit


def PhaseSpaceFit(r_list, V_list):
    # read in bond distance (angstrom) and energy (hartree) from bond scan

    # required constant
    a0 = 5.29177210903e-1  # Bohr radius, angstrom

    # define the functional form for phase space theory fits in MESS/PAPR
    def MESSpotential(r, A, n):
        # r: Coordinate in bohr
        # A: Prefactor in hartree
        # n: Exponent
        return -A * (r ** -n)

    # make arrays from input
    r_bohr = np.asarray(r_list, dtype=np.float64) / a0
    V_hartree = np.asarray(V_list, dtype=np.float64)

    # set zero for potential ("infinite" separation)
    V_hartree = V_hartree - np.mean(V_hartree[-3:])

    # fit the data
    # MESS requires n > 2
    fit = curve_fit(
        MESSpotential, r_bohr, V_hartree, bounds=([-np.inf, 2.01], [np.inf, np.inf])
    )
    A = fit[0][0]  # prefactor
    n = fit[0][1]
    return A, n

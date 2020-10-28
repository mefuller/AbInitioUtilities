import numpy as np
from scipy.optimize import curve_fit

def PhaseSpaceFit(r_list, V_list):
    #read in bond distance (angstrom) and energy (hartree) from bond scan
    
    #required constant
    a0 = 5.29177210903e-1 #Bohr radius, angstrom
    
    #define the functional form for phase space theory fits in MESS/PAPR
    def MESSpotential(r, A, n):
        #r: Coordinate in bohr
        #A: Prefactor in hartree
        #n: Exponent
        return -A * ( r ** -n )
    
    #make arrays from input
    r_bohr = np.asarray(r_list, dtype=np.float64) / a0 
    V_hartree = np.asarray(V_list, dtype=np.float64)

    #set zero for potential ("infinite" separation)
    V_hartree = V_hartree - np.mean(V_hartree[-3:])

    #fit the data
    fit = curve_fit(MESSpotential,r_bohr,V_hartree)
    A = fit[0][0] #prefactor
    n = fit[0][1]
    return A, n

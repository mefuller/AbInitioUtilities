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

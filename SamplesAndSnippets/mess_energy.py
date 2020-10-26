#! /usr/bin/env python

#information for R+NO2 project

from FileParsers import *

MagicNo = 627.5095 #(kcal/mol)/hartree

toplevel = './'

#define extensions based on chosen methods for project
ext_dft = '_b2plypd3_ccpvtz.log'
ext_spe = ext_dft.replace('.log','_f12_tz.orca.out')

#list locations in file tree relative to toplevel
WellLocationDict = {}
FragLocationDict = {}
TSLocationDict = {}
BimolecDict={}
ReactantDict = {}
ProductDict = {}

#fragments
FragLocationDict['no'] = 'Brown/no/n1o1/no/no'
FragLocationDict['no2'] = 'Brown/no/n1o2/no2'
FragLocationDict['hno'] = 'noh/hno'
FragLocationDict['hono'] = 'Brown/noh/n1o2/h1n1o2/antihono/antihono'
FragLocationDict['1-pentyl'] = 'ch/c5/c5h11/n-c5h11-1'
FragLocationDict['2-pentyl'] = 'ch/c5/c5h11/n-c5h11-2'
FragLocationDict['3-pentyl'] = 'ch/c5/c5h11/n-c5h11-3'
FragLocationDict['1-pentyloxy'] = 'coh/c5o1/n-c5h11o-1/n-c5h11o-1'
FragLocationDict['2-pentyloxy'] = 'coh/c5o1/n-c5h11o-2/n-c5h11o-2'
FragLocationDict['3-pentyloxy'] = 'coh/c5o1/n-c5h11o-3/n-c5h11o-3'
FragLocationDict['pentanal'] = 'coh/c5o1/pc4h9cho/pc4h9cho'
FragLocationDict['2-pentanone'] = 'coh/c5o1/nc3h7coch3/nc3h7coch3'
FragLocationDict['3-pentanone'] = 'coh/c5o1/c2h5coc2h5/c2h5coc2h5'
FragLocationDict['1-pentene'] = 'ch/c5/c5h10/c5h10-1'
FragLocationDict['2-pentene'] = 'ch/c5/c5h10/c5h10-2'

#fragment pairs for bimoleculars in PES
BimolecDict['1-pentyl'] = 'no2'
BimolecDict['2-pentyl'] = 'no2'
BimolecDict['3-pentyl'] = 'no2'
BimolecDict['1-pentyloxy'] = 'no'
BimolecDict['2-pentyloxy'] = 'no'
BimolecDict['3-pentyloxy'] = 'no'
BimolecDict['pentanal'] = 'hno'
BimolecDict['2-pentanone'] = 'hno'
BimolecDict['3-pentanone'] = 'hno'
BimolecDict['1-pentene'] = 'hono'
BimolecDict['2-pentene'] = 'hono'

################# H11C5N1O2 ################# 
#wells
WellLocationDict['1-nitropentane'] = 'cnoh/c5n1o2/nitropentan-1'
WellLocationDict['2-nitropentane'] = 'cnoh/c5n1o2/nitropentan-2'
WellLocationDict['3-nitropentane'] = 'cnoh/c5n1o2/nitropentan-3'
WellLocationDict['1-pentylnitrite'] = 'cnoh/c5n1o2/pentylnitrite-1'
WellLocationDict['2-pentylnitrite'] = 'cnoh/c5n1o2/pentylnitrite-2'
WellLocationDict['3-pentylnitrite'] = 'cnoh/c5n1o2/pentylnitrite-3'

#transition states
TSlevel = 'cnoh/c5n1o2/ts/'
TSLocationDict['ts_nitro_nitrite-1'] = 'ts_nitropentan-1_to_pentylnitrite-1'
TSLocationDict['ts_nitro_nitrite-2'] = 'ts_nitropentan-2_to_pentylnitrite-2'
TSLocationDict['ts_nitro_nitrite-3'] = 'ts_nitropentan-3_to_pentylnitrite-3'
TSLocationDict['ts_nitrite_hno-1'] = 'ts_pentylnitrite-1_to_hno_pentanal'
TSLocationDict['ts_nitrite_hno-2'] = 'ts_pentylnitrite-2_to_hno_pentanone-2'
TSLocationDict['ts_nitrite_hno-3'] = 'ts_pentylnitrite-3_to_hno_pentanone-3'
TSLocationDict['ts_nitro_hono-1'] = 'ts_nitropentan-1_to_hono_pentene-1'
TSLocationDict['ts_nitro_hono-2_1'] = 'ts_nitropentan-2_to_hono_pentene-1'
TSLocationDict['ts_nitro_hono-2_2'] = 'ts_nitropentan-2_to_hono_pentene-2'
TSLocationDict['ts_nitro_hono-3'] = 'ts_nitropentan-3_to_hono_pentene-2'

ReactantDict['ts_nitro_nitrite-1'] = '1-nitropentane'
ReactantDict['ts_nitro_nitrite-2'] = '2-nitropentane'
ReactantDict['ts_nitro_nitrite-3'] = '3-nitropentane'
ReactantDict['ts_nitrite_hno-1'] = '1-pentylnitrite'
ReactantDict['ts_nitrite_hno-2'] = '2-pentylnitrite'
ReactantDict['ts_nitrite_hno-3'] = '3-pentylnitrite'
ReactantDict['ts_nitro_hono-1'] = '1-nitropentane'
ReactantDict['ts_nitro_hono-2_1'] = '2-nitropentane'
ReactantDict['ts_nitro_hono-2_2'] = '2-nitropentane'
ReactantDict['ts_nitro_hono-3'] = '3-nitropentane'

ProductDict['ts_nitro_nitrite-1'] = '1-pentylnitrite'
ProductDict['ts_nitro_nitrite-2'] = '2-pentylnitrite'
ProductDict['ts_nitro_nitrite-3'] = '3-pentylnitrite'
ProductDict['ts_nitrite_hno-1'] = 'pentanal'
ProductDict['ts_nitrite_hno-2'] = '2-pentanone'
ProductDict['ts_nitrite_hno-3'] = '3-pentanone'
ProductDict['ts_nitro_hono-1'] = '1-pentene'
ProductDict['ts_nitro_hono-2_1'] = '1-pentene'
ProductDict['ts_nitro_hono-2_2'] = '2-pentene'
ProductDict['ts_nitro_hono-3'] = '2-pentene'

#get raw energy values (Hartree)
EnergyDict = {}
for S, loc in FragLocationDict.items():
    EnergyDict[S] = get_energy(toplevel+loc+ext_dft, toplevel+loc+ext_spe)
for S, loc in WellLocationDict.items():
    EnergyDict[S] = get_energy(toplevel+loc+ext_dft, toplevel+loc+ext_spe)
for S, loc in TSLocationDict.items():
    EnergyDict[S] = get_energy(toplevel+TSlevel+loc+ext_dft, toplevel+TSlevel+loc+ext_spe)

E0 = EnergyDict['no2'] + EnergyDict['2-pentyl']
print('\nZero Energy:')
print(f'{E0:.2e} Hartree')
print(f'{MagicNo*E0:.2f} kcal/mol\n')

print('\n##### Bimoleculars #####\n')
for A, B in BimolecDict.items():
    print(A + '+' + B)
    Etemp = EnergyDict[A] + EnergyDict[B] - E0
    print(f'{Etemp:.2e} Hartree')
    print(f'{MagicNo*Etemp:.2f} kcal/mol\n')

print('\n##### Wells #####\n')
for well in WellLocationDict:
    print(well)
    Etemp = EnergyDict[well] - E0
    print(f'{Etemp:.2e} Hartree')
    print(f'{MagicNo*Etemp:.2f} kcal/mol\n')

print('\n##### Transition States #####\n')
for TS in TSLocationDict:
    print(TS)
    Etemp = EnergyDict[TS] - E0
    print(f'{Etemp:.2e} Hartree')
    print(f'{MagicNo*Etemp:.2f} kcal/mol\n')
    R = ReactantDict[TS] #convention is that these are always wells
    print(f'\tBarrier to {R}')
    Etemp = EnergyDict[TS] - EnergyDict[R]
    print(f'\t{Etemp:.2e} Hartree')
    print(f'\t{MagicNo*Etemp:.2f} kcal/mol\n')
    P1 = ProductDict[TS]
    try:
        #check if bimolecular
        P2 = BimolecDict[P1]
        Etemp = EnergyDict[TS] - (EnergyDict[P1] + EnergyDict[P2])
        name = P1 + ' + ' + P2
    except:
        #it's a well
        Etemp = EnergyDict[TS] -  EnergyDict[P1]
        name = P1
    print(f'\tBarrier to {name}')
    print(f'\t{Etemp:.2e} Hartree')
    print(f'\t{MagicNo*Etemp:.2f} kcal/mol\n')

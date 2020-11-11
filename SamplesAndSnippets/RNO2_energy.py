#! /usr/bin/env python
#
#    RNO2_energy.py: a template for organizing calculation results
#    return energies and phase-space fits, barrier heights by reading current results
#    goal is to be more systematic and less error-prone
#    this is an updated version of mess_energy.py utilizing the messmanager in the
#    top directory
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
#    RNO2_energy.py  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.

#information for R+NO2 project

from FileParsers import *
from PhaseSpaceFit import PhaseSpaceFit
from messmanager import messmanager

MagicNo = 627.5095 #(kcal/mol)/hartree

toplevel = '/home/fuller/Dropbox/Documents/PCFC/CompChem/structures/HPC_sync/'

R = 'c2h5'#'n-pentane'

#define extensions based on chosen methods for project
ext_dft = '_b2plypd3_ccpvtz.log'
ext_spe = ext_dft.replace('.log','_f12_tz.orca.out')
ext_dft_NO = ext_dft.replace('.log', '_scan_RO_NO_rigid.log')
ext_dft_NO2 = ext_dft.replace('.log', '_scan_R_NO2_rigid.log')
scantype = 'rigid'


#list locations in file tree relative to toplevel
WellLocationDict = {}
FragLocationDict = {}
TSLocationDict = {}
BimolecDict={}

#fragments
FragLocationDict['no'] = 'no/no'
FragLocationDict['no2'] = 'no/no2'
FragLocationDict['hno'] = 'noh/hno'
FragLocationDict['hono'] = 'noh/antihono'


if R == 'ch3':
    FragLocationDict['ch3'] = 'ch/c1/ch3'
    FragLocationDict['ch3o'] = 'coh/c1o1/ch3o'
    FragLocationDict['ch2o'] = 'coh/c1o1/ch2o'
    BimolecDict['ch3'] = 'no2'
    BimolecDict['ch3o'] = 'no'
    BimolecDict['ch2o'] = 'hno'
    WellLocationDict['nitromethane'] = 'cnoh/c1n1o2/ch3no2'
    WellLocationDict['methylnitrite'] = 'cnoh/c1n1o2/ch3ono'

    TSlevel = 'cnoh/c1n1o2/ts/'
    TSLocationDict['ts_nitromethane_methylnitrite'] = 'ts_nitromethane_to_methylnitrite'
    TSLocationDict['ts_methylnitrite_ch2o'] = 'ts_methylnitrite_to_hno_methanal'
    TSLocationDict['ts_nitromethane_ch3'] = 'pst'
    TSLocationDict['ts_methylnitrite_ch3'] = 'pst'
    TSLocationDict['ts_methylnitrite_ch3o'] = 'pst'

elif R == 'c2h5':
    FragLocationDict['c2h5'] = 'ch/c2/c2h5'
    FragLocationDict['c2h4'] = 'ch/c2/c2h4'
    FragLocationDict['c2h5o'] = 'coh/c2o1/c2o1h5/c2h5o'
    FragLocationDict['ch3cho'] = 'coh/c2o1/ch3cho'
    BimolecDict['c2h5'] = 'no2'
    BimolecDict['c2h4'] = 'hono'
    BimolecDict['c2h5o'] = 'no'
    BimolecDict['ch3cho'] = 'hno'
    WellLocationDict['nitroethane'] = 'cnoh/c2n1o2/c2h5no2'
    WellLocationDict['ethylnitrite'] = 'cnoh/c2n1o2/c2h5ono'

    TSlevel = 'cnoh/c2n1o2/ts/'
    TSLocationDict['ts_nitroethane_ethylnitrite'] = 'ts_nitroethane_to_ethylnitrite'
    TSLocationDict['ts_nitroethane_c2h4'] = 'ts_nitroethane_to_hono_ethene'
    TSLocationDict['ts_ethylnitrite_ch3cho'] = 'ts_ethylnitrite_to_hno_ethanal'
    TSLocationDict['ts_nitroethane_c2h5'] = 'pst'
    TSLocationDict['ts_ethylnitrite_c2h5'] = 'pst'
    TSLocationDict['ts_ethylnitrite_c2h5o'] = 'pst'

elif R == 'nc3h7':
    FragLocationDict['nc3h7'] = 'ch/c3/nc3h7'
    FragLocationDict['propene'] = 'ch/c3/propene'
    FragLocationDict['nc3h7o'] = 'coh/c3o1/nc3h7o'
    FragLocationDict['propanal'] = 'coh/c3o1/propanal'
    BimolecDict['nc3h7'] = 'no2'
    BimolecDict['propene'] = 'hono'
    BimolecDict['nc3h7o'] = 'no'
    BimolecDict['propanal'] = 'hno'
    WellLocationDict['nitropropane'] = 'cnoh/c3n1o2/nc3h7no2'
    WellLocationDict['1-propylnitrite'] = 'cnoh/c3n1o2/nc3h7ono'

    TSlevel = 'cnoh/c3n1o2/ts/'
    TSLocationDict['ts_nitropropane_1-propylnitrite'] = 'ts_nitropropane_to_1-propylnitrite'
    TSLocationDict['ts_nitropropane_propene'] = 'ts_nitropropane_to_hono_propene'
    TSLocationDict['ts_1-propylnitrite_propanal'] = 'ts_1-propylnitrite_to_hno_propanal'
    TSLocationDict['ts_nitropropane_nc3h7'] = 'pst'
    TSLocationDict['ts_1-propylnitrite_nc3h7'] = 'pst'
    TSLocationDict['ts_1-propylnitrite_nc3h7o'] = 'pst'

elif R == 'ic3h7':
    FragLocationDict['ic3h7'] = 'ch/c3/ic3h7'
    FragLocationDict['propene'] = 'ch/c3/propene'
    FragLocationDict['ic3h7o'] = 'coh/c3o1/ic3h7o'
    FragLocationDict['propanal'] = 'coh/c3o1/propanal'
    BimolecDict['ic3h7'] = 'no2'
    BimolecDict['propene'] = 'hono'
    BimolecDict['ic3h7o'] = 'no'
    BimolecDict['propanal'] = 'hno'
    WellLocationDict['2-nitropropane'] = 'cnoh/c3n1o2/ic3h7no2'
    WellLocationDict['2-propylnitrite'] = 'cnoh/c3n1o2/ic3h7ono'

    TSlevel = 'cnoh/c3n1o2/ts/'
    TSLocationDict['ts_2-nitropropane_2-propylnitrite'] = 'ts_2-nitropropane_to_2-propylnitrite'
    TSLocationDict['ts_2-nitropropane_propene'] = 'ts_2-nitropropane_to_hono_propene'
    TSLocationDict['ts_2-propylnitrite_acetone'] = 'ts_2-propylnitrite_to_hno_acetone'
    TSLocationDict['ts_2-nitropropane_ic3h7'] = 'pst'
    TSLocationDict['ts_2-propylnitrite_ic3h7'] = 'pst'
    TSLocationDict['ts_2-propylnitrite_ic3h7o'] = 'pst'

elif R == 'pc4h9':
    FragLocationDict['pc4h9'] = 'ch/c4/pc4h9'
    FragLocationDict['1-butene'] = 'ch/c4/1-butene'
    FragLocationDict['pc4h9o'] = 'coh/c4o1/pc4h9o'
    FragLocationDict['butanal'] = 'coh/c4o1/butanal'
    BimolecDict['pc4h9'] = 'no2'
    BimolecDict['1-butene'] = 'hono'
    BimolecDict['pc4h9o'] = 'no'
    BimolecDict['butanal'] = 'hno'
    WellLocationDict['1-nitrobutane'] = 'cnoh/c4n1o2/pc4h9no2'
    WellLocationDict['1-butylnitrite'] = 'cnoh/c4n1o2/pc4h9ono'

    TSlevel = 'cnoh/c4n1o2/ts/'
    TSLocationDict['ts_1-nitrobutane_1-butylnitrite'] = 'ts_1-nitrobutane_to_1-butylnitrite'
    TSLocationDict['ts_1-nitrobutane_1-butene'] = 'ts_1-nitrobutane_to_hono_1-butene'
    TSLocationDict['ts_1-butylnitrite_butanal'] = 'ts_1-butylnitrite_to_hno_butanal'
    TSLocationDict['ts_1-nitrobutane_pc4h9'] = 'pst'
    TSLocationDict['ts_1-butylnitrite_pc4h9'] = 'pst'
    TSLocationDict['ts_1-butylnitrite_pc4h9o'] = 'pst'

elif R == 'sc4h9':
    FragLocationDict['sc4h9'] = 'ch/c4/sc4h9'
    FragLocationDict['1-butene'] = 'ch/c4/1-butene'
    FragLocationDict['2-butene'] = 'ch/c4/2-butene'
    FragLocationDict['sc4h9o'] = 'coh/c4o1/sc4h9o'
    FragLocationDict['butanal'] = 'coh/c4o1/butanal'
    BimolecDict['sc4h9'] = 'no2'
    BimolecDict['1-butene'] = 'hono'
    BimolecDict['2-butene'] = 'hono'
    BimolecDict['sc4h9o'] = 'no'
    BimolecDict['butanal'] = 'hno'
    WellLocationDict['2-nitrobutane'] = 'cnoh/c4n1o2/sc4h9no2'
    WellLocationDict['2-butylnitrite'] = 'cnoh/c4n1o2/sc4h9ono'

    TSlevel = 'cnoh/c4n1o2/ts/'
    TSLocationDict['ts_2-nitrobutane_2-butylnitrite'] = 'ts_2-nitrobutane_to_2-butylnitrite'
    TSLocationDict['ts_2-nitrobutane_1-butene'] = 'ts_2-nitrobutane_to_hono_1-butene'
    TSLocationDict['ts_2-nitrobutane_2-butene'] = 'ts_2-nitrobutane_to_hono_2-butene'
    TSLocationDict['ts_2-butylnitrite_butanal'] = 'ts_2-butylnitrite_to_hno_butanal'
    TSLocationDict['ts_2-nitrobutane_sc4h9'] = 'pst'
    TSLocationDict['ts_2-butylnitrite_sc4h9'] = 'pst'
    TSLocationDict['ts_2-butylnitrite_sc4h9o'] = 'pst'

elif R == '1-pentyl':
    FragLocationDict['1-pentyl'] = 'ch/c5/c5h11/n-c5h11-1'
    FragLocationDict['1-pentyloxy'] = 'coh/c5o1/n-c5h11o-1/n-c5h11o-1'
    FragLocationDict['pentanal'] = 'coh/c5o1/pc4h9cho/pc4h9cho'
    FragLocationDict['1-pentene'] = 'ch/c5/c5h10/c5h10-1'
    BimolecDict['1-pentyl'] = 'no2'
    BimolecDict['1-pentyloxy'] = 'no'
    BimolecDict['pentanal'] = 'hno'
    BimolecDict['1-pentene'] = 'hono'
    WellLocationDict['1-nitropentane'] = 'cnoh/c5n1o2/nitropentan-1'
    WellLocationDict['1-pentylnitrite'] = 'cnoh/c5n1o2/pentylnitrite-1'

    TSlevel = 'cnoh/c5n1o2/ts/'
    TSLocationDict['ts_1-nitropentane_1-pentylnitrite'] = 'ts_nitropentan-1_to_pentylnitrite-1'
    TSLocationDict['ts_1-pentylnitrite_pentanal'] = 'ts_pentylnitrite-1_to_hno_pentanal'
    TSLocationDict['ts_1-nitropentane_1-pentene'] = 'ts_nitropentan-1_to_hono_pentene-1'
    TSLocationDict['ts_1-nitropentane_1-pentyl'] = 'pst'
    TSLocationDict['ts_1-pentylnitrite_1-pentyl'] = 'pst'
    TSLocationDict['ts_1-pentylnitrite_1-pentyloxy'] = 'pst'

elif R == '2-pentyl':
    FragLocationDict['2-pentyl'] = 'ch/c5/c5h11/n-c5h11-2'
    FragLocationDict['2-pentyloxy'] = 'coh/c5o1/n-c5h11o-2/n-c5h11o-2'
    FragLocationDict['2-pentanone'] = 'coh/c5o1/nc3h7coch3/nc3h7coch3'
    FragLocationDict['1-pentene'] = 'ch/c5/c5h10/c5h10-1'
    FragLocationDict['2-pentene'] = 'ch/c5/c5h10/c5h10-2'
    BimolecDict['2-pentyl'] = 'no2'
    BimolecDict['2-pentyloxy'] = 'no'
    BimolecDict['2-pentanone'] = 'hno'
    BimolecDict['1-pentene'] = 'hono'
    BimolecDict['2-pentene'] = 'hono'
    #WellLocationDict['2-nitropentane'] = 'cnoh/c5n1o2/nitropentan-2'
    #WellLocationDict['2-pentylnitrite'] = 'cnoh/c5n1o2/pentylnitrite-2'

    TSlevel = 'cnoh/c5n1o2/ts/'
    #TSLocationDict['ts_2-nitropentane_2-pentylnitrite'] = 'ts_nitropentan-2_to_pentylnitrite-2'
    #TSLocationDict['ts_2-pentylnitrite_2-pentanone'] = 'ts_pentylnitrite-2_to_hno_pentanone-2'
    #TSLocationDict['ts_2-nitropentane_1-pentene'] = 'ts_nitropentan-2_to_hono_pentene-1'
    #TSLocationDict['ts_2-nitropentane_2-pentene'] = 'ts_nitropentan-2_to_hono_pentene-2'
    TSLocationDict['ts_2-nitropentane_2-pentyl'] = 'pst'
    TSLocationDict['ts_2-pentylnitrite_2-pentyl'] = 'pst'
    TSLocationDict['ts_2-pentylnitrite_2-pentyloxy'] = 'pst'

elif R == '3-pentyl':
    FragLocationDict['3-pentyl'] = 'ch/c5/c5h11/n-c5h11-3'
    FragLocationDict['3-pentyloxy'] = 'coh/c5o1/n-c5h11o-3/n-c5h11o-3'
    FragLocationDict['3-pentanone'] = 'coh/c5o1/c2h5coc2h5/c2h5coc2h5'
    FragLocationDict['2-pentene'] = 'ch/c5/c5h10/c5h10-2'
    BimolecDict['3-pentyl'] = 'no2'
    BimolecDict['3-pentyloxy'] = 'no'
    BimolecDict['3-pentanone'] = 'hno'
    BimolecDict['2-pentene'] = 'hono'
    WellLocationDict['3-nitropentane'] = 'cnoh/c5n1o2/nitropentan-3'
    WellLocationDict['3-pentylnitrite'] = 'cnoh/c5n1o2/pentylnitrite-3'

    #transition states
    TSlevel = 'cnoh/c5n1o2/ts/'
    TSLocationDict['ts_3-nitropentane_3-pentylnitrite'] = 'ts_nitropentan-3_to_pentylnitrite-3'
    TSLocationDict['ts_3-pentylnitrite_3-pentanone'] = 'ts_pentylnitrite-3_to_hno_pentanone-3'
    TSLocationDict['ts_3-nitropentane_2-pentene'] = 'ts_nitropentan-3_to_hono_pentene-2'
    TSLocationDict['ts_3-nitropentane_3-pentyl'] = 'pst'
    TSLocationDict['ts_3-pentylnitrite_3-pentyl'] = 'pst'
    TSLocationDict['ts_3-pentylnitrite_3-pentyloxy'] = 'pst'

elif R == '1-hydroxyethyl':
    FragLocationDict['1-hydroxyethyl'] = 'coh/c2o1/c2o1h5/c2h4oh-1'
    FragLocationDict['1-hydroxyethyloxy'] = 'coh/c2o2/hydroxyethyloxy-1'
    FragLocationDict['aceticacid'] = 'coh/c2o2/aceticacid'
    FragLocationDict['ethenol'] = 'coh/c2o1/ethenol'
    BimolecDict['1-hydroxyethyl'] = 'no2'
    BimolecDict['1-hydroxyethyloxy'] = 'no'
    BimolecDict['aceticacid'] = 'hno'
    BimolecDict['ethenol'] = 'hono'
    WellLocationDict['1-nitroethanol'] = 'cnoh/c2n1o3/nitroethanol-1'
    WellLocationDict['1-hydroxyethylnitrite'] = 'cnoh/c2n1o3/hydroxyethylnitrite-1'

    TSlevel = 'cnoh/c2n1o3/ts/'
    TSLocationDict['ts_1-nitroethanol_1-hydroxyethylnitrite'] = 'ts_nitroethanol-1_to_hydroxyethylnitrite-1'
    TSLocationDict['ts_1-hydroxyethylnitrite_aceticacid'] = 'ts_hydroxyethylnitrite-1_to_hno_aceticacid'
    TSLocationDict['ts_1-nitroethanol_ethenol'] = 'ts_nitroethanol-1_to_hono_ethenol'
    TSLocationDict['ts_1-nitroethanol_1-hydroxyethyl'] = 'pst'
    TSLocationDict['ts_1-hydroxyethylnitrite_1-hydroxyethyl'] = 'pst'
    TSLocationDict['ts_1-hydroxyethylnitrite_1-hydroxyethyloxy'] = 'pst'

elif R == '2-hydroxyethyl':
    FragLocationDict['2-hydroxyethyl'] = 'coh/c2o1/c2o1h5/c2h4oh-2'
    FragLocationDict['2-hydroxyethyloxy'] = 'coh/c2o2/hydroxyethyloxy-2'
    FragLocationDict['2-hydroxyethanal'] = 'coh/c2o2/hydroxyethanal'
    FragLocationDict['ethenol'] = 'coh/c2o1/ethenol'
    BimolecDict['2-hydroxyethyl'] = 'no2'
    BimolecDict['2-hydroxyethyloxy'] = 'no'
    BimolecDict['2-hydroxyethanal'] = 'hno'
    BimolecDict['ethenol'] = 'hono'
    WellLocationDict['2-nitroethanol'] = 'cnoh/c2n1o3/nitroethanol-2'
    WellLocationDict['2-hydroxyethylnitrite'] = 'cnoh/c2n1o3/hydroxyethylnitrite-2'

    TSlevel = 'cnoh/c2n1o3/ts/'
    TSLocationDict['ts_2-nitroethanol_2-hydroxyethylnitrite'] = 'ts_nitroethanol-2_to_hydroxyethylnitrite-2'
    TSLocationDict['ts_2-hydroxyethylnitrite_2-hydroxyethanal'] = 'ts_hydroxyethylnitrite-2_to_hno_hydroxyethanal-2'
    TSLocationDict['ts_2-nitroethanol_ethenol'] = 'ts_nitroethanol-2_to_hono_ethenol'
    TSLocationDict['ts_2-nitroethanol_2-hydroxyethyl'] = 'pst'
    TSLocationDict['ts_2-hydroxyethylnitrite_2-hydroxyethyl'] = 'pst'
    TSLocationDict['ts_2-hydroxyethylnitrite_2-hydroxyethyloxy'] = 'pst'
#elif RH == 'butanone':

#get raw energy values (Hartree)
EnergyDict = {}
for S, loc in FragLocationDict.items():
    EnergyDict[S] = get_energy(toplevel+loc+ext_dft, toplevel+loc+ext_spe)
for S, loc in WellLocationDict.items():
    EnergyDict[S] = get_energy(toplevel+loc+ext_dft, toplevel+loc+ext_spe)
for S, loc in TSLocationDict.items():
    if loc != 'pst':
        EnergyDict[S] = get_energy(toplevel+TSlevel+loc+ext_dft, toplevel+TSlevel+loc+ext_spe)

E0 = EnergyDict['no2'] + EnergyDict[R]

#common code to run through systems
messmanager(FragLocationDict, WellLocationDict, TSLocationDict, BimolecDict, EnergyDict, E0, toplevel, ext_dft_NO, ext_dft_NO2, scantype)

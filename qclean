#!/bin/bash
# A housekeeping script for deleting unneeded files from QChem calculations
# M.E. Fuller, DEC 2019

#go to the appropriate top-level directory
cd ~/qchem/

#remove submission scripts
find . -type f -name 'job*.sh' -delete
find . -type f -name 'script*.sh' -delete

#remove unneeded Gaussian output
find . -name '*scan*.fchk' -delete
find . -name '*.chk' -delete #uncomment only when no Gaussian jobs currently running and no IRCs to do

#remove scan input prep
find . -name '*scan_.gjf' -delete

#remove unneeded Orca output
find . -name '*f12_tz.gbw' -delete #uncomment only when no Orca jobs currently running
find . -name '*f12_tz.loc' -delete #uncomment only when no Orca jobs currently running

#remove unneeded cluster output
find . -type f -name 'core.*.hpc.itc.rwth-aachen.de.*' -delete #uncomment only when no jobs currently running

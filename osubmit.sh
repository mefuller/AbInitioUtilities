#!/bin/bash
#    osubmit: a submission script for ORCA jobs via slurm
#    derived from the multi-purpose submission script written by Malte Döntgen
#    this version is a template script and should be modified as appropriate
#    Usage: $ osubmit file1.inp file2.inp ...
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
#    osubmit  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################
# submit script for ORCA jobs: takes Orca input file and generates submission script and submits job to slurm
# M.E. Fuller, DEC 2019
# derived from the multi-purpose submission script written by Malte Döntgen
# this version is a template script and should be modified as appropriate
# Usage: $ osubmit file1.inp file2.inp ...

EMAIL=mark.e.fuller@gmx.de
HASACCT=true
ACCTNUM=rwth0453

TIME=10		# hours

args=("$@")
COUNTER=1
until [ $COUNTER -gt $# ]; do
	# . receive job name / directly submit Gaussian job
	SUBMIT=true
	if [[ ${args[COUNTER-1]} == *".inp"* ]]; then
		FILENAME=${args[COUNTER-1]%.inp}
	else 
	    SUBMIT=false
	fi

	# . create ORCA / MOLPRO job files
	if [ "$SUBMIT" = true ]; then
		DIR=$PWD
		JOB=job_$FILENAME.sh

		rm -f $JOB #wipeout old script if present; force flag accounts for file not existing

		# . write job file
		echo "#!/usr/local_rwth/bin/zsh" >> $JOB
		echo "#SBATCH --job-name=${FILENAME}" >> $JOB
		echo "#SBATCH --output=${FILENAME}.out" >> $JOB
		echo "#SBATCH --error=${FILENAME}.err" >> $JOB
		echo "#SBATCH --time=${TIME}:00:00" >> $JOB
		echo "#SBATCH --ntasks=12" >> $JOB
		echo "#SBATCH --mem-per-cpu=5000" >> $JOB 
		echo "#SBATCH --nodes=1" >> $JOB
		echo "#SBATCH --cpus-per-task=1" >> $JOB
		echo "#SBATCH --mail-user=${EMAIL}" >> $JOB
        echo "#SBATCH --mail-type=ALL" >> $JOB
		#
		if [ "$HASACCT" = true ]; then
		    ### PUT YOUR RWTH HPC PROJECT NAME HERE; format rwthXXXX, cf. below
		    echo "#SBATCH --account=${ACCTNUM}" >> $JOB
		fi
		#

		echo "SDIR=`pwd`" >> $JOB
		echo 'echo "Submission directory is: $SDIR"' >> $JOB
		echo 'echo "The job ID assigned by the Batch system is: $SLURM_JOBID"' >> $JOB
		echo 'echo "Number of requested processes: $SLURM_NPROCS"' >> $JOB

    	# NEW ORCA VERSION
    	echo 'module switch intelmpi openmpi/3.1.4' >> $JOB
    	echo 'ulimit -s unlimited' >> $JOB
    	echo 'ulimit -m unlimited' >> $JOB
    	echo 'export OMPI_MCA_btl=^openib' >> $JOB		    		
		#
		echo 'TOORCA=$HOME/qchem/ORCA/orca_4_2_1_linux_x86-64_shared_openmpi314' >> $JOB
   		echo 'PATH=$PATH:$TOORCA' >> $JOB
    	echo 'LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$TOORCA' >> $JOB
		### PUT YOUR ABSOLUTE PATH TO ORCA EXECUTABLE HERE
		printf '$TOORCA/orca %b.inp > %b.orca.out\n' $FILENAME $FILENAME >> $JOB
		###
		#
		printf 'rm -rf %b*.tmp*' $FILENAME >> $JOB

		
		echo "" >> $JOB

		# . submit job
		sbatch $JOB
	fi

	# . next job
	COUNTER=$((COUNTER + 1))
done


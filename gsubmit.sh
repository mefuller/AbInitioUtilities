#!/bin/bash
# 
#    gsubmit: a submission script for Gaussian jobs via slurm
#    derived from the multi-purpose submission script written by Malte Döntgen
#    this version is a template script and should be modified as appropriate
#    Usage: $ gsubmit file1.gjf file2.com ...
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
#    gsubmit  Copyright (C) 2020  Mark E. Fuller
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.


################################################################################

EMAIL=mark.e.fuller@gmx.de
HASACCT=true
ACCTNUM=rwth0453

TIME=2	# days

args=("$@")
COUNTER=1
until [ $COUNTER -gt $# ]; do
	# . receive job name
	SUBMIT=true
	if [[ ${args[COUNTER-1]} == *".gjf"* ]]; then
		FILENAME=${args[COUNTER-1]%.gjf}
		EXT="gjf"
	elif [[ ${args[COUNTER-1]} == *".com"* ]]; then
		FILENAME=${args[COUNTER-1]%.com}
		EXT="com"
	else 
	    SUBMIT=false
	fi

	# . create submission script
	if [ "$SUBMIT" = true ]; then
		DIR=$PWD
		JOB=script_$FILENAME.sh

		rm -f $JOB #wipeout old script if present; force flag accounts for file not existing
		
		# . write job file
		echo "#!/usr/local_rwth/bin/zsh" >> $JOB
		echo "#SBATCH --job-name=${FILENAME}" >> $JOB
		echo "#SBATCH --output=${FILENAME}.out" >> $JOB
		echo "#SBATCH --error=${FILENAME}.err" >> $JOB
		echo "#SBATCH --time=${TIME}-00:00:00" >> $JOB
		echo "#SBATCH --nodes=1" >> $JOB
		echo "#SBATCH --cpus-per-task=12" >> $JOB
		echo "#SBATCH --mem-per-cpu=2000M" >> $JOB
		echo "#SBATCH --mail-user=${EMAIL}" >> $JOB
        echo "#SBATCH --mail-type=ALL" >> $JOB
		#
		if [ "$HASACCT" = true ]; then
		    ### PUT YOUR RWTH HPC PROJECT NAME HERE; format rwthXXXX, cf. below
		    echo "#SBATCH --account=${ACCTNUM}" >> $JOB
		fi
		###
		#
		echo "" >> $JOB
		echo "module load CHEMISTRY" >> $JOB
		echo "module load gaussian/16.c01_bin" >> $JOB
		echo "srun g16 < ${FILENAME}.${EXT} > ${FILENAME}.log" >> $JOB
		echo "formchk ${FILENAME}.chk ${FILENAME}.fchk" >> $JOB
		#echo "rm ${FILENAME}.chk" >> $JOB
		echo "" >> $JOB

		# . submit job
		sbatch $JOB
	fi

	# . next job
	COUNTER=$((COUNTER + 1))
done


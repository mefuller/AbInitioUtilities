#!/bin/bash
# run on successfully-completed Gaussian log file(s)
# print energies, make scan template, and write/submit single-point calculation
# Usage: $ zweifliege file1.log file2.log ...
# M.E. Fuller, APR 2020

args=("$@")
COUNTER=1
until [ $COUNTER -gt $# ]; do
	# . receive job name
	SUBMIT=true
	if [[ ${args[COUNTER-1]} == *".log"* ]]; then
		FILENAME=${args[COUNTER-1]%.log}
	else
	    SUBMIT=false
	fi

	if [ "$SUBMIT" = true ]; then
		extractdft.py $FILENAME.log
		writescan.py $FILENAME.log
		writeorca.py $FILENAME.log
		osubmit.sh $FILENAME\_ccsdt_tz.inp
		osubmit.sh $FILENAME\_ccsdt_qz.inp
		#osubmit $FILENAME*.inp
	fi

	COUNTER=$((COUNTER + 1))
done

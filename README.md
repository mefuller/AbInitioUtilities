# AbInitioUtilities
Utility scripts and functions for use with ab initio and chemical kinetics packages

This project contains scripts and functions developed to ease the tedium of preparing input and analyzing output in conjunction with ab initio and chemical kinetics software packages.
At present, workflow is envisioned as submitting geometry and frequency jobs to Gaussian 09/16, followed by single-point energy calculations in Molpro or Orca, and then kinetics calculations with TAMkin or MESS/PAPR.

In addition to functions or scripts which should work as drop-ins with no modification, some example scripts that are facility or path dependent are included which allow easy modification.
These scripts, such as automatic job file creation and submission to slurm, could and should be developed into separate functions and configuration files for broader distribution.

Finally, I'm a hack when it comes to programming.
Virtually all functions and scripts in this project are modifications of routines and ideas developed and implemented originally by Prof. C. Franklin Goldsmith (Argonne National Laboratory / Brown University), Aaron Danliack (Brown University), and/or Malte Döntgen (Brown University / RWTH Aachen).

Happy (transition state) hunting,

Mark E. Fuller
mark.e.fuller@gmail.com
15 April 2020

# AbInitioUtilities
Utility scripts and functions for use with ab initio and chemical kinetics packages

This project contains scripts and functions developed to ease the tedium of preparing input and analyzing output in conjunction with ab initio and chemical kinetics software packages.
At present, workflow is envisioned as submitting geometry and frequency jobs to Gaussian 09/16, followed by single-point energy calculations in Molpro or Orca, and then kinetics calculations with TAMkin or MESS/PAPR.

In addition to functions or scripts which should work as drop-ins with no modification, some example scripts that are facility or path dependent are included which allow easy modification.
These scripts, such as automatic job file creation and submission to slurm, could and should be developed into separate functions and configuration files for broader distribution.

Finally, I'm a hack when it comes to programming.
Virtually all functions and scripts in this project are modifications of routines and ideas developed and implemented originally by Prof. C. Franklin Goldsmith (Argonne National Laboratory / Brown University), Aaron Danliack (Brown University), and/or Malte Döntgen (Brown University / RWTH Aachen).
At some point I hope to package this in a way that the folder structure can just be copied somewhere in the Python path and everything will "just work", but I'm not quite there yet.

Finally, as a convention, files with no extension are intended to be command line executables (with files supplied as input arguments) and python functions utilized in those executables (and also available for inclusion in other scripts or tools) are properly named and appended with '.py'.

Happy (transition state) hunting,

Mark E. Fuller
mark.e.fuller@gmx.de
15 April 2020
Rev. 28 September 2020

#! /usr/bin/env python
"""
open column data of T, k for unimolecular dissociation and fit
modded from CFG H-abstraction bimolecular fitting script
"""
import os, sys
import numpy
import scipy
#import pylab
#import pylab 
#import matplotlib.gridspec as gridspec
#import matplotlib.pyplot as pyplot
#from scipy import optimize
#from scipy.optimize import curve_fit
#from scipy.optimize import leastsq
#from scipy.optimize import fmin as simplex
#from numpy import linalg
#from numpy import random
#from scipy import stats

class paper:
	start_here = 0
	color_list = ['BurlyWood','Blue','Red','Fuchsia','Chartreuse','Black','Aqua','DarkGray','Gold']
	Tmin = 0.0
	Tmax = 1.0E4
class reaction:
	theory = 0.0
	
class fit_type:
	style = 'single'


####################################################################################################

#initialize the class in which to store the results
print '\n'
data = paper()
data.reactions = []
# set some constants, depending upon whether the rate coefficients are to be used for CHEMKIN or something else.
chemkin = 1
if chemkin==1:
    data.T0 = 1.0
    data.R = 1.987 # cal/mol-K.  Note that PLOG formalism requires Ea in cal/mol-K!
    data.N_avo = 6.0221415E23 #convert bimolecular rate coefficients from cm^3/sec to cm^3/mol/s
elif chemkin==0:
    data.T0 = 298.0
    data.R = 1.0 # K^-1.
    data.N_avo = 1.0  #leave bimolecular rate coefficients in cm^3/sec

# set the minimum and maximum temperature
#data.Tmin = 600.0
#data.Tmax = 1200.0

# read me.out file from the command line
command_line = sys.argv[1:]

me_dot_out = command_line[0]
results = open(me_dot_out,'r')
lines = results.readlines()
results.close()

NT = 231#len(lines)-3

local_T = []
local_kfwd = []
#local_krev = []

for i in range(NT):
	bits = lines[i+14].split()
	local_T.append(bits[0])
	local_kfwd.append(bits[2])
#	local_krev.append(bits[2])

T = numpy.array(local_T,dtype=numpy.float64)
k_fwd = numpy.array(local_kfwd,dtype=numpy.float64)
#k_rev = numpy.array(local_krev,dtype=numpy.float64)

threefit = False

if threefit:
    X = numpy.array( [ numpy.ones( len(T) ), numpy.log(T/data.T0), -1.0 / data.R / T ],dtype=numpy.float64 )
    X = X.transpose()
    theta_fwd = numpy.linalg.lstsq(X, numpy.log(k_fwd),rcond=None)[0]
    A_fwd = numpy.exp(theta_fwd[0])
    n_fwd = theta_fwd[1]
    Ea_fwd = theta_fwd[2]
    print "%s\t%5.2E    %8.2F    %2.1F\t\t"%(me_dot_out, A_fwd, n_fwd, Ea_fwd)
else:
    X = numpy.array( [ numpy.ones( len(T) ), -1.0 / data.R / T ],dtype=numpy.float64 )
    X = X.transpose()
    theta_fwd = numpy.linalg.lstsq(X, numpy.log(k_fwd),rcond=None)[0]
    A_fwd = numpy.exp(theta_fwd[0])
    Ea_fwd = theta_fwd[1]
    print "%s\t%5.2E    %2.1F\t\t"%(me_dot_out, A_fwd, Ea_fwd)

#theta_rev = numpy.linalg.lstsq(X, numpy.log(k_rev))[0]
#A_rev = numpy.exp(theta_rev[0])
#n_rev = theta_rev[1]
#Ea_rev = theta_rev[2]

#print "%s\t%5.2E    %8.2F    %2.1F\t\t"%(me_dot_out, A_fwd, n_fwd, Ea_fwd)#!k_rev: \t%5.2E    %8.2F    %2.1F"%(me_dot_out, A_fwd, n_fwd, Ea_fwd,A_rev, n_rev, Ea_rev)

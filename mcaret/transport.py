#!/usr/bin/env python

"""@package transport
"""

import numpy as np
import math

__author__ = "Kyle Beyer"

import exciton
import pairWiseRatePhysics

####################################################################
#
# Transport kernel
####################################################################


# given the choice of next event, updates the occupation function and tallies light output
def updateSystem( choice ,  occFunc , time , light_times):

    if choice == 0:
        occFunc.eliminateRandomSinglet()
        light_times.append(time)

    elif choice == 1:
        occFunc.eliminateRandomTriplet()
        light_times.append(time)

    elif choice == 2:
        occFunc.tripletAnnhilate()

    elif choice == 3:
        occFunc.singletQuench()

    elif choice == 4:
        ## transport - randomly choose an exciton to transport and hop it to an unnocupied neighboring cell
        # For now, do not distinguish between triplets and singlets
        occFunc.randomExcitonRandomWalk()

    return( occFunc , light_times)

# given an initial condition in the form of a list of singlets and triplets
# runs full kinetic monte carlo simualtion for N time steps
def transport( N  , ratePhysics , occFunc ):

    # to reconstruct pulse shape, every light emission will be time tagged
    light_times = []

    # start time at 0
    time = 0

    for i in range(N):
        # calculate rates
        rates = ratePhysics.getRates( occFunc )

        # get total rate and sample timestep from an exponential distribution
        totalRate = sum(rates)
        time = time - np.log( np.random.rand() ) / totalRate

        # select process from individual rates
        rates = rates / totalRate
        choice = np.random.choice(5, p=rates)

        if totalRate == 0:
            print("System relaxed")
            break

        occFunc , light_times = updateSystem( choice , occFunc , time , light_times )

    return(light_times)


#!/usr/bin/env python

"""@package transport
"""

import numpy as np
import math

__author__ = "Kyle Beyer"

import exciton
import pairWiseRatePhysics
from state import State

####################################################################
#
# Transport kernel
####################################################################


# given the choice of next event, updates the occupation function and tallies light output
def updateSystem( choice ,  occFunc , time ):

    numDecays = 0

    if choice == 0:
        occFunc.eliminateRandomSinglet()
        numDecays = 1

    elif choice == 1:
        occFunc.eliminateRandomTriplet()
        numDecays = 1

    elif choice == 2:
        occFunc.tripletAnnhilate()

    elif choice == 3:
        occFunc.singletQuench()

    elif choice == 4:
        ## transport - randomly choose an exciton to transport and hop it to an unnocupied neighboring cell
        # For now, do not distinguish between triplets and singlets
        occFunc.randomExcitonRandomWalk()

    return( numDecays )

# given an initial condition in the form of a list of singlets and triplets
# runs full kinetic monte carlo simualtion for N time steps
def transport( N  , ratePhysics , occFunc , outputFile ):

    # open output file
    with open(outputFile , "a") as output_file_object:
        occFunc.printInitialCondition( output_file_object  )

        # start time at 0
        time = 0

        for i in range(N):
            # calculate rates
            rates = ratePhysics.getRates( occFunc )

            # get total rate and sample timestep from an exponential distribution
            totalRate = sum(rates)
            deltaT = - np.log( np.random.rand() ) / totalRate
            if deltaT < 0:
                  print(totalRate)
            time = time + deltaT

            # select process from individual rates
            norm_rates = rates / totalRate
            choice = np.random.choice(5, p=norm_rates)

            if totalRate == 0:
                print("System relaxed")
                break

            numDecays = updateSystem( choice , occFunc , time )
            state = occFunc.getCurrentState(time , numDecays , rates)
            if choice == 4:
                state.printTransportStateLine( output_file_object )
            else:
                state.printStateLine( output_file_object )

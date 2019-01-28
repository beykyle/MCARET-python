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
# Functionality to randomly walk excitons to unnocupied neighboring
# orbitals
####################################################################

# helper class for doing hops in constrianed geometry
# kind of clunky but it is what it is
# available_dirs = [i+1 , i-1 , j+1 , j-1 , k+1 , k-1]
class Hopper:
    def __init__(self , exciton ):
        self.available_dirs = np.ones( 6 , dtype=bool)
        self.exciton = exciton

    def eliminatePathway(self , neighbor ):
        if self.exciton.i + 1 == neighbor.i:
            self.available_dirs[0] = False
            return None
        elif self.exciton.i - 1 == neighbor.i:
            self.available_dirs[1] = False
            return None
        elif self.exciton.j - 1 == neighbor.j:
            self.available_dirs[2] = False
            return None
        elif self.exciton.j + 1 == neighbor.j:
            self.available_dirs[3] = False
            return None
        elif self.exciton.k - 1 == neighbor.k:
            self.available_dirs[4] = False
            return None
        elif self.exciton.k + 1 == neighbor.k:
            self.available_dirs[5] = False
            return None

    def chooseDirectionAndHop(self):
        num_choices = np.sum(self.available_dirs)
        x = np.random.choice( num_choices )
        for i , val in enumerate( self.available_dirs ):
            if x == 0:
                self.doHop(i)

            if val == True:
                x = x - 1

        return(self.exciton)

    def doHop(self , i ):
        if i == 0:
            self.exciton.i = self.exciton.i +  1
        elif i == 1:
            self.exciton.i = self.exciton.i -  1
        elif i == 2:
            self.exciton.j = self.exciton.j +  1
        elif i == 3:
            self.exciton.j = self.exciton.j -  1
        elif i == 4:
            self.exciton.k = self.exciton.k +  1
        elif i == 5:
            self.exciton.k = self.exciton.k -  1

def checkAvailable( exciton , neighbors ,  other_excitons ):
    h = Hopper(exciton)
    for neighbor in neighbors:
        h.eliminatePathway( neighbor )
    for other_exciton in other_excitons:
        if areNeighbors( exciton , other_exciton ):
            h.eliminatePathway( other_exciton )
    return(h)

# hopping function
def hop( index , exciton , exciton_pairs , excitons , other_excitons ):
    redundant_relevant_pairs = [ pair for pair in exciton_pairs if (index == pair[0] or index == pair[1]) ]
    neighbors = [  ]
    for pair in redundant_relevant_pairs:
        if( pair[0] == index ):
            neighbors.append( excitons[pair[1]] )
        else:
            neighbors.append( excitons[pair[0]] )
    hopper = checkAvailable( exciton , neighbors , other_excitons )
    return( hopper.chooseDirectionAndHop() )


####################################################################
#
# Transport kernel
####################################################################


# given the choice of next event, updates the occupation function and tallies light output
def updateSystem( choice ,  occFunc , time , light_times):

    if choice == 0:
        light_times.append(time)

    elif choice == 1:
        light_times.append(time)

    elif choice == 2:
        #TT annhilate - uniformly random sample one of the triplet pairs to annhilate
        pass

    elif choice == 3:
        #SS quench - uniformly random sample one of the singlet pairs to annhilate
        pass

    elif choice == 4:
        ## transport - randomly choose an exciton to transport and hop it to an unnocupied neighboring cell
        # For now, do not distinguish between triplets and singlets
        p = np.random.choice( list( occFunc.keys()  ) )
        while not occFunc.randomSingleHop(p):
            p = np.random.choice( list( occFunc.keys() ) )

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

        occFunc , light_times = updateSystem( choice , occFunc , time , light_times )

    return(light_times)


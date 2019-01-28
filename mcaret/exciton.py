#!/usr/bin/env python

"""@package exciton
"""

import numpy as np
import math
import sys

__author__ = "Kyle Beyer"


sys.path.append('./visualization/')
import excitonPlotter

####################################################################
#
# Point definition
####################################################################

# point class
class Point:
    # constructor requires position in lattice
    def __init__(self, i,j,k):
        self.i = i
        self.j = j
        self.k = k

    # uses large primes to get a decent hash function
    # not injective but should minimize collisions
    def __hash__(self):
        return hash( self.i + 32416189717 * ( self. j +  15487291 * self.k ) )

    def __eq__(self , other ):
        if( other.i == self.i and other.j == self.j and other.k == self.k ):
            return(True)
        else:
            return(False)

    def __ne__(self , other):
        if( other.i == self.i and other.j == self.j and other.k == self.k ):
            return(False)
        else:
            return(True)

# Point iterator
# 0   ->   1   ->   2   ->  ...
# ijk -> i+1jk -> i-1jk -> ij+1k -> ij-1k -> ijk+1 -> ijk-1

####################################################################
#
# Initial condition
####################################################################

# given index ind and cube side length sLen, 'ravel' the index into 3D
# as if the linear index numbered along the i direction, then j, then k
def ravelCubicIndex(ind , sLen):
    k = ( ind + 1) // ( sLen * sLen )
    j = ( ind + 1 - k * sLen * sLen ) // sLen
    i = ( ind + 1 - k * sLen * sLen - j * sLen )
    return(i,j,k)

def randomInitialDistribution( numTriplets , numSinglets , sideLength , occFunc):
    # sample N_excitons w/o replacement along the linearized index
    unraveled_locations = np.random.choice(int(sideLength**3) , numSinglets + numTriplets , replace=False)

    # sample singlets
    for val in unraveled_locations[0:numTriplets]:
        i,j,k = ravelCubicIndex(val , sideLength)
        occFunc[ Point( i , j , k ) ] = False

    # sample triplets
    for val in unraveled_locations[numTriplets:numTriplets + numSinglets]:
        i,j,k = ravelCubicIndex(val , sideLength)
        occFunc[ Point( i , j , k ) ] = True

    #print("Plotting initial exciton distribution")
    #fig , ax = excitonPlotter.makeCommonAxis()
    #excitonPlotter.makePlot(ax , singlets , triplets)

    return( occFunc )

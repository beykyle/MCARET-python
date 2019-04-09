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
        self.i = int(i)
        self.j = int(j)
        self.k = int(k)

    # uses large primes to get a decent hash function
    # not injective but should minimize collisions
    def __hash__(self):
        return hash( int(self.i) + 32416189717 * ( int(self. j) +  15487291 * int(self.k) ) )

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

# given index ind and cube side length boundaryCondition, 'ravel' the index into 3D
# as if the linear index numbered along the i direction, then j, then k
def ravelCubicIndex(ind , boundaryCondition):
    k = ( ind + 1) // ( boundaryCondition.xMax * boundaryCondition.yMax )
    j = ( ind + 1 - k * boundaryCondition.xMax * boundaryCondition.yMax ) // boundaryCondition.xMax
    i = ( ind + 1 - k * boundaryCondition.xMax * boundaryCondition.yMax - j * boundaryCondition.xMax )
    return(i,j,k)

def randomInitialDistribution( numSinglets , numTriplets , singlets , triplets, boundaryCondition):
    # sample N_excitons w/o replacement along the linearized index
    l = boundaryCondition.xMax * boundaryCondition.yMax * boundaryCondition.zMax
    unraveledLocations = np.random.choice(int(l) , numSinglets + numTriplets , replace=False)

    # sample singlets
    for val in unraveledLocations[0:numSinglets]:
        i,j,k = ravelCubicIndex(val , boundaryCondition)
        singlets[ Point( i , j , k ) ]  = True

    # sample triplets
    for val in unraveledLocations[numSinglets:(numTriplets + numSinglets)]:
        i,j,k = ravelCubicIndex(val , boundaryCondition)
        triplets[ Point( i , j , k ) ] = True

    #print("Plotting initial exciton distribution")
    #fig , ax = excitonPlotter.makeCommonAxis()
    #excitonPlotter.makePlot(ax , singlets , triplets)

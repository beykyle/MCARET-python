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

def randomInitialDistribution( numTriplets , numSinglets , sideLength ):
    # sample N_excitons w/o replacement along the linearized index
    unraveled_locations = np.random.choice(int(sideLength**3) , numSinglets + numTriplets , replace=False)

    singlets = []
    triplets = []

    # sample singlets
    for val in unraveled_locations[0:numTriplets]:
        i,j,k = ravelCubicIndex(val , sideLength)
        triplets.append( Point(i,j,k) )

    # sample triplets
    for val in unraveled_locations[numTriplets:numTriplets + numSinglets]:
        i,j,k = ravelCubicIndex(val , sideLength)
        singlets.append( Point(i,j,k) )


    print("Plotting initial exciton distribution")
    fig , ax = excitonPlotter.makeCommonAxis()
    excitonPlotter.makePlot(ax , singlets , triplets)

    return( singlets , triplets )


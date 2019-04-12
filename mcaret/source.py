#!/usr/bin/env python

"""@package Source
"""

import numpy as np
import math
import sys

__author__ = "Kyle Beyer"

sys.path.append('./visualization/')
from exciton import Point
import excitonPlotter

####################################################################
#
# Initial condition
####################################################################

class Source:
    def __init__(self):
        pass

    def sample(self , numSinglets , numTriplets , singlets , triplets , plot=True):
        pass

class RandomRectangularSource(Source):
    def __init__( self , boundaryCondition ):
        self.boundaryCondition = boundaryCondition

    # given index ind and cube side length boundaryCondition, 'ravel' the index into 3D
    # as if the linear index numbered along the i direction, then j, then k
    def ravelCubicIndex(self , ind ):
        k = ( ind + 1) // ( self.boundaryCondition.xMax * self.boundaryCondition.yMax )
        j = ( ind + 1 - k * self.boundaryCondition.xMax * self.boundaryCondition.yMax ) // self.boundaryCondition.xMax
        i = ( ind + 1 - k * self.boundaryCondition.xMax * self.boundaryCondition.yMax - j * self.boundaryCondition.xMax )
        return(i,j,k)

    def sample(self,  numSinglets , numTriplets , singlets , triplets , plot=True):
        # sample N_excitons w/o replacement along the linearized index
        l = self.boundaryCondition.xMax * self.boundaryCondition.yMax * self.boundaryCondition.zMax
        unraveledLocations = np.random.choice(int(l) , numSinglets + numTriplets , replace=False)

        # sample singlets
        for val in unraveledLocations[0:numSinglets]:
            i,j,k = self.ravelCubicIndex(val , boundaryCondition)
            singlets[ Point( i , j , k ) ]  = True

        # sample triplets
        for val in unraveledLocations[numSinglets:(numTriplets + numSinglets)]:
            i,j,k = self.ravelCubicIndex(val , boundaryCondition)
            triplets[ Point( i , j , k ) ] = True

        if plot:
          print("Plotting initial exciton distribution")
          fig , ax = excitonPlotter.makeCommonAxis()
          excitonPlotter.makePlot(ax , singlets , triplets)

class TrackSource(Source):
    def __init__(self, start , end ):
        self.start = start
        self.end = end

    def randomRadialWalkResample(self,  excitons):
        # sample an initial point on the chord between  start and end
        xch = np.random.choice( np.arange( self.start.i , self.end.i)  , 1 )
        ych = self.start.j + int((self.end.j - self.start.j) * ( xch - self.start.i ) / (self.end.i - self.start.i))
        zch = self.start.k + int((self.end.k - self.start.k) * ( xch - self.start.i ) / (self.end.i - self.start.i))
        e = Point( xch , ych , zch )

        while e in excitons:
            # choose i j or k to adjust up or down
            ch = np.random.choice( [0,1,2,3,4,5] , 1 )
            if ch == 0:
                e.i = e.i + 1
            if ch == 1:
                e.i = e.i - 1
            if ch == 2:
                e.j = e.j + 1
            if ch == 3:
                e.j = e.j - 1
            if ch == 4:
                e.k = e.k + 1
            if ch == 5:
                e.k = e.k - 1

        excitons[e] = True

    def sample(self , numSinglets , numTriplets , singlets , triplets, plot=True):
        # run until all the singlets and triplets have been populated
        while( numSinglets > 0 and  numTriplets > 0 ):
            ptrip = numTriplets / ( numSinglets + numTriplets)
            if bool( np.random.choice( [0 ,1] , 1 ,  p=[ ptrip , 1 - ptrip ] ) ): # if a triplet
                numTriplets = numTriplets - 1
                self.randomRadialWalkResample( triplets  )
            else:
                numSinglets = numSinglets - 1
                self.randomRadialWalkResample( singlets)

        if plot:
          print("Plotting initial exciton distribution")
          fig , ax = excitonPlotter.makeCommonAxis()
          excitonPlotter.makePlot(ax , singlets , triplets, self.start , self.end)

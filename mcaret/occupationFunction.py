#!/usr/bin/env python

"""@package occupationFunction
"""

import numpy as np
import math
import sys
from collections import defaultdict


__author__ = "Kyle Beyer"

from exciton import Point

# True is triplet, false is singlet, None
class OccupationStatus:
    def __init__(singlet=True):
        self.singlet = False
        if singlet:
            self.singlet = True

class OccupationFunction:
    def __init__(self , numSinglets , numTriplets , initialConditionGenerator , sideLength ):
        occFunc = defaultdict(lambda: None)
        self.num_triplets = numTriplets
        self.num_singlets = numSinglets
        self.occFunc = initialConditionGenerator( numSinglets , numTriplets , sideLength ,  occFunc )

    def items(self):
        return( self.occFunc.items() )

    def keys(self):
        return( self.occFunc.keys() )

    def checkStatus(self , p , tripletNeighbors , singletNeighbors):
        if p in self.occFunc:
            status = self.occFunc[p]
            if status:
                tripletNeighbors.append(p)
            else:
                singletNeighbors.append(p)

        return( tripletNeighbors , singletNeighbors )

    def checkForNeighbors(self,  i , j , k ):
        singletNeighbors = []
        tripletNeighbors = []
        p  = Point( i + 1 , j , k)
        tripletNeighbors , singletNeighbors = self.checkStatus(p , tripletNeighbors , singletNeighbors)

        p  = Point( i - 1 , j , k)
        tripletNeighbors , singletNeighbors = self.checkStatus(p , tripletNeighbors , singletNeighbors)

        p  = Point( i  , j + 1 , k)
        tripletNeighbors , singletNeighbors = self.checkStatus(p , tripletNeighbors , singletNeighbors)

        p  = Point( i , j - 1, k)
        tripletNeighbors , singletNeighbors = self.checkStatus(p , tripletNeighbors , singletNeighbors)

        p  = Point( i , j , k + 1)
        tripletNeighbors , singletNeighbors = self.checkStatus(p , tripletNeighbors , singletNeighbors)

        p  = Point( i , j , k - 1)
        tripletNeighbors , singletNeighbors = self.checkStatus(p , tripletNeighbors , singletNeighbors)

        return( singletNeighbors , tripletNeighbors )

    def eliminateExciton( self, p ):
          del self.occFunc[p]

    # Attempts to randomly chooose from the unoccupied indices directly
    # neighboring p. If succesful, deletes the value at p in self.occFunc
    # and add the same value at the randomly chosen, neighboring  point,
    # and returns True.
    # If there are no unnoccupied neighboring indices, returns False
    def randomSingleHop( self , p ):
        i , j , k = p.i , p.j , p.k
        successfulMove = False
        numTries = 0

        # choose an order to try directions
        # [i+1,i-1,j+1,j-1,k+1,k-1]
        directions = np.random.choice(6,6 , replace=False)

        while successfulMove == False and numTries < 6:
            if directions[numTries] == 0:
                i =  i + 1
            elif directions[numTries] == 1:
                 i =  i - 1
            elif directions[numTries] == 2:
                 j = j + 1
            elif directions[numTries] == 3:
                 j = j - 1
            elif directions[numTries] == 4:
                 k = k + 1
            elif directions[numTries] == 5:
                 k = k - 1

            # increment try count
            numTries = numTries + 1

            # Check if new point is already occupied
            pNew = Point(i,j,k)
            if pNew not in self.occFunc:
                  successfulMove = True
                  # delete the old point and make a new one
                  self.occFunc[pNew] = self.occFunc[p]
                  del self.occFunc[p]

        return(successfulMove)

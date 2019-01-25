#!/usr/bin/env python

"""@package occupationFunction
"""

import numpy as np
import math
import sys

__author__ = "Kyle Beyer"

from exciton import Point

# True is triplet, false is singlet, None
class OccupationStatus:
    def __init__(singlet=True):
        self.singlet = False
        if singlet:
            self.singlet = True

class OccupationFunction:
    self.occFunc = defaultdict(lambda: None)

    def __init__( numSinglets , numTriplets , initialConditionGenerator ):
        self.occFunc = initialConditionGenerator( numSinglets , numTriplets )

    def checkForNeighbors( i , j , k ):
        singletNeighbors = []
        tripletNeighbors = []
        p  = Point( i + 1 , j , k)
        if self.occFunc[p] == True:
            tripletNeighbors.append(p)
        elif self.occFunc[p] == False:
            singletNeighbors.append(p)
        p  = Point( i - 1 , j , k)
        if self.occFunc[p] == True:
            tripletNeighbors.append(p)
        elif self.occFunc[p] == False:
            singletNeighbors.append(p)
        p  = Point( i  , j + 1 , k)
        if self.occFunc[p] == True:
            tripletNeighbors.append(p)
        elif self.occFunc[p] == False:
            singletNeighbors.append(p)
        p  = Point( i , j - 1, k)
        if self.occFunc[p] == True:
            tripletNeighbors.append(p)
        elif self.occFunc[p] == False:
            singletNeighbors.append(p)
        p  = Point( i , j , k + 1)
        if self.occFunc[p] == True:
            tripletNeighbors.append(p)
        elif self.occFunc[p] == False:
            singletNeighbors.append(p)
        p  = Point( i , j , k - 1)
        if self.occFunc[p] == True:
            tripletNeighbors.append(p)
        elif self.occFunc[p] == False:
            singletNeighbors.append(p)

        return( singletNeighbors , tripletNeighbors )

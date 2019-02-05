#!/usr/bin/env python

"""@package occupationFunction
"""

import numpy as np
import math
import sys
from randomdict import RandomDict

__author__ = "Kyle Beyer"

from exciton import Point

class OccupationFunction:
    def __init__(self , numSinglets , numTriplets , initialConditionGenerator , boundaryCondition ):
        self.singlets = RandomDict()
        self.triplets = RandomDict()
        self.boundaryCondition = boundaryCondition
        initialConditionGenerator( numSinglets   , numTriplets , self.singlets ,
                                   self.triplets , boundaryCondition )

    def checkStatus(self , p , tripletNeighbors , singletNeighbors):
        if p in self.singlets:
            singletNeighbors.append(p)
        elif p in self.triplets:
            tripletNeighbors.append(p)
        return( tripletNeighbors , singletNeighbors )

    # main exciton loop in pairwise transport
    def getPairwiseRateMultipliers(self):
        numSinglets , numTriplets =  len(self.singlets) , len(self.triplets)
        numSingletPairs , numTripletPairs = 0 , 0
        for point in self.singlets:
            singletNeighbors , tripletNeighbors = self.checkForNeighbors( point.i , point.j , point.k )
            numSingletPairs = numSingletPairs + len( singletNeighbors )

        for point in self.triplets:
            singletNeighbors , tripletNeighbors = self.checkForNeighbors( point.i , point.j , point.k )
            numTripletPairs = numTripletPairs + len( tripletNeighbors )

        return(numSinglets,  numTriplets , numSingletPairs , numTripletPairs )

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

    def eliminateRandomSinglet(self):
        ## Flourescence - S_1 -> S_0 + hnu
        # randomly select a singlet and remove it from occFunc
        p = self.singlets.random_key()
        del self.singlets[p]

    def eliminateRandomTriplet(self):
        ## Phosphorescence - T_1 -> S_0 + hnu
        # randomly select a triplet and remove it from occFunc
        p = self.triplets.random_key()
        del self.triplets[p]

    def linearSelectFromPair( self, excitonMap, singlet=True ):
        pairs = RandomDict()
        for key , val in excitonMap.items():
            singletNeighbors , tripletNeighbors = self.checkForNeighbors(key.i  , key.j , key.k)
            neighbors = []
            if singlet:
                neighbors = singletNeighbors
            else:
                neighbors = tripletNeighbors

            pairs[key] = neighbors

        # select a pair and return
        return( pairs.random_key() )

    def singletQuench(self):
        #SS quench - uniformly random sample one of the singlet pairs to annhilate
        pair = self.linearSelectFromPair(self.singlets ,  singlet=True)
        del self.singlets[pair]

    def tripletAnnhilate(self):
        #TT annhilate - uniformly random sample one of the triplet pairs to annhilate
        pair = self.linearSelectFromPair(self.triplets ,  singlet=False)
        del self.triplets[pair]

    def chooseRandomExciton(self):
        s = len(self.singlets)
        t = len(self.triplets)
        singlet = bool(np.random.choice(2,p=[s/(t+s) , t/(t+s)]) )
        if singlet:
            return( self.singlets.random_key() , True)
        else:
            return( self.triplets.random_key() , False)

    def randomExcitonRandomWalk(self):
        p , isSinglet = self.chooseRandomExciton()
        while not self.randomDirectionSingleHop(p , singlet=isSinglet):
            p , isSinglet = self.chooseRandomExciton()

    # Attempts to randomly chooose from the unoccupied indices directly
    # neighboring p. If succesful, deletes the value at p in self.occFunc
    # and add the same value at the randomly chosen, neighboring  point,
    # and returns True.
    # If there are no unnoccupied neighboring indices, returns False
    def randomDirectionSingleHop( self , p , singlet=True):

        i , j , k = p.i , p.j , p.k
        successfulMove = False
        numTries = 0

        # choose an order to try directions
        # [i+1,i-1,j+1,j-1,k+1,k-1]
        directions = np.random.choice(6,6 , replace=False)

        while successfulMove == False and numTries < 6:
            if directions[numTries] == 0:
                i = self.boundaryCondition.incrementX(i)
            elif directions[numTries] == 1:
                i = self.boundaryCondition.decrementX(i)
            elif directions[numTries] == 2:
                j = self.boundaryCondition.incrementY(j)
            elif directions[numTries] == 3:
                j = self.boundaryCondition.decrementY(j)
            elif directions[numTries] == 4:
                k = self.boundaryCondition.incrementZ(k)
            elif directions[numTries] == 5:
                k = self.boundaryCondition.decrementZ(k)

            # increment try count
            numTries = numTries + 1

            # Check if new point is already occupied
            pNew = Point(i,j,k)
            if singlet: # point to hop is singlet
                if pNew not in self.singlets:
                    successfulMove = True
                    self.singlets[pNew] = True
                    del self.singlets[p]
            else: # point to hop is triplet
                if pNew not in self.triplets:
                    successfulMove = True
                    self.triplets[pNew] = True
                    del self.triplets[p]

        return(successfulMove)

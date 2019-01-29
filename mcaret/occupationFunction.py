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
    def __init__(self , numSinglets , numTriplets , initialConditionGenerator , sideLength ):
        self.occFunc = RandomDict() # map :  Point -> OccupationStatus
        self.singlets = RandomDict()
        self.triplets = RandomDict()
        initialConditionGenerator( numSinglets  , numTriplets   , sideLength ,
                                   self.occFunc , self.singlets , self.triplets )

    def checkStatus(self , p , tripletNeighbors , singletNeighbors):
        if p in self.occFunc:
            status = self.occFunc[p]
            if status:
                tripletNeighbors.append(p)
            else:
                singletNeighbors.append(p)
        return( tripletNeighbors , singletNeighbors )

    # main exciton loop in pairwise transport
    def getPairwiseRateMultipliers(self):
        numSinglets , numTriplets =  len(self.singlets) , len(self.triplets)
        numSingletPairs , numTripletPairs = 0 , 0
        for point , status in self.occFunc.items():
            singletNeighbors , tripletNeighbors = self.checkForNeighbors( point.i , point.j , point.k )
            if status: # Status == True -> triplet
                numTripletPairs = numTripletPairs + len( tripletNeighbors )
            else: # staus == False -> singlet
                numSingletPairs = numSingletPairs + len( singletNeighbors )

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

        if p not in self.occFunc:
            print("p not in occFunc!")
            print("(" + str(p.i) + "," + str(p.j) + "," + str(p.k) + ")")
            print("length of occFunc:")
            print(len(self.occFunc))
            print("length of singlets:")
            print(len(self.singlets))
            print("contents of occFunc:")
            for p , value in self.occFunc.items():
                print("(" + str(p.i) + "," + str(p.j) + "," + str(p.k) + ")")

            print("Contents of singlets:")
            for p , value in self.singlets.items():
                print("(" + str(p.i) + "," + str(p.j) + "," + str(p.k) + ")")
            print("  ")
            if p not in self.singlets:
                print("Impossible!")

        del self.occFunc[p]
        del self.singlets[p]

    def eliminateRandomTriplet(self):
        ## Phosphorescence - T_1 -> S_0 + hnu
        # randomly select a triplet and remove it from occFunc
        p = self.triplets.random_key()
        del self.occFunc[p]
        del self.triplets[p]

    def singletQuench(self):
        #SS quench - uniformly random sample one of the singlet pairs to annhilate
        pass

    def tripletAnnhilate(self):
        #TT annhilate - uniformly random sample one of the triplet pairs to annhilate
        pass

    def randomExcitonRandomWalk(self):
        p = self.occFunc.random_key()
        while not self.randomDirectionSingleHop(p):
            p = self.occFunc.random_key()

    # Attempts to randomly chooose from the unoccupied indices directly
    # neighboring p. If succesful, deletes the value at p in self.occFunc
    # and add the same value at the randomly chosen, neighboring  point,
    # and returns True.
    # If there are no unnoccupied neighboring indices, returns False
    def randomDirectionSingleHop( self , p ):
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
                if self.occFunc[p]: # Triplet
                    self.triplets[pNew] = True
                    del self.triplets[p]
                else:
                    self.singlets[pNew] = True
                    del self.singlets[p]
                del self.occFunc[p]


        return(successfulMove)

#!/usr/bin/env python

"""@package occupationFunction
"""

import numpy as np
import math
import sys
from beykylerandomdict import RandomDict

__author__ = "Kyle Beyer"

from exciton import Point
from state import State

class OccupationFunction:
    def __init__(self , numSinglets , numTriplets , initialConditionGenerator , boundaryCondition , plotSrc=False):
        # initialize exciton population
        self.boundaryCondition = boundaryCondition
        self.singlets = RandomDict()
        self.triplets = RandomDict()
        initialConditionGenerator.sample( numSinglets   , numTriplets , self.singlets ,
                                          self.triplets , plot=plotSrc )

        # initialize state readout
        self.oldPoint = Point(0,0,0)
        self.newPoint = Point(0,0,0)

    def printInitialCondition( self , outputfile ):
        outputfile.write("Initial Condition\n")
        outputfile.write("===========================================================================\n")
        outputfile.write("singlets\n")
        for s in self.singlets:
            outputfile.write( str(s) + "\n" )
        outputfile.write("triplets\n")
        for t in self.triplets:
            outputfile.write( str(t) + "\n" )
        State.printHeader(outputfile)

    def checkStatus(self , p , tripletNeighbors , singletNeighbors):
        if p in self.singlets:
            singletNeighbors.append(p)
        elif p in self.triplets:
            tripletNeighbors.append(p)
        return( tripletNeighbors , singletNeighbors )

    def getCurrentState(self , time , numDecays, rates):
        return( State(time , len(self.singlets) , len(self.triplets) , numDecays , self.oldPoint , self.newPoint , rates ) )

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
        neighbors = []
        for key , val in excitonMap.items():
            singletNeighbors , tripletNeighbors = self.checkForNeighbors(key.i  , key.j , key.k)
            if singlet:
                neighbors = singletNeighbors
            else:
                neighbors = tripletNeighbors

            pairs[key] = neighbors

        # select a pair and return
        return( pairs.random_key() )

    def singletQuench(self): #S_1 + S_1 -> S_0 + S+0
        #SS quench - uniformly random sample one of the singlet pairs to annhilate
        pair = self.linearSelectFromPair(self.singlets ,  singlet=True)
        del self.singlets[pair]

    def tripletAnnhilate(self): #T_1 + T_1 -> S_1 + S_0
        #TT annhilate - uniformly random sample one of the triplet pairs to annhilate
        pair = self.linearSelectFromPair(self.triplets ,  singlet=False)
        # create a new singlet in its place
        self.singlets[pair] = True
        del self.triplets[pair]

    def chooseRandomExciton(self):
        s = len(self.singlets)
        t = len(self.triplets)
        singlet = np.random.choice([True , False], 1 ,p=[s/(t+s) , t/(t+s)])
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
        successfulMove = False
        numTries = 0

        # choose an order to try directions
        # [i+1,i-1,j+1,j-1,k+1,k-1]
        directions = np.random.choice(6,6 , replace=False)

        while successfulMove == False and numTries < 6:
            i , j , k = p.i , p.j , p.k
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
                    self.oldPoint = p
                    self.newPoint = pNew

            else: # point to hop is triplet
                if pNew not in self.triplets:
                    successfulMove = True
                    self.triplets[pNew] = True
                    del self.triplets[p]
                    self.oldPoint = p
                    self.newPoint = pNew

        return(successfulMove)

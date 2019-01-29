#!/usr/bin/env python

"""@package pairWiseRatePhysics
"""

import numpy as np
import math
import configparser

__author__ = "Kyle Beyer"

import exciton
from occupationFunction import OccupationFunction
####################################################################
#
# Rate physics
####################################################################

# Now lets set up how we calculate our rates

# For now we will ignore real calculations, which would involve rates for an individual
# exciton-exciton interaction going with the inter-exciton distance, and, instead approximate
# the total rate of an exciton-exciton interaction as being proportional to the number of
# direct neighbors in the lattice

class PairWiseRatePhysics:
    def __init__(self , kFluorescence , kPhosphorescence , kTripletAnnhilation , kSingletQuench , kTransport ):
        self.kFluorescence = kFluorescence
        self.kPhosphorescence = kPhosphorescence
        self.kTripletAnnhilation = kTripletAnnhilation
        self.kSingletQuench = kSingletQuench
        self.kTransport = kTransport

    # simply gets the number of direct triplet neighbors and direct singlet neighbors
    # Linear time - runs through all occupied points and checks for neighbors with
    # constant time lookups at each one

    def getRates(self, occFunc ):
        numSinglets,  numTriplets , numSingletPairs , numTripletPairs = occFunc.getPairwiseRateMultipliers()
        # calculate rates, populating rate array
        rates = np.array([ self.fluorescenceRate(numSinglets)             , \
                           self.phosphorescenceRate(numTriplets)          , \
                           self.TT_annhilationRate( numTripletPairs )     , \
                           self.SS_quenchRate( numSingletPairs )          , \
                           self.transportRate( numSinglets + numTriplets)  ])
        return(rates)

    # fluorescence is a linear rate
    def fluorescenceRate(self ,  numSinglets ):
        return( self.kFluorescence * numSinglets)

    # TT annhilation is a quadratic rate
    def TT_annhilationRate(self ,  numTripletPairs ):
        return( self.kTripletAnnhilation * numTripletPairs)

    # SS quenching is a quadratic rate
    def SS_quenchRate(self ,  numSingletPairs ):
        return( self.kSingletQuench * numSingletPairs )

    # phosphorescence is a linear rate
    def phosphorescenceRate( self ,  numTriplets ):
        return( self.kPhosphorescence * numTriplets )

    # for now we will model transport as a constant scalar rate
    def transportRate(self , numExcitons):
        return( self.kTransport * numExcitons )

####################################################################
#
# Rate constants input
####################################################################

def readRateConstants( config ):
    if 'Rate Constants' in config:
        if 'fluorescence' in config['Rate Constants']:
            kFluorescence = float(config['Rate Constants']['fluorescence'])
        else:
            print("No fluorescence rate constant found")
            exit(1)

        if 'phosphorescence' in config['Rate Constants']:
            kPhosphorescence = float(config['Rate Constants']['phosphorescence'])
        else:
            print("No phosphorescence rate constant found")
            exit(1)

        if 'TT_annhilation' in config['Rate Constants']:
            kTripletAnnhilation = float(config['Rate Constants']['TT_annhilation'])
        else:
            print("No TT annhilation  rate constant found")
            exit(1)

        if 'SS_quench' in config['Rate Constants']:
            kSingletQuench = float(config['Rate Constants']['SS_quench'])
        else:
            print("No SS quench rate constant found")
            exit(1)

        if 'transport' in config['Rate Constants']:
            kTransport = float(config['Rate Constants']['transport'] )
        else:
            print("No transport rate constant found")
            exit(1)
    else:
        print("Rate Constants section not found")
        exit(1)

    return( PairWiseRatePhysics(kFluorescence       , kPhosphorescence ,
                                kTripletAnnhilation , kSingletQuench   , kTransport ) )

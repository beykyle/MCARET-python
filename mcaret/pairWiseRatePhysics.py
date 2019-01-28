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
    def __init__(self , k_fluorescence , k_phosphorescence , k_TT_annhilation , k_SS_quench , k_transport ):
        self.k_fluorescence = k_fluorescence
        self.k_phosphorescence = k_phosphorescence
        self.k_TT_annhilation = k_TT_annhilation
        self.k_SS_quench = k_SS_quench
        self.k_transport = k_transport

    # simply gets the number of direct triplet neighbors and direct singlet neighbors
    # Linear time - runs through all occupied points and checks for neighbors with
    # constant time lookups at each one

    def getRateMultipliers( self , occFunc):
        num_singlet_pairs , num_triplet_pairs , num_singlets ,  num_triplets =  0 , 0 , 0 , 0
        for point , status in occFunc.items():
            singlet_neighbors , triplet_neighbors = occFunc.checkForNeighbors( point.i , point.j , point.k )
            if status: # Status == True -> triplet
                num_triplets = num_triplets + 1
                num_triplet_pairs = num_triplet_pairs + len( triplet_neighbors )
            else: # staus == False -> singlet
                num_singlets = num_singlets + 1
                num_singlet_pairs = num_singlet_pairs + len( singlet_neighbors )
        return(num_singlets,  num_triplets , num_singlet_pairs , num_triplet_pairs )


    def getRates(self, occFunc ):
        num_singlets,  num_triplets , num_singlet_pairs , num_triplet_pairs = self.getRateMultipliers( occFunc )
        # calculate rates, populating rate array
        rates = np.array([ self.fluorescenceRate(num_singlets)            , \
                           self.phosphorescenceRate(num_triplets)         , \
                           self.TT_annhilationRate( num_triplet_pairs )  , \
                           self.SS_quenchRate( num_singlet_pairs )       , \
                           self.transportRate()                            ])
        return(rates)

    # fluorescence is a linear rate
    def fluorescenceRate(self ,  num_singlets ):
        return( self.k_fluorescence * num_singlets)

    # TT annhilation is a quadratic rate
    def TT_annhilationRate(self ,  num_TT_pairs ):
        return( self.k_TT_annhilation * num_TT_pairs)

    # SS quenching is a quadratic rate
    def SS_quenchRate(self ,  num_SS_pairs ):
        return( self.k_SS_quench * num_SS_pairs )

    # phosphorescence is a linear rate
    def phosphorescenceRate( self ,  num_triplets ):
        return( self.k_phosphorescence * num_triplets )

    # for now we will model transport as a constant scalar rate
    def transportRate(self ):
        return( self.k_transport)


####################################################################
#
# Rate constants input
####################################################################

def readRateConstants( config ):
    if 'Rate Constants' in config:
        if 'fluorescence' in config['Rate Constants']:
            k_fluorescence = float(config['Rate Constants']['fluorescence'])
        else:
            print("No fluorescence rate constant found")
            exit(1)

        if 'phosphorescence' in config['Rate Constants']:
            k_phosphorescence = float(config['Rate Constants']['phosphorescence'])
        else:
            print("No phosphorescence rate constant found")
            exit(1)

        if 'TT_annhilation' in config['Rate Constants']:
            k_TT_annhilation = float(config['Rate Constants']['TT_annhilation'])
        else:
            print("No TT annhilation  rate constant found")
            exit(1)

        if 'SS_quench' in config['Rate Constants']:
            k_SS_quench = float(config['Rate Constants']['SS_quench'])
        else:
            print("No SS quench rate constant found")
            exit(1)

        if 'transport' in config['Rate Constants']:
            k_transport = float(config['Rate Constants']['transport'] )
        else:
            print("No transport rate constant found")
            exit(1)

    else:
        print("Rate Constants section not found")
        exit(1)

    return( PairWiseRatePhysics(k_fluorescence , k_phosphorescence ,
                                k_TT_annhilation , k_SS_quench , k_transport ) )




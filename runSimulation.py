#!/usr/bin/env python

"""@package runSimulation
"""

import configparser
import sys
import math

__author__ = "Kyle Beyer"

sys.path.append('./visualization/')
sys.path.append('./mcaret/')
sys.path.append('./input/')
sys.path.append('./output/')

import transport
from pairWiseRatePhysics import PairWiseRatePhysics , readRateConstants
from exciton import randomInitialDistribution as randInit
import excitonPlotter
import pulsePlotter
from occupationFunction import OccupationFunction


def parseConfig( filename , required_fields ):
    print("Reading from " + filename )

    config = configparser.ConfigParser()
    config.read( filename )

    if "Setup" in config:
        for field in required_fields:
            if field not in config['Setup']:
                print("No " + field + " field found")
                exit(1)
    else:
        print("No Setup section found")
        exit(1)

    return( config )

def main():

    if len(sys.argv) < 1:
        print("Usage:\npython runSimulation.py <input_filename>")
        exit(1)

    filename = sys.argv[1]

    required_fields = ['cube_side_length' , 'num_excitons' ,
                       'triplet_fraction' ,  'time_steps'   ]

    config = parseConfig( filename , required_fields )

    num_triplets =  int( math.floor( float(config['Setup']['num_excitons']) *
                         float(config['Setup']["triplet_fraction"] ) ) )
    num_singlets =  int( math.floor( float(config['Setup']['num_excitons']) *
                         ( 1 - float(config['Setup']["triplet_fraction"] ) ) ) )

    side_length = float( config['Setup']["cube_side_length"] )
    time_steps = int( config['Setup']["time_steps"] )

    print(" beginning simulation with " + str(num_triplets) + " triplets, and " + \
          str(num_singlets) + " singlets.")
    print("Using a cubic geometry with side length " + str(side_length) )
    print("Running for " + str(time_steps) + " time steps")

    occFunc = OccupationFunction( num_singlets , num_triplets , randInit , side_length )
    print("Generated initial condition")

    # generate rate physics object
    rp = readRateConstants( config )

    print("Running transport...")
    times = transport.transport( time_steps , rp , occFunc )
    print("Transport finished")
    print("Plotting results...")
    pulsePlotter.plotPulse( times )

if __name__ == "__main__":
  main()



#!/usr/bin/env python

"""@package runSimulation
"""

import configparser
import sys
import math
import numpy

__author__ = "Kyle Beyer"

sys.path.append('./visualization/')
sys.path.append('./mcaret/')
sys.path.append('./input/')
sys.path.append('./output/')

import transport
from pairWiseRatePhysics import PairWiseRatePhysics , readRateConstants
from boundaryCondition import RectangularPeriodicBoundaryCondition , readBoundaryCondition
from exciton import randomInitialDistribution as randInit
import excitonPlotter
import pulsePlotter
from occupationFunction import OccupationFunction

def writeOutput( pulse , time , fname ):
    with open(fname , 'w') as out:
        for p , t in zip(pulse , time):
            out.write("{0:.8e}".format(t) + " , " + "{0:.8e}".format(p) + "\n")

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

    required_fields = ['num_excitons' , 'triplet_fraction' ,  'time_steps' , 'name'  ]

    config = parseConfig( filename , required_fields )

    num_triplets =  int( math.floor( float(config['Setup']['num_excitons']) *
                         float(config['Setup']["triplet_fraction"] ) ) )
    num_singlets =  int( math.floor( float(config['Setup']['num_excitons']) *
                         ( 1 - float(config['Setup']["triplet_fraction"] ) ) ) )

    time_steps = int( config['Setup']["time_steps"] )

    name = config['Setup']['name']

    print("Beginning simulation " + name + " with " + str(num_triplets) + " triplets, and " + \
          str(num_singlets) + " singlets.")
    print("Running for " + str(time_steps) + " time steps")


    # generate rate physics object
    print("Reading rate constants...")
    rp = readRateConstants( config )

    # generate boundary conditions object
    print("Reading boundary condition...")
    bc = readBoundaryCondition( config )

    # generate occupation function
    print("Generating initial condition...")
    occFunc = OccupationFunction( num_singlets , num_triplets , randInit , bc)

    print("Running transport...")
    outputfile = name + ".out"
    transport.transport( time_steps , rp , occFunc , outputfile )
    print("Transport finished")

if __name__ == "__main__":
  main()



#!/usr/bin/env python

"""@package runSimulation
"""

import configparser
import sys
import math
import numpy
import os.path

__author__ = "Kyle Beyer"

sys.path.append('./visualization/')
sys.path.append('./mcaret/')
sys.path.append('./input/')
sys.path.append('./output/')

import transport
from pairWiseRatePhysics import PairWiseRatePhysics , readRateConstants
from boundaryCondition import RectangularPeriodicBoundaryCondition , readBoundaryCondition
from source import RandomRectangularSource
from source import TrackSource
from exciton import Point
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
    plotSrc =  config['Setup']['plot_src'] in [ "True" , "true" , "T" , "t" , "yes" , "y" , "Yes" ]
    if config['Initial Condition']['type'] == "track":
        source = TrackSource( Point.fromString(config['Initial Condition']['start']) ,
                              Point.fromString(config['Initial Condition']['end'])   )
    elif config['Initial Condition']['type'] == "random":
        source = RandomRectangularSource( bc )
    else:
        print("Unknown initial distribution!")
        exit(1)

    occFunc = OccupationFunction( num_singlets , num_triplets , source , bc , plotSrc=plotSrc )

    outputfile = name + ".out"
    i = 1
    while os.path.isfile(outputfile):
      print (outputfile + " already exists!")
      outputfile = name + "_" + str(i) + ".out"
      i = i + 1

    print("Running transport, printing results to " + outputfile + "...")
    transport.transport( time_steps , rp , occFunc , outputfile )
    print("Transport finished")

if __name__ == "__main__":
  main()



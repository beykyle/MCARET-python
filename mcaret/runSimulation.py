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
from exciton import randomInitialDistribution as randInit
import excitonPlotter
import pulsePlotter

def parseConfig( fileName , required_fields ):
    config = configparser.ConfigParse()
    config.read( filename )

    if "Setup" in config:
        for field in required_fields:
            if field not in config:
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

    num_triplets =  int( math.floor( float(config['num_excitons']) *
                         float(config["triplet_fraction"] ) ) )
    num_singlets =  int( math.floor( float(config['num_excitons']) *
                         ( 1 - float(config["triplet_fraction"] ) ) ) )

    side_length = float( config["cube_side_length"] )
    time_steps = int( config["time_steps"] )

    singlets , triplets = randInit( num_triplets , num_singlets , side_length)

    times = transport.transport( singlets , triplets , time_steps )
    pulsePlotter.plotPulse( times )



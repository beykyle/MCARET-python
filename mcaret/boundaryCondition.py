#!/usr/bin/env python

"""@package boundaryCondition
"""

__author__ = "Kyle Beyer"

from exciton import Point

####################################################################
#
# Boundary condition definition
####################################################################

# repetitive funcitons for speed
class RectangularPeriodicBoundaryCondition:
    def __init__(self, xMax , yMax , zMax ):
        self.xMax = int(xMax)
        self.yMax = int(yMax)
        self.zMax = int(zMax)

    def incrementX(self , x):
        if( x + 1 > self.xMax ):
            return(int(0))
        else:
            return( int(x + 1) )

    def decrementX(self , x):
        if( x - 1 < 0 ):
            return(int(self.xMax))
        else:
            return( int(x - 1))

    def incrementY(self , y):
        if( y + 1 > self.yMax ):
            return(int(0))
        else:
            return(int(y + 1))

    def decrementY(self , y):
        if( y - 1 < 0 ):
            return(int(self.yMax))
        else:
            return(int(y - 1))

    def incrementZ(self , z):
        if( z + 1 > self.zMax ):
            return(int(0))
        else:
            return(int(z + 1))

    def decrementZ(self , z):
        if( z - 1 < 0 ):
            return(int(self.zMax))
        else:
            return(int(z - 1))

####################################################################
#
# Read boundary condition
####################################################################

def readBoundaryCondition( config ):
    if 'Boundary Conditions' in config:
        if 'type' in config['Boundary Conditions']:
            BCtype = config['Boundary Conditions']['type']
        else:
            print("Type not in Boundary Conditions")
            exit(1)

        if 'xMax' in config['Boundary Conditions']:
            xMax = int(config['Boundary Conditions']['xMax'])
        else:
            print("No xMax founda in Boundary Conditions")
            exit(1)

        if 'yMax' in config['Boundary Conditions']:
            yMax = int(config['Boundary Conditions']['yMax'])
        else:
            print("No yMax founda in Boundary Conditions")
            exit(1)

        if 'zMax' in config['Boundary Conditions']:
            zMax = int(config['Boundary Conditions']['zMax'])
        else:
            print("No zMax founda in Boundary Conditions")
            exit(1)
    else:
        print("Boundary Conditions section not found")
        exit(1)

    if BCtype == "rectangular periodic":
        b = RectangularPeriodicBoundaryCondition( xMax , yMax , zMax )
    else:
        raise NotImplementedError("Only rectangular periodic boundaries are possible")

    return( b )

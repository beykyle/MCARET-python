#!/usr/bin/env python

"""@package exciton
"""

import numpy as np
import math
import sys

__author__ = "Kyle Beyer"

####################################################################
#
# Point definition
####################################################################

# point class
class Point:
    # constructor requires position in lattice
    def __init__(self, i,j,k):
        self.i = int(i)
        self.j = int(j)
        self.k = int(k)

    def fromString( string ):
        p = [ int(x.strip().rstrip("\n")) for x in string.split(",") ]
        return( Point(p[0] , p[1] , p[2] ) )

    # uses large primes to get a decent hash function
    # not injective but should minimize collisions
    def __hash__(self):
        return hash( int(self.i) + 32416189717 * ( int(self. j) +  15487291 * int(self.k) ) )

    def __eq__(self , other ):
        if( other.i == self.i and other.j == self.j and other.k == self.k ):
            return(True)
        else:
            return(False)

    def __ne__(self , other):
        if( other.i == self.i and other.j == self.j and other.k == self.k ):
            return(False)
        else:
            return(True)

    def __str__(self):
        return ( "(" + str(self.i) + "," + str(self.j) + "," +  str(self.k) + ")" )

# Point iterator
# 0   ->   1   ->   2   ->  ...
# ijk -> i+1jk -> i-1jk -> ij+1k -> ij-1k -> ijk+1 -> ijk-1


#!/usr/bin/env python

"""@package state
"""

__author__ = "Kyle Beyer"


####################################################################
#
# System state definition
####################################################################

class State:
    def __init__(self , time , numSinglets , numTriplets , numDecays):
        self.time = time
        self.numSinglets = numSinglets
        self.numTriplets = numTriplets
        self.numDecays = numDecays

    def printStateLine(self , output_file_object ):
        ostr = "{:1.8E} , {:1.8E} , {:1.8E} , {:1.8E}\n".format(
              self.time , float(self.numSinglets) , float(self.numTriplets) , float(self.numDecays) )
        print(ostr)
        output_file_object.write(ostr)

    def readStateLine(string):
        v = [float(x.strip().strip("\n")) for x in  string.split(",")]
        return( v[0] , v[1] , v[2] , v[3] ) # time, num S , num T ,  decays


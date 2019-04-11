#!/usr/bin/env python

"""@package state
"""

__author__ = "Kyle Beyer"


####################################################################
#
# System state definition
####################################################################

class State:
    def __init__(self , time , numSinglets , numTriplets , numDecays , oldPoint , newPoint):
        self.time = time
        self.numSinglets = numSinglets
        self.numTriplets = numTriplets
        self.numDecays = numDecays
        self.oldPoint = oldPoint
        self.newPoint = newPoint

    def printHeader(outputfile):
        outputfile.write("\nTransport\n")
        outputfile.write("===========================================================================\n")
        outputfile.write("time           , singlets       ,  triplets      , decay          , oldpoint    ->  newpoint\n")

    def printTransportStateLine(self , output_file_object ):
        # should only be called if successful transport happens
        output_file_object.write(
            "{:1.8E} , {:1.8E} , {:1.8E} , {:1.8E}".format(
              self.time , float(self.numSinglets) , float(self.numTriplets) , float(self.numDecays)
              ) + " , " + str(self.newPoint) + " -> " + str(self.oldPoint) + "\n"
            )

    def printStateLine(self , output_file_object ):
        output_file_object.write(
            "{:1.8E} , {:1.8E} , {:1.8E} , {:1.8E}\n".format(
              self.time , float(self.numSinglets) , float(self.numTriplets) , float(self.numDecays)
              )
            )

    def readStateLine(string):
        v = [float(x.strip().strip("\n")) for x in  string.split(",")]
        return( v[0] , v[1] , v[2] , v[3] ) # time, num S , num T ,  decays


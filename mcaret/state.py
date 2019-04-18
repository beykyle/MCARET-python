#!/usr/bin/env python

"""@package state
"""

__author__ = "Kyle Beyer"


####################################################################
#
# System state definition
####################################################################

class State:
    def __init__(self , time , numSinglets , numTriplets , numDecays , oldPoint , newPoint , rates ):
        self.time = time
        self.numSinglets = numSinglets
        self.numTriplets = numTriplets
        self.numDecays = numDecays
        self.oldPoint = oldPoint
        self.newPoint = newPoint
        self.flourRate = rates[0]
        self.phosRate = rates[1]
        self.ttRate = rates[2]
        self.ssRate = rates[3]
        self.transRate = rates[4]

    def printHeader(outputfile):
        outputfile.write("\nTransport\n")
        outputfile.write("=======================================================================================================================================================\n")
        outputfile.write("time           , singlets       ,  triplets      , decay          , flour rate     , phos rate      , TT rate        , SS rate        , trans rate     ,  oldpoint              ->  newpoint\n")
        outputfile.write("=======================================================================================================================================================\n")

    def printTransportStateLine(self , output_file_object ):
        # should only be called if successful transport happens
        output_file_object.write(
            "{:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E}".format(
              float(self.time)      , float(self.numSinglets) , float(self.numTriplets) , float(self.numDecays) ,
              float(self.flourRate) , float(self.phosRate)    , float(self.ttRate)      , float(self.ssRate)    ,
              float(self.transRate)  )  + " , " + str(self.newPoint) + " -> " + str(self.oldPoint) + "\n"
            )

    def printStateLine(self , output_file_object ):
        output_file_object.write(
            "{:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E} , {:1.8E}\n".format(
              float(self.time)      , float(self.numSinglets) , float(self.numTriplets) , float(self.numDecays) ,
              float(self.flourRate) , float(self.phosRate)    , float(self.ttRate)      , float(self.ssRate)    ,
              float(self.transRate)  )
            )

    def readStateLine(string):
        v = [float(x.strip().strip("\n")) for x in  string.split(",")[0:4]]
        return( v[0] , v[1] , v[2] , v[3] ) # time, num S , num T ,  decays


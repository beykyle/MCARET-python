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
        output_file_object.write(
            "{:1.8E} , {:1.8E} , {:1.8E} , {:1.8E}\n".format(
              self.time , float(self.numSinglets) , float(self.numTriplets) , float(self.numDecays)
              )
            )

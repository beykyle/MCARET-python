#!/usr/bin/env python

"""@package popPlotter
"""

import sys
import numpy as np
import math
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator
import pylab
from pylab import arange,pi,sin,cos,sqrt

__author__ = "Kyle Beyer"

# Advanced Plot Setup
###########################################################################
colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00']
fig_width     = 6.5
golden_ratio  = (sqrt(5)-1.0)/2.0
fig_height    = fig_width*golden_ratio
fig_size      =  [fig_width,fig_height]
fig_font_size = 22

params        = { 'axes.labelsize' : 14,
                  'axes.titlesize' : 14,
                  'backend'        : 'ps',
                  'font.family'    : 'serif',
                  'font.size'      : fig_font_size,
                  'legend.fontsize': fig_font_size / 2,
                  'figure.dpi'     : 150,
                  'figure.figsize' : fig_size,
                  'savefig.dpi'    : 200,
                  'savefig.bbox'   : 'tight',
                  'font.size'      : fig_font_size,
#                  'text.usetex'    : True,
                  'xtick.labelsize': fig_font_size / 2,
                  'ytick.labelsize': fig_font_size / 2,
}

pylab.rcParams.update(params)


sys.path.append('./mcaret/')
from state import State

def getData( fname ):
    with open( fname, "r" ) as f:
        lines = f.readlines()

    time = []
    numS = []
    numT = []
    dec = []

    for i , line in enumerate(lines):
        if line == "Transport\n":
            break

    for line in lines[i+3:]:
        t , s , T , d = State.readStateLine(line)
        time.append(t)
        numS.append(s)
        numT.append(T)
        dec.append(d)

    lightTimes = []
    for i , t in enumerate(time):
        if( dec[i] > 0 ):
            lightTimes.append(t)

    pulse , ptimes = np.histogram(lightTimes , bins=12)

    return numS , numT , pulse , time , ptimes

def createSingletPlot( times , pops , names ):
    fig = createPopPlot(times , pops , names )
    plt.savefig("singlets.pdf", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    plt.show()

def createTripletPlot( times , pops , names ):
    fig = createPopPlot(times , pops , names )
    plt.savefig("triplets.pdf", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    plt.show()

def createPulsePlot( times , pulse , names ):
    # create figure
    fig = plt.figure()
    # add a plot for each pop
    for t , p , n in zip(times,  pulse , names):
      plt.step(t[:-1] , p ,label=n )
    # set ax labels
    plt.xlabel("Time [a.u.]")
    plt.ylabel("Pulse [light emissions / unit time]")
    plt.legend()
    plt.savefig("pulse.pdf", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    plt.show()

def createPopPlot( times ,  pops , names ):
    # create figure
    fig = plt.figure()
    # add a plot for each pop
    for t , p , n in zip(times,  pops , names):
        plt.plot(t , p ,label=n )
    # set ax labels
    plt.xlabel("Time [a.u.]")
    plt.ylabel("Exciton Population")
    plt.legend()
    return fig

def createPlots( data , filenames ):
    # remove .out and underscore from names
    names = [ n.replace('.out' , '').replace("_" , " ") for n in filenames ]
    createSingletPlot( [ d['singlets'] for d in data ], [d['time'] for d in data ] , names  )
    createTripletPlot( [ d['singlets'] for d in data ], [d['time'] for d in data ] , names  )
    createPulsePlot( [d['ptime'] for d in data], [d['pulse'] for d in data] , names )


def main():

    if len(sys.argv) < 1:
        print("Usage:\npython populationCompare.py <input_filename1> <input_filename2> ...")
        exit(1)

    filenames = []
    for a in sys.argv[1:]:
        filenames.append(a)

    data = []
    for filename in filenames:
        singlets , triplets , pulse, time , ptime = getData(filename)
        data.append(dict())
        data[-1]["singlets"] = singlets
        data[-1]["triplets"] = triplets
        data[-1]["pulse"] = pulse
        data[-1]["time"] = time
        data[-1]["ptime"] = ptime

    createPlots(data , filenames)


if __name__ == "__main__":
  main()

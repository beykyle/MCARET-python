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

def plotPulse( fname ):
    with open( fname, "r" ) as f:
        lines = f.readlines()

    time = []
    numS = []
    numT = []
    dec = []

    for line in lines:
        t , s , T , d = State.readStateLine(line)
        time.append(t)
        numS.append(s)
        numT.append(T)
        dec.append(d)

    lightTimes = []
    for i , t in enumerate(time):
        if( dec[i] > 0 ):
            lightTimes.append(t)

    y , x = np.histogram(lightTimes , bins=12)

    fig, ax1 = plt.subplots()
    pylab.rcParams.update(params)

    ax2 = ax1.twinx()

    ax2.plot(time , numS , label="Singlets" , zorder=2)
    ax2.plot(time , numT , label="Triplets" , zorder=3)
    ax2.set_ylabel('exciton population')

    ax1.plot(x[:-1] , y  , "k." , label="pulse" , markersize=12 , zorder=1)
    ax1.set_xlabel(r"time [a.u.]")
    ax1.set_ylabel(r"light-emitting decays")
    ax1.legend(loc=1)
    ax2.legend(loc=2)

    fname = fname.replace('.out' , '')
    plt.savefig(fname + ".pdf", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    plt.show()

def main():

    if len(sys.argv) < 1:
        print("Usage:\npython runSimulation.py <input_filename>")
        exit(1)

    filename = sys.argv[1]
    plotPulse(filename)

if __name__ == "__main__":
  main()

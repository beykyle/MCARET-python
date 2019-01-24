#!/usr/bin/env python

"""@package pulsePlotter
"""

import numpy as np
import math

__author__ = "Kyle Beyer"

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator
import matplotlib.pylab as pylab

def plotPulse( times ):
  fig=plt.figure(figsize=(12, 10), dpi= 160, facecolor='w', edgecolor='k')
  ax = fig.add_subplot(111)

  ax.set_xlabel(r"time [a.u.]")
  ax.set_ylabel(r"$light-emitting decays$")

  params = {'legend.fontsize': 22,
            'axes.labelsize': 20,
            'xtick.labelsize':20,
            'ytick.labelsize':20}
  pylab.rcParams.update(params)
  plt.hist(times)
  plt.show()

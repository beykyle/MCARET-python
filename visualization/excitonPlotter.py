#!/usr/bin/env python

"""@package excitonPlotter
"""

import numpy as np
import math
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator
import matplotlib.pylab as pylab

__author__ = "Kyle Beyer"


def makePlot(ax , singlets , triplets):
    singlets = list( singlets )
    triplets = list( triplets )

    # lets plot our initial distribution
    for singlet in singlets:
        ax.scatter(singlet.i , singlet.j , singlet.k , marker="*" , c="k" )

    for triplet in triplets:
        ax.scatter(triplet.i , triplet.j , triplet.k , marker="." , c="r" )

    # janky way to add legend
    ax.scatter(triplets[0].i , triplets[0].j , triplets[0].k , marker="*" , c="k" , label="singlets")
    ax.scatter(singlets[0].i , singlets[0].j , singlets[0].k , marker="." , c="r" , label="triplets")

    plt.legend(loc='upper left')
    plt.show()

def makeCommonAxis():
  # Now lets get our axes set up, so we can reuse them as we go
  fig=plt.figure(figsize=(12, 10), dpi= 160, facecolor='w', edgecolor='k')
  ax = fig.add_subplot(111, projection='3d')

  ax.set_xlabel(r"$\mathbf{i}$")
  ax.set_ylabel(r"$\mathbf{j}$")
  ax.set_zlabel(r"$\mathbf{k}$")

  ax.yaxis.set_major_locator(MaxNLocator(integer=True))
  ax.xaxis.set_major_locator(MaxNLocator(integer=True))
  ax.zaxis.set_major_locator(MaxNLocator(integer=True))

  params = {'legend.fontsize': 18,
            'axes.labelsize': 20,
            'xtick.labelsize':20,
            'ytick.labelsize':20}
  pylab.rcParams.update(params)

  return( fig , ax)

#! /usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
         description='Plots ModeMap Potential Energy Surface Along Two Phonon Modes (PES)')
parser.add_argument('-f', '--file', metavar='file path',
                    default='ModeMap_PostProcess_2DMap.csv',
                    help='path to file (ModeMap_PostProcess_2DMap.csv)')
parser.add_argument('--mapcolour', metavar='Map colour', default='viridis',
                    help='colour map for PES')
parser.add_argument('--contourCol', metavar='Contour colour', default='#000000',
                    help='colour of contour lines')
parser.add_argument('-q', '--qlabels', metavar='qpoint labels', nargs='+', 
                    default=None,
                    help='qpoint labels for the modes to go into the x- and y-axis labels')
parser.add_argument('-a', '--num_atoms', metavar='number of atoms', default='1',
                    help='number of atoms in the supercell used for mode-mapping')
parser.add_argument('-o', '--output', metavar='output file suffix', default=None,
                     help='suffix for the output filename')
parser.add_argument('--style', metavar='style sheet', nargs='+', default='',
                    help='style sheets to use. Later ones will \
                          override earlier ones if they conflict.')
parser.add_argument('--dpi', type=int, default=300,
                        help='pixel density for image file')
parser.add_argument('--font', default=None, help='font to use')
parser.add_argument('-z', action='store_true',
                    help='dark mode')
args = parser.parse_args()


def add_map(axis, mapfile, cmap, contourCol, qlabels, num_atoms):
    """Plots the Potential Energy Surface Spanned by Two Phonon Modes.

    Args:
        axis (:obj:'matplotlib.pyplot'): Axis to plot on.
        mapfile (:obj:'str'): Path to file (ModeMap_PostProcess).csv.
        colours(:obj:'list'): Line colours.
        labels(:obj:'str'): Line labels.

    Returns:
        :obj:'matplotlib.pyplot': Axis with PES.
    """


    with open(mapfile) as csvfile: 
        reader = csv.reader(csvfile)

        q2, potentialSurf = [], []

        count = 0
        for row in reader:
            if len(row) == 1 and row[0] == "dU(Q_1,Q_2) [meV]":
                break

        next(reader)

        q1  = [float(i) for i in next(reader)[1:]]
    
        for row in reader:
            q2.append(float(row[0]))
            potentialSurf.append([float(i)/int(num_atoms) for i in row[1:]]) 

   
    q1, q2, potentialSurf = np.array(q1, dtype = np.float64), np.array(q2, dtype = np.float64), np.array(potentialSurf, dtype = np.float64)
    

    PES = axis.pcolormesh(q1, q2, potentialSurf, cmap=cmap, rasterized=True, shading="gouraud", antialiased=True)
    
    levels = np.geomspace(1, np.amax(potentialSurf)-np.amin(potentialSurf)+1, 10)
    levels_transformed = levels + np.amin(potentialSurf) - 1
    plt.contour(q1, q2, potentialSurf, linestyles='solid', colors = contourCol, levels = levels_transformed) 

    cbar = plt.colorbar(PES) 
    
    if num_atoms == 1:
        cbar.set_label(r'$\mathregular{{\Delta U\ [meV]}}$', fontsize=50, labelpad=15)
    else:
        cbar.set_label(r'$\mathregular{{\Delta U\ [meV\ atom^{-1}]}}$', fontsize=50, labelpad=15)
    cbar.ax.tick_params(which='major', direction='in', length=18, labelsize=50, rotation=70)
    cbar.outline.set_linewidth(1.5)



    if qlabels: 
        for i in qlabels:
            if i == 'Gamma':
                i = '\Gamma'
            else:
                i = i

    axis.set_xlabel(r'$\mathregular{{Q_{{{}}}\ [amu^\frac{{1}}{{2}}\ \AA]}}$'.format(qlabels[0]) if qlabels is not None else r'$\mathregular{Q\ [amu^\frac{1}{2}\ \AA]}$', fontsize=50)
    axis.set_ylabel(r'$\mathregular{{Q_{{{}}}\ [amu^\frac{{1}}{{2}}\ \AA]}}$'.format(qlabels[1]) if qlabels is not None else r'$\mathregular{Q\ [amu^\frac{1}{2}\ \AA]}$', fontsize=50)
   
    axis.tick_params(axis='both', which='major', direction='in', pad=15, length=24, labelsize=50)
    axis.tick_params(axis='both', which='minor', direction='in', pad=15, length=12)
    axis.xaxis.set_major_locator(ticker.MaxNLocator(5))
    axis.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    axis.yaxis.set_major_locator(ticker.MaxNLocator(5))
    axis.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
   
    # find q1_and_q2 where energy is minimum
    E_min_index = np.where(potentialSurf == np.amin(potentialSurf))
    q1_and_q2 = [[q1[i], q2[j]] for i, j in zip(E_min_index[0], E_min_index[1])]
    print("q1_and_q2:", q1_and_q2)


    return axis

import os
import csv
import matplotlib.pyplot as plt
from pylab import genfromtxt
from matplotlib import rcParams, rc
import matplotlib.ticker as ticker
import numpy as np
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from cycler import cycler
from scipy.interpolate import interp2d
from os.path import isfile

fonts = ['Whitney Book Extended']
plt.rc('font', **{'family': 'sans-serif', 'sans-serif': fonts})
plt.rc('text', usetex=False)
plt.rc('pdf', fonttype=42)
plt.rc('mathtext', fontset='stixsans')

mpl.rcParams['axes.linewidth'] = 2
fig, ax = plt.subplots(figsize=(15.5, 12)) 

ax = add_map(ax, args.file, args.mapcolour, args.contourCol, args.qlabels, args.num_atoms)

plt.subplots_adjust(left=0.14, right=0.94, top=0.95, bottom=0.15)
plt.savefig('2D-modemap{}.pdf'.format(args.output) if args.output is not None else '2D-modemap.pdf')
plt.savefig('2D-modemap{}.png'.format(args.output) if args.output is not None else '2D-modemap.png')
#plt.show()

#! /usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
         description='Plots ModeMap Potential Energy Curves (PEC)')
parser.add_argument('-m', '--map', metavar='mappath', nargs='+',
                    default='ModeMap_PostProcess.csv',
                    help='path to ModeMap (ModeMap_PostProcess).dat')
parser.add_argument('--mapcolour', metavar='Map colour', nargs='+', default='#B43864',
                    help='colours for the PEC')
parser.add_argument('-q', '--qlabel', metavar='qpoint label', default=None,
                     help='qpoint label for the mode to go into the xaxis label')
parser.add_argument('-a', '--num_atoms', metavar='number of atoms', default='1',
                     help='number of atoms in the supercell used for mode-mapping')
parser.add_argument('--legendlab', metavar='PEC legend labels', nargs='+',
                    help='labels for the PECs to go into the legend')
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


def add_map(axis, mapfile, colours, qlabel, num_atoms, legendlab):
    """Plots the Potential Energy Curve Spanned by a Phonon Mode.

    Args:
        axis (:obj:'matplotlib.pyplot'): Axis to plot on.
        mapfile (:obj:'str'): Path to ModeMap (ModeMap_PostProcess).dat.
        colours(:obj:'list'): Line colours.
        labels(:obj:'str'): Line labels.

    Returns:
        :obj:'matplotlib.pyplot': Axis with PEC.
    """


    #files = os.listdir(mapfile)

    x_val, y_val = [], []    
        
    for i in mapfile:
        with open(i) as csvfile: 
            reader = csv.reader(csvfile)

            [next(reader, None) for item in range(3)]
        
            x, y = [], []

            for rows in reader:
                x.append(float(rows[0]))
                y.append(float(rows[2])/int(num_atoms))
            x_val.append(x)
            y_val.append(y)

    try:
        colormap = plt.cm.get_colormap(colours)
        colours =  colormap(np.linspace(0, 1, 5))
    except Exception:
        pass
        
    axis.set_prop_cycle(color=colours)

    labs = []
    if len(mapfile) > 1:
        if legendlab:
            labs.append(legendlab)
        else:
            labs.append('mode{}'.format(i) for i in range(1,len(mapfile)+1))
        
        for i, j, k in zip(x_val, y_val, labs[0]):
            axis.plot(i, j, linewidth=4, markersize=18, marker="o", label=k)
    else:
        axis.plot(x_val[0], y_val[0], linewidth=4, markersize=18, marker="o")
   

    if qlabel == 'Gamma':
        qlab = '\Gamma'
    else:
        qlab = qlabel


    axis.set_xlabel(r'$\mathregular{{Q_{{{}}}\ [amu^\frac{{1}}{{2}}\ \AA]}}$'.format(qlab) if qlab is not None else r'$\mathregular{Q\ [amu^\frac{1}{2}\ \AA]}$', fontsize=50)
    if num_atoms == 1:
        axis.set_ylabel(r'$\mathregular{{\Delta U(Q_{{{}}})\ [meV]}}$'.format(qlab) if qlab is not None else r'$\mathregular{\Delta U(Q)\ [meV]}$', fontsize=50)
    else:
        axis.set_ylabel(r'$\mathregular{{\Delta U(Q_{{{}}})\ [meV\ atom^{{-1}}]}}$'.format(qlab) if qlab is not None else r'$\mathregular{\Delta U(Q)\ [meV]\ atom^{-1}}$', fontsize=50)

    axis.tick_params(axis='both', which='major', direction='in', pad=15, length=24, labelsize=50)
    axis.tick_params(axis='both', which='minor', direction='in', pad=15, length=12)
  
    axis.xaxis.set_major_locator(ticker.MaxNLocator(5))
    axis.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    axis.yaxis.set_major_locator(ticker.MaxNLocator(6))
    axis.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))


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
from os.path import isfile

fonts = ['Whitney Book Extended']
plt.rc('font', **{'family': 'sans-serif', 'sans-serif': fonts})
plt.rc('text', usetex=False)
plt.rc('pdf', fonttype=42)
plt.rc('mathtext', fontset='stixsans')

mpl.rcParams['axes.linewidth'] = 2
fig, ax = plt.subplots(figsize=(12.6, 12)) 

ax = add_map(ax, args.map, args.mapcolour, args.qlabel, args.num_atoms, args.legendlab)
if len(ax.get_legend_handles_labels()[0]) > 1:
       legend = ax.legend(frameon=False, prop={'size': 36})

plt.subplots_adjust(left = 0.17, right = 0.97, top  = 0.97, bottom = 0.16)
plt.savefig('modemap{}.pdf'.format(args.output) if args.output is not None else 'modemap.pdf')
plt.savefig('modemap{}.png'.format(args.output) if args.output is not None else 'modemap.png')
#plt.show()

# ModeMap-Plotting

A tool for plotting potential-energy surfaces along phonon modes.

Prerequisites
-------------

The tools use the output from the [ModeMap code] (https://github.com/JMSkelton/ModeMap) [Ref. 1](#Ref1)
To use it requires a phonon mode-mapping calculation with ModeMap code to have been performed on the system of interest.

The code is written in Python.

Usage
-----

1. The `modemap.py` requires only 1 file `ModeMap_PostProcess.csv` and produces a 1D potential energy curve (PEC).

(It can also plot multiple 1D potential energy curves in a single plot)

2. The `modemap_2D.py` also requires only 1 file `ModeMap_PostProcess_2D.csv` and produces a 2D potential energy surface (PES).


Examples
--------

The following examples are provided to illustrate the outputs of the code for 1D PECs, multiple PECs, 2D PES:

* [*Bi2Sn2O7*](./Example_plots) Reproduces plots for some of the calculations in [Ref. 2](#Ref2).


References
----------

1. <a name="Ref1"></a> J. M. Skelton, L. A. Burton, S. C. Parker, A. Walsh, C.-E. Kim, A. Soon, J. Buckeridge, A. A. Sokol, C. R. A. Catlow, A. Togo and I. Tanaka, "Anharmonicity in the High-Temperature Cmcm Phase of SnSe: Soft Modes and Three-Phonon Interactions", Physical Review Letters **117**, 075502 (**2016**), DOI: [10.1103/PhysRevLett.117.075502](https://doi.org/10.1103/PhysRevLett.117.075502)

2. <a name="Ref2"></a>W. Rahim, J. M. Skelton, C. N. Savory, I. R. Evans, J. S. O. Evans, A. Walsh, D. O. Scanlon, "Polymorph Prediction of Bismuth Stannate Using First-Principles Phonon Mode Mapping", CChemical Science, (**2020**), DOI: [10.1039/D0SC02995E](https://doi.org/10.1039/D0SC02995E)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to analyze fracture orientation data and produce
Figure 9 in the following paper:
    
    Colaianne, N.J., Shobe, C.M., Moler, J., Benison, K.C., and Chilton, K.D.
    (resubmitted September 2024) Beyond boundaries: Depositional environment 
    controls on erodibility, process, and form in rivers incising sedimentary 
    bedrock. Geosphere.
    
Please cite the code repository and/or paper if you use this code.

@author: Charles M. Shobe, U.S. Forest Service Rocky Mountain Research Station
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

orientations = pd.read_csv('../data/fracture_orientation/fracture_orientations.csv', delimiter = ',')
orientations = orientations[:123] #cut out trailing NaNs

#duplicate orientations but point them in the other direction
#so that rose diagram points in both directions for a given fracture
orientations_dupes = orientations.copy(deep=True)
orientations_dupes.loc[orientations['Bearing'] < 180, 'Bearing'] += 180
orientations_dupes.loc[orientations['Bearing'] > 180, 'Bearing'] -= 180

#now recombine the two orientation series
orientations = pd.concat([orientations, orientations_dupes])

#separate out data by fracture assemblage
carb_thalweg = orientations[orientations['AssemblageID'] == 1.0]
carb_bench = orientations[orientations['AssemblageID'] == 2.0]
fine = orientations[orientations['AssemblageID'] == 3.0]
coarse = orientations[orientations['AssemblageID'] == 4.0]

#for each assemblage, bin the orientations: count how many measurements fall 
#into each bin. Then normalize by the total number of measurements.

N = 10 #number of bins to slice the unit circle into

#use Pandas cut to bin the measurements from each fracture assemblage and count 
#the number in each bin
carb_thalweg = carb_thalweg.sort_values('Bearing', inplace=False)
carb_thalweg_binned = pd.cut(carb_thalweg['Bearing'], np.arange(0, 360+N, N), 
                             retbins = False)
carb_thalweg_counts = carb_thalweg_binned.value_counts(sort = False)

carb_bench = carb_bench.sort_values('Bearing', inplace=False)
carb_bench_binned = pd.cut(carb_bench['Bearing'], np.arange(0, 360+N, N), 
                           retbins = False)
carb_bench_counts = carb_bench_binned.value_counts(sort = False)

coarse = coarse.sort_values('Bearing', inplace=False)
coarse_binned = pd.cut(coarse['Bearing'], np.arange(0, 360+N, N), 
                       retbins = False)
coarse_counts = coarse_binned.value_counts(sort = False)

fine = fine.sort_values('Bearing', inplace=False)
fine_binned = pd.cut(fine['Bearing'], np.arange(0, 360+N, N), retbins = False)
fine_counts = fine_binned.value_counts(sort = False)

#mke the figure
fig, axes = plt.subplots(2, 2, figsize = (8, 8), 
                         subplot_kw={'projection': 'polar'})
carb_thalweg = axes[0, 0] 
carb_bench = axes[0, 1]
coarse = axes[1, 0]
fine = axes[1,1]

#define "x" coordinate, which in this case is the orientation
theta = np.arange(np.radians(N/2), np.radians(360+N/2), np.radians(N)) 
width = np.pi/4*np.ones(N)

carb_thalweg.bar(theta, carb_thalweg_counts, width = np.radians(N), 
                 color = 'lightblue', edgecolor = 'k')
carb_thalweg.set_theta_zero_location("N")
carb_thalweg.set_theta_direction(-1)
carb_thalweg.set_ylim(0, 10)
carb_thalweg.set_yticks(np.arange(0, 15, 5))
carb_thalweg.set_yticklabels(['', '5', '10'])
carb_thalweg.set_axisbelow(True)
carb_thalweg.grid(True, color = 'gray', linewidth = 1)
carb_thalweg.set_title('Carbonate (thalweg)', fontsize = 16)

carb_bench.bar(theta, carb_bench_counts, width = np.radians(N), 
               color = 'lightblue', edgecolor = 'k')
carb_bench.set_theta_zero_location("N")
carb_bench.set_theta_direction(-1)
carb_bench.set_ylim(0, 10)
carb_bench.set_yticks(np.arange(0, 15, 5))
carb_bench.set_yticklabels(['', '5', '10'])
carb_bench.set_axisbelow(True)
carb_bench.grid(True, color = 'gray', linewidth = 1)
carb_bench.set_title('Carbonate (bank)', fontsize = 16)


coarse.bar(theta, coarse_counts, width = np.radians(N), 
           color = 'moccasin', edgecolor = 'k')
coarse.set_theta_zero_location("N")
coarse.set_theta_direction(-1)
coarse.set_ylim(0, 10)
coarse.set_yticks(np.arange(0, 15, 5))
coarse.set_yticklabels(['', '5', '10'])
coarse.set_axisbelow(True)
coarse.grid(True, color = 'gray', linewidth = 1)
coarse.set_title('Coarse sandstone', fontsize = 16)

fine.bar(theta, fine_counts, width = np.radians(N), 
         color = 'moccasin', edgecolor = 'k')
fine.set_theta_zero_location("N")
fine.set_theta_direction(-1)
fine.set_ylim(0, 10)
fine.set_yticks(np.arange(0, 15, 5))
fine.set_yticklabels(['', '5', '10'])
fine.set_axisbelow(True)
fine.grid(True, color = 'gray', linewidth = 1)
fine.set_title('Fine sandstone', fontsize = 16)

plt.tight_layout()

fig.savefig('../figures/fig9_fracture_orientation.png', dpi=1000, bbox_inches = 'tight')
fig.savefig('../figures/fig9_fracture_orientation.pdf', dpi=1000, bbox_inches = 'tight')
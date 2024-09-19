#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to analyze bed thickness and fracture spacing data and produce
Figure 8 in the following paper:
    
    Colaianne, N.J., Shobe, C.M., Moler, J., Benison, K.C., and Chilton, K.D.
    (resubmitted September 2024) Beyond boundaries: Depositional environment 
    controls on erodibility, process, and form in rivers incising sedimentary 
    bedrock. Geosphere.
    
Please cite the code repository and/or paper if you use this code.

@author: Charles M. Shobe, U.S. Forest Service Rocky Mountain Research Station
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kruskal, mannwhitneyu
import scikit_posthocs

#import and analyze bed thickness data
beds = pd.read_csv('bedding_thickness.csv', delimiter = ',', 
                   encoding = 'UTF-8')
beds = beds[:25] #cut out trailing NaNs

#calculate averages
beds_fine_mean = beds.mean(skipna = True).iloc[0]
beds_coarse_mean = beds.mean(skipna = True).iloc[1]
beds_carb_mean = beds.mean(skipna = True).iloc[2]

#import and analyze fracture spacing data
fractures = pd.read_csv('fracture_spacing.csv', delimiter = ',', 
                        encoding = 'UTF-8')*100 #convert m to cm

fractures_fine_mean = fractures.mean(skipna = True).iloc[0]
fractures_coarse_mean = fractures.mean(skipna = True).iloc[1]

#separate carbonate fractures into thalweg and bank set based on the indicator 
# number in column 'Carb-transect.' 100 = thalweg; 200 = bank
fractures_carb_thalweg = fractures[['Carb', 'Carb-transect']][fractures['Carb-transect'] == 100]
fractures_carb_thalweg_mean = fractures_carb_thalweg.mean().iloc[0]

fractures_carb_bank = fractures[['Carb', 'Carb-transect']][fractures['Carb-transect'] == 200]
fractures_carb_bank_mean = fractures_carb_bank.mean().iloc[0]

#make figure#################################################################
fig, ax = plt.subplots(figsize = (6, 4.7))
size = 300

#plot bed thickness/fracture spacing data
ax.scatter(beds_fine_mean, fractures_fine_mean, s = size, marker = 's', 
           facecolor = 'moccasin', edgecolor = 'k', zorder = 2, 
           label = 'Fine sandstone')
ax.scatter(beds_coarse_mean, fractures_coarse_mean, s = size, marker = 'o', 
           facecolor = 'moccasin', edgecolor = 'k', zorder = 2, 
           label = 'Coarse sandstone')
ax.scatter(beds_carb_mean, fractures_carb_thalweg_mean, s = size, marker = '^', 
           facecolor = 'lightblue', edgecolor = 'k', zorder = 2, 
           label = 'Carbonate T (thalweg)')
ax.scatter(beds_carb_mean, fractures_carb_bank_mean, s = size, marker = '^', 
           facecolor = 'lightblue', edgecolor = 'k', zorder = 4, 
           label = 'Carbonate B (bank)')

#plot bed thickness/fracture spacing error bars
beds_fine_stdev = beds.std().iloc[0]
fractures_fine_stdev = fractures.std().iloc[0]
ax.errorbar(beds_fine_mean, fractures_fine_mean, xerr = beds_fine_stdev, 
            yerr = fractures_fine_stdev, color = 'k', zorder = 1, capsize = 4)

beds_coarse_stdev = beds.std().iloc[1]
fractures_coarse_stdev = fractures.std().iloc[1]
ax.errorbar(beds_coarse_mean, fractures_coarse_mean, xerr = beds_coarse_stdev, 
            yerr = fractures_coarse_stdev, color = 'k', zorder = 1, 
            capsize = 4)

beds_carb_stdev = beds.std().iloc[2]
fractures_thalweg_stdev = fractures_carb_thalweg.std().iloc[0]
fractures_bank_stdev = fractures_carb_bank.std().iloc[0]

eb1 = ax.errorbar(beds_carb_mean, fractures_carb_thalweg_mean, 
                  xerr = beds_carb_stdev, yerr = fractures_thalweg_stdev, 
                  color = 'k', zorder = 1, capsize = 4)
eb2 = ax.errorbar(beds_carb_mean, fractures_carb_bank_mean, 
                  xerr = beds_carb_stdev, yerr = fractures_bank_stdev, 
                  color = 'k', zorder = 3, capsize = 4, ecolor = 'gray')
eb2[-1][0].set_linestyle(':')
eb2[-1][1].set_linestyle(':')

ax.set_xlabel('Bed thickness [cm]', fontsize = 16)
ax.set_ylabel('Fracture spacing [cm]', fontsize = 16)

ax.set_xlim(-5, 100)
ax.set_ylim(-10, 500)
ax.legend(loc = 'lower right', labelspacing = 1, edgecolor = 'k', 
          borderpad = 1)

ax.text(39.5, 148, 'T', fontsize = 14)
ax.text(39.5, 285, 'B', fontsize = 14)

plt.tight_layout()
fig.savefig('fig8_beds_fractures.png', dpi=1000, bbox_inches = 'tight')

#statistical testing: bed thickness
beds_fine = beds['Fine'][0:17]
beds_coarse = beds['Coarse'][0:18]
beds_carb = beds['Carb']
beds_all_ss = pd.concat([beds['Fine'][0:17], beds['Coarse'][0:18]])
kw_beds = kruskal(beds_fine, beds_coarse, beds_carb)
dunns_beds = scikit_posthocs.posthoc_dunn([beds_fine, beds_coarse, beds_carb], 
                                          p_adjust = 'bonferroni')
mwu_beds = mannwhitneyu(beds_all_ss, beds_carb)

#statistical testing: fracture spacing
fractures_carb_thalweg_stats = fractures_carb_thalweg['Carb']
fractures_carb_bank_stats = fractures_carb_bank['Carb']
fractures_fine_stats = fractures['Fine']
fractures_coarse_stats = fractures['Coarse'][0:26]
fracs_all_ss = pd.concat([fractures_fine_stats, fractures_coarse_stats])
fracs_all_carb = pd.concat([fractures_carb_thalweg_stats, 
                            fractures_carb_bank_stats])
kw_fracs = kruskal(fractures_fine_stats, fractures_coarse_stats, 
                   fractures_carb_thalweg_stats, fractures_carb_bank_stats)
dunns_fracs = scikit_posthocs.posthoc_dunn([fractures_fine_stats, 
                                            fractures_coarse_stats, 
                                            fractures_carb_thalweg_stats, 
                                            fractures_carb_bank_stats], 
                                           p_adjust = 'bonferroni')
kw_fracs_combined_carbs = kruskal(fractures_fine_stats, fractures_coarse_stats, fracs_all_carb)
dunns_fracs_combined_carbs = scikit_posthocs.posthoc_dunn([fractures_fine_stats, fractures_coarse_stats, fracs_all_carb], p_adjust = 'bonferroni')
mwu_fracs = mannwhitneyu(fracs_all_ss, fracs_all_carb)


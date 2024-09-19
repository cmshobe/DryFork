#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to analyze channel cross-section surveys and produce
Figure 11 in the following paper:
    
    Colaianne, N.J., Shobe, C.M., Moler, J., Benison, K.C., and Chilton, K.D.
    (resubmitted September 2024) Beyond boundaries: Depositional environment 
    controls on erodibility, process, and form in rivers incising sedimentary 
    bedrock. Geosphere.
    
Please cite the code repository and/or paper if you use this code.

@author: Charles M. Shobe, U.S. Forest Service Rocky Mountain Research Station
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu
import scikit_posthocs

#define function to linearly interpolate cross-sections to dx resolution
def densify_xs(df, dx):
    df = df.sort_values(by = 'Position').reset_index(drop=True)
    x = df['Position']
    z = df['Normalized_Z']
    xnew = np.arange(df.loc[0, 'Position'], df.loc[df.index[-1], 'Position'] + dx, dx)
    znew = np.interp(xnew, x, z)
    return xnew, znew

#import cross-section survey data#############################################

#import carbonate cross-section survey data
carb1 = pd.read_csv('DFC_1.csv')
carb2 = pd.read_csv('DFC_2.csv')
carb3 = pd.read_csv('DFC_3.csv')
carb4 = pd.read_csv('DFC_4.csv')
carb5 = pd.read_csv('DFC_5.csv')
carb6 = pd.read_csv('DFC_6.csv')
carb7 = pd.read_csv('DFC_7.csv')
carb8 = pd.read_csv('DFC_8.csv')
carb9 = pd.read_csv('DFC_9.csv')
carb10 = pd.read_csv('DFC_10.csv')

#import fine sandstone cross-section survey data
fine1 = pd.read_csv('DFSSF_1.csv')
fine2 = pd.read_csv('DFSSF_2.csv')
fine3 = pd.read_csv('DFSSF_3.csv')
fine4 = pd.read_csv('DFSSF_4.csv')
fine5 = pd.read_csv('DFSSF_5.csv')
fine6 = pd.read_csv('DFSSF_6.csv')
fine7 = pd.read_csv('DFSSF_7.csv')
fine8 = pd.read_csv('DFSSF_8.csv')
fine9 = pd.read_csv('DFSSF_9.csv')
fine10 = pd.read_csv('DFSSF_10.csv')

#import coarse sandstone cross-section survey data
coarse1 = pd.read_csv('DFSSC_1.csv')
coarse2 = pd.read_csv('DFSSC_2.csv')
coarse3 = pd.read_csv('DFSSC_3.csv')
coarse4 = pd.read_csv('DFSSC_4.csv')
coarse5 = pd.read_csv('DFSSC_5.csv')
coarse6 = pd.read_csv('DFSSC_6.csv')
coarse7 = pd.read_csv('DFSSC_7.csv')
coarse8 = pd.read_csv('DFSSC_8.csv')
coarse9 = pd.read_csv('DFSSC_9.csv')
coarse10 = pd.read_csv('DFSSC_10.csv')

list_of_dfs_carb = [carb1, carb2, carb3, carb4, carb5, carb6, carb7, carb8, carb9, carb10]
list_of_dfs_coarse = [coarse1, coarse2, coarse3, coarse4, coarse5, coarse6, coarse7, coarse8, coarse9, coarse10]
list_of_dfs_fine = [fine1, fine2, fine3, fine4, fine5, fine6, fine7, fine8, fine9, fine10]
list_of_dfs = list_of_dfs_carb + list_of_dfs_coarse + list_of_dfs_fine

save_carb_elevs = np.array([])
save_coarse_elevs = np.array([])
save_fine_elevs = np.array([])

save_carb_elevs_uniform_banks = np.array([])
save_coarse_elevs_uniform_banks = np.array([])
save_fine_elevs_uniform_banks = np.array([])

#interpolate cross-sections to dx resolution, then resample to sample_spacing

dx = 0.01

for i in range(len(list_of_dfs)):
    df = list_of_dfs[i]
    xnew, znew = densify_xs(df, dx)
    
    #sample densified xs at known spacing
    sample_spacing = 0.1 #m
    factor = 100
    sample_spacing *= factor
    xnew *= factor
    sampled_x = xnew[xnew % sample_spacing == 0]
    sampled_x /= factor
    
    sampled_z = znew[xnew % sample_spacing == 0]

    #decimate to cut out bank elevations that were not surveyed on both banks
    if i == 20:
        sampled_z_uniform_banks = sampled_z[sampled_z < np.minimum(sampled_z[1], sampled_z[-1])]
    else:
        sampled_z_uniform_banks = sampled_z[sampled_z < np.minimum(sampled_z[0], sampled_z[-1])]

    
    if i < 10: #data is carbonate
        save_carb_elevs = np.concatenate((save_carb_elevs, sampled_z))
        save_carb_elevs_uniform_banks = np.concatenate((save_carb_elevs_uniform_banks, sampled_z_uniform_banks))
    elif (i >= 10) and (i < 20):
        save_coarse_elevs = np.concatenate((save_coarse_elevs, sampled_z))
        save_coarse_elevs_uniform_banks = np.concatenate((save_coarse_elevs_uniform_banks, sampled_z_uniform_banks))
    elif i >= 20:
        save_fine_elevs = np.concatenate((save_fine_elevs, sampled_z))
        save_fine_elevs_uniform_banks = np.concatenate((save_fine_elevs_uniform_banks, sampled_z_uniform_banks))
    else:
        print('no condition satisfied! check code')
    
    
#create Figure 11: cross-section hypsometry#################################
bins = np.arange(0, 2, 0.1)

fig2, axs2 = plt.subplots(1, 3, figsize = (10, 4))
ax1 = axs2[0]
ax2 = axs2[1]
ax3 = axs2[2]
bins = np.arange(0, 4, 0.1)
ax1.hist(save_carb_elevs_uniform_banks, color = 'lightblue', alpha = 1., edgecolor = 'k', label = 'carb', density = True, bins = bins, orientation = 'horizontal', histtype='stepfilled')
ax2.hist(save_coarse_elevs_uniform_banks, color = 'moccasin', alpha = 1., edgecolor = 'k', label = 'coarse', density = True, bins = bins, orientation = 'horizontal', histtype='stepfilled')
ax3.hist(save_fine_elevs_uniform_banks, color = 'moccasin', alpha = 1., edgecolor = 'k', label = 'fine', density = True, bins = bins, orientation = 'horizontal', histtype='stepfilled')


ax1.set_title('A) Carbonate', y = 1.0, pad = -16, fontsize = 16)
ax2.set_title('B) Coarse sandstone', y = 1.0, pad = -16, fontsize = 16)
ax3.set_title('C) Fine sandstone', y = 1.0, pad = -16, fontsize = 16)

ax1.set_xlabel('Density', fontsize = 16)
ax2.set_xlabel('Density', fontsize = 16)
ax3.set_xlabel('Density', fontsize = 16)

ax1.set_xlim(0, 1.7)
ax2.set_xlim(0, 1.7)
ax3.set_xlim(0, 1.7)


ax1.set_xticks(np.arange(0, 2, 0.5))
ax1.set_yticks(np.arange(0, 4.5, 0.5))
ax2.set_xticks(np.arange(0, 2, 0.5))
ax2.set(yticklabels=[])
ax3.set_xticks(np.arange(0, 2, 0.5))
ax3.set(yticklabels=[])

ax1.set_ylabel('Elevation above thalweg [m]', fontsize = 16)
plt.tight_layout()
fig2.savefig('fig11_xs_hypsometry.png', dpi = 1000, bbox_inches = 'tight')


#statistical testing to assess whether distributions differ among rock units
kw = kruskal(save_carb_elevs, save_coarse_elevs, save_fine_elevs)
dunns = scikit_posthocs.posthoc_dunn([save_carb_elevs, save_coarse_elevs, save_fine_elevs], p_adjust = 'bonferroni')

#combine coarse and fine sandstone data to assess carbonate versus sandstone
all_ss_elevs_uniform_banks = np.concatenate((save_coarse_elevs_uniform_banks, save_fine_elevs_uniform_banks), axis = 0)
mwu = mannwhitneyu(save_carb_elevs_uniform_banks, all_ss_elevs_uniform_banks)

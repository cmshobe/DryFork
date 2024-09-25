#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to analyze channel cross-section surveys and produce
Figure 12 in the following paper:
    
    Colaianne, N.J., Shobe, C.M., Moler, J., Benison, K.C., and Chilton, K.D.
    (resubmitted September 2024) Beyond boundaries: Depositional environment 
    controls on erodibility, process, and form in rivers incising sedimentary 
    bedrock. Geosphere.
    
Please cite the code repository and/or paper if you use this code.

@author: Charles M. Shobe, U.S. Forest Service Rocky Mountain Research Station
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

def densify_xs(df, dx):
    df = df.sort_values(by = 'Position').reset_index(drop=True)
    x = df['Position']
    z = df['Normalized_Z']
    xnew = np.arange(df.loc[0, 'Position'], df.loc[df.index[-1], 'Position'] + dx, dx)
    znew = np.interp(xnew, x, z)
    return xnew, znew

#import cross-section survey data#############################################
path = '../data/cross_section_form/'

#import carbonate cross-section survey data
carb1 = pd.read_csv(path + 'DFC_1.csv')
carb2 = pd.read_csv(path + 'DFC_2.csv')
carb3 = pd.read_csv(path + 'DFC_3.csv')
carb4 = pd.read_csv(path + 'DFC_4.csv')
carb5 = pd.read_csv(path + 'DFC_5.csv')
carb6 = pd.read_csv(path + 'DFC_6.csv')
carb7 = pd.read_csv(path + 'DFC_7.csv')
carb8 = pd.read_csv(path + 'DFC_8.csv')
carb9 = pd.read_csv(path + 'DFC_9.csv')
carb10 = pd.read_csv(path + 'DFC_10.csv')

#import fine sandstone cross-section survey data
fine1 = pd.read_csv(path + 'DFSSF_1.csv')
fine2 = pd.read_csv(path + 'DFSSF_2.csv')
fine3 = pd.read_csv(path + 'DFSSF_3.csv')
fine4 = pd.read_csv(path + 'DFSSF_4.csv')
fine5 = pd.read_csv(path + 'DFSSF_5.csv')
fine6 = pd.read_csv(path + 'DFSSF_6.csv')
fine7 = pd.read_csv(path + 'DFSSF_7.csv')
fine8 = pd.read_csv(path + 'DFSSF_8.csv')
fine9 = pd.read_csv(path + 'DFSSF_9.csv')
fine10 = pd.read_csv(path + 'DFSSF_10.csv')

#import coarse sandstone cross-section survey data
coarse1 = pd.read_csv(path + 'DFSSC_1.csv')
coarse2 = pd.read_csv(path + 'DFSSC_2.csv')
coarse3 = pd.read_csv(path + 'DFSSC_3.csv')
coarse4 = pd.read_csv(path + 'DFSSC_4.csv')
coarse5 = pd.read_csv(path + 'DFSSC_5.csv')
coarse6 = pd.read_csv(path + 'DFSSC_6.csv')
coarse7 = pd.read_csv(path + 'DFSSC_7.csv')
coarse8 = pd.read_csv(path + 'DFSSC_8.csv')
coarse9 = pd.read_csv(path + 'DFSSC_9.csv')
coarse10 = pd.read_csv(path + 'DFSSC_10.csv')

list_of_dfs_carb = [carb1, carb2, carb3, carb4, carb5, 
                    carb6, carb7, carb8, carb9, carb10]
list_of_dfs_coarse = [coarse1, coarse2, coarse3, coarse4, coarse5, 
                      coarse6, coarse7, coarse8, coarse9, coarse10]
list_of_dfs_fine = [fine1, fine2, fine3, fine4, fine5, 
                    fine6, fine7, fine8, fine9, fine10]
list_of_dfs = list_of_dfs_carb + list_of_dfs_coarse + list_of_dfs_fine

for df in list_of_dfs:
    if df['Position'].is_monotonic_increasing == False:
        df.sort_values('Position', inplace = True)

#interpolate cross-sections to dx resolution, then resample to 
#a number of different sample_spacings, finding inflection points each time

#iterate through resampling scales (will be x-axis of plot ultimately)
spacings = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,  
                     1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 5.5, 6., 6.5, 7., 
                     7.5, 8., 8.5, 9., 9.5, 10.])

#create data structure to hold output: n_spacings x n_dfs
inflection_data = np.zeros((len(spacings), len(list_of_dfs)))

dx = 0.1

for j in range(len(spacings)):
    #iterate through the 30 cross-sections, calculating the number of inflection 
    #points in each one (at a given resampling scale)
    for i in range(len(list_of_dfs)):
        sample_spacing = spacings[j]
        df = list_of_dfs[i]
        xnew, znew = densify_xs(df, dx)
        
        #sample densified xs at known spacing
        factor = 100
        sample_spacing *= factor
        xnew *= factor
        sampled_x = xnew[np.isclose(xnew % sample_spacing, 0, atol=1e-3)]
        sampled_x /= factor
        
        sampled_z = znew[np.isclose(xnew % sample_spacing, 0, atol=1e-3)]
        
        # find inflection points
        infls = np.where(np.diff(np.sign(np.diff(sampled_z))) != 0)[0]
        infls += 1

        inflection_data[j, i] = len(infls)

xs_lengths = np.zeros(30)
iter = 0
for df in list_of_dfs:
    xs_lengths[iter] = df.loc[df.index[-1], 'Position']
    iter += 1
    
inflection_frequency = np.divide(inflection_data, xs_lengths)

carb_averages_raw = np.mean(inflection_data[:, 0:10], axis = 1)
coarse_averages_raw = np.mean(inflection_data[:, 10:20], axis = 1)
fine_averages_raw = np.mean(inflection_data[:, 20:30], axis = 1)

carb_averages = np.mean(inflection_frequency[:, 0:10], axis = 1)
coarse_averages = np.mean(inflection_frequency[:, 10:20], axis = 1)
fine_averages = np.mean(inflection_frequency[:, 20:30], axis = 1)


#create Figure 12: cross-section roughness#################################

fig, axs = plt.subplots(1, 1, figsize = (6, 4.5))

edgecolor = matplotlib.colors.ColorConverter().to_rgba('k', alpha=0.2)
markersize = 100

carb_facecolor = matplotlib.colors.ColorConverter().to_rgba('lightblue', 
                                                            alpha = 0.2)
carb_zorder = 5


coarse_facecolor = matplotlib.colors.ColorConverter().to_rgba('moccasin', 
                                                              alpha = 0.2)
coarse_zorder = 4


fine_facecolor = matplotlib.colors.ColorConverter().to_rgba('moccasin', 
                                                            alpha = 0.2)
fine_alpha = 0.5
fine_zorder = 3

averages = axs

averages.scatter(spacings, carb_averages, s = 100, color = carb_facecolor, 
                 marker = '^', alpha = 1., edgecolor = 'k', zorder = 3, 
                 label = 'Carbonate', clip_on = False)
averages.scatter(spacings, coarse_averages, s = 100, color = coarse_facecolor, 
                 marker = 'o', alpha = 1., edgecolor = 'k', zorder = 3, 
                 label = 'Coarse sandstone', clip_on = False)
averages.scatter(spacings, fine_averages, s = 100, color = fine_facecolor, 
                 marker = 's', alpha = 1., edgecolor = 'k', zorder = 3, 
                 label = 'Fine sandstone', clip_on = False)

averages.text(-1.7, 0.23, 'rougher' '\n' 'boundary', style = 'italic')
averages.text(-1.7, 0.0, 'smoother' '\n' 'boundary', style = 'italic')


averages.set_xlabel('Sampling interval [m]', fontsize = 16)
averages.set_ylabel('Inflection frequency [m$^{-1}$]', fontsize = 16)

handles, labels = averages.get_legend_handles_labels()
averages.legend(handles[::-1], labels[::-1], loc='upper right', 
                edgecolor = 'k')

averages.set_xlim(0, 10)

averages.axvspan(0.2, 3, alpha = 0.5, color = 'gray')
averages.text(1, 0.02, 
              'typical' + '\n' 'surveyed' + '\n' + 'point' + '\n' + 'spacing')

plt.tight_layout()
fig.savefig('../figures/fig12_xs_roughness.png', dpi = 1000, 
            bbox_inches = 'tight')
fig.savefig('../figures/fig12_xs_roughness.pdf', dpi = 1000, 
            bbox_inches = 'tight')
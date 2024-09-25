#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to analyze channel cross-section surveys and produce
Figure 10 in the following paper:
    
    Colaianne, N.J., Shobe, C.M., Moler, J., Benison, K.C., and Chilton, K.D.
    (resubmitted September 2024) Beyond boundaries: Depositional environment 
    controls on erodibility, process, and form in rivers incising sedimentary 
    bedrock. Geosphere.
    
Please cite the code repository and/or paper if you use this code.

@author: Charles M. Shobe, U.S. Forest Service Rocky Mountain Research Station
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

#create Figure 10: all channel cross-sections#################################

#plot only some of the XSs
n_rows = 10 #number of rows in the figure
to_plot = np.arange(0, n_rows)
list_of_dfs_carb = [carb1, carb2, carb3, carb4, carb5, carb6, carb7, carb8, carb9, carb10]
list_of_dfs_coarse = [coarse1, coarse2, coarse3, coarse4, coarse5, coarse6, coarse7, coarse8, coarse9, coarse10]
list_of_dfs_fine = [fine1, fine2, fine3, fine4, fine5, fine6, fine7, fine8, fine9, fine10]

fig, axs = plt.subplots(n_rows, 3, figsize= (10, n_rows * 0.75))
#fig.patch.set_alpha(0.)
markersize = 3
for i in to_plot:
    

    axcarb = axs[i, 0]
    axcarb.plot(list_of_dfs_carb[i]['Position'], 
                list_of_dfs_carb[i]['Normalized_Z'], 
                color = 'lightblue', linewidth = 3, 
                zorder = 1, clip_on=False)
    axcarb.scatter(list_of_dfs_carb[i]['Position'], 
                   list_of_dfs_carb[i]['Normalized_Z'], 
                   color = 'k', s = markersize, 
                   zorder = 2, clip_on=False)
    axcarb.spines['top'].set_visible(False)
    axcarb.set_yticks(np.arange(0, 3, 1))
    axcarb.patch.set_alpha(0)
    
    axcoarse = axs[i, 1]
    axcoarse.plot(list_of_dfs_coarse[i]['Position'], 
                  list_of_dfs_coarse[i]['Normalized_Z'], 
                  color = 'moccasin', linewidth = 3, 
                  zorder = 1, clip_on=False)
    axcoarse.scatter(list_of_dfs_coarse[i]['Position'], 
                     list_of_dfs_coarse[i]['Normalized_Z'], 
                     color = 'k', s = markersize, 
                     zorder = 2, clip_on=False)
    axcoarse.spines['top'].set_visible(False)
    axcoarse.patch.set_alpha(0)
    
    axfine = axs[i, 2]
    axfine.plot(list_of_dfs_fine[i]['Position'], 
                list_of_dfs_fine[i]['Normalized_Z'], 
                color = 'moccasin', linewidth = 3, 
                zorder = 1, clip_on=False)
    axfine.scatter(list_of_dfs_fine[i]['Position'], 
                   list_of_dfs_fine[i]['Normalized_Z'], 
                   color = 'k', s = markersize, 
                   zorder = 2, clip_on=False)
    axfine.spines['top'].set_visible(False)
    axfine.patch.set_alpha(0)
    
    if i < n_rows - 1:
        axcarb.get_xaxis().set_visible(False)
        axcoarse.get_xaxis().set_visible(False)
        axfine.get_xaxis().set_visible(False)
        
        axcarb.spines['bottom'].set_visible(True)
        axcoarse.spines['bottom'].set_visible(True)
        axfine.spines['bottom'].set_visible(True)
        
        axcarb.get_yaxis().set_visible(True)
    
    axcoarse.get_yaxis().set_visible(False)
    axfine.get_yaxis().set_visible(False)
    
    if i == 0:
        axcarb.set_title('Carbonate', y = 1, pad = -16, fontsize = 16)
        axcoarse.set_title('Coarse sandstone', y = 1, pad = -16, fontsize = 16)
        axfine.set_title('Fine sandstone', y = 1, pad = -16, fontsize = 16)
        
        axcarb.spines['top'].set_visible(True)
        axcoarse.spines['top'].set_visible(True)
        axfine.spines['top'].set_visible(True)
        
        axcarb.set_yticks(np.arange(4))
            
#set all xlims and ylims to the maximum value
plt.setp(axs, xlim=(0, 57), ylim=(0, 3))

plt.tight_layout()
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.0)

axcarb.set_ylabel('Elevation above thalweg [m]', fontsize = 16)
axcarb.yaxis.set_label_coords(-0.1,5)

axcarb.set_xlabel('Distance [m]', fontsize = 16)
axcarb.xaxis.set_label_coords(1.5,-0.5)

fig.savefig('../figures/fig10_all_XSs.png', dpi=1000, bbox_inches = 'tight')
fig.savefig('../figures/fig10_all_XSs.pdf', dpi=1000, bbox_inches = 'tight')
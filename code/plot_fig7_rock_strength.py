#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to analyze rock strength data and produce
Figure 7 in the following paper:
    
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

all_breaks = pd.read_csv('../data/rock_strength/strength_data.csv')
all_breaks = all_breaks[all_breaks['Is50MPa'] != '#VALUE!']
all_breaks['Is50MPa'] = all_breaks['Is50MPa'].astype(float)

carb = all_breaks.loc[(all_breaks['Lithology'] == 'C1') | (all_breaks['Lithology'] == 'C2') | (all_breaks['Lithology'] == 'C3') | (all_breaks['Lithology'] == 'C4')]
c1 = all_breaks.loc[(all_breaks['Lithology'] == 'C1')]
c2 = all_breaks.loc[(all_breaks['Lithology'] == 'C2')]
c3 = all_breaks.loc[(all_breaks['Lithology'] == 'C3')]
c4 = all_breaks.loc[(all_breaks['Lithology'] == 'C4')]

sandstone = all_breaks.loc[(all_breaks['Lithology'] == 'SS1') | (all_breaks['Lithology'] == 'SS2')]
coarse =  all_breaks.loc[(all_breaks['Lithology'] == 'SS2')]
fine = all_breaks.loc[(all_breaks['Lithology'] == 'SS1')]

#make figure#################################################################
hfont = {'fontname':'Arial'}

fig = plt.figure(figsize = (8, 4))
widths = [7, 2]
gs = fig.add_gridspec(ncols = 2, nrows = 1, width_ratios = widths)
separate = fig.add_subplot(gs[0])
combined = fig.add_subplot(gs[1])

separate.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

color = dict(boxes='black', whiskers='black', medians='black', caps='black')

box = dict(linewidth = 2.0)
whiskers = dict(linewidth = 2.0)
median = dict(linewidth = 2.0, color = 'k')
caps = dict(linewidth = 2.0)
means = dict(marker = 'o', markeredgecolor = 'k', markerfacecolor = 'k')

separate_violin = separate.violinplot([c1['Is50MPa'], c2['Is50MPa'], c3['Is50MPa'], c4['Is50MPa'], coarse['Is50MPa'], fine['Is50MPa']], showextrema = False)
combined_violin = combined.violinplot([carb['Is50MPa'], sandstone['Is50MPa']], showextrema = False)

separate.set_ylim(0, 8)
combined.set_ylim(0, 8)

separate.set_ylabel('Point load index [MPa]', fontsize = 16, **hfont)
separate.set_xticks([1, 2, 3, 4, 5, 6], ['C1', 'C2', 'C3', 'C4', 'Coarse', 'Fine'], **hfont)
separate.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8], ['0', '1', '2', '3', '4', '5', '6', '7', '8'], **hfont)

separate.tick_params(axis='both', which='major', labelsize=12)
combined.tick_params(axis='both', which='major', labelsize=12)


combined.set_xticks([1,2], ['All carb', 'All SS'], **hfont)
combined.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

combined.yaxis.set_ticklabels([])

iter = 0
for pc in separate_violin['bodies']:
    colors = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'moccasin', 'moccasin']
    pc.set_facecolor(colors[iter])
    pc.set_edgecolor('black')
    pc.set_linewidth = 2
    pc.set_alpha(1)
    iter += 1

iter = 0
for pc in combined_violin['bodies']:
    colors = ['lightblue', 'moccasin']
    pc.set_facecolor(colors[iter])
    pc.set_edgecolor('black')
    pc.set_linewidth = 2
    pc.set_alpha(1)
    iter += 1

def adjacent_values(vals, q1, q3):
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value


quartile1, medians, quartile3 = np.percentile(c1['Is50MPa'], [25, 50, 75], axis=0)
inds = np.arange(1, 1 + 1)
separate.scatter(inds, medians, marker='^', color='white', s=30, zorder=3)
separate.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
separate.vlines(inds, np.min(c1['Is50MPa']), np.max(c1['Is50MPa']), color='k', linestyle='-', lw=1)


quartile1, medians, quartile3 = np.percentile(c2['Is50MPa'], [25, 50, 75], axis=0)
inds = np.arange(2, 2 + 1)
separate.scatter(inds, medians, marker='^', color='white', s=30, zorder=3)
separate.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
separate.vlines(inds, np.min(c2['Is50MPa']), np.max(c2['Is50MPa']), color='k', linestyle='-', lw=1)

quartile1, medians, quartile3 = np.percentile(c3['Is50MPa'], [25, 50, 75], axis=0)
inds = np.arange(3, 3 + 1)
separate.scatter(inds, medians, marker='^', color='white', s=30, zorder=3)
separate.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
separate.vlines(inds, np.min(c3['Is50MPa']), np.max(c3['Is50MPa']), color='k', linestyle='-', lw=1)

quartile1, medians, quartile3 = np.percentile(c4['Is50MPa'], [25, 50, 75], axis=0)
inds = np.arange(4, 4 + 1)
separate.scatter(inds, medians, marker='^', color='white', s=30, zorder=3)
separate.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
separate.vlines(inds, np.min(c4['Is50MPa']), np.max(c4['Is50MPa']), color='k', linestyle='-', lw=1)

quartile1, medians, quartile3 = np.percentile(coarse['Is50MPa'], [25, 50, 75], axis=0)
inds = np.arange(5, 5 + 1)
separate.scatter(inds, medians, marker='^', color='white', s=30, zorder=3)
separate.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
separate.vlines(inds, np.min(coarse['Is50MPa']), np.max(coarse['Is50MPa']), color='k', linestyle='-', lw=1)

quartile1, medians, quartile3 = np.percentile(fine['Is50MPa'], [25, 50, 75], axis=0)
inds = np.arange(6, 6 + 1)
separate.scatter(inds, medians, marker='^', color='white', s=30, zorder=3)
separate.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
separate.vlines(inds, np.min(fine['Is50MPa']), np.max(fine['Is50MPa']), color='k', linestyle='-', lw=1)


quartile1, medians, quartile3 = np.percentile(carb['Is50MPa'], [25, 50, 75], axis=0)
inds = np.arange(1, 1 + 1)
combined.scatter(inds, medians, marker='^', color='white', s=30, zorder=3)
combined.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
combined.vlines(inds, np.min(carb['Is50MPa']), np.max(carb['Is50MPa']), color='k', linestyle='-', lw=1)


quartile1, medians, quartile3 = np.percentile(sandstone['Is50MPa'], [25, 50, 75], axis=0)
inds = np.arange(2, 2 + 1)
combined.scatter(inds, medians, marker='^', color='white', s=30, zorder=3)
combined.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
combined.vlines(inds, np.min(sandstone['Is50MPa']), np.max(sandstone['Is50MPa']), color='k', linestyle='-', lw=1)

separate.text(0.75, 7.7, 'n = ' + str(len(c1)))
separate.text(1.75, 7.7, 'n = ' + str(len(c2)))
separate.text(2.75, 7.7, 'n = ' + str(len(c3)))
separate.text(3.75, 7.7, 'n = ' + str(len(c4)))
separate.text(4.75, 7.7, 'n = ' + str(len(coarse)))
separate.text(5.75, 7.7, 'n = ' + str(len(fine)))

combined.text(0.75, 7.7, 'n = ' + str(len(carb)))
combined.text(1.75, 7.7, 'n = ' + str(len(sandstone)))

plt.tight_layout()
fig.savefig('../figures/fig7_rock_strength.png', dpi=1000, bbox_inches = "tight")

#statistical testing
kw = kruskal(c1['Is50MPa'], c2['Is50MPa'], c3['Is50MPa'], c4['Is50MPa'], coarse['Is50MPa'], fine['Is50MPa'])
dunns = scikit_posthocs.posthoc_dunn([c1['Is50MPa'], c2['Is50MPa'], c3['Is50MPa'], c4['Is50MPa'], coarse['Is50MPa'], fine['Is50MPa']], p_adjust = 'bonferroni')
dunns_lumped_carbs = scikit_posthocs.posthoc_dunn([carb['Is50MPa'], coarse['Is50MPa'], fine['Is50MPa']], p_adjust = 'bonferroni')
mw = mannwhitneyu(carb['Is50MPa'], sandstone['Is50MPa'])
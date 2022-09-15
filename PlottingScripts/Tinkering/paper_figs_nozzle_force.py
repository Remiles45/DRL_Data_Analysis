# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:34:22 2022

@author: Becca
"""

from plottingFunctions import *
import numpy as np
import time 
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
from ParseFile import ParseFile
from matplotlib import cm
import general_plotting_definitions


backpath = '../../../../ExperimentData/LatEmitter/Nozzle Data/'
'''
Single Stage Files
'''
straight_1_path   = backpath + 'Straight/stage_1/straight_IV_T'
convergent_1_path = backpath + 'Convergent/half/stage_1/convergent_h_IV_T'
divergent_1_path  = backpath + 'Divergent/stage_1/divergent_IV_T'
naked_1_path      = backpath + 'No Nozzle/stage_1/no_nozzle_IV_T' 

straight_1_trials   = [1,2,3,4,5,6]
convergent_1_trials = [1,2,'2_1','2_2',3,4,5,6]
divergent_1_trials  = [1,2,3,4,5]
naked_1_trials      = [1,2,3,4,5,6]

straight_1_lbl   = 'Straight'
convergent_1_lbl = 'Convergent'
divergent_1_lbl  = 'Divergent'
naked_1_lbl      = 'No Nozzle'
'''
Two Stage Files
'''
straight_2_path   = backpath + 'Straight/stage_2/straight_2_stage_IV_T'
convergent_2_path = backpath + 'Convergent/half/stage_2/convergent_2_stage_IV_T'
divergent_2_path  = backpath + 'Divergent/stage_2/divergent_2_stage_IV_T'
naked_2_path      = backpath + 'No Nozzle/stage_2/no_nozzle_2_stage_IV_T' 

straight_2_trials   = [1,2,'2_1','2_2',3,4,5,6,'6_2']
convergent_2_trials = [1,2,'2_1',3,4,5] #trial 4 good before 3kV
divergent_2_trials  = [1,4,5,6,7,8,9,10]
naked_2_trials      = [1,2,'2_1','2_2','2_3',3,4,'4_1','4_2',5,6,'6_1']

straight_2_lbl   = '2 Stage Straight'
convergent_2_lbl = '2 Stage Convergent'
divergent_2_lbl  = '2 Stage Divergent'
naked_2_lbl      = '2 Stage No Nozzle'
'''
Three Stage Files
'''
straight_3_path   = backpath + 'Straight/stage_3/straight_3_stage_IV_T'
convergent_3_path = backpath + 'Convergent/half/stage_3/convergent_3_stage_IV_T'
divergent_3_path  = backpath + 'Divergent/stage_3/divergent_3_stage_IV_T'
naked_3_path      = backpath + 'No Nozzle/stage_3/no_nozzle_3_stage_IV_T' 

straight_3_trials   = [3,4,'4_1',5,6,'6_1','6_2','6_3',7,8,'8_1']#1
convergent_3_trials = [1,2,'2_1',3,4,5,6]
divergent_3_trials  = [1,2,3,4,'4_1',5,6,'6_1']
naked_3_trials      = [1,2,5,6,'6_1']#3,4,'4_1','4_2'

straight_3_lbl   = '3 Stage Straight'
convergent_3_lbl = '3 Stage Convergent'
divergent_3_lbl  = '3 Stage Divergent'
naked_3_lbl      = '3 Stage No Nozzle'


plot_data_paths     = [straight_3_path,convergent_3_path,divergent_3_path,naked_3_path]
plot_trial_nums     = [straight_3_trials,convergent_3_trials,divergent_3_trials,naked_3_trials]
plot_legend_entries = [straight_3_lbl,convergent_3_lbl,divergent_3_lbl,naked_3_lbl]
plot_symbols        = ['o','*','x','D']

fig = mpl.figure()
plt = fig.add_subplot()


for i in range(len(plot_data_paths)):
    trials = plot_trial_nums[i]
    path   = plot_data_paths[i]
    if len(plot_symbols)>0:
        sym = plot_symbols[i]
    else:
        sym = 'o'
    
    x,y,y_err = PlotBalance(trials,path)
    y_err = np.array(y_err)
    y_err = np.transpose(y_err)
    adjusted_x = []
    print(i*0.1)
    for pt in x:
        adjusted_x.append(pt+i*0.01)
    plt.errorbar(adjusted_x,y,yerr=y_err,fmt=sym,capsize=5)
   # plt.scatter(x,y)
    
plt.legend(plot_legend_entries)
plt.set_xlabel('Voltage (kV)')
plt.set_ylabel('Force (mN)')
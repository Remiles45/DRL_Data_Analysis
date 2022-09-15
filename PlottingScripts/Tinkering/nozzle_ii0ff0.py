# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 22:39:21 2022

@author: Drew Lab Computer
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 17:25:27 2022

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

    
'''
Init folder locations
'''

path_reverse = '../../../../ExperimentData/LatEmitter/Nozzle Data/'
no_lip_path = path_reverse + 'No Nozzle/stage_3/no_nozzle_3_stage_IV_T'
con_path = path_reverse + 'Convergent/half/stage_3/convergent_3_stage_IV_T'
div_path = path_reverse + 'Divergent/stage_3/divergent_3_stage_IV_T'
straight_path = path_reverse + 'Straight/stage_3/straight_3_stage_IV_T'

no_lip_xy_trials = [11,12,13,14,15,16,17]
no_lip_iv_trials = [5,6,'6_1']
no_lip_lbl = 'No Nozzle' #8.25 uA

deg_20_xy_trials = []
convergent_iv_trials = [1,2,'2_1']#[5,6,7,8]
convergent_lbl = 'Convergent'

deg_45_xy_trials = [1,2,3,4,5]
divergent_iv_trials = [5,6,'6_1']
divergent_lbl = 'Divergent' # 8.6 uA

deg_75_xy_trials = []
straight_iv_trials = [7,8,'8_1']
straight_lbl = 'Straight'



iv_paths = [no_lip_path,con_path,div_path,straight_path]
iv_trials = [no_lip_iv_trials,convergent_iv_trials,divergent_iv_trials,straight_iv_trials]
iv_legend = [convergent_lbl,divergent_lbl,straight_lbl]


mpl.rc('font', family='Arial') 
fig = mpl.figure()
fig.set_size_inches(3.25, 2.5)
plt = fig.add_subplot()
fig.tight_layout()
plot_symbols = []

f2 = mpl.figure()
f2.set_size_inches(3.25, 2.5)
plt2 = f2.add_subplot()
f2.tight_layout()

# f3 = mpl.figure()
# f3.set_size_inches(3.25, 2.5)
# plt3 = f2.add_subplot()
# f3.tight_layout()

IS_NONE = True
n_y = []
cnt = 0
for i in range(len(iv_paths)):
    trials = iv_trials[i]
    path   = iv_paths[i]
    if len(plot_symbols)>0:
        sym = plot_symbols[i]
    else:
        sym = 'o' 
    x,y,y_err = PlotBalance(trials,path,norm=n_y)
    if IS_NONE:
        v_norm,c_norm = PlotCurrent(trials,path,plt2,OUTPUT=True) 
        c_norm = np.array(c_norm)
        v_norm = np.array(v_norm)
        n_y = np.array(y)+0.00000000000001
        IS_NONE = False
        
    
    plt_y = np.array(y)#((np.array(y)/n_y))
    
    y_err = np.array(y_err)
    y_err = np.transpose(y_err)
    shifted_x = np.array(x)+cnt*0.01
    cnt = cnt + 1
    if i>0:
        # plt.scatter(x,plt_y)
        plt.errorbar(shifted_x,plt_y,yerr=y_err,fmt=sym,capsize=3)
        v,c = PlotCurrent(trials,path,plt2,OUTPUT=True)   
        v = np.array(v)
        c = np.array(c)
        plt_v = []
        plt_c = []
        unique_voltages = np.unique(v)
        for voltage in unique_voltages:
            naked_c_idx = np.logical_and(v_norm<=voltage+0.06, v_norm>=voltage-0.06)
            if np.max(naked_c_idx)>0:
                naked_c = np.average(c_norm[naked_c_idx])
                curr_c_idx = v==voltage
                curr_c = np.average(c[curr_c_idx])
                normalized_current = curr_c / naked_c
                plt_c.append(normalized_current)
                plt_v.append(voltage)
        # c_plt = np.array(c)/np.array(c_norm)
        plt2.scatter(plt_v,plt_c)
# plt2.plot([0,4],[1,1],'k--')
plt.legend(iv_legend,loc='lower center',ncol=3,markerscale=0.5,frameon=False,columnspacing=0.5,labelspacing=0.1,handlelength=1)
plt.set_xlabel('Voltage (kV)',labelpad=1)
plt.set_ylabel('F/F$_0$',labelpad=1)

plt.set_ylim(0,1.5)
plt.set_xlim(3,3.55)

# plt2.set_ylim(0,7)
# iv_legend.append('I/I$_0$ = 1')
plt2.legend(iv_legend,loc='lower center',ncol=3,markerscale=0.5,frameon=False,columnspacing=0.5,labelspacing=0.1,handlelength=1)
plt2.set_xlabel('Voltage (kV)',labelpad=1)
plt2.set_ylabel('I/I$_0$',labelpad=1)


plt2.set_ylim(0,2)
plt2.set_xlim(3,3.55)
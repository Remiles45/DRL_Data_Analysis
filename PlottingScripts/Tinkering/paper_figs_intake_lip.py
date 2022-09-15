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

path_reverse = '../../../../ExperimentData/'
no_lip_iv_path_base = path_reverse + 'LatEmitter/Nozzle Data/No Nozzle/stage_1/'
no_lip_xy_path_base = path_reverse + 'LatEmitter/XY data/D1_8mmD2_4mm/'
deg_20_path_base = path_reverse + 'LatEmitter/Intake Lip Data/Without Nozzles/deg_20/'
deg_45_path_base = path_reverse + 'LatEmitter/Intake Lip Data/Without Nozzles/deg_45/'
deg_75_path_base = path_reverse + 'LatEmitter/Intake Lip Data/Without Nozzles/deg_75/'

no_lip_IV_path = no_lip_iv_path_base + 'no_nozzle_IV_T'
deg_20_IV_path = deg_20_path_base + 'Intake_20deg_7e_IV_T'
deg_45_IV_path = deg_45_path_base + 'Intake_45deg_7e_IV_T'
deg_75_IV_path = deg_75_path_base + 'Intake_75deg_7e_IV_T'


no_lip_XY_path = no_lip_xy_path_base + 'D1_8_D2_4_7e_XY_T'
deg_20_XY_path = deg_20_path_base + 'Intake_20deg_7e_XY_T'
deg_45_XY_path = deg_45_path_base + 'Intake_45deg_7e_XY_T'
deg_75_XY_path = deg_75_path_base + 'Intake_75deg_7e_XY_T'

no_lip_xy_trials = [11,12,13,14,15,16,17]
no_lip_iv_trials = [1,2,3,4,5,6]
no_lip_lbl = 'No Intake Lip' #8.25 uA

deg_20_xy_trials = [1,2,3,4,5,6,7,8,9]
deg_20_iv_trials = [5,6,7]#8
deg_20_lbl = '20$^\circ$'

deg_45_xy_trials = [7,8,9,10,11]
deg_45_iv_trials = [1,2,3,5,6] #3,5,6
deg_45_lbl = '45$^\circ$' # 8.6 uA

deg_75_xy_trials = [1,2,3,4,5,6] # 9.25 uA
deg_75_iv_trials = [1,2,3,4]
deg_75_lbl = '75$^\circ$'

xy_paths = [no_lip_XY_path,deg_20_XY_path,deg_45_XY_path,deg_75_XY_path]
xy_trials = [no_lip_xy_trials,deg_20_xy_trials,deg_45_xy_trials,deg_75_xy_trials]
xy_legend = [no_lip_lbl,deg_20_lbl,deg_45_lbl,deg_75_lbl]

iv_paths = [no_lip_IV_path,deg_20_IV_path,deg_45_IV_path,deg_75_IV_path]
iv_trials = [no_lip_iv_trials,deg_20_iv_trials,deg_45_iv_trials,deg_75_iv_trials]
iv_legend = [deg_20_lbl,deg_45_lbl,deg_75_lbl]


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

f3 = mpl.figure()
f3.set_size_inches(3.25, 2.5)
plt3 = f2.add_subplot()
f3.tight_layout()

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

plt.set_ylim(0.8,1.5)
plt.set_xlim(3,3.55)

# plt2.set_ylim(0,7)
# iv_legend.append('I/I$_0$ = 1')
plt2.legend(iv_legend,loc='lower center',ncol=3,markerscale=0.5,frameon=False,columnspacing=0.5,labelspacing=0.1,handlelength=1)
plt2.set_xlabel('Voltage (kV)',labelpad=1)
plt2.set_ylabel('I/I$_0$',labelpad=1)


plt2.set_ylim(0.8,1.6)
plt2.set_xlim(3,3.55)

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 17:57:59 2022

@author: Wintermute
"""
from plottingFunctions import *
import numpy as np
import time 
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
from ParseFile import ParseFile
from matplotlib import cm

file_type = '.csv'

anemometer_path = 'Anemometer'+file_type
stage_path = 'XY Stage'+file_type
current_path = 'Current Monitor'+file_type
voltage_path = 'Voltage Monitor'+file_type
force_path = 'Force'+file_type
gnd_path = 'Ground'+file_type

    
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



iv_paths = [con_path,div_path,straight_path]
iv_trials = [convergent_iv_trials,divergent_iv_trials,straight_iv_trials]
iv_legend = [convergent_lbl,divergent_lbl,straight_lbl]


#///////////////////////////////////////////////////////////#
mpl.rc('font', family='Arial') 
separate_figs = True 
num_rows = 1
num_cols = 2
plt_cnt = 1
fig_ttl = 'Output Air Velocity'
if not separate_figs:
    fig = mpl.figure()
    

'''
Plot Force data from Balance
'''  

# if separate_figs:
#     fig = mpl.figure()
#     iv_ax = fig.add_subplot()
# else:
#     iv_ax = fig.add_subplot(num_rows,num_cols,plt_cnt)
#     plt_cnt = plt_cnt + 1

# for i in range(len(iv_paths)):
#     path = iv_paths[i]
#     trials = iv_trials[i]
#     PlotBalance(trials,path,iv_ax)

# iv_ax.set_xlabel('Voltage (kV)')
# iv_ax.set_ylabel('Force (mN)')
# if iv_legend is not None:
#     iv_ax.legend(iv_legend)
# iv_ax.set_title('Force Response')  

'''
Plot Force Vs PWM
'''
# legent_lbls = []

# if separate_figs:
#     fig = mpl.figure()
#     f_ax = fig.add_subplot()
# else:
#     f_ax = fig.add_subplot(num_rows,num_cols,plt_cnt)
#     plt_cnt = plt_cnt + 1
    
# for i in range(len(f_paths)):
#     path = f_paths[i]
#     trial = f_trials[i]
#     PlotForceVsPWM(trial,path,f_ax)
# f_ax.set_title('Force vs PWM 2300V')
# f_ax.legend(f_legend)

'''
Plot Force Vs Voltage
'''

# if separate_figs:
#     fig = mpl.figure()
#     fv_ax = fig.add_subplot()
# else:
#     fv_ax = fig.add_subplot(num_rows,num_cols,plt_cnt)
#     plt_cnt = plt_cnt + 1
    
# for i in range(len(f_paths)):
#     path = iv_paths[i]
#     trial = iv_trials[i]
#     PlotForceVsVoltage(trial,path,fv_ax)
# fv_ax.set_title('Force vs Voltage')
#fv_ax.legend(iv_legend)

'''
Plot IV Curve
'''
legend_lbls = []

if separate_figs:
    fig = mpl.figure()
    iv_ax = fig.add_subplot()
else:
    iv_ax = fig.add_subplot(num_rows,num_cols,plt_cnt)
    plt_cnt = plt_cnt + 1

for i in range(len(iv_paths)):
    path = iv_paths[i]
    trials = iv_trials[i]
    PlotCurrent(trials,path,iv_ax)

iv_ax.set_xlabel('Voltage (kV)')
iv_ax.set_ylabel('Current (micro A)')

if iv_legend is not None:
    iv_ax.legend(iv_legend)
iv_ax.set_title('20 deg')
'''
Plot AV Curve
'''

# if separate_figs:
#     fig = mpl.figure()
#     av_ax = fig.add_subplot()
# else:
#     av_ax = fig.add_subplot(num_rows,num_cols,plt_cnt)
#     plt_cnt = plt_cnt + 1

# for i in range(len(iv_paths)):
#     path = iv_paths[i]
#     trials = iv_trials[i]
#     PlotAnemometer(trials,path,av_ax,mode='av',max_v=4)

# av_ax.set_ylabel('Velocity')
# av_ax.set_xlabel('Voltage (kV)')

# av_ax.legend(iv_legend)
# av_ax.set_title('Velocity Response')


'''
Plot 3d Anemometer Data Scatter
'''
# if separate_figs:
#     fig = mpl.figure()
#     xy_ax = fig.add_subplot(projection='3d')
# else:
#     xy_ax = fig.add_subplot(num_rows,num_cols,plt_cnt,projection='3d')
#     plt_cnt = plt_cnt + 1
    
# xy_ax.set_title('Thruster Exhaust Velocity')
# xy_ax.set_xlabel('x (mm)')
# xy_ax.set_ylabel('y (mm)')

# for i in range(len(xy_paths)):
#     path = xy_paths[i]
#     trials = xy_trials[i]
#     z,x,y = PlotAnemometer2d(trials, path,show_plot=False)
#     xy_ax.scatter(x,y,z)

# xy_ax.legend(xy_legend)
'''
Plot 3d Anemometer Data Surface
'''

# for i in range(len(xy_paths)):
#     if separate_figs:
#         fig = mpl.figure()
#         xy_ax = fig.add_subplot(projection='3d')
#         ttl = fig_ttl
#     else:
#         ttl = xy_legend[i]
#         xy_ax = fig.add_subplot(num_rows,num_cols,plt_cnt,projection='3d')
#         plt_cnt = plt_cnt + 1
        
#     xy_ax.set_title(ttl)
#     xy_ax.set_xlabel('x (mm)')
#     xy_ax.set_ylabel('y (mm)')
#     xy_ax.set_zlabel('Velocity (m/s)')
#     xy_ax.set_zlim(0,1)

#     path = xy_paths[i]
#     trials = xy_trials[i]
#     z,x,y = PlotAnemometer2d(trials, path,show_plot=False)
#     x=np.array(x)
#     y=np.array(y)
#     z=np.array(z)
# xy_ax.plot_trisurf(x,y,z,cmap=cm.coolwarm)
# if xy_legend is not None:
#     xy_ax.legend(xy_legend)
'''
Plot 2d Cross Section
'''

# if separate_figs:
#     fig = mpl.figure()
#     xyc_ax = fig.add_subplot()
# else:
#     xyc_ax = fig.add_subplot(num_rows,num_cols,plt_cnt)
#     plt_cnt = plt_cnt + 1

# xyc_ax.set_title('Thruster Exhaust Velocity')
# xyc_ax.set_xlabel('x (mm)')
# xyc_ax.set_ylabel('Velocity (m/s)')

# for i in range(len(xy_paths)):
#     path = xy_paths[i]
#     trials = xy_trials[i]
#     pose,amp = PlotCrossSection(trials,path,xyc_ax,slice_width=0.5,slice_axis='x',outputOn=True)
#     xyc_ax.scatter(pose,amp)
# xyc_ax.legend(xy_legend)

'''
Plot Voltage over Time
'''

# if separate_figs:
#     fig = mpl.figure()
#     v_ax = fig.add_subplot()
# else:
#     v_ax = fig.add_subplot(num_rows,num_cols,plt_cnt)
#     plt_cnt = plt_cnt + 1
    
# for i in range(len(iv_paths)):
#     path = iv_paths[i]
#     trials = iv_trials[i]
#     PlotVoltage(trials,path,v_ax)

# v_ax.set_title('Voltage')
# v_ax.set_ylabel('Voltage (kV)')
# v_ax.set_xlabel('Time (S)')
# v_ax.legend(iv_legend)
# v_ax.grid(True)

'''
Plot Anemometer over Time
'''

# if separate_figs:
#       fig = mpl.figure()
#       a_ax = fig.add_subplot()
# else:
#       a_ax = fig.add_subplot(num_rows,num_cols,plt_cnt)
#       plt_cnt = plt_cnt + 1

# for i in range(len(iv_paths)):
#       path = iv_paths[i]
#       trials = iv_trials[i]
     
#       PlotAnemometer(trials,path,a_ax)
    

# a_ax.set_title('Anemometer')
# a_ax.set_ylabel('Anemometer')
# a_ax.set_xlabel('Time (S)')
# a_ax.legend(iv_legend)
# a_ax.grid(True)

'''
Plot Current over Time
'''

# if separate_figs:
#     fig = mpl.figure()
#     c_ax = fig.add_subplot()
# else:
#     c_ax = fig.add_subplot(num_rows,num_cols,plt_cnt)
#     plt_cnt = plt_cnt + 1
# for i in range(len(iv_paths)):
#     path = iv_paths[i]
#     trials = iv_trials[i]
#     PlotCurrent(trials,path,c_ax,mode='time')

# c_ax.set_ylabel('Current (micro A)')
# c_ax.set_xlabel('Time (S)')
# c_ax.grid(True)
# c_ax.legend(iv_legend)
'''
Subplot management
'''
if not separate_figs:
    fig.align_xlabels()
    fig.align_ylabels()
    mpl.suptitle(fig_ttl)
    mpl.tight_layout()
    
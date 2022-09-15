# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:53:00 2022

@author: Becca
"""


from plottingFunctions import *
import numpy as np
import time 
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
from ParseFile import ParseFile
from matplotlib import cm
from general_plotting_definitions import Data

    
'''
Init folder locations
'''

path_reverse = '../../../../ExperimentData/'
# all at 3.3kV
path_8_7 = path_reverse + 'LatEmitter/XY data/D1_8mmD2_4mm/D1_8_D2_4_7e_XY_T'
path_8_3 = path_reverse + 'LatEmitter/XY data/D1_8mmD2_4mm/D1_8_D2_4_3e_XY_T'
path_6_3 = path_reverse + 'LatEmitter/6mm diam/D1_6_3mm_XY_T'
p = path_reverse + 'LatEmitter/Nozzle Data/Straight/stage_3/straight_XY_T'

# d_87 = Data(path_8_7,[11,12,13,14,15,16,17],'8mm Diameter, 7 Emitters')
# d_83 = Data(path_8_3,[1,2,3,4,5,6,7,8,9,10],'8mm Diameter, 3 Emitters')
# d_63 = Data(path_6_3,[12,13,14,15],'6mm Diameter, 3 Emitters')

test = Data(p,[11,12,13,14],'test')
plot_data = [test]
legend_entries = []

# fig_1 = mpl.figure(dpi=100)
# # fig_1.set_size_inches(6,3,forward=True)
# ax_1 = fig_1.add_subplot(projection='3d')
# ax_1.set_box_aspect((2,1,1))  # aspect ratio is 1:1:1 in data space

font = {'fontname':'Arial'}

fig_2 = mpl.figure(dpi=100)
ax_2 = fig_2.add_subplot()

cnt = 0
color = ['b','#ff7f0e']
formatted_3d_x = []
formatted_3d_y = []
formatted_3d_z = []

for d in plot_data:
    all_x = []
    all_y = []
    all_z = []
    
    fig_1 = mpl.figure(dpi=100)
    ax_1 = fig_1.add_subplot(projection='3d')
    # ax_1.set_title('Output Velocity')
    ax_1.set_xlabel('X (mm)',**font)
    ax_1.set_ylabel('Y (mm)',**font)
    ax_1.set_zlabel('Velocity (m/s)',**font)
    stationary_anem_data = {}
    for t in d.trials:
        xs_3d = []
        ys_3d = []
        zs_3d = []
        xy_data, xy_timestamp = ParseFile(d.getPath(t,'stage'))
        anem_data, anem_timestamp = ParseFile(d.getPath(t,'anem'))
        
        
        #data matching
        stationary_times = xy_timestamp[1:] - xy_timestamp[:-1]
        min_stationary_time = 0.5
        extra_stabilizing_time = 0.1
        important_xy_indices = np.argwhere(stationary_times>min_stationary_time)
        # stationary_anem_data = {}
        
        for index in important_xy_indices:
            xy_strings = xy_data[index][0].split(' ')
            xy = (float(xy_strings[0]),float(xy_strings[1]))
            start_stationary_time = xy_timestamp[index] + extra_stabilizing_time
            end_stationary_time = xy_timestamp[index+1] - extra_stabilizing_time
            anem = anem_data[np.logical_and(anem_timestamp>start_stationary_time,anem_timestamp<end_stationary_time)]
            stationary_anem_data[xy] = anem
            
        #3d plot
        for key in stationary_anem_data.keys():
            xs_3d.append(key[0])
            ys_3d.append(key[1])
            zs_3d.append(np.average(stationary_anem_data[key]))
    
        formatted_3d_x.extend((np.array(xs_3d)/1000) )#+ cnt*15)
        formatted_3d_y.extend(np.array(ys_3d)/1000)
        formatted_3d_z.extend(np.array(zs_3d))    
        all_x.extend(xs_3d)
        all_y.extend(ys_3d)
        all_z.extend(zs_3d)
        # formatted_3d_x = ((np.array(xs_3d)/1000) )#+ cnt*15)
        # formatted_3d_y = (np.array(ys_3d)/1000)
        # formatted_3d_z = (np.array(zs_3d)) 
    
        
        # ax_1.plot_trisurf(all_x,all_y,all_z,cmap=cm.coolwarm)
    shifted_x = np.array(formatted_3d_x) #+ cnt*15
    
    ax_1.plot_trisurf(shifted_x,formatted_3d_y,formatted_3d_z,cmap=cm.coolwarm)
    #     #2d plot
        
    max_vel_idx = np.argmax(all_z)  
    print('max x: ' + str(all_x[max_vel_idx]))
    y_adjust = all_y[max_vel_idx]
    x_slice = all_x[max_vel_idx]
    x_width = 300
    
    ys_cross = []
    zs_cross = []
    stds = []
    
    for key in stationary_anem_data.keys():
        if abs(key[0] - x_slice) < x_width:
            ys_cross.append(key[1])
            zs_cross.append(np.average(stationary_anem_data[key]))
            stds.append(np.std(stationary_anem_data[key]))
    
    legend_entries.append(d.lbl)    
    
    # ax_2 = fig_2.add_subplot()
    y_cross_formatted = (np.array(ys_cross)-y_adjust)/1000
    # ax_2.errorbar(y_cross_formatted,zs_cross,yerr=stds,fmt='o',capsize=5)
    ax_2.scatter(y_cross_formatted,zs_cross,c=color[cnt])
    cnt = cnt + 1
    # ax_2.plot(y_cross_formatted,zs_cross,marker='o')
    

   
ax_2.legend(legend_entries)
ax_2.set_xlabel('X (mm)',**font)
ax_2.set_ylabel('Velocity (m/s)',**font)
# ax_2.set_title('Output Velocity')
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:55:40 2022

@author: Becca
"""

from ParseFile import ParseFile
import numpy as np
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D

xy_file = 'C:/Users/Becca/Documents/ExperimentData/LatEmitter/Intake Lip Data/Without Nozzles/deg_75/Intake_75deg_7e_XY_T3/XY Stage.csv'
anem_file = 'C:/Users/Becca/Documents/ExperimentData/LatEmitter/Intake Lip Data/Without Nozzles/deg_75/Intake_75deg_7e_XY_T3/Anemometer.csv'

xy_data, xy_timestamp = ParseFile(xy_file)
anem_data, anem_timestamp = ParseFile(anem_file)


#data matching
stationary_times = xy_timestamp[1:] - xy_timestamp[:-1]
min_stationary_time = 0.5
extra_stabilizing_time = 0.1
important_xy_indices = np.argwhere(stationary_times>min_stationary_time)
stationary_anem_data = {}

for index in important_xy_indices:
    xy_strings = xy_data[index][0].split(' ')
    xy = (float(xy_strings[0]),float(xy_strings[1]))
    start_stationary_time = xy_timestamp[index] + extra_stabilizing_time
    end_stationary_time = xy_timestamp[index+1] - extra_stabilizing_time
    anem = anem_data[np.logical_and(anem_timestamp>start_stationary_time,anem_timestamp<end_stationary_time)]
    stationary_anem_data[xy] = anem
    


# #3d plot
# xs = []
# ys = []
# zs = []
# for key in stationary_anem_data.keys():
#     xs.append(key[0])
#     ys.append(key[1])
#     zs.append(np.average(stationary_anem_data[key]))
    
    
# fig = mpl.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(xs,ys,zs)


# #2d plot

# x_slice = 3000
# x_width = 15

# ys = []
# zs = []
# stds = []
# for key in stationary_anem_data.keys():
#     if abs(key[0] - x_slice) < x_width:
#         ys.append(key[1])
#         zs.append(np.average(stationary_anem_data[key]))
#         stds.append(np.std(stationary_anem_data[key]))

# fig = mpl.figure()
# ax = fig.add_subplot()
# ax.errorbar(ys,zs,yerr=stds,fmt='o',capsize=5)
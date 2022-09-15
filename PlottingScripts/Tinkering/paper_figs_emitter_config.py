# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 16:43:09 2022

@author: Drew Lab Computer
"""


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

iv_path = 'C:/Users/drewl/Documents/RebeccaData/ExperimentData/LatEmitter/'

p1 = 'mm diam/diam_'
p2 = 'mm_inside_IV_T'

fp_4_2 = iv_path+'4'+p1+'4_2'+p2
fp_4_3 = iv_path+'4'+p1+'4_3'+p2

fp_6_2 = iv_path+'6'+p1+'6_2'+p2
fp_6_3 = iv_path+'6'+p1+'6_3'+p2
fp_6_4 = iv_path+'6'+p1+'6_4'+p2

fp_8_2 = iv_path+'8'+p1+'8_2'+p2
fp_8_3 = iv_path+'8'+p1+'8_3'+p2
fp_8_4 = iv_path+'8'+p1+'8_4'+p2

iv_paths = [fp_4_2,fp_4_3,fp_6_2,fp_6_3,fp_6_4,fp_8_2,fp_8_3,fp_8_4] 
iv_trials = [[2],[3],[1],[1],[1],[2],[1],[3]]
iv_legend = ['(4,2)','(4,3)','(6,2)','(6,3)','(6,4)','(8,2)','(8,3)','(8,4)']


#///////////////////////////////////////////////////////////#
mpl.rc('font', family='Arial') 
# mpl.gcf().subplots_adjust(bottom=0.15,left=0.15)

'''
Plot IV Curve
'''
legend_lbls = []
fig = mpl.figure()
fig.set_size_inches(3.25, 2.5)
iv_ax = fig.add_subplot()
mpl.tight_layout()
for i in range(len(iv_paths)):
    path = iv_paths[i]
    trials = iv_trials[i]
    PlotCurrent(trials,path,iv_ax,mkr_sz=0.5)

iv_ax.set_xlabel('Voltage (kV)')
iv_ax.set_ylabel('Current (micro A)')
iv_ax.set_xlim(1.5,3.7)

if iv_legend is not None:
    iv_ax.legend(iv_legend,ncol=1,markerscale=0.5,frameon=False,title='(D1,D2)[mm]',borderpad=0,columnspacing=0.5,labelspacing=0.1,handlelength=1)
# mpl.savefig('EmitterConfig',bbox_inches='tight')
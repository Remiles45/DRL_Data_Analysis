# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:16:31 2022

@author: Becca
"""


from plottingFunctions import *
import numpy as np
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
from ParseFile import ParseFile
from matplotlib import cm
from general_plotting_definitions import Data

mpl.rc('font',family='Arial')

path_reverse = '../../../../ExperimentData/LatEmitter/'

d4_e3_2_path = path_reverse + '4mm diam/diam_4_2mm_inside_IV_T'
d4_e3_3_path = path_reverse + '4mm diam/diam_4_3mm_inside_IV_T'
d6_e3_2_path = path_reverse + '6mm diam/diam_6_2mm_inside_IV_T'
d6_e3_3_path = path_reverse + '6mm diam/diam_6_3mm_inside_IV_T'
d6_e3_4_path = path_reverse + '6mm diam/diam_6_4mm_inside_IV_T'
d8_e3_2_path = path_reverse + '8mm diam/diam_8_2mm_inside_IV_T'
d8_e3_3_path = path_reverse + '8mm diam/diam_8_3mm_inside_IV_T'
d8_e3_4_path = path_reverse + '8mm diam/diam_8_4mm_inside_IV_T'

d8_e5_4_path = path_reverse + 'XY data/D1_8mmD2_4mm/D1_8_D2_4_5e_IV_T'
d8_e7_4_path = path_reverse + 'XY data/D1_8mmD2_4mm/D1_8_D2_4_7e_IV_T'

d4_e3_2 = Data(d4_e3_2_path,[1,2],'4mm od, 2mm id')
d4_e3_3 = Data(d4_e3_2_path,[1,2,3],'4mm od, 3mm id')
d6_e3_2 = Data(d6_e3_2_path,[1,2,3],'6mm od, 2mm id')
d6_e3_3 = Data(d6_e3_3_path,[1,3],'6mm od, 3mm id')
d6_e3_4 = Data(d6_e3_4_path,[1,2,3],'6mm od, 4mm id')
d8_e3_2 = Data(d8_e3_2_path,[2],'8mm od, 2mm id') 
d8_e3_3 = Data(d8_e3_3_path,[1,2,3,4],'8mm od, 3mm id')

d8_e3_4 = Data(d8_e3_4_path,[2,3,4],'8mm od, 4mm id')

d8_e5_4 = Data(d8_e5_4_path,[4,5,6],'5 Emitters')
d8_e7_4 = Data(d8_e7_4_path,[1],'7 Emitters')



plot_data = [d4_e3_2,d4_e3_3,d6_e3_2,d6_e3_3,d6_e3_4,d8_e3_2,d8_e3_3,d8_e3_4]

legend_lbls = []

fig = mpl.figure(dpi=100)
iv_ax = fig.add_subplot()


for d in plot_data:
    legend_lbls.append(d.lbl)
    # t = d.trials
    # p = d.path
    PlotCurrent(d.trials[0],d.path,iv_ax)

iv_ax.set_xlabel('Voltage (kV)')
iv_ax.set_ylabel('Current (micro A)')
iv_ax.legend(legend_lbls)
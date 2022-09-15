# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:18:02 2022

@author: Wintermute
"""

from plottingFunctions import *
import numpy as np
import time 
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
from ParseFile import ParseFile
from math import tan 
'''
Init folder locations
'''

file_type = '.csv'

anemometer_path = 'Anemometer'+file_type
stage_path = 'XY Stage'+file_type
current_path = 'Current Monitor'+file_type
voltage_path = 'Voltage Monitor'+file_type
gnd_path = 'Ground'+file_type

   

def PlotCoronaOnset(path,diameters,trials,probe_height,max_v=None,plotOn=True):
    '''
    finds the corona onset voltage using a threshold of 10 micro A above the noise 
    floor and returns values to plot. 
    Codes to add extra tests:
        999: air reset
        1000: supply reset
        1001: supply reset long
    '''
    if plotOn:
        mpl.figure()
    x = []
    y = []
    leg = []
    for d in diameters:
        for t in trials:
            if t == 999:
                pre_path = path + str(d) + 'mm_AirResetTest/'
            elif t == 1000:
                pre_path = path + str(d) + 'mm_SupplyResetTest/'
            elif t == 1001:
                pre_path = path + str(d) + 'mm_SupplyResetTestLong/'
            else:
                pre_path = path + str(d) + 'mm_T' + str(t) + '/'
    
            raw_voltage,voltage_timestamps = GetVoltage(pre_path)
            raw_current,current_timestamps = ParseFile(pre_path+current_path)
            scaled_current = ((raw_current * 750)/10)
            voltage,current = AverageIV(raw_voltage, scaled_current)
            current = np.array(current)
            voltage = np.array(voltage)
            onsetV = FindCoronaOnsetV(voltage,current)
            
            cone = d / (2*tan(1.0472)*probe_height) # diam / (2*tan(60)*d)
            x.append(cone)
            y.append(onsetV)
            
            print('Diameter: '+str(d)+' Trial '+str(t)+' Vonset: '+str(onsetV))
    
            if plotOn:
                leg.append(str(d)+'mm trial '+str(t))
                if max_v != None:
                    valid_pts = voltage <= max_v
                    voltage = voltage[valid_pts]
                    current = current[valid_pts]
                mpl.scatter(voltage,current)
                # mpl.axvline(x=onsetV)
                print('Diameter: '+str(d)+' Vonset: '+str(onsetV))
    if plotOn:
        mpl.title('Collector Shape Effect on IV Curves')
        mpl.xlabel('Voltage (kV)')
        mpl.ylabel('Current (micro A)')
        mpl.legend(leg)
    return x,y


folder1 = '../../Experiment Runs/Experiment_Runs_4_7_22/IVcurves/'
folder2 = '../../Experiment Runs/Experiment_Runs_4_8_22/IVcurves/'
folder3 = '../../Experiment Runs/Ducting Experiments/VenturiDucts/Experiment_Runs_4_11_22/IVcurves/'

num_trials = 4
diameters = [3]#[4,5,6,7,8]
probe_height = 2.03 #mm
max_v = 3
leg=[]
p = folder3 + 'D1_0_D2_0_'

mpl.figure()    

for i in range(1,num_trials+1):
    leg.append('Trial '+str(i))
    x,y = PlotCoronaOnset(p,diameters,[i],probe_height,max_v=max_v,plotOn=False)
    mpl.scatter(x,y)


# leg.append('Air Reset')
# x,y = PlotCoronaOnset(p,[3],[999],probe_height,max_v=max_v,plotOn=False)
# mpl.scatter(x,y)

# leg.append('Supply Reset (1 min)')
# x,y = PlotCoronaOnset(p,[3],[1000],probe_height,max_v=max_v,plotOn=False)
# mpl.scatter(x,y)

# leg.append('Supply Reset (5 min)')
# x,y = PlotCoronaOnset(p,[3],[1001],probe_height,max_v=max_v,plotOn=False)
# mpl.scatter(x,y)


mpl.xlabel('Diameter/(2tan(60)d)')
mpl.ylabel('Corona Onset Voltage (kV)')
mpl.title('Collector Shape Effect on Corona Onset')
mpl.legend(leg)
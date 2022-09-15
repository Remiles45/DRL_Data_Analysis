# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 21:28:06 2022

@author: Wintermute
"""

from ParseFile import ParseFile
import matplotlib.pyplot as mpl
import numpy as np

def Filter(data,window_size=500,mode='average'):
    filtered_data = []
    for i in range(len(data)):
        if i < len(data)-window_size:
            window = data[i:i+window_size]
        else:
            window = active_current[i:-1]
        if mode == 'median':
            filtered_val = np.median(window)
        elif mode == 'average':
            filtered_val = np.average(window)
        filtered_data.append(filtered_val)
    return filtered_data

folder = '../../Experiment Runs/Experiment_Runs_1_27_22/'
file_type = '.csv'
trial  = 'no_duct_IV_T5/' 

anemometer_path = 'Anemometer'+file_type
stage_path = 'XY Stage'+file_type
current_path = 'Current Monitor'+file_type
voltage_path = 'Voltage Monitor'+file_type
supply_path = 'Power Supply'+file_type

pre_path = folder+trial

print("Parsing Power Supply")
power_supply_data, power_supply_timestamps = ParseFile(pre_path+supply_path)
experiment_start_time = power_supply_timestamps[0]

print("Parsing Voltage Monitor")
raw_voltage,voltage_timestamps = ParseFile(pre_path+voltage_path)
voltage = (8 * raw_voltage) / 10  # kV
active_timestamp_idx = voltage_timestamps >= experiment_start_time
# active_voltage_ts = voltage_timestamps[active_timestamp_idx]
active_voltage = voltage[active_timestamp_idx]

print("Parsing Current Monitor")
raw_current,current_timestamps = ParseFile(pre_path+current_path)
current = ((0.0075 * raw_current) / 10) * 1e3 # mA
active_current = current[active_timestamp_idx]


# median_filtered_current = Filter(active_current,window_size = 1000,mode = 'median')
filtered_current = Filter(active_current,window_size = 100,mode = 'average')



# mpl.scatter(current_timestamps[active_timestamp_idx],filtered_current)#active_current)
mpl.scatter(active_voltage,filtered_current)
mpl.title('IV')
mpl.xlabel('Voltage (kV)')
mpl.ylabel('Current (mA)')


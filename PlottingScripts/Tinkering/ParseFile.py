# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 19:41:53 2022

@author: Wintermute
"""

import pandas as pd

def ParseFile(file_path):
    '''
    Input: full file path
    Output: 
        data (list) - data from file
        timestamps (list) - timestamps converted into seconds
    '''
    
#    start_time = time.time()
    
    file = open(file_path,'r')
    lines = file.readlines()
    #first 3 lines are extra info
    #line 0 : label (dont need)
    #line 1 : unit
    unit = lines[1].strip()
    #line 2 : extra info
    extra_info_full = lines[2].strip()
    extra_info = None
    extra_info_unit = None
    if extra_info_full != '' :
        ei_parsed = extra_info_full.split(' ')
        extra_info = float(ei_parsed[0])
        extra_info_unit = ei_parsed[1]

    # use pandas to read in large datafile
    df = pd.read_csv(file_path,skiprows=3,header=None)   
    df.columns = ['data','timestamps']
    data = df['data']
    timestamps = df['timestamps']
    
    file.close()
    
    return data.values,timestamps.values



def ParseSingle(file_path):    
    file = open(file_path,'r')
    lines = file.readlines()
    #first 3 lines are extra info
    #line 0 : label (dont need)
    #line 1 : unit
    unit = lines[1].strip()
    #line 2 : extra info
    extra_info_full = lines[2].strip()
    extra_info = None
    extra_info_unit = None
    if extra_info_full != '' :
        ei_parsed = extra_info_full.split(' ')
        extra_info = float(ei_parsed[0])
        extra_info_unit = ei_parsed[1]

    # use pandas to read in large datafile
    df = pd.read_csv(file_path,skiprows=3,header=None)   
    df.columns = ['data']
    data = df['data']
    
    file.close()
    
    return data.values
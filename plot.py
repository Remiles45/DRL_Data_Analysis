# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 17:03:53 2022

@author: Becca
"""

import matplotlib.pyplot as mpl
import pandas as pd
import numpy as np

base_pathiv = '../ExperimentalData/Junk/testiv/'
base_pathxy = '../ExperimentalData/Junk/testxy/'

iv_path  = base_pathiv + 'IV.csv'
fv_path  = base_pathiv + 'FV.csv'
bv_path  = base_pathiv + 'BV.csv'
av_path  = base_pathiv + 'AV.csv'
xya_path = base_pathxy + 'XYA.csv'
it_path  = base_pathiv + 'IT.csv'
vt_path  = base_pathiv + 'VT.csv'
at_path  = base_pathxy + 'AT.csv'
ft_path  = base_pathiv + 'FT.csv'




def plotXYA(path):
    df = pd.read_csv(path,skiprows=1,header=None)
    df.columns=['x','y','anem','std_dev']
    
    x = np.array(df['x'].values)
    y = np.array(df['y'].values)
    a = np.array(df['anem'].values)
    sdev=np.array(df['std_dev'].values)
    
    fig = mpl.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(x,y,a)
    
def plot2D(path,ttl=''):
    df = pd.read_csv(path,skiprows=1,header=None)
    if df.shape[1] == 2:
        df.columns=['y','x']
        x = np.array(df['x'].values)
        y = np.array(df['y'].values)
        
        fig = mpl.figure()
        ax = fig.add_subplot()
        ax.scatter(x,y)
    else:
        df.columns=['y','x','std']
        x = np.array(df['x'].values)
        y = np.array(df['y'].values)
        std = np.array(df['std'].values)
        
        fig = mpl.figure()
        ax = fig.add_subplot()
        ax.errorbar(x,y,std)
    
    ax.set_title(ttl)
    
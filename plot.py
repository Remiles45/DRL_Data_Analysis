# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 17:03:53 2022

@author: Becca
"""

import matplotlib.pyplot as mpl
import pandas as pd
import numpy as np

path = '../junk/test (6)/XYA.csv'

df = pd.read_csv(path,skiprows=1,header=None)
df.columns=['x','y','anem','std_dev']

x = np.array(df['x'].values)
y = np.array(df['y'].values)
a = np.array(df['anem'].values)
sdev=np.array(df['std_dev'].values)

fig = mpl.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(x,y,a)
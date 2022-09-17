# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 16:58:14 2022

@author: Becca
"""
import numpy as np

class Data:
    def __init__(self,filepath,lbl,process_method=None,data=np.array([]),timestamps=np.array([])):
        self.filepath = filepath
        self.lbl = lbl
        self.process_method = process_method
        self.data = data
        self.timestamps = timestamps
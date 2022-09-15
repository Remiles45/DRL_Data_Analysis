# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:35:32 2022

@author: Becca
"""

file_type = '.csv'

anemometer_path = 'Anemometer'+file_type
stage_path = 'XY Stage'+file_type
current_path = 'Current Monitor'+file_type
voltage_path = 'Voltage Monitor'+file_type
force_path = 'Force'+file_type
gnd_path = 'Ground'+file_type



class Data:
    def __init__(self,path='',trials=[],lbl=''):
        self.path = path
        self.trials = trials
        self.lbl = lbl
    def setPath(self,p):
        self.path = p
        self.updatePaths()
    def setTrials(self,t):
        self.trials = t
        self.updatePaths()
    def setLbl(self,b):
        self.lbl = b
    def getPath(self,trial,key):
        pathlookup = {
            'anem' : anemometer_path,
            'curr' : current_path,
            'stage': stage_path,
            'volt' : voltage_path,
            'force': force_path
            }
        return self.path + str(trial) + '/' + pathlookup[key]
            
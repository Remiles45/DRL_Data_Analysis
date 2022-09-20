# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 14:42:24 2022

@author: Becca
"""
import csv
from ProcessDataFunctions import DataProcessor


class CSVGenerator:
    def __init__(self,base_paths,destination_path,options,dec_factor):
        self.base_paths = base_paths
        self.destination_path = destination_path
        self.options = options
        self.dec_factor = dec_factor
        
        self.desired_files = self.options.GetChecked()
        
    def run(self):
        self.ProcessedTrials = []
        for path in self.base_paths:
            processor = DataProcessor(path,dec_factor=self.dec_factor)
            self.ProcessedTrials.append(processor)
        
        self.generate_options = {
            'IV'  : self.IV,
            'FV'  : self.FV,
            'BV'  : self.BV,
            'AV'  : self.AV,
            'XYA' : self.XYA,
            'IT'  : self.IT,
            'VT'  : self.VT,
            'AT'  : self.AT,
            'FT'  : self.FT
            }
        
        for key in self.desired_files:
            generate = self.generate_options[key]
            generate()
    
    def IV(self):
        pass
    def FV(self):
        pass
    def BV(self):
        pass
    def AV(self):
        pass
    def XYA(self):
        header=['x[mm]','y[mm]','anemometer avg[m/s]','anemometer std']
        out_path = self.destination_path + '/XYA.csv'
        
        with open(out_path,mode='w',newline='') as f:
            writer = csv.writer(f,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for trial in self.ProcessedTrials:
                trial.XYA(writer)
            
            
            
    def IT(self):
        pass
    def VT(self):
        pass
    def AT(self):
        pass
    def FT(self):
        pass 
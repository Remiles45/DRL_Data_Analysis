# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 14:42:24 2022

@author: Becca
"""
import csv
from ProcessDataFunctions import DataProcessor
import numpy as np


class CSVGenerator:
    def __init__(self,base_paths,destination_path,options,dec_factor):
        self.base_paths = base_paths
        self.destination_path = destination_path
        self.options = options
        self.dec_factor = dec_factor
        
        if self.options != None:
            self.desired_files = self.options.GetChecked()
        else:
            self.desired_files = []
        
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
    
    def GroupData(self,full_x,full_y,thresh=50):  
        out_x = np.array([])
        out_y = np.array([])
        y_std = np.array([])
        
        unique_xs,unique_cts = np.unique(full_x,return_counts=True)
        for index,x in enumerate(unique_xs):
            if unique_cts[index] >= thresh:
                idxs_at_pt = full_x == x
                out_x = np.append(out_x,x)
                out_y = np.append(out_y,np.average(full_y[idxs_at_pt]))
                y_std = np.append(y_std,np.std(full_y[idxs_at_pt]))
        
        return out_x,out_y,y_std
                
    
    def IV(self):
        print('Creating IV file...')
        header=['Current[uA]','Voltage[kV]','Std']
        out_path = self.destination_path + '/IV.csv'
                
        combined_curr = np.concatenate([trial.IV()[0] for trial in self.ProcessedTrials])    
        combined_v = np.concatenate([trial.IV()[1] for trial in self.ProcessedTrials])    
        v,curr,dev = self.GroupData(combined_v, combined_curr)
        
        with open(out_path,mode='w',newline='') as file:
            writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for i,this_v in enumerate(v):
                row = [str(curr[i]), str(this_v), str(dev[i])]
                writer.writerow(row)
        # print('Finished IV File')
        
    def FV(self):
        print('Creating FV file...')
        header=['Force[mN]','Voltage[kV]','Std']
        out_path = self.destination_path + '/FV.csv'
                
        combined_f = np.concatenate([trial.FV()[0] for trial in self.ProcessedTrials])    
        combined_v = np.concatenate([trial.FV()[1] for trial in self.ProcessedTrials])    
        v,f,dev = self.GroupData(combined_v, combined_f)
        
        with open(out_path,mode='w',newline='') as file:
            writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for i,this_v in enumerate(v):
                row = [str(f[i]), str(this_v), str(dev[i])]
                writer.writerow(row)
        # print('Finished FV File')
        
    def BV(self):
        print('Creating BV file...')
        header=['Force[mN]','Voltage[kV]','Std']
        out_path = self.destination_path + '/BV.csv'
                
        combined_f = np.concatenate([trial.BV()[0] for trial in self.ProcessedTrials])    
        combined_v = np.concatenate([trial.BV()[1] for trial in self.ProcessedTrials])    
        v,f,dev = self.GroupData(combined_v, combined_f,thresh=1)
        
        with open(out_path,mode='w',newline='') as file:
            writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for i,this_v in enumerate(v):
                row = [str(f[i]), str(this_v), str(dev[i])]
                writer.writerow(row)
        # print('Finished BV File')
        
    def AV(self):
        print('Creating AV file...')
        header=['Velocity[m/s]','Voltage[kV]','Std']
        out_path = self.destination_path + '/AV.csv'
                
        combined_a = np.concatenate([trial.AV()[0] for trial in self.ProcessedTrials])    
        combined_v = np.concatenate([trial.AV()[1] for trial in self.ProcessedTrials])    
        v,a,dev = self.GroupData(combined_v, combined_a)
        
        with open(out_path,mode='w',newline='') as file:
            writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for i,this_v in enumerate(v):
                row = [str(a[i]), str(this_v), str(dev[i])]
                writer.writerow(row)
        # print('Finished AV File')
        
    def XYA(self):
        print('Creating XYA file...')
        header=['x[mm]','y[mm]','anemometer avg[m/s]','anemometer std']
        out_path = self.destination_path + '/XYA.csv'
        
        with open(out_path,mode='w',newline='') as file:
            writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for trial in self.ProcessedTrials:
                trial.XYA(writer)
            
    def IT(self):
        print('Creating IT file...')
        header=['Current[uA]','Time[s]']
        out_path = self.destination_path + '/IT.csv'
                
        combined_curr = np.concatenate([trial.IT()[0] for trial in self.ProcessedTrials])    
        combined_time = np.concatenate([trial.IT()[1] for trial in self.ProcessedTrials])    
        t,curr,dev = self.GroupData(combined_time, combined_curr,thresh=1)
        
        with open(out_path,mode='w',newline='') as file:
            writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for i,this_t in enumerate(t):
                row = [str(curr[i]), str(this_t)]
                writer.writerow(row)
        # print('Finished IT File')
        
    def VT(self):
        print('Creating VT file...')
        header=['Voltage[kV]','Time[s]']
        out_path = self.destination_path + '/VT.csv'
                
        combined_v = np.concatenate([trial.VT()[0] for trial in self.ProcessedTrials])    
        combined_time = np.concatenate([trial.VT()[1] for trial in self.ProcessedTrials])    
        t,v,dev = self.GroupData(combined_time, combined_v,thresh=1)
        
        with open(out_path,mode='w',newline='') as file:
            writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for i,this_t in enumerate(t):
                row = [str(v[i]), str(this_t)]
                writer.writerow(row)
        # print('Finished VT File')
        
    def AT(self):
        print('Creating AT file...')
        header=['Velocity[m/s]','Time[s]']
        out_path = self.destination_path + '/AT.csv'
                
        combined_a = np.concatenate([trial.AT()[0] for trial in self.ProcessedTrials])    
        combined_time = np.concatenate([trial.AT()[1] for trial in self.ProcessedTrials])    
        t,a,dev = self.GroupData(combined_time, combined_a,thresh=1)
        with open(out_path,mode='w',newline='') as file:
            writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for i,this_t in enumerate(t):
                row = [str(a[i]), str(this_t)]
                writer.writerow(row)
        # print('Finished AT File')
        
    def FT(self):
        print('Creating FT file...')
        header=['Force[mN]','Time[s]']
        out_path = self.destination_path + '/FT.csv'
                
        combined_f = np.concatenate([trial.FT()[0] for trial in self.ProcessedTrials])    
        combined_time = np.concatenate([trial.FT()[1] for trial in self.ProcessedTrials])  
        t,f,dev = self.GroupData(combined_time, combined_f,thresh=1)
        with open(out_path,mode='w',newline='') as file:
            writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            for i,this_t in enumerate(t):
                row = [str(f[i]), str(this_t)]
                writer.writerow(row)
        # print('Finished FT File')
        
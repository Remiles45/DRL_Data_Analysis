# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:02:57 2022

@author: Becca
"""
import numpy as np
import pandas as pd
from os.path import exists
from Data import Data,CSVData
from scipy import ndimage
import csv


class DataProcessor:
    def __init__(self,base_path,dec_factor=1):
        self.base_path = base_path
        self.dec_factor = dec_factor # reduce size of large files
        
        self.voltage    = Data(self.base_path + '/Voltage Monitor.csv','Voltage',self.ProcessVoltage)
        self.current    = Data(self.base_path + '/Current Monitor.csv','Current',self.ProcessCurrent)
        self.anemometer = Data(self.base_path + '/Anemometer.csv','Anemometer',self.ProcessAnemometer)
        self.force      = Data(self.base_path + '/Force.csv','Force',self.ProcessForce)
        self.supply     = Data(self.base_path + '/Power Supply.csv','Power Supply',self.ProcessPowerSupply)
        self.stage      = Data(self.base_path + '/XY Stage.csv','XY Stage',self.ProcessXYStage)
        self.balance    = Data(self.base_path + '/Balance.csv','Balance',self.ProcessBalance)
        self.balance_v  = Data(self.base_path + '/Balance Voltages.csv','Balance Voltage',self.ProcessBalanceVoltage)
        
        self.experiment_begin_time = None
        self.ProcessPowerSupply()
        self.experiment_begin_time = self.supply.timestamps[0]        
        
    def ProcessCurrent(self):
        #check if the current has already been parsed
        if len(self.current.data) == 0:
            raw_current , self.current.timestamps = self.ParseFile(self.current.filepath,reduce=True)
            # current off of the shunt resistor (91.3 kOhm R) (I = V/R)[A] therefore microA = *1e6
            self.current.data = (raw_current/91.3e3)*1e6
    
    def ProcessVoltage(self):
        #check if the voltage has already been parsed
        if len(self.voltage.data) == 0:
            raw_voltage , self.voltage.timestamps = self.ParseFile(self.voltage.filepath,reduce=True)
            #filter the raw voltage (tends to have random impulse noise)
            filt_voltage = ndimage.median_filter(raw_voltage,size=5)
            # convert voltage to kV where vkv = (vsupplyout*kvmax)/vsupplymax
            self.voltage.data = (filt_voltage*8)/10
    
    def ProcessAnemometer(self,velocity_range=7.5):
        '''
        Anemometer conversion:
            V = ((Eout - E0)/(Efs - E0)) * Vfs
            V = measured velocity (m/s)
            Vfs = full scale velocity setting in ft/min or m/s
            Eout = measured output voltage or current signal
            E0 = zero flow output voltage or current
            Efs = full scale voltage or current output
        '''
        #check if the anemometer has already been parsed
        if len(self.anemometer.data) == 0:
            raw_anemometer , self.anemometer.timestamps = self.ParseFile(self.anemometer.filepath,reduce=True)
            e0 = 0 #0 velocity signal
            if velocity_range == 7.5:
                scalar = 1.5
            else:
                scalar = 2.8
            # convert voltage to kV where vkv = (vsupplyout*kvmax)/vsupplymax
            self.anemometer.data = (((raw_anemometer-e0)*scalar)/(10-e0))*velocity_range
            
    def ProcessForce(self):
        #check if the force has already been parsed
        if len(self.force.data) == 0:
            self.force.data , self.force.timestamps = self.ParseFile(self.force.filepath)
        
    def ProcessPowerSupply(self):
        #check if the power supply has already been parsed
        if len(self.supply.data) == 0:
            self.supply.data , self.supply.timestamps = self.ParseFile(self.supply.filepath)
    
    def ProcessXYStage(self):
        if len(self.stage.data) == 0:
            xydata = []
            xy_raw , self.stage.timestamps = self.ParseFile(self.stage.filepath)
            for coord in xy_raw:
                parsed = coord.split(' ')
                xycoord = (float(parsed[0])/1000,float(parsed[1])/1000)#convert um to mm
                xydata.append(xycoord)
            self.stage.data = np.array(xydata)
    
    def ProcessBalance(self):
        #check if the balance has already been parsed
        if len(self.balance.data) == 0:
            raw_balance = self.ParseFile(self.balance.filepath)
            baseline = raw_balance[0]
            self.balance.data = (raw_balance-baseline) * 9.81 * 1e-3 #mg to kg = 1e-6, N to mN = 1e3 end result is 1e-3
    
    def ProcessBalanceVoltage(self):
        #check if the balance voltage has already been parsed
        if len(self.balance_v.data) == 0:
            self.balance_v.data = self.ParseFile(self.balance_v.filepath)
    
    def DecimateData(self,in_data,in_ts):
        '''
        Current implementation of this assumes that data will only ever be decimated if it 
        has both a data and timestamp array. 
        syntax: [start:end:step]
        '''
        out_data = in_data[:-1*self.dec_factor:self.dec_factor]
        out_ts   = in_ts[:-1*self.dec_factor:self.dec_factor]
        return out_data,out_ts
    
    def ParseFile(self,file_path,reduce=False):
        '''
        Input: full file path
        Output: 
            data (np array) - data from file
            timestamps (np array) - timestamps converted into seconds
        '''
        out_data = None
        out_ts   = None
        
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
        df_shape = df.shape
        # some files may be a single list of data while others may be data with timestamps, parse accordingly.
        if df_shape[1] == 1:
            df.columns = ['data']
            data = df['data']
            file.close()
            return np.array(data.values)
        elif df_shape[1] == 2:
            df.columns = ['data','timestamps']
            data = df['data']
            timestamps = df['timestamps']
            file.close()
            if self.experiment_begin_time == None:
                ts = np.array(timestamps.values)
            else:
                ts   = np.array(timestamps.values) - self.experiment_begin_time
            out_data = np.array(data.values)
            #convert timestamp time to be wrt beginning of experiment
            out_ts = ts - ts[0] 
            #decimate the data if necessary
            if reduce and (self.dec_factor>1):
                out_data,out_ts = self.DecimateData(out_data,out_ts)
            return out_data,out_ts
        else:
            raise ValueError('Unrecognized File Format')
            
    def IV(self):
        if exists(self.current.filepath) and exists(self.voltage.filepath):
            #ensure the required data exists
            self.ProcessVoltage()
            self.ProcessCurrent()
            
            #Both data are coming from the oscilloscope, therefore there should be the same number of datapoints
            #and all of those datapoints should have aligning timestamps.
            return self.current.data,self.voltage.data
        else:
            print('Could not generate IV plot for '+self.base_path+ ' due to missing files')
            return [],[]
        
    def FV(self):
        if exists(self.force.filepath) and exists(self.voltage.filepath):
            #ensure the required data exists
            self.ProcessVoltage() 
            self.ProcessForce()
            # must align timestamps from force sensor to timestamps in the voltage data
            # voltage data should be significantly more dense than force data
            thresh = 0.01
            v_ts = np.copy(self.voltage.timestamps)
            v    = np.copy(self.voltage.data)
            vout = np.array([])
            fout = np.array([])
            for i,ts in enumerate(self.force.timestamps):
                #get the voltage points at this time
                valid_voltages_idx = np.logical_and((v_ts>=ts-thresh),(v_ts<=ts+thresh))
                if np.max(valid_voltages_idx):
                    #average the voltage
                    vout = np.append(vout,np.average(v[valid_voltages_idx]))
                    fout = np.append(fout,self.force.data[i])
            return fout,vout
        else:
            print('Could not generate FV plot for '+self.base_path+ ' due to missing files')
            return [],[]
        
    def BV(self):
        if exists(self.balance.filepath) and exists(self.balance_v.filepath):
            #ensure the required data exists
            self.ProcessBalanceVoltage()    
            self.ProcessBalance()
            
            #Both data are designed to match up, these files do not actually have timestamps to align anyways
            return self.balance.data,self.balance_v.data
        else:
            print('Could not generate BV plot for '+self.base_path+ ' due to missing files')
            return [],[]
        
    def AV(self):
        if exists(self.anemometer.filepath) and exists(self.voltage.filepath):
            #ensure the required data exists
            self.ProcessVoltage()     
            self.ProcessAnemometer()
            
            #Both data are coming from the oscilloscope, therefore there should be the same number of datapoints
            #and all of those datapoints should have aligning timestamps.
            return self.anemometer.data,self.voltage.data
        else:
            print('Could not generate AV plot for '+self.base_path+ ' due to missing files')
            return [],[]
        
    def XYA(self,writer=None):
        if exists(self.stage.filepath) and exists(self.anemometer.filepath):
            #ensure the required data exists
            self.ProcessAnemometer()
            self.ProcessXYStage()
            
            out_x = np.array([])
            out_y = np.array([])
            out_anem_avg = np.array([])
            out_anem_std = np.array([])
            
            #match up timestamps between the xy stage and anemometer
            stationary_times = self.stage.timestamps[1:] - self.stage.timestamps[:-1]
            min_stationary_time = 0.5 #amount of time that we know the stage will sit there to collect data before moving
            extra_stabilizing_time = 0.1 #time to allow stabalization after movement
            important_xy_indices = np.argwhere(stationary_times>min_stationary_time)
            stationary_anem_data = []
    
            for index in important_xy_indices:
                xy = self.stage.data[index]
                #create buffer for stabalizing time
                start_stationary_time = self.stage.timestamps[index] + extra_stabilizing_time
                end_stationary_time = self.stage.timestamps[index+1] - extra_stabilizing_time 
                #gather anemometer data during the relevant timeframe
                anem = self.anemometer.data[np.logical_and(self.anemometer.timestamps>start_stationary_time,self.anemometer.timestamps<end_stationary_time)]
                
                anem_avg = np.average(anem)
                anem_std = np.std(anem)
                x = xy[0][0]
                y = xy[0][1]
                if writer == None:
                    out_x = np.append(out_x,x)
                    out_y = np.append(out_y,y)
                    out_anem_avg = np.append(out_anem_avg,anem_avg)
                    out_anem_std = np.append(out_anem_std,anem_std)
                else:
                    writer.writerow([x,y,anem_avg,anem_std])
                
                if writer == None:
                    return out_x,out_y,out_anem_avg,out_anem_std
        else:
            print('Could not generate XYA plot for '+self.base_path+ ' due to missing files')
            if writer == None:
                return [],[],[],[]
            
    def IT(self):
        if exists(self.current.filepath):
            #ensure that the required data exists
            self.ProcessCurrent()
            return self.current.data,self.current.timestamps  
        else:
            print('Could not generate IT plot for '+self.base_path+ ' due to missing files')  
            return [],[]
            
    def VT(self):
        if exists(self.voltage.filepath):
            #ensure that the required data exists
            self.ProcessVoltage()
            return self.voltage.data,self.voltage.timestamps 
        else:
            print('Could not generate VT plot for '+self.base_path+ ' due to missing files')  
            return [],[]
        
    def AT(self):
        if exists(self.anemometer.filepath):
            #ensure that the required data exists
            self.ProcessAnemometer()
            return self.anemometer.data,self.anemometer.timestamps    
        else:
            print('Could not generate AT plot for '+self.base_path+ ' due to missing files')
            return [],[]
        
    def FT(self):
        if exists(self.force.filepath):
            #ensure that the required data exists
            self.ProcessForce()
            return self.force.data,self.force.timestamps   
        else:
            print('Could not generate FT plot for '+self.base_path+ ' due to missing files') 
            return [],[]
    
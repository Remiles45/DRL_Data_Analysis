# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:02:57 2022

@author: Becca
"""
import numpy as np
import pandas as pd
from os.path import exists
from Data import Data
from scipy import ndimage

class DataProcessor:
    def __init__(self,base_path=None,dec_factor=1):
        self.base_path = base_path
        self.dec_factor = dec_factor # reduce size of large files
        
        #idk if I will ever use this, but it might be nice to be able to identify a specific trial
        self.trial_key = None
        try:
            path_parts = self.base_path.split('_T')
            self.trial_key = path_parts[-1]
        except:
            print('Could not identify trial key for '+self.base_path)
        
        
        self.voltage    = Data(self.base_path + '/Voltage Monitor.csv','Voltage',self.ProcessVoltage)
        self.current    = Data(self.base_path + '/Current Monitor.csv','Current',self.ProcessCurrent)
        self.anemometer = Data(self.base_path + '/Anemometer.csv','Anemometer',self.ProcessAnemometer)
        self.force      = Data(self.base_path + '/Force.csv','Force',self.ProcessForce)
        self.supply     = Data(self.base_path + '/Power Supply.csv','Power Supply',self.ProcessPowerSupply)
        self.stage      = Data(self.base_path + '/XY Stage.csv','XY Stage',self.ProcessXYStage)
        self.balance    = Data(self.base_path + '/Balance.csv','Balance',self.ProcessBalance)
        self.balance_v  = Data(self.base_path + '/Balance Voltages.csv','Balance Voltage',self.ProcessBalanceVoltage)
                
        self.generate_options = {
            'IV'  : (self.current,self.voltage),
            'FV'  : (self.force,self.voltage),
            'BV'  : (self.balance,self.balance_v),
            'AV'  : (self.anemometer,self.voltage),
            'XYA' : (self.stage,self.anemometer),
            'IT'  : (self.current),
            'VT'  : (self.voltage),
            'AT'  : (self.anemometer),
            'FT'  : (self.force)            
            }
        
        
    def ProcessFile(self,options):
        '''
        This function will process all of the data for a single Trial 
        ("File" is misleading, it is technically one directory with several files) 
        Parameters
        ----------
        options : OptionsManager
            class which stores all of the options for different types of CSV file to generate

        Returns
        -------
        None.
        '''
        print('Generating Files....')
        for key in options.options_list:
            #if that option is selected
            if options.GetState(key):
                PASSED = True
                #check all the required files to ensure they exist
                for obj in self.generate_options[key]:
                    if not exists(obj.filepath):
                        print('Could not generate '+str(key)+' CSV due to missing files')
                        PASSED = False
                        break;
                #if all files exist, proceed. 
                if PASSED:
                    pass
       
        
        
        
        
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
            raw_anemometer , self.anemometer.timestamps = self.ParseFile(self.voltage.filepath,reduce=True)
            e0 = 0 #0 velocity signal
            if velocity_range == 7.5:
                scalar = 1.5
            else:
                scalar = 2.8
            #filter the signal because why not ()
            filt_anemometer = ndimage.median_filter(raw_anemometer,size=5)
            # convert voltage to kV where vkv = (vsupplyout*kvmax)/vsupplymax
            self.anemometer.data = (((filt_anemometer-e0)*scalar)/(10-e0))*velocity_range

    def ProcessForce(self):
        #check if the force has already been parsed
        if len(self.force.data) == 0:
            self.force.data , self.force.timestamps = self.ParseFile(self.force.filepath)
        
    def ProcessPowerSupply(self):
        #check if the power supply has already been parsed
        if len(self.supply.data) == 0:
            self.supply.data , self.supply.timestamps = self.ParseFile(self.supply.filepath)
    
    def ProcessXYStage(self):
        pass
    
    def ProcessBalance(self):
        #check if the balance has already been parsed
        if len(self.balance.data) == 0:
            self.balance.data = self.ParseFile(self.balance.filepath)
    
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
            out_data = np.array(data.values)
            out_ts   = np.array(timestamps.values)
            #decimate the data if necessary
            if reduce and (self.dec_factor>1):
                out_data,out_ts = self.DecimateData(out_data,out_ts)
            return out_data,out_ts
        else:
            raise ValueError('Unrecognized File Format')

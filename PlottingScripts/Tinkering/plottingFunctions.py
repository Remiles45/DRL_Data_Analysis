# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:07:47 2022

@author: Wintermute
"""
import numpy as np
import time 
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D
from ParseFile import ParseFile
from ParseFile import ParseSingle

file_type = '.csv'
# define possible filenames that you may want to plot
anemometer_path = 'Anemometer'+file_type
stage_path = 'XY Stage'+file_type
current_path = 'Current Monitor'+file_type
voltage_path = 'Voltage Monitor'+file_type
power_supply_path = 'Power Supply'+file_type
force_path = 'Force'+file_type
pwm_path = 'PWM Controller' + file_type
balance_path = 'Balance' + file_type
balance_voltages = 'Balance Voltages'+ file_type
            
def PlotAnemometer2d(file_range,path,show_plot=True,mode='raw',velocity_range=7.5):
    '''
    This fuction will map each anemometer reading to its xy position based
    on the recorded timestamps for each point. 
    Inputs: 
        file_range (list)- trial numbers that the user wants to include in the plot
        path (string)- full filepath for the anemometer file that should be plotted. 
            This assumes that the final part of the naming scheme for the file is a trial number
            and that the filepath is the entire path minus that trial number. 
            for example: 
                PlotAnemometer2d([1,2],'Documents/Data/ExampleExperiment/some_experiment_T')
                will parse 2 files:
                    'Documents/Data/ExampleExperiment/some_experiment_T1/anemometer.csv' and
                    'Documents/Data/ExampleExperiment/some_experiment_T2/anemometer.csv'
        show_plot (boolean)- toggle whether the plot should pop up immediately or not
        mode (string)- should the xy position be normalized such that the highest velocity 
            measured is centered at (0,0) or as it is saved in the file
            options: 
                    'raw' - xy position will be the raw position according to the xy stage in mm
                    'norm' - xy position will be centered at 0 where the peak of the air velocity is the centerpoint.
    '''
    # initialize empty lists to output x,y,z data to plot
    full_data = []
    full_x_out = []
    full_y_out = []
    e0 = -0.003
    if velocity_range == 7.5:
        scalar = 1.5
    else:
        scalar = 2.8
    # for a given file path, read and combine together all of the desired trials
    for t in file_range:
        pre_path = path + str(t)+'/'
            
        
        print("Parsing Anemometer")
        '''
        Anemometer conversion:
            V = ((Eout - E0)/(Efs - E0)) * Vfs
            V = measured velocity (m/s)
            Vfs = full scale velocity setting in ft/min or m/s
            Eout = measured output voltage or current signal
            E0 = zero flow output voltage or current
            Efs = full scale voltage or current output
        '''
        # read in data
        raw_anemometer,anemometer_timestamps = ParseFile(pre_path+anemometer_path)
        print("Parsing Voltage")
        full_voltage,voltage_timestamps = GetVoltage(pre_path)
        experiment_start_time,settle_voltage = FindStartTime(pre_path,return_settle_voltage=True)
        print("Parsing xy stage")
        str_coord,stage_timestamps = ParseFile(pre_path+stage_path)
        full_x = []
        full_y = []
        # xy coordinates need an extra step to parse
        for coord in str_coord:
            xy = coord.split(' ')
            full_x.append(float(xy[0])*1e-3)#convert to mm
            full_y.append(float(xy[1])*1e-3)
        full_x = np.array(full_x)
        full_y = np.array(full_y)    
        
#        experiment_start_time = stage_timestamps[0]+5 # cut off ramp 
        #only use data collected after the experiment officially began
        active_stage_idx = stage_timestamps >= experiment_start_time 
        stage_timestamps = stage_timestamps[active_stage_idx]-experiment_start_time
        x = full_x[active_stage_idx]
        y = full_y[active_stage_idx]
        
        
        active_anemometer_idx = (anemometer_timestamps >= experiment_start_time)
        active_anemometer_ts = anemometer_timestamps[active_anemometer_idx] - experiment_start_time
        active_anemometer_data = raw_anemometer[active_anemometer_idx]
        
        active_voltage_idx = (voltage_timestamps >= experiment_start_time)
        active_voltage_ts = voltage_timestamps[active_voltage_idx] - experiment_start_time
        voltage = full_voltage[active_voltage_idx]
#        e0 = np.average(active_anemometer_data[0:100])
        # find the 0 velocity anemometer reading- grab this data from before the experiment
        # started as that is the one point we know no air velocity was being generated and
        # the xy stage was stationary.
#        e0 = np.average(raw_anemometer[0:100])
        
        # calculate actual air velocity using the equation provided by the datasheet
        anemometer = (((active_anemometer_data-e0)*scalar)/(10-e0))*velocity_range #((active_anemometer_data - e0) / (10-e0))*2#active_anemometer_data most recent validation reported *2.8 not 2
        
        raw_pts_out = []
        raw_y_out = []
        raw_x_out = []
        avg_pts_out = []
        avg_y_out = []
        avg_x_out = []
        
        for i in range(len(x)):
            
            curr_x = x[i]
            curr_y = y[i]
            # for each x,y coordinate, find the timestamp range to compare to the 
            # anemometer data.
            this_stage_ts = stage_timestamps[i]
            ts_read_end_time = this_stage_ts + 0.6 # assume stationary for about 0.6 seconds
            
            voltage_low_bnd = (active_voltage_ts >= this_stage_ts)
            voltage_high_bnd = (active_voltage_ts < ts_read_end_time)
            voltage_idx = voltage_low_bnd & voltage_high_bnd
            voltage_at_pose = voltage[voltage_idx]
            if np.average(voltage_at_pose >= (settle_voltage - 50)):
                #Only record the datapoint if it isnt part of an arc or is after the 
                #experiment start 
                ''' 
                Anemometer
                '''
                # get the anemometer values for the time range defined by the xy stage
                low_bnd = (active_anemometer_ts >= this_stage_ts)
                upper_bnd =  (active_anemometer_ts < ts_read_end_time)
                ane_idx = low_bnd & upper_bnd
                ane_vals_at_pose = anemometer[ane_idx]
                for j in range(len(ane_vals_at_pose)):
                    raw_pts_out.append(ane_vals_at_pose[j])
                    raw_y_out.append(curr_y)
                    raw_x_out.append(curr_x)
                # average all of the recorded anemometer readings at that pose 
                avg_pts_out.append(np.average(ane_vals_at_pose))
                avg_y_out.append(curr_y)
                avg_x_out.append(curr_x)
                
                full_data.append(np.average(ane_vals_at_pose))
                full_y_out.append(curr_y)
                full_x_out.append(curr_x)
        
    peak = np.argmax(full_data)
    peak_x = full_x_out[peak]
    peak_y = full_y_out[peak]
    # this print is handy for locating the center of the thruster exhaust 
    # to ensure extra data is collected around that center point when running 
    # experiments.
    print("found data center at ("+str(peak_x)+', '+str(peak_y)+')')
    if mode == 'norm':
        full_x_out = full_x_out - peak_x
        full_y_out = full_y_out - peak_y
    if show_plot:
        fig = mpl.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(full_x_out,full_y_out,full_data)
        ax.title('Averaged Air Velocity '+path)
    return full_data,full_x_out,full_y_out        
def PlotCurrent(num_trials,path,plt,mode='iv',max_v=None,plt_mode='scatter',mkr_sz=2,OUTPUT=False):
    '''
    This fuction will plot the current read from the current file. 
    Inputs: 
        file_range (list)- trial numbers that the user wants to include in the plot
        path (string)- full filepath for the anemometer file that should be plotted. 
            This assumes that the final part of the naming scheme for the file is a trial number
            and that the filepath is the entire path minus that trial number. 
            for example: 
                PlotCurrent([1,2],'Documents/Data/ExampleExperiment/some_experiment_T')
                will parse 2 files:
                    'Documents/Data/ExampleExperiment/some_experiment_T1/current.csv' and
                    'Documents/Data/ExampleExperiment/some_experiment_T2/current.csv'
        plt (plot)- The plot which the data should appear on (Passing this in makes it easier
            to put multiple IV curves on the same plot)
        mode (string) [optional] - what type of plot you would like to see
            options: 
                    'iv' - current vs voltage plot
                    'time' - current vs time
        max_v (int) [optional] - Maximum voltage to plot 
        plt_mode (string) [optional] - allows you to toggle between a scatter plot and line plot
            options: 
                'scatter' - creates a scatter plot (recommended)
                'line' - creates a line plot
    '''
    curr= []
    v = []
    ts = []
    o_c = []
    o_v = []
    for t in num_trials:
        pre_path = path + str(t) + '/'
            
        print("Parsing Current")
        raw_current,current_timestamps = ParseFile(pre_path+current_path)
        # print('parsing voltage')
        df = 10000
        d_v,v_ts = GetVoltage(pre_path,dec_factor=df)
        
        zero_bias = np.average(raw_current[0:50])
        # print(np.shape(raw_current))
        d_curr = np.array([])
        d_ts = np.array([])
        # d_v = np.array([])
        for i in range(0,len(raw_current),df):
            d_curr = np.append(d_curr,raw_current[i])
            d_ts = np.append(d_ts,current_timestamps[i])
            # d_v = np.append(d_v, scaled_v[i])
        # print(np.shape(d_curr))
        scaled_current = (((d_curr-zero_bias)/91.3e3))*1e6 # current off of the shunt resistor (91.3 kOhm R) (I = V/R)[A] therefore microA = *1e6
        
        if mode == 'iv':
            out_v,out_curr = AverageIV(d_v,scaled_current)
            out_v = np.array(out_v)
            out_curr = np.array(out_curr)
            if max_v != None:#cut off data outside of voltage range
                valid_pts1 = out_v <= max_v
                valid_pts2 = out_v >= 0
                valid_pts = valid_pts1 & valid_pts2
                out_v = out_v[valid_pts]
                out_curr = out_curr[valid_pts]
        else:
            out_curr = scaled_current
            out_v = d_v
        ts.extend( d_ts - d_ts[0])
        curr.extend(out_curr)
        v.extend(out_v)
    if OUTPUT:
        return v,curr
    else:
        if mode == 'iv':
            if plt_mode == 'scatter':
                plt.scatter(v,curr)
            elif plt_mode == 'line':
                plt.plot(v,curr)
        elif mode == 'time':
            if plt_mode == 'scatter':
                plt.scatter(ts,curr)
            elif plt_mode == 'line':
                plt.plot(ts,curr)
def calcCurrent(mv):
    return  (((mv)/91.3e3))*1e6                
def AverageIV(voltages,currents):
    avg_current = []
    avg_v = np.unique(voltages) 
    for this_v in avg_v:
        v_idx = voltages == this_v
        avg_current.append(np.average(currents[v_idx]))
    out_v = avg_v
    out_curr = avg_current 
    return out_v,out_curr
def AvgDataChunks(x,y):
    '''
    Reduces data using unique numbers in x, averaging respective y values
    '''
    out_x = []
    out_y = []
    u = np.unique(x)
    for val in u:
        idx = x == val
        avg_y = np.average(y[idx])
        out_x.append(val)
        out_y.append(avg_y)
    return out_x,out_y
def PlotErrorBar(x,y,plt=None,output=False,norm=[]):
    
    out_x = []
    out_y = []
    y_err = []
    
    u = np.unique(x)
    cnt = 0
    for val in u:
        idx = x == val
        if len(norm)>0:
            y_vals = np.array(y[idx])/norm[cnt]
            cnt = cnt+1
        else:
            y_vals = y[idx]
        avg_y = np.average(y_vals)
        err = np.std(y_vals)#(np.max(y_vals)-avg_y, avg_y-np.min(y_vals))
        out_x.append(val)
        out_y.append(avg_y)
        y_err.append(err)
    if plt != None:
        y_err = np.array(y_err)
        y_err = np.transpose(y_err)
        plt.errorbar(out_x,out_y,yerr=y_err,fmt='o',capsize=5)
    if output:
        return out_x,out_y,y_err
# def PlotErrorBarV2(x,y,plt=None,output=False):
         
    
    
def FindCoronaOnsetV(voltage,current):
    zero_current = np.average(current[0:10])
               
    for i in range(len(current)):
        this_current = current[i]
        if this_current > (zero_current+10): # 5 micro A above the noise floor
            return voltage[i]
    return None
def GetVoltage(path,dec_factor = 1):
        raw_v,v_timestamps = ParseFile(path+voltage_path)
            
        ts = v_timestamps - v_timestamps[0]
        dec_ts = np.array([])
        for i in range(0,len(ts),dec_factor):
            dec_ts = np.append(dec_ts,ts[i])
        filt_v = medianFilt(raw_v,dec_factor=dec_factor)
        v = PowerSupply2KV(filt_v)
        return v,dec_ts
def PowerSupply2KV(v):
    return (v*8)/10 #kV  
def medianFilt(arr,window_rad=5,dec_factor=1):
    filt_out = []
    for i in range(0,len(arr),dec_factor): 
        if i <= window_rad:
            window = arr[i:window_rad]
        elif i >= len(arr)-window_rad:
            window = arr[i:len(arr)-1]
        else:
            window = arr[i-window_rad:i+window_rad]
        if len(window)<=1:
            filt_pt = arr[i]
        else:
            filt_pt = np.median(window)
        filt_out.append(filt_pt)
    return np.array(filt_out)
    
def FindStartTime(pre_path, return_settle_voltage=False):
    commands,ts = ParseFile(pre_path+power_supply_path)
    start_time = ts[-2] 
    if return_settle_voltage:
        settle_v = PowerSupply2KV(commands[-2]) #kV
        return start_time, settle_v
    else:
        return start_time
def PlotVoltage(num_trials,path,plot):
    out_v = []
    out_ts = []
    for t in num_trials:
        pre_path = path + str(t) + '/'
            
        print("Parsing Voltage")
        v,ts = GetVoltage(pre_path)
        out_v.append(v)
        out_ts.append(ts)
    plot.scatter(out_ts,out_v)
def PlotBalance(num_trials,path,plot=None,norm=[]):
    v = []
    f = []
    # out_v = []
    # out_f = []
    for t in num_trials:
        pre_path = path + str(t) + '/'    
        print(pre_path)
        voltages = ParseSingle(pre_path+balance_voltages)
        masses = ParseSingle(pre_path + balance_path)
        
        baseline_idx = voltages == 0
        baseline = masses[baseline_idx]
        
        forces = (masses-baseline) * 9.81 * 1e-3 #mg to kg = 1e-6, N to mN = 1e3 end result is 1e-3
        v.extend(voltages)
        f.extend(forces)
    v = np.array(v)
    f = np.array(f)
    # unique_pts = np.unique(v)
    # for pt in unique_pts:
    #     this_v_idx = v == pt
    #     v_pts = v[this_v_idx]
    #     f_pts = f[this_v_idx]
    #     avg_f = np.average(f_pts)
    #     out_v.append(pt)
    #     out_f.append(avg_f)
    if plot != None:
        # plot.plot(out_v,out_f)
        PlotErrorBar(v,f,plt=plot)
    else:
        xout,yout,yerr = PlotErrorBar(v,f,output=True,norm=norm)
        return xout,yout,yerr
def PlotAnemometer(num_trials,path,plot,mode='time',max_v=None):
    for t in num_trials:
        pre_path = path + str(t) + '/'
            
        print("Parsing Anemometer")
        raw_a,a_timestamps = ParseFile(pre_path+anemometer_path)
        
        ts = a_timestamps - a_timestamps[0]
        a = (raw_a)#*8e3)/10           
        if mode == 'time':
            plot.scatter(ts,a)
        else:
            scaled_v,v_ts = GetVoltage(pre_path)
            avg_ane = []
            avg_v = np.unique(scaled_v) # HACK, fix for real
            if max_v != None:
                valid_pts = avg_v <= max_v
                avg_v = avg_v[valid_pts]
            for this_v in avg_v:
                v_idx = scaled_v == this_v
                avg_ane.append(np.average(a[v_idx]))
            out_v = avg_v
            out_ane = avg_ane  
            
            plot.scatter(out_v,out_ane)
def PlotCrossSection(num_trials,path,plot,slice_width=0.1,slice_axis='x',outputOn=False):
    z_data,x_data,y_data = PlotAnemometer2d(num_trials, path,show_plot=False,mode='norm')
    bound = slice_width / 2
    z_data = np.array(z_data)
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    if slice_axis=='x':
        slice_idx = (y_data>-bound) & (y_data<bound)
        sliced_pose = x_data[slice_idx]
#        axis_lbl = 'X (mm)'
    elif slice_axis=='y':
        slice_idx = (x_data>-bound) & (x_data<bound)
        sliced_pose = y_data[slice_idx]
#        axis_lbl = 'Y (mm)'
    else:
        print("ERROR: axis must be 'x' or 'y'")
    
    sliced_amp = z_data[slice_idx]
    if outputOn:
        return sliced_pose,sliced_amp
    else:
        out_pose = []
        out_amp = []
        unique_pts = np.unique(sliced_pose)
        for pt in unique_pts:
            this_pose = pt
            upper_bnd = sliced_pose <= (this_pose + 0.1)
            low_bnd = sliced_pose >= (this_pose - 0.1)
            idx = upper_bnd & low_bnd
            unique_pts = np.delete(unique_pts,idx)
            amp_pts_here_idx = sliced_amp[idx]
            avg_pt = np.average(sliced_pose[amp_pts_here_idx])
            out_pose.append(this_pose)   
            out_amp.append(avg_pt)
        plot.scatter(out_pose,out_amp)
        #plot.scatter(sliced_pose,sliced_amp)
def PlotForceVsPWM(trial_nums,path,plot):
    
    forces = []
    pwms = []
    for t in trial_nums:
        pre_path = path + str(t) + '/'
        print("Parsing Force Data")
        force_data, force_timestamps = ParseFile(pre_path+force_path)
        print("Parsing PWM Data")
        pwm_data,pwm_timestamps = ParseFile(pre_path+pwm_path)
        force_data = force_data # mN
        trial_pwms,trial_forces = MatchTimestamps(pwm_data,pwm_timestamps,force_data,force_timestamps)
        pwms.extend(trial_pwms)
        forces.extend(trial_forces)
        # for i in range(len(pwm_data)):
        #     pwm_pt = pwm_data[i]
        #     pwm_ts = pwm_timestamps[i]
        #     start_t = pwm_ts #+ 0.01 # allow to settle
        #     end_t = start_t #+ 0.05 # to plot correctly this means each pwm point needs to sit still for at least 0.6 seconds
            
        #     idx = (force_timestamps >= start_t) & (force_timestamps <= end_t)
        #     valid_force_pts = force_data[idx]
        #     # print(len(valid_force_pts))
        #     force = np.average(valid_force_pts)
        #     forces.append(force)
        #     pwms.append(pwm_pt)
    # plot.scatter(force_timestamps,force_data)
    # print(forces)
    # print('pwm len: ' + str(len(pwms))+ ' forces len: ' + str(len(forces)))
    plot.scatter(pwms,forces)
    plot.set_xlabel('PWM (% duty cycle)')#
    plot.set_ylabel('Force (mN)')
        
def PlotForceVsVoltage(trial_nums,path,plot):
     voltages = []
     forces = []
     for t in trial_nums:
         pre_path = path + str(t) + '/'
         print("Parsing Force Data")
         force_data, force_timestamps = ParseFile(pre_path+force_path)
         print("Parsing Voltage Data")
         v_data,v_timestamps = ParseFile(pre_path+voltage_path)
         force_data = force_data #*1000#convert to mN
         v, f = MatchTimestamps(v_data, v_timestamps, force_data, force_timestamps)
         voltages.extend(v)
         forces.extend(f)
         
     plot.scatter(voltages,forces)
     plot.set_xlabel('Voltage')#'PWM (% duty cycle)')#
     plot.set_ylabel('Force (mN)')   
     
def MatchTimestamps(dataA,tsA,dataB,tsB):
     '''
     Parameters
     ----------
     dataA : List(float)
         Data for plot x axis (voltage, duty cycle etc)
     tsA : list(float)
         timestamps corresponding to x axis data.
     dataB : list(float)
         data for plot y axis. (anemometer, current etc)
     tsB : list(float)
         timestamps corresponding to y axis data.

     Returns
     -------
     matched_dataA: list(float)
         points from dataA that match with dataB timestamps. 
    matched_dataB: list(float)
        points from dataB that match with dataA timestamps.
         

     '''
     matched_dataA = []
     matched_dataB = []
     
     for i in range(len(dataA)):
         a_pt = dataA[i]
         a_ts = tsA[i]
         start_t = a_ts + 1 # allow to settle
         end_t = start_t + 0.5#0.5 # to plot correctly this means each pwm point needs to sit still for at least 0.6 seconds
         
         idx = (tsB >= start_t) & (tsB <= end_t)
         valid_pts = dataB[idx]
         b_pt = np.average(valid_pts)
         matched_dataB.append(b_pt)
         matched_dataA.append(a_pt)
     return matched_dataA,matched_dataB
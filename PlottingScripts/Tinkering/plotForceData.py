# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:26:40 2022

@author: Drew Lab Computer
"""
from ParseFile import ParseSingle

from plottingFunctions import *

import matplotlib.pyplot as mpl

# Intake Lip Data
path_reverse = '../../../../ExperimentData/'
balance_path = 'Balance.csv'
no_lip_path_base = path_reverse + 'LatEmitter/'
deg_20_path_base = path_reverse + 'LatEmitter/Intake Lip Data/Without Nozzles/deg_20/'
deg_45_path_base = path_reverse + 'LatEmitter/Intake Lip Data/Without Nozzles/deg_45/'
deg_75_path_base = path_reverse + 'LatEmitter/Intake Lip Data/Without Nozzles/deg_75/'

no_lip_IV_path = no_lip_path_base + 'Intake Lip Data/No Lip/Intake_None_7e_IV_T'
deg_20_IV_path = deg_20_path_base + 'Intake_20deg_7e_IV_T'
deg_45_IV_path = deg_45_path_base + 'Intake_45deg_7e_IV_T'
deg_75_IV_path = deg_75_path_base + 'Intake_75deg_7e_IV_T'


no_lip_XY_path = no_lip_path_base + 'XY data/D1_8mmD2_4mm/D1_8_D2_4_7e_XY_T'
deg_20_XY_path = deg_20_path_base + 'Intake_20deg_7e_XY_T'
deg_45_XY_path = deg_45_path_base + 'Intake_45deg_7e_XY_T'
deg_75_XY_path = deg_75_path_base + 'Intake_75deg_7e_XY_T'

no_lip_xy_trials = [11,12,13,14,15,16,17]
no_lip_iv_trials = [1,2,3,4,5,6]
no_lip_lbl = 'No Intake Lip' #8.25 uA

deg_20_xy_trials = []
deg_20_iv_trials = [6,7]#[5,6,7,8]
deg_20_lbl = '20 Degree Intake Lip'

deg_45_xy_trials = [1,2,3,4,5]
deg_45_iv_trials = [1,2,3]
deg_45_lbl = '45 Degree Intake Lip' # 8.6 uA

deg_75_xy_trials = []
deg_75_iv_trials = [1,2,3,4,5]
deg_75_lbl = '75 Degree Intake Lip'

voltage_path = no_lip_IV_path + '5/Balance Voltages.csv' # all of these files are identical

# voltages = ParseSingle(voltage_path)
# no_lip = ParseSingle(no_lip_IV_path+balance_path)
# deg_20 = ParseSingle(deg_20_IV_path+balance_path)
# deg_45 = ParseSingle(deg_45_IV_path+balance_path)
# deg_75 = ParseSingle(deg_75_IV_path+balance_path)


fig = mpl.figure()
plt = fig.add_subplot()

PlotBalance([6,7],deg_20_IV_path,plt)
PlotBalance([1,2],deg_45_IV_path,plt)
PlotBalance([1,2,3,4],deg_75_IV_path,plt)
# PlotBalance([7],deg_20_IV_path,plt)
plt.legend(['robot 2, 20 deg','robot 1 45 deg','robot 1,2 75 deg'])
# mpl.plot(no_lip,voltages,deg_20,voltages,deg_45,voltages,deg_75,voltages)
# mpl.legend(no_lip_lbl,deg_20_lbl,deg_45_lbl,deg_75_lbl)

plt.set_ylabel('force (mN)')
plt.set_xlabel('Voltage (kV)')
plt.set_xlim(2.95,3.55)
plt.set_ylim(0.04,0.14)
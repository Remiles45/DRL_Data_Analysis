# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 22:17:04 2022

@author: Drew Lab Computer
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:26:40 2022

@author: Drew Lab Computer
"""
from ParseFile import ParseSingle

from plottingFunctions import *

import matplotlib.pyplot as mpl

# Intake Lip Data
path_reverse = '../../../../ExperimentData/LatEmitter/Nozzle Data/'
balance_path = 'Balance.csv'
no_lip_path = path_reverse + 'No Nozzle/stage_3/no_nozzle_3_stage_IV_T'
con_path = path_reverse + 'Convergent/half/stage_3/convergent_3_stage_IV_T'
div_path = path_reverse + 'Divergent/stage_3/divergent_3_stage_IV_T'
straight_path = path_reverse + 'Straight/stage_3/straight_3_stage_IV_T'

# no_lip_IV_path = no_lip_path_base + 'Intake Lip Data/No Lip/Intake_None_7e_IV_T'
# deg_20_IV_path = deg_20_path_base + 'Intake_20deg_7e_IV_T'
# deg_45_IV_path = deg_45_path_base + 'Intake_45deg_7e_IV_T'
# deg_75_IV_path = deg_75_path_base + 'Intake_75deg_7e_IV_T'


# no_lip_XY_path = no_lip_path_base + 'XY data/D1_8mmD2_4mm/D1_8_D2_4_7e_XY_T'
# deg_20_XY_path = deg_20_path_base + 'Intake_20deg_7e_XY_T'
# deg_45_XY_path = deg_45_path_base + 'Intake_45deg_7e_XY_T'
# deg_75_XY_path = deg_75_path_base + 'Intake_75deg_7e_XY_T'

no_lip_xy_trials = [11,12,13,14,15,16,17]
no_lip_iv_trials = [5,6,'6_1']
no_lip_lbl = 'No Nozzle' #8.25 uA

deg_20_xy_trials = []
convergent_iv_trials = [1,2,'2_1']#[5,6,7,8]
convergent_lbl = 'Convergent'

deg_45_xy_trials = [1,2,3,4,5]
divergent_iv_trials = [5,6,'6_1']
divergent_lbl = 'Divergent' # 8.6 uA

deg_75_xy_trials = []
straight_iv_trials = [7,8,'8_1']
straight_lbl = 'Straight'

# voltage_path = no_lip_IV_path + '5/Balance Voltages.csv' # all of these files are identical

# voltages = ParseSingle(voltage_path)
# no_lip = ParseSingle(no_lip_IV_path+balance_path)
# deg_20 = ParseSingle(deg_20_IV_path+balance_path)
# deg_45 = ParseSingle(deg_45_IV_path+balance_path)
# deg_75 = ParseSingle(deg_75_IV_path+balance_path)


fig = mpl.figure()
plt = fig.add_subplot()

PlotBalance(straight_iv_trials,straight_path,plt)
PlotBalance(convergent_iv_trials,con_path,plt)
PlotBalance(divergent_iv_trials,div_path,plt)
PlotBalance(no_lip_iv_trials,no_lip_path,plt)
# PlotBalance([7],deg_20_IV_path,plt)
plt.legend(['straight','convergent','divergent','No Nozzle'])
# mpl.plot(no_lip,voltages,deg_20,voltages,deg_45,voltages,deg_75,voltages)
# mpl.legend(no_lip_lbl,deg_20_lbl,deg_45_lbl,deg_75_lbl)

plt.set_ylabel('force (mN)')
plt.set_xlabel('Voltage (kV)')
# plt.set_xlim(2.95,3.55)
# plt.set_ylim(0.04,0.14)
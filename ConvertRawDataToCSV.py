# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 12:25:02 2022

@author: Becca
"""

#TODO: add check/uncheck all buttons?


from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QMainWindow, QApplication, QLineEdit, QMessageBox, QSpacerItem, QComboBox, QCheckBox,QSizePolicy
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator
from PyQt5.QtCore import QSize, QTimer, Qt, pyqtSignal

import sys
import os
import time
import csv
import tkinter as tk   
from tkinter import filedialog as fd
import datetime
import tkfilebrowser as fb
import math

import CSVGenerator as gen
import OptionsManager as om


class ConverterWindow(QMainWindow):
    '''
    This is the main GUI window, it handles all jobs that are not device specific
    '''
    def __init__(self):
        QMainWindow.__init__(self)
        self.init_gui()
        
        self.chosen_dirs = ()
        
    def init_gui(self):
        '''
        Window Settings
        '''
        self.setMinimumSize(QSize(500, 300)) 
        self.setMaximumSize(QSize(1000,1000))
        self.setWindowTitle("Raw Data Converter") 
        
        self.window = QWidget()
        self.layout = QGridLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
        lbl_font = QFont('Arial',10)
        #spacer that helps keep GUI items where I tell them to go in the layout
        spacer_item = QSpacerItem(1, 1)   
        
        '''
        Save Filename Input
        '''
        self.save_file_lbl = QLabel('Output CSV Filename:')
        self.save_file_lbl.setFont(lbl_font)
        self.save_file_box = QLineEdit()  
        
        '''
        Plot Options to Generate
        '''
        self.plot_options = om.OptionsManager()
        options_lbl = QLabel('Create File Types:')
        options_lbl.setFont(lbl_font)
        #IV 
        self.IV_plot_cb  = QCheckBox('Current,Voltage')
        self.plot_options.options['IV'] = self.IV_plot_cb
        
        #FV 
        self.FV_plot_cb  = QCheckBox('Force,Voltage')
        self.plot_options.options['FV'] = self.FV_plot_cb
        
        #BV 
        self.BV_plot_cb  = QCheckBox('Force[balance],Voltage')
        self.plot_options.options['BV'] = self.BV_plot_cb
        
        #AV
        self.AV_plot_cb  = QCheckBox('Anemometer,Voltage')
        self.plot_options.options['AV'] = self.AV_plot_cb
        
        #XYA
        self.XYA_plot_cb  = QCheckBox('X,Y,Anemometer')
        self.plot_options.options['XYA'] = self.XYA_plot_cb
        
        #Decimated I vs Time
        self.IT_cb  = QCheckBox('Current,Time')
        self.IT_cb.setChecked(True)
        self.plot_options.options['IT'] = self.IT_cb
        
        #Decimated V vs Time
        self.VT_cb  = QCheckBox('Voltage,Time')
        self.VT_cb.setChecked(True)
        self.plot_options.options['VT'] = self.VT_cb
        
        #Decimated A vs Time
        self.AT_cb  = QCheckBox('Anemometer,Time')
        self.AT_cb.setChecked(True)
        self.plot_options.options['AT'] = self.AT_cb
        
        #Force vs Time 
        self.FT_cb  = QCheckBox('Force,Time')
        self.FT_cb.setChecked(True)
        self.plot_options.options['FT'] = self.FT_cb
        
        
        self.decimate_lbl = QLabel('Reduce Large Data by ')
        self.decimate_input = QLineEdit('1')
        self.decimate_input.setValidator(QIntValidator(1, 10000))
        self.decimate_input.setFixedWidth(40)
        
        '''
        Select Files
        '''
        select_warning_lbl = QLabel('CAUTION: selecting multiple files at once will combine all data from\nall files into a single csv (for each selected csv format)')
        self.sel_files_btn = QPushButton('Select Files')
        self.sel_files_btn.clicked.connect(self.handleSelFilesBtn)
        
        self.remove_files_btn = QPushButton('Remove All Files')
        self.remove_files_btn.clicked.connect(self.resetChosenDirs)
        self.remove_files_btn.hide()
        '''
        Select Destination Folder / Process Data
        '''
        self.convert_btn = QPushButton('Process Data')
        self.convert_btn.clicked.connect(self.handleProcessBtn)
        
        '''
        Chosen Files Descriptor
        '''
        chosen_files_lbl = QLabel('Selected Files:')
        chosen_files_lbl.setFont(lbl_font)
        self.chosen_files_msg = QLabel('')
        
        '''
        Layout
        '''
        
        # Layout : widget, row, col, row_span, col_span
        self.layout.addWidget(self.save_file_lbl,0,0,1,1)
        self.layout.addWidget(self.save_file_box,0,1,1,3)
        
        self.layout.addWidget(options_lbl,0,10,1,1)
        bottom_row = 0
        for i in range(self.plot_options.GetNumOptions()):
            self.layout.addWidget(self.plot_options.GetBox(i),i+1,10,1,1)
            bottom_row = i+1
        
        self.layout.addWidget(self.decimate_lbl,bottom_row+1,10,1,1)
        self.layout.addWidget(self.decimate_input,bottom_row+1,11,1,1)
        
        self.layout.addWidget(select_warning_lbl,1,0,2,4)
        self.layout.addWidget(self.sel_files_btn, 3, 1, 1, 1)
        self.layout.addWidget(self.convert_btn, 4, 1, 1, 1)
        self.layout.addWidget(chosen_files_lbl,5,0,1,2)
        self.layout.addWidget(self.remove_files_btn,6,0,1,1)
        self.layout.addWidget(self.chosen_files_msg,7,0,10,10)
    def handleProcessBtn(self):
        #check if a filename has been specified, only save if so
        if self.checkFilename(self.save_file_box.text(),bool_out=True) and self.checkDataSelection():
            root = tk.Tk()
            root.withdraw()
            root.title('Tkinter File Dialog')
            root.resizable(False, False)
            root.geometry('300x150')
            save_directory = fd.askdirectory()
            savefile = self.checkFilename(self.save_file_box.text())
            
            if (save_directory != '') and (savefile != None):
                
                self.path = save_directory + '/' + savefile
                # if file already exists, add increment to name to guarantee unique names
                if os.path.exists(self.path):
                    
                    i=0
                    test_path = self.path
                    while os.path.exists(test_path):
                        i=i+1
                        test_path = self.path + ' (' + str(i) + ')'
                    self.path = test_path
                os.mkdir(self.path) 
                print('Generating Files for '+self.path)
                #create data process object. This will avoid parsing files more than once
                generator = gen.CSVGenerator(self.chosen_dirs,self.path,self.plot_options,int(self.decimate_input.text()))
                generator.run()
                print('Finished')
                #reset the chosen directories and corresponding GUI text
                self.chosen_dirs = () 
                self.updateMsgText()
          
    def resetChosenDirs(self):
        self.chosen_dirs = ()
        self.updateMsgText()
    def select_directories(self):
        root = tk.Tk()
        root.withdraw()
        dirs = fb.askopendirnames(filetypes=[("CSV Files","*.csv"),])
        return dirs
        
    def handleSelFilesBtn(self):
        self.chosen_dirs = self.select_directories()
        if len(self.chosen_dirs)>0:
            self.updateMsgText()
        else:
            return
    def checkFilename(self,name,bool_out=False):
        '''
        check to ensure the user has entered a valid name to save the data to 
        when they run an experiment. Throw error if no name has been entered
        '''
        if name == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Must enter a valid filename")
            msg.setWindowTitle("Error")
            msg.exec_()
            return False
        else:
            if bool_out:
                return True
            else:
                return name
    
    def checkDataSelection(self):
        '''
        check to ensure the user has entered a valid name to save the data to 
        when they run an experiment. Throw error if no name has been entered
        '''
        if self.chosen_dirs == ():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Must select files to process")
            msg.setWindowTitle("Error")
            msg.exec_()
            return False
        else:
            return True    
    def updateMsgText(self):
        msg = ''
        dirs = self.chosen_dirs
        if len(dirs)>0:
            for path in dirs:
                msg = msg + '\n' + str(path)
        
        self.chosen_files_msg.setText(msg)
        # hide button if there are no files to remove
        if msg == '':
            self.remove_files_btn.hide()
        else:
            self.remove_files_btn.show()
            
        # Adjust the GUI size to display full filepaths
        w = self.window.sizeHint().width() 
        h = self.window.sizeHint().height() 
        # self.setFixedSize(w, h)
        self.resize(w, h)
    def closeEvent(self,event):
        pass
if __name__ == "__main__":
    '''
    This starts the GUI as an application and allows the user to close the GUI 
    using the red x button
    '''
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True) 
    mainWin = ConverterWindow()
    mainWin.show()
    sys.exit( app.exec() )
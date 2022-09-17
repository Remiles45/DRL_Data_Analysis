# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:44:10 2022

@author: Becca
"""


class OptionsManager:
    def __init__(self):
        self.options = {
            'IV'  : None,
            'FV'  : None,
            'BV'  : None,
            'AV'  : None,
            'XYA' : None,
            'IT'  : None,
            'VT'  : None,
            'AT'  : None,
            'FT'  : None
            }
        self.options_list = list(self.options.keys())
    def GetState(self,key):
        return self.options[key].isChecked()
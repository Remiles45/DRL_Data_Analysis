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
    def GetBox(self,key):
        if type(key) == str:
            return self.options[key]
        elif type(key) == int:
            realkey = self.options_list[key]
            return self.options[realkey]
    def GetState(self,key):
        if self.options[key] == None:
            ans = False
        else: 
            ans = self.options[key].isChecked()
        return ans
    def GetChecked(self):
        checked = []
        for op in self.options_list:
            if self.GetState(op):
                checked.append(op)
        return checked
    def GetNumOptions(self):
        return len(self.options_list)
        
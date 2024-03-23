from ntpath import join
import os
import sys
import comtypes.client

from api_setting_numbers import *
# import api_setting_numbers

import file
import geometry as geo
import table as tb
import analyze
import define
import select_

# Units Number Dictory

class ETABS :
    def __init__(self, software : str = 'ETABS'):
        self.software = software
        self.etabs = None
        self.sap = None
        self.success = False
    
        try:  
            #To get the active ETABS object
            # helper = comtypes.client.CreateObject('ETABSv1.Helper') # CSI code
            # helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper) # CSI code
            # etabs = helper.GetObject("CSI.ETABS.API.ETABSObject") # CSI code
            etabs = comtypes.client.GetActiveObject(f"CSI.{software}.API.ETABSObject")
            
        except (OSError, comtypes.COMError):
            print("No running instance of the program found or failed to attach.")
            sys.exit(-1)
        
        print("Successfully Loaded")

        ## Setup ##
        self.success = True
        sapModel = etabs.SapModel
        
        self.etabs = etabs
        self.sapModel = sapModel

        self.EDB_name = self.get_edb_name()
        print(f'EDB ({self.EDB_name}) is LOADED!!')
        
        self.set_units()
        self.version = self.get_version()
        print(f'Set units (default tonf,m), and Get verion ({self.version})')

        #### Loading Other Objects
        self.Table = tb.Table(etabs)
        mod =  'TABLE'
        print(f'- {mod:10s} modulus is loaded')
        
        self.File = file.File(etabs)
        mod =  'FILE'
        print(f'- {mod:10s} modulus is loaded')

        self.Points = geo.Points(etabs)
        mod =  'POINTS'
        print(f'- {mod:10s} modulus is loaded')

        self.Frames = geo.Frames(etabs)
        mod =  'FRAMES'
        print(f'- {mod:10s} modulus is loaded')

        self.Areas = geo.Areas(etabs)
        mod =  'AREA'
        print(f'- {mod:10s} modulus is loaded')

        self.Define = define.Define(etabs)
        mod =  'DEFINE'
        print(f'- {mod:10s} modulus is loaded')

        self.Select = select_.Select(etabs)
        mod =  'SELECT'
        print(f'- {mod:10s} modulus is loaded')

        self.Analyze = analyze.Analyze(etabs)
        mod =  'ANALYZE'
        print(f'- {mod:10s} modulus is loaded')

        self.DesignConcFrame = None
        self.DesignConcSlab = None
    
    #### LOCK
    def is_locked(self) -> bool :
        return self.sapModel.GetModelIsLocked()
    
    def model_lock(self) :
        if self.is_locked() : 
            pass
        else :
            self.sapModel.SetModelIsLocked(True)
            print('Model Locked')
    
    def model_unlock(self) :
        if self.is_locked() : 
            self.sapModel.SetModelIsLocked(False)
            print('Model Unlocked')
        else :
            pass
    
    #### Get Version
    def get_version(self) :
        ver = self.sapModel.GetVersion()[0]
        return ver
    
    #### UNITS
    def set_units(self, units = ['tonf', 'm']) :
        num = units2num(f'{units[0]}_{units[1]}'.lower()) 
        self.sapModel.SetPresentUnits(num)
        
    def get_units(self) :
        n = self.sapModel.GetPresentUnits()
        return num2units(n)
    
    #### FILE
    def get_edb_name(self, with_full_path = False) :
        return self.sapModel.GetModelFilename(with_full_path)


if __name__ == '__main__' :
    et = ETABS()
    
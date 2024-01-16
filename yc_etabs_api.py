from ntpath import join
import os
import sys
import comtypes.client

from api_setting_numbers import *

import geometry as geo
import table as tb


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
        self.success = True
        sapModel = etabs.SapModel
        
        self.etabs = etabs
        self.sapModel = sapModel
        
        self.set_units()
        self.version = self.get_version()
        
        #### Loading Other Objects
        self.Table = tb.Table(etabs)
        self.Points = geo.Points(etabs)
        self.Frames = geo.Frames(etabs)
    
    def get_version(self) :
        ver = self.sapModel.GetVersion()[0]
        return ver
    
    def set_units(self, units = ['tonf', 'm']) :
        num = units2num[f'{units[0]}_{units[1]}'.lower()] 
        self.sapModel.SetPresentUnits(num)
        
    def get_units(self) :
        n = self.sapModel.GetPresentUnits()
        for units, num in units2num.items() :
            if num == n :
                return units.split('_')
    
            
if __name__ == '__main__' :
    et = ETABS()
    
    # ret = sap.PropMaterial.SetMaterial('CONC', 2)
    # ret = sap.PropMaterial.SetMPIsotropic('CONC', 3600, 0.2, 0.0000055)
    
    # print(et.create_pt(0,0,10))
    
    # print(et.Point.get(1))
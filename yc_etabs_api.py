from ntpath import join
import os
import sys
import comtypes.client

from point import Point

# Units Number Dictory
force_units = {
    'N' : 3, 
    'kN' : 4,  
    'kgf' : 5, 
    'tonf' : 6
}

length_units = {
    'mm' : 4, 
    'cm' : 5, 
    'm' : 6
}

enum_units = {
        'kn_mm' : 5,
        'kn_m' : 6,
        'kgf_mm' : 7,
        'kgf_m' : 8,
        'n_mm' : 9,
        'n_m' : 10,
        'tonf_mm' : 11,
        'tonf_m' : 12,
        'kn_cm' : 13,
        'kgf_cm' : 14,
        'n_cm' : 15,
        'tonf_cm' : 16,
}

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
        
        self.Point = Point(etabs)
    
    def get_version(self) :
        ver = self.sapModel.GetVersion()[0]
        return ver
    
    def set_units(self, units = ['tonf', 'm']) :
        # force = force_units[units[0]]
        # length = length_units[units[1]]
        
        num = enum_units[f'{units[0]}_{units[1]}'.lower()]
        
        self.sapModel.SetPresentUnits(num)
        
    def create_pt(self, x, y, z) :
        # Return PtLabel, returnValue
        return self.sap.PointObj.AddCartesian(x, y, z)
            
if __name__ == '__main__' :
    et = ETABS()
    
    # ret = sap.PropMaterial.SetMaterial('CONC', 2)
    # ret = sap.PropMaterial.SetMPIsotropic('CONC', 3600, 0.2, 0.0000055)
    
    # print(et.create_pt(0,0,10))
    
    print(et.Point.get(1))
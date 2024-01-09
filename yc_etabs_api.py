from ntpath import join
import os
import sys
import comtypes.client

class etabs() :
    def __init__(self):
        helper = comtypes.client.CreateObject('ETABSv1.Helper')
        helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
        
        try:  
            #To get the active ETABS object
            etabs = helper.GetObject("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            print("No running instance of the program found or failed to attach.")
            sys.exit(-1)
        
        print("Successfully Loaded")
        sap = etabs.SapModel
        
        self.set_units()
        
        self.helper = helper
        self.etabs = etabs
        self.sap = sap
        
    def set_units(self, units = ['tf', 'm']) :
        if units == ['tf', 'm'] :
            unit = 12
        else : 
            print('No Units to set')
            pass
        
        self.sap.SetPresentUnits(unit)
        
    def create_pt(self, x, y, z) :
        # Return PtLabel, returnValue
        return self.sap.PointObj.AddCartesian(x, y, z)
            
if __name__ == '__main__' :
    et = etabs()
    sap = et.sap
    
    # ret = sap.PropMaterial.SetMaterial('CONC', 2)
    # ret = sap.PropMaterial.SetMPIsotropic('CONC', 3600, 0.2, 0.0000055)
    
    print(et.create_pt(0,0,10))
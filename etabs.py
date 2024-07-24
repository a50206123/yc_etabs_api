from ntpath import join

import os
import sys
cdr = os.path.abspath(__file__).split('\\')
del cdr[-1]
sys.path.append('\\'.join(cdr))

import comtypes.client

from setting import *

#### Import ETABS APIs
import file, points, frames, areas, strips
import table as tb
import analyze, define, select_, design, results

## APPS
from apps.tedchu import TedChuMethods


class ETABS :
    def __init__(self, software : str = 'ETABS', isTedChu = False, 
                 msg_signal = None, print_log = None) :
        self.software = software
        self.etabs = None
        self.sap = None
        self.success = False


        if msg_signal :
            self.msg_signal = msg_signal
            self.print_log = print_log
        else :
            import yc_print
            self.msg_signal = yc_print.msg_signal
            print_log = yc_print.print_log
            self.print_log = print_log


        try:  
            #To get the active ETABS object
            # helper = comtypes.client.CreateObject('ETABSv1.Helper') # CSI code
            # helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper) # CSI code
            # etabs = helper.GetObject("CSI.ETABS.API.ETABSObject") # CSI code
            etabs = comtypes.client.GetActiveObject(f"CSI.{software}.API.ETABSObject")
            
        except (OSError, comtypes.COMError):
            print_log("No running instance of the program found or failed to attach.")
            # sys.exit(-1)
            return None # Skip to adding following stuffs
        
        print_log(f"{'#'*10}  Successfully Loaded  {'#'*10}", self.msg_signal)

        ## Setup ##
        sapModel = etabs.SapModel
        
        # API Objects
        self.success = True
        self.etabs = etabs
        self.sapModel = sapModel

        # ETABS Info
        self.EDB_name = self.get_edb_name()
        self.EDB_path = self.get_edb_path()
        self.version = self.get_version()
        print_log(f'EDB ({self.EDB_name}) is LOADED!!', self.msg_signal)
        
        # Initialize ETABS
        self.set_units()
        print_log(f'Set units (default tonf,m), and Get verion ({self.version})', self.msg_signal)

        print_log(f'\n{"#"*10}  Initialized  {"#"*10}', self.msg_signal)

        #### Loading Other Objects
        self.Table = tb.Table(etabs, print_log, self.msg_signal)
        print_log('TABLE', self.msg_signal, add_mod = True)
        
        self.File = file.File(etabs, print_log, self.msg_signal)
        print_log('FILE', self.msg_signal, add_mod = True)

        self.Points = points.Points(etabs, print_log, self.msg_signal)
        print_log('POINTS', self.msg_signal, add_mod = True)

        self.Frames = frames.Frames(etabs, print_log, self.msg_signal)
        print_log('FRAMES', self.msg_signal, add_mod = True)

        self.Areas = areas.Areas(etabs, print_log, self.msg_signal)
        print_log('AREAS', self.msg_signal, add_mod = True)

        self.Strips = strips.Strips(etabs, print_log, self.msg_signal)
        print_log('STRIPS', self.msg_signal, add_mod = True)

        self.Define = define.Define(etabs, print_log, self.msg_signal)
        print_log('DEFINE', self.msg_signal, add_mod = True)

        self.Select = select_.Select(etabs, print_log, self.msg_signal)
        print_log('SELECT', self.msg_signal, add_mod = True)

        # self.LoadComb = load_.LoadComb(etabs)
        # mod =  'LOAD COMBINATION'
        # print(f'- {mod:10s} modulus is loaded')

        self.Analyze = analyze.Analyze(etabs, print_log, self.msg_signal)
        print_log('ANALYZE', self.msg_signal, add_mod = True)

        self.Results = results.Results(etabs, print_log, self.msg_signal)
        print_log('RESULT', self.msg_signal, add_mod = True)

        self.Design = design.Design(etabs, print_log, self.msg_signal)
        print_log('Design', self.msg_signal, add_mod = True)

        # if isTedChu :
        #     self.TedChu = TedChuMethods(etabs, print_log)
        #     print_log('TedChu', self.msg_signal, add_mod = True)
        
        print_log(f'\n{"#"*10}  "{self.EDB_name}" is Connected!  {"#"*10}\n\n', self.msg_signal)




    #### LOCK ####
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
    
    #### Get Version ####
    def get_version(self) :
        ver = self.sapModel.GetVersion()[0]
        return ver
    
    #### UNITS ####
    def set_units(self, units = ['tonf', 'm']) :
        num = units2num(f'{units[0]}_{units[1]}'.lower()) 
        self.sapModel.SetPresentUnits(num)
        
    def get_units(self) :
        n = self.sapModel.GetPresentUnits()
        return num2units(n)
    
    #### FILE ####
    def get_edb_name(self, with_full_path = False) :
        return self.sapModel.GetModelFilename(with_full_path)
    
    def get_edb_path(self) :
        ret = self.sapModel.GetModelFilename(True).split('\\')
        del ret[-1]
        return '\\'.join(ret)
    
    #### REFRESH ####
    def refresh(self) :
        obj = self.sapModel.View
        obj.RefreshView()

    #### OTHER FUNCTIONS ####

if __name__ == '__main__' :
    et = ETABS(isTedChu = True)
    
    # print(et.get_edb_path())

    # et.refresh()
import numpy as np
import pandas as pd
from yc_etabs_api import ETABS

class Table :
    def __init__(self, etabs):
        self.etabs = etabs
        self.sapModel = etabs.sapModel

        print('To Load Table successfully!')
    #### READ TABLE    
    def read(self, key : str, col = None) :
        if not self.is_table_exist(key) :
            return None
        
        TableKey = key
        FieldKeyList = []
        GroupName = key
        TableVersion = 0
        FieldsKeysIncluded = []
        NumberRecords = 0
        TableData = []
        ## From API
        table = self.sapModel.DatabaseTables.GetTableForDisplayArray(\
            TableKey, FieldKeyList, GroupName, TableVersion,\
            FieldsKeysIncluded, NumberRecords, TableData)
            
        if not table :
            print('No Tables to read')
            return None
        
        print(f'Successfully Read Table ({key})')
        
        fields = table[2]
        datas = table[4]
        
        n = len(fields)
        data = np.reshape(datas, (int(len(datas)/n),n))
        
        if col == None :
            print('Got all tables')
            return pd.DataFrame(data, columns= fields)
        else :
            print(f'Got some tables of which is {lambda x for x in fields}')
            get_col = []
            for i in range(n) :
                if fields[i] in col :
                    get_col.append(i)
            
            some_data = data[:,get_col]
            
            return pd.DataFrame(some_data, columns=col)
    
    def apply(self, key : str, data : pd.core.frame.DataFrame) :
        fields = list(data.columns) # get fields you want to apply
        data_1d = data.values.reshape(1, len(data.size)[0])
        
        self.sapModel.DatabaseTables.SetTableForEditingArray(key, 0, fields, 0, data_1d)

        if self.sapModel.GetModelIsLocked():
            self.sapModel.SetModelIsLocked(False) # unlock
        
        FillImportLog = True
        NumFatalErrors = 0
        NumErrorMsgs = 0
        NumWarnMsgs = 0
        NumInfoMsgs = 0
        ImportLog = ''

        [NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog,
            ret] = self.SapModel.DatabaseTables.ApplyEditedTables(FillImportLog, NumFatalErrors,
                                                            NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)
        
        results = {
            'num_fatal_error' : NumFatalErrors,
            'num_error_msg' : NumErrorMsgs,
            'num_warning_msg' : NumWarnMsgs,
            'num_info_msg' : NumInfoMsgs,
            'log' : ImportLog,
            'return' : ret
        }
        
        print(f'Apply tables successfully. ({key})')
        return results

    def get_all_tables(self) :
        return self.sapModel.DatabaseTables.GetAvailableTables()[1]
        
    def is_table_exist(self, key : str) :
        all_tables = self.get_all_tables()
        
        if key in all_tables :
            return True
        else :
            return False
    
    #### GET BASIC SETTING
    def get_story(self,col = None) :
        return self.read('Story Definitions', col)
    
    #### GET CONNECTIVITY
    ## case = 0 --> UniqueName ...
    ## case = 1 --> Label(Bay) Story ...
    def get_points(self,col = None, case = None) :
        key = 'Point Object Connectivity'
        if case != None :
            if case == 0 :
                col = ['UniqueName', 'X', 'Y', 'Z']
            elif case == 1 :
                col = ['PointBay', 'Story', 'X', 'Y', 'Z']
            else :
                pass
        
        return self.read(key, col)
    
    def get_col_connectivity(self,col = None, case = None) :
        key = 'Column Object Connectivity'
        if case != None :
            if case == 0 :
                col = ['UniqueName', 'UniquePtI', 'UniquePtJ', 'Length']
            elif case == 1 :
                col = ['ColumnBay', 'Story', 'UniquePtI', 'UniquePtJ', 'Length']
            else :
                pass
        
        return self.read(key, col)
    
    def get_beam_connectivity(self,col = None, case = None) :
        key = 'Beam Object Connectivity'
        if case != None :
            if case == 0 :
                col = ['UniqueName', 'UniquePtI', 'UniquePtJ', 'Length']
            elif case == 1 :
                col = ['ColumnBay', 'Story', 'UniquePtI', 'UniquePtJ', 'Length']
            else :
                pass
        
        return self.read(key, col)
    
    #### GET ASSIGNMENTS
    ## case = 0 --> UniqueName ...
    ## case = 1 --> Label(Bay) Story ...
    def get_frame_sect_prop(self, col = None, case = None) :
        key = 'Frame Assignments - Section Properties'
        if case != None :
            if case == 0 :
                col = ['UniqueName', 'Shape', 'SectProp']
            elif case == 1 :
                col = ['Story', 'Label', 'Shape', 'SectProp']
            else :
                pass
        
        return self.read(key, col)

if __name__ == '__main__' :
    
    et = ETABS()
    tb = Table(et)
    
    sd = tb.read('Story Definitions', ['Story', 'Height'])
    cfd= tb.read('Concrete Frame Design Preferences - ACI 318-19')
    
    pt = tb.get_points()
    bm = tb.get_beam_connectivity(case = 0)
    col = tb.get_col_connectivity(case = 0)
    frame_prop = tb.get_frame_sect_prop(case = 0)
import pandas as pd
from yc_etabs_api import ETABS

class Table :
    def __init__(self, etabs):
        self.etabs = etabs
        self.sapModel = etabs.sapModel
        
    def read(self, key : str, col = None) :
        if not self.is_table_exist(key) :
            return None
        
        '''SapModel.DatabaseTables.GetTableForDisplayArray(
            table_key, FieldKeyList, GroupName, TableVersion, 
            FieldsKeysIncluded, NumberRecords, TableData)
        '''
        table = self.sapModel.DatabaseTables.GetTableForDisplayArray(\
            key, [], key, 0, [], 0, [])
            
        if not table :
            return None
        
        fields = table[2]
        datas = table[4]
        
        n = len(fields)
        data = [(table[i:i+n]) for i in range(0, len(table))]
        
        
    def is_table_exist(self, key : str) :
        all_tables = self.sapModel.Database.GetAvailableTables()[1]
        
        if key in all_tables :
            return True
        else :
            return False

if __name__ == '__main__' :
    
    et = ETABS()
    
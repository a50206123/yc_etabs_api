class Table :
    def __init__(self, etabs):
        self.etabs = etabs
        self.sapModel = etabs.sapModel
        
    def read(self, key : str, col : list) :
        pass
        tables = self.sapModel.DatabaseTables.ApplyEditedTables
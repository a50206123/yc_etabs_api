class Point :
    def __init__(self, etabs):
        sapModel = etabs.sapModel
        
        self.etabs = etabs
        self.sapModel = sapModel
    
    #----- Geometry -----#
    def add(self, x : float, y : float, z : float) :
        # Input Info
        # x, y, z are global coordinates
        
        etabs = self.etabs
        sapModel = self.sapModel
        
        # etabs.unlock_model()
        
        unique, returnValue = sapModel.PointObj.AddCartesian(x, y, z)
        
        return unique
    
    def get(self, unique : int) :
        key = 'Point Object Connectivity'
        cols = ['UniqueName', 'X', 'Y', 'Z']
        
        db = self.etabs.database_read(key, to_dateframe = True, cols = cols)
        
        return db
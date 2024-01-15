class GeometryObj :
    def __init__(self, etabs) :
        sapModel = etabs.sapModel
        
        self.etabs = etabs
        self.sapModel = sapModel

    def add(self) :
        pass
    
    def modify(self) :
        pass
    
class Point(GeometryObj) :
    def __init__(self, etabs):
        super.__init__(self, etabs)

    #----- Geometry -----#
    def add(self, coor : list) :
        # Input Info
        # x, y, z are global coordinates
        x, y, z = coor
        
        sapModel = self.sapModel
        
        unique, returnValue = sapModel.PointObj.AddCartesian(x, y, z)
        
        return unique
    
    def modify(self, unique : int) :
        pass
    
if __name__ == '__main__' :
    pass
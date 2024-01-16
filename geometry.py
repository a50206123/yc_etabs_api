import table as tb

class GeometryObj :
    def __init__(self, etabs) :
        sapModel = etabs.sapModel
        
        self.etabs = etabs
        self.sapModel = sapModel

    def add(self) :
        pass
    
    def modify(self) :
        pass
    
class Points(GeometryObj) :
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
    
    def delete(self, unique : int) :
        self.sapModel.PointObj.DeleteSpecialPoint(unique)
    
    def selected(self):
        return self.sapModel.PointObj.GetAllPoints(0,[],[],[],[])
    
class Frames(GeometryObj) :
    def __init__(self, etabs) :
        super.__init__(self, etabs)
    
    #----- Geometry -----#
    def add(self, coor1 : list, coor2 : list) :
        sapModel = self.sapModel
        XI, YI, ZI = coor1
        XJ, YJ, ZJ = coor2
        Name = []
        unique, returnValue = sapModel.FrameObj.AddByCoor(XI, YI,\
                                ZI, XJ, YJ, ZJ, Name) # API
        return unique
    
    def delete(self, unique) :
        sapModel = self.sapModel
        sapModel.FrameObj.Delete(unique)
        
class Areas(GeometryObj) :
    def __init__(self, etabs) :
        super.__init__(self, etabs)
    
    #----- Geometry -----#
    def add(self, X : list, Y : list, Z : list, prop = "Default") :
        sapModel = self.sapModel
        NumberPoints = len(X)
        Name = ''
        PropName = prop
        UserName = ''
        CSys = 'Global'
        unique, returnValue = sapModel.AreaObj.\
            AddByCoor(NumberPoints, X, Y, Z, Name, \
                      PropName, UserName, CSys)) # API
        return unique
    
    def delete(self, unique) :
        sapModel = self.sapModel
        sapModel.AreaObj.Delete(unique)
    
if __name__ == '__main__' :
    pass
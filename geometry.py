import table as tb

class GeometryObj :
    def __init__(self, etabs) :
        sapModel = etabs.sapModel
        
        self.etabs = etabs
        self.sapModel = sapModel
        self.Table = tb.Table(etabs)

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
    
    def get_all(self, case=0) :
        pts = self.Table.get_points(case = case)

        pts_dict = {}
        if case == 0 :
            unique = pts['UniqueName']
            X = pts['X']
            Y = pts['Y']
            Z = pts['Z']

            for name, x,y,z in unique,X,Y,Z :
                pts_dict[name] = [x, y, z]
        elif case == 1 :
            bays = pts['PointBay']
            stories = pts['Story']
            X = pts['X']
            Y = pts['Y']
            Z = pts['Z']

            for bay, story, x, y, z in bays, stories, X, Y, Z :
                pts[story+bay] = [x, y, z]

        return pts_dict

    
class Frames(GeometryObj) :
    def __init__(self, etabs) :
        super.__init__(self, etabs)
    
    #----- Geometry -----#
    def add(self, inputs:list, add_mode=0, sect_prop="Default", rotate=0) :
        sapModel = self.sapModel

        Name = []
        PropName = sect_prop
        UserName = ''
        CSys = 'Global'
        if add_mode == 0 :
            XI, YI, ZI = inputs[0]
            XJ, YJ, ZJ = inputs[1]
            unique, returnValue = sapModel.FrameObj.AddByCoor(XI, YI,
                                    ZI, XJ, YJ, ZJ, Name, PropName, UserName, CSys) # API
        elif add_mode == 1:
            Point1, Point2 = inputs
            unique, returnValue = sapModel.FrameObj.AddByPoint(Point1, 
	                                Point2, Name, PropName, UserName) # API
        else :
            returnValue = 1
        
        if returnValue == 0 :
            print(f'Frame {unique} added successfully.')
            return unique
        else :
            print('No Frame Added.')
            return None
    
    def delete(self, unique) :
        sapModel = self.sapModel
        sapModel.FrameObj.Delete(unique)
        
class Areas(GeometryObj) :
    def __init__(self, etabs) :
        super.__init__(self, etabs)
    
    #----- Geometry -----#
    def add(self, inputs:list, add_mode=0, sect_prop="Default", rotate=0) :
        sapModel = self.sapModel

        NumberPoints = len(inputs)
        Name = []
        PropName = sect_prop
        UserName = ''
        CSys = 'Global'
        if add_mode == 0 :
            X = []
            Y = []
            Z = []
            for coor in inputs:
                X.append(coor[0])
                Y.append(coor[1])
                Z.append(coor[2])

            unique, returnValue = sapModel.AreaObj.AddByCoord(NumberPoints, 
                                        	X, Y, Z, Name, PropName, UserName, CSys) # API
        elif add_mode == 1:
            Point = inputs
            unique, returnValue = sapModel.AreaObj.AddByPoint(NumberPoints, 
                                        	Point, Name, PropName, UserName) # API
        else :
            returnValue = 1
        
        if returnValue == 0 :
            print(f'Frame {unique} added successfully.')
            return unique
        else :
            print('No Frame Added.')
            return None
    
    def delete(self, unique) :
        sapModel = self.sapModel
        sapModel.AreaObj.Delete(unique)
    
if __name__ == '__main__' :
    pass
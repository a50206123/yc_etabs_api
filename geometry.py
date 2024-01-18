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

    def set_suppot(self, unique:str, restraints:list) :
        Name = unique
        Value = restraints
        ItemType = 0
        
        self.sapModel.PointObj.SetRestraint(Name, Value, ItemType)
        
    def set_spring(self, unique:str , stiff:list, is_replaced:bool=True):
        Name = unique
        K = stiff
        ItemType = 0
        IsLocalCSys = False
        Replace = is_replaced
        
        self.sapModel.PointObj.SetSpring(Name, K, ItemType, IsLocalCSys, Replace)
        
    def assign_load(self, unique:str, load_pattern:str, loads, 
                    is_replaced:bool=True, is_gravity=False) :
        Name = unique
        LoadPat = load_pattern
        Value = loads
        Replace = is_replaced
        CSys = 'Global'
        ItemType = 0
        
        if is_gravity :
            Value = [0, 0, -1*loads, 0, 0, 0]
        
        self.sapModel.PointObj.SetLoadForce(Name, LoadPat, Value, Replace, CSys, 
                                            ItemType)

    
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
    
    def set_release(self) :
        pass
    
    def set_rigidzone(self) :
        pass
    
    def assign_load(self) :
        pass
        
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
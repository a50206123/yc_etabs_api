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
        super().__init__(etabs)

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
        super().__init__(etabs)
        self.obj = self.sapModel.FrameObj
    
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
            unique, returnValue = self.obj.AddByCoor(XI, YI,
                                    ZI, XJ, YJ, ZJ, Name, PropName, UserName, CSys) # API
        elif add_mode == 1:
            Point1, Point2 = inputs
            unique, returnValue = self.obj.AddByPoint(Point1, 
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
        self.obj.Delete(unique)
    
    def set_material(self, unique:str, mat:str) : # TEST OK
        Name = unique
        PropName = mat

        ret = self.obj.SetMaterialOverwrite(Name, PropName)

        if ret == 0 :
            print(f'Frame {unique} change material {mat} successfully!!')
        else :
            print(f'Frame {unique} do NOT change material {mat} !!!!!!!!')

    def set_section(self, unique:str, sect:str) : # TEST OK
        Name = unique
        PropName = sect

        ret = self.obj.SetSection(Name, PropName)

        if ret == 0 :
            print(f'Frame {unique} change section {sect} successfully!!')
        else :
            print(f'Frame {unique} do NOT change section {sect} !!!!!!!!')

    def set_release(self, unique:str, 
                    P:bool = False, T:bool = False,
                    V2i:bool = False, V2j:bool = False,
                    V3i:bool = False, V3j:bool = False,
                    M2i:bool = False, M2j:bool = False,
                    M3i:bool = False, M3j:bool = False,
                    quick:str = None
                    ) : # TEST OK
        if quick :
            if quick == 'Mi' :
                M2i = True
                M3i = True
            elif quick == 'Mj' :
                M2j = True
                M3j = True
            elif quick == 'Mij' :
                M2i = True
                M3i = True
                M2j = True
                M3j = True

        ii = [P, V2i, V3i, T, M2i, M3i]
        jj = [False, V2j, V3j, False, M2j, M3j]
        StartValue = [0] * 6
        EndValue = [0] * 6

        ret = self.obj.SetReleases(unique, ii, jj, StartValue, EndValue)[-1]

        if ret == 0 :
            print(f'Frame {unique} set release successfully!!')
        else :
            print(f'Frame {unique} do NOT set release !!!!!!!!')
    
    def get_release(self, unique:str) : # TEST OK
        Name = unique
        II = [0] * 6
        JJ = [0] * 6
        StartValue = [0] * 6
        EndValue = [0] * 6

        return self.obj.GetReleases(Name, II, JJ, StartValue, EndValue)[0:2]
    
    def set_rigidzone(self,unique:str, RZ:float) : # OK
        AutoOffset, Length1, Length2  = self.get_offset(unique)
        Name = unique
        
        ret = self.obj.SetEndLengthOffset(Name, AutoOffset, Length1, Length2, RZ)[-1]
        if ret == 0 :
            print(f'Frame {unique} set rigidzone successfully!!')
        else :
            print(f'Frame {unique} do NOT set rigidzone !!!!!!!!')
    
    def get_offset(self, unique:str) : # OK
        Name = unique
        AutoOffset = False
        Length1 = 0.0
        Length2 = 0.0
        RZ = 0.0

        ret = self.obj.\
            GetEndLengthOffset(Name, AutoOffset, Length1, Length2, RZ)[0:3]
        
        return ret

    def get_rigidzone(self, unique:str) : # OK
        Name = unique
        AutoOffset = False
        Length1 = 0.0
        Length2 = 0.0
        RZ = 0.0

        ret = self.obj.\
            GetEndLengthOffset(Name, AutoOffset, Length1, Length2, RZ)[-2]
        
        return ret
    
    def set_modifier(self, unique:str, A:float = None,
                     V2:float = None, V3:float = None,
                     T:float = None,
                     M2:float = None, M3 :float = None,
                     M:float = None, W:float = None) : # OK
        
        Name = unique
        input = [A, V2,V3, T, M2, M3, M, W]

        Value = list(self.get_modifier(unique))

        for i in range(len(input)) :
            if input[i] is None :
                pass
            else :
                Value[i] = input[i]

        ret = self.obj.SetModifiers(Name, Value)[-1]

        if ret == 0 :
            print(f'Frame {unique} set modifiers successfully!!')
        else :
            print(f'Frame {unique} do NOT set modifiers !!!!!!!!')

    def get_modifier(self, unique:str) : # TEST OK
        Name = unique
        Value = []

        return self.obj.GetModifiers(Name, Value)[0]

    def get_section(self, unique:str) : # TEST OK
        Name = unique
        PropName = ''
        SAuto = ''
        return self.obj.GetSection(Name, PropName, SAuto)[0]
    
    def get_name_list(self, by_unique = True) :
        NumberNames = 0
        MyName = []
        ret = self.obj.GetNameList(NumberNames, MyName)
        # print(ret)
        print(f'Total Number of Frame = {ret[0]}')
        
        if by_unique :
            return ret[1]
        else :
            name_list = []

            for label in ret[1] :
                name_list.append(self.unique2label(label))
            return name_list
    
    def unique2label(self, unique:str) :
        Name = unique
        Label = ''
        Story = ''

        ret = self.obj.GetLabelFromName(Name, Label, Story)
        # print(ret)
        return ret[0:2]
    
    def label2unique(self, story:str, label:str) :
        Name = ''
        Label = label
        Story = story

        ret = self.obj.GetNameFromLabel(Label, Story, Name)
        # print(ret)
        return ret[0]

    def assign_load(self) :
        pass
        
class Areas(GeometryObj) :
    def __init__(self, etabs) :
        super().__init__(etabs)
        self.obj = self.sapModel.AreaObj
    
    #----- Geometry -----#
    def add(self, inputs:list, add_mode=0, sect_prop="Default", rotate=0) :
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

            unique, returnValue = self.obj.AddByCoord(NumberPoints, 
                                        	X, Y, Z, Name, PropName, UserName, CSys) # API
        elif add_mode == 1:
            Point = inputs
            unique, returnValue = self.obj.AddByPoint(NumberPoints, 
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
        self.obj.Delete(unique)
    
if __name__ == '__main__' :
    from yc_etabs_api.etabs import ETABS

    etabs = ETABS()

    #### TEST material
    # etabs.Frames.set_material("4040", "BEAM560") # OK

    #### TEST section
    # etabs.Frames.set_section('4040', 'SB2540CJ') # OK
    # print(etabs.Frames.get_section('4040')) # OK

    #### TEST release
    # etabs.Frames.set_release("4040", quick='Mij') # OK
    # print(etabs.Frames.get_release('4040')) # OK

    #### TEST modifier
    # etabs.Frames.set_modifier('4040', A = 0.002)
    # print(etabs.Frames.get_modifier('4040'))

    #### TEST rigidzone
    # print(etabs.Frames.get_rigidzone('3496'))
    # print(etabs.Frames.get_rigidzone('4040'))
    # print(etabs.Frames.get_offset('4040'))

    # print(etabs.Frames.get_name_list(by_unique=False))
    print(etabs.Frames.unique2label('3494'))
    print(etabs.Frames.label2unique('PRF', 'B96'))
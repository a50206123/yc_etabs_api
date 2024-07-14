import table as tb
from setting import *

class GeometryObj :
    def __init__(self, etabs, print_log) :
        sapModel = etabs.sapModel
        
        self.etabs = etabs
        self.sapModel = sapModel
        self.print_log = print_log

        self.Table = tb.Table(etabs, print_log)

    def add(self) :
        pass
    
    def modify(self) :
        pass

    def delete(self) :
        pass
    
class Points(GeometryObj) : ## NEED TO UPDATES
    def __init__(self, etabs, print_log) :
        super().__init__(etabs, print_log)
        self.obj = self.sapModel.PointObj

    #----- Geometry -----#
    def add(self, coor : list) : # OK
        # Input Info
        # x, y, z are global coordinates
        x, y, z = coor

        unique, ret = self.obj.AddCartesian(x, y, z)

        if ret == 0 :
            self.print_log(f'Point {unique}({x},{y},{z}) is added successfully.')
            return unique
        else :
            self.print_log(f'Point ({x},{y},{z}) is Not added successfully.')
            return None
    
    def delete(self, unique : str) :
        unique = str(unique)
        ret = self.obj.DeleteSpecialPoint(unique)
        # print(ret)

        if ret == 0 :
            self.print_log(f'Point {unique} is deleted successfully.')
        else :
            self.print_log(f'Point {unique} is Not deleted successfully.')
    
    def get_name_list(self, by_unique = True) :
        NumberNames = 0
        MyName = []
        ret = self.obj.GetNameList(NumberNames, MyName)
        # print(ret)
        self.print_log(f'Total Number of Points = {ret[0]}')
        
        if by_unique :
            return ret[1]
        else :
            name_list = []

            for label in ret[1] :
                name_list.append(self.unique2label(label))
            return name_list

    def assign_suppot(self, unique:str, UX = False, UY = False, UZ = False,
                   RX = False, RY = False, RZ = False, quick:str = None) :
        
        if quick == 'pin' :
            UX = True
            UY = True
            UZ = True
        elif quick == 'fix' :
            UX = True
            UY = True
            UZ = True
            RX = True
            RY = True
            RZ = True           
        elif quick == 'roller' :
            UZ = True
        elif quick == 'free' :
            pass

        Name = str(unique)
        Value = [UX, UY, UZ, RX, RY, RZ]
        
        ret = self.obj.SetRestraint(Name, Value, 0)
        # print(ret)
        if ret[-1] == 0 :
            self.print_log(f'Point {unique} set support successfully.')
            return unique
        else :
            self.print_log(f'Point {name} do Not set successfully.')
            return None

    def assign_spring(self, unique:str , spring_prop: str = '') :
        Name = str(unique)
        SpringProp = spring_prop
        ItemType = 0
        
        # returnValue = instance.SetSpringAssignment(Name, SpringProp, ItemType)
        ret = self.sapModel.PointObj.SetSpringAssignment(Name, SpringProp, ItemType)
        
        if ret == 0 :
            self.print_log(f'Point {unique} set spring successfully.')
            return ret
        else :
            self.print_log(f'Point {unique} do Not set spring successfully.')
            return None
        
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

    def assign_load(self) :
        pass

    def unique2label(self, unique:str) : # OK
        Name = str(unique)
        Label = ''
        Story = ''

        ret = self.obj.GetLabelFromName(Name, Label, Story)
        # print(ret)
        return ret[0:2]
    
    def label2unique(self, story:str, label:str) : # OK
        Name = ''
        Label = str(label)
        Story = story

        ret = self.obj.GetNameFromLabel(Label, Story, Name)
        # print(ret)
        return ret[0]
    
class Frames(GeometryObj) :
    def __init__(self, etabs, print_log):
        super().__init__(etabs, print_log)
        self.obj = self.sapModel.FrameObj
    
    #----- Geometry -----#
    def add(self, inputs:list, add_by_2points = True, sect_prop = None, rotate=0) :
        sapModel = self.sapModel

        Name = ''
        PropName = sect_prop
        UserName = ''
        CSys = 'Global'
        if not add_by_2points :
            XI, YI, ZI = inputs[0]
            XJ, YJ, ZJ = inputs[1]
            # returnValue = instance.AddByCoord(XI, YI, ZI, XJ, YJ, ZJ, Name, PropName, UserName, CSys)
            unique, _ = self.obj.AddByCoord(XI, YI,
                                    ZI, XJ, YJ, ZJ, Name, PropName, UserName, CSys) # API
        else :
            Point1, Point2 = inputs
            # returnValue = instance.AddByPoint(Point1, Point2, Name, PropName, UserName)
            unique, _ = self.obj.AddByPoint(Point1, 
	                                Point2, Name, PropName, UserName) # API

        if unique :
            self.print_log(f'Frame {unique} is added successfully.')
            return unique
        else :
            self.print_log('No Frame is added.')
            return None
    
    def delete(self, unique) :
        ret = self.obj.Delete(unique)

        return ret

    def set_selected(self, unique) :
        if type(unique) != list :
            unique = [unique]

        for uniq in unique :
            self.obj.SetSelected(str(uniq), True)
            self.print_log(f'Frame {uniq} is selected now')
    
    def assign_material(self, unique:str, mat:str) :
        Name = unique
        PropName = mat

        ret = self.obj.SetMaterialOverwrite(Name, PropName)

        if ret == 0 :
            self.print_log(f'Frame {unique} change material {mat} successfully!!')
        else :
            self.print_log(f'Frame {unique} do NOT change material {mat} !!!!!!!!')

    def assign_section(self, unique:str, sect:str) : # TEST OK
        Name = unique
        PropName = sect

        ret = self.obj.SetSection(Name, PropName)

        if ret == 0 :
            self.print_log(f'Frame {unique} changes section {sect} successfully!!')
        else :
            self.print_log(f'Frame {unique} does NOT change section {sect} !!!!!!!!')

    def assign_release(self, unique:str, 
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
            elif quick == 'P' :
                P = True
            

        ii = [P, V2i, V3i, T, M2i, M3i]
        jj = [False, V2j, V3j, False, M2j, M3j]
        StartValue = [0] * 6
        EndValue = [0] * 6

        ret = self.obj.SetReleases(unique, ii, jj, StartValue, EndValue)[-1]

        if ret == 0 :
            self.print_log(f'Frame {unique} set release successfully!!')
        else :
            self.print_log(f'Frame {unique} do NOT set release !!!!!!!!')
    
    def get_release(self, unique:str) : # TEST OK
        Name = unique
        II = [0] * 6
        JJ = [0] * 6
        StartValue = [0] * 6
        EndValue = [0] * 6

        return self.obj.GetReleases(Name, II, JJ, StartValue, EndValue)[0:2]
    
    def assign_rigidzone(self,unique:str, RZ:float) : # OK
        AutoOffset, Length1, Length2  = self.get_offset(unique)
        Name = unique

        AutoOffset = True
        
        ret = self.obj.SetEndLengthOffset(Name, AutoOffset, Length1, Length2, RZ)
        if ret == 0 :
            self.print_log(f'Frame {unique} sets rigidzone successfully!!')
        else :
            self.print_log(f'Frame {unique} does NOT set rigidzone !!!!!!!!')
    
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
    
    def assign_modifier(self, unique:str, A:float = None,
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
            self.print_log(f'Frame {unique} set modifiers successfully!!')
        else :
            self.print_log(f'Frame {unique} do NOT set modifiers !!!!!!!!')

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
        self.print_log(f'Total Number of Frame = {ret[0]}')
        
        if by_unique :
            return ret[1]
        else :
            name_list = []

            for label in ret[1] :
                name_list.append(self.unique2label(label))
            return name_list
    
    def assign_spring(self, unique:str, spring_prop: str, isSelected = False) :
        # returnValue = instance.SetSpringAssignment(Name, SpringProp, ItemType)

        if isSelected :
            ItemType = 2
        else :
            ItemType = 0

        ret = self.obj.SetSpringAssignment(str(unique), spring_prop, ItemType)
        print(ret)

        if ret : 
            self.print_log(f'Frame {unique} do not set spring!!')
        else : 
            self.print_log(f'Frame {unique} set spring successfully!!')

    def assign_local_axis(self, unique: str, ang: float, isSelected = False) :

        if isSelected :
            ItemType = 2
        else :
            ItemType = 0

        Name = str(unique)
        Ang = ang

        #returnValue = instance.SetLocalAxes(Name, Ang, ItemType)
        ret = self.obj.SetLocalAxes(Name, Ang, ItemType)

        if ret : 
            self.print_log(f'Frame {unique} do not set local axis!!')
        else : 
            self.print_log(f'Frame {unique} set local axis ({ang} deg) successfully!!')
        

    def assign_load(self, unique:str, load_pattern:str, loading:float, is_force:bool = True, dir = 'g', is_replace = False) :
        Name = unique
        LoadPat = load_pattern
        MyType = 1 if is_force else 2
        Dir = load_dir2num(dir)
        Dist1, Dist2 = (0, 1)
        Val1, Val2 = (loading, loading)
        Replace = is_replace
        ret = self.obj.SetLoadDistributed (Name, LoadPat, MyType, Dir, 
                            Dist1, Dist2, Val1, Val2, Replace = Replace)
        
        if ret == 0 :
            self.print_log(f'Frame {unique} assigns {load_pattern} = {loading:.3f} successfully!!')
        else :
            self.print_log(f'Frame {unique} does NOT assign load !!!!!!!!')


    def unique2label(self, unique:str) :
        Name = str(unique)
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
        
class Areas(GeometryObj) :
    def __init__(self, etabs, print_log) :
        super().__init__(etabs, print_log)
        self.obj = self.sapModel.AreaObj
    
    #----- Geometry -----#
    def add(self, inputs:list, add_mode=0, sect_prop= None, rotate=0) :
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
            self.print_log(f'Area {unique} added successfully.')
            return unique
        else :
            self.print_log('No Area Added.')
            return None
    
    def delete(self, unique) :
        self.obj.Delete(unique)

    def assign_section(self, unique:str, section:str) :
        pass

    def assign_modifier(self, unique:str, modifier:str) :
        pass

    def assign_local_axis(self, unique:str, axis:str) :
        pass

    def assign_diaphragm(self, unique:str, diaphragm:str) :
        pass

    def assign_uniform_load(self, unique:str, load_pattern:str, loading:float) :
        pass

    def assign_load_set(self, unique:str, load_set:str) :
        pass

    def assign_automesh(self, unique:str) :
        pass

    def assign_spring(self, unique:str , stiff:list, is_replaced:bool=True) :
        pass

class Strips(GeometryObj) :
    def __init__(self, etabs, print_log) :
        super().__init__(etabs, print_log)
        # self.obj = self.sapModel.StripObj

    def add(self) :
        pass

    def assign_material(self) :
        pass

    
    
if __name__ == '__main__' :
    from yc_etabs_api.etabs import ETABS

    etabs = ETABS()

    #### TEST Points ####
    # uniq = etabs.Points.add([1,1,52.1]) # OK
    # etabs.Points.delete('728') # OK
    # print(etabs.Points.unique2label(1670)) # OK
    # print(etabs.Points.label2unique('PRF', 81)) # OK
    # print(etabs.Points.get_name_list(by_unique=False)) # OK
    # etabs.Points.assign_suppot(2643, quick='free') # OK   
    # print(etabs.Points.assign_spring('2643', spring_prop = 'KVFS')) # OK
    

    #### TEST Frames ####
    # etabs.Frames.add(inputs = ['2643', '24'], add_by_2points = True, sect_prop="BEAM210", rotate=0) # OK
    # etabs.Frames.add(inputs = [[3.2, 62.6, 40.35], [32.2, 64.6, 40.35]], add_by_2points = False, sect_prop="BEAM210", rotate=0) # OK
    # etabs.Frames.delete('32') # OK
    # etabs.Frames.set_selected([1781, 1782, 1783, 1784]) # OK
    # etabs.Frames.assign_material('1783', 'BEAM210') # OK
    # etabs.Frames.assign_section(unique = '1783', sect = 'C5090CJ') # OK
    # etabs.Frames.assign_release(unique = '1783', M2i = True) # OK
    # etabs.Frames.assign_spring('1783', spring_prop = 'KV15000') # OK
    # etabs.Frames.assign_local_axis('1783', ang = 0) # OK
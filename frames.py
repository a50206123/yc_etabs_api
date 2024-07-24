from geometry import GeometryObj
# import yc_print as print_log

class Frames(GeometryObj) :
    def __init__(self, etabs, print_log, msg_signal):
        super().__init__(etabs, print_log, msg_signal)
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
            self.print_log(f'Frame {uniq} is selected now', self.msg_signal)
    
    def assign_material(self, unique:str, mat:str) :
        Name = unique
        PropName = mat

        ret = self.obj.SetMaterialOverwrite(Name, PropName)

        if ret == 0 :
            self.print_log(f'Frame {unique} change material {mat} successfully!!', self.msg_signal)
        else :
            self.print_log(f'Frame {unique} do NOT change material {mat} !!!!!!!!', self.msg_signal)

    def assign_section(self, unique:str, sect:str) : # TEST OK
        Name = unique
        PropName = sect

        ret = self.obj.SetSection(Name, PropName)

        if ret == 0 :
            self.print_log(f'Frame {unique} changes section {sect} successfully!!', self.msg_signal)
        else :
            self.print_log(f'Frame {unique} does NOT change section {sect} !!!!!!!!', self.msg_signal)

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
            self.print_log(f'Frame {unique} set release successfully!!', self.msg_signal)
        else :
            self.print_log(f'Frame {unique} do NOT set release !!!!!!!!', self.msg_signal)
    
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
            self.print_log(f'Frame {unique} sets rigidzone successfully!!', self.msg_signal)
        else :
            self.print_log(f'Frame {unique} does NOT set rigidzone !!!!!!!!', self.msg_signal)
    
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
            self.print_log(f'Frame {unique} set modifiers successfully!!', self.msg_signal)
        else :
            self.print_log(f'Frame {unique} do NOT set modifiers !!!!!!!!', self.msg_signal)

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
        self.print_log(f'Total Number of Frame = {ret[0]}', self.msg_signal)
        
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
            self.print_log(f'Frame {unique} do not set spring!!', self.msg_signal, self.msg_signal)
        else : 
            self.print_log(f'Frame {unique} set spring successfully!!', self.msg_signal, self.msg_signal)

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
            self.print_log(f'Frame {unique} do not set local axis!!', self.msg_signal)
        else : 
            self.print_log(f'Frame {unique} set local axis ({ang} deg) successfully!!', self.msg_signal)
        

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
            self.print_log(f'Frame {unique} assigns {load_pattern} = {loading:.3f} successfully!!', self.msg_signal)
        else :
            self.print_log(f'Frame {unique} does NOT assign load !!!!!!!!', self.msg_signal)


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
    
if __name__ == '__main__' :
    from yc_etabs_api.etabs import ETABS
    etabs = ETABS()

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
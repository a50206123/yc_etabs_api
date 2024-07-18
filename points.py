from geometry import GeometryObj
import yc_print as print_log

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
            print_log(f'Point {unique}({x},{y},{z}) is added successfully.', self.msg_signal)
            return unique
        else :
            print_log(f'Point ({x},{y},{z}) is Not added successfully.', self.msg_signal)
            return None
    
    def delete(self, unique : str) :
        unique = str(unique)
        ret = self.obj.DeleteSpecialPoint(unique)
        # print(ret)

        if ret == 0 :
            print_log(f'Point {unique} is deleted successfully.', self.msg_signal)
        else :
            print_log(f'Point {unique} is Not deleted successfully.', self.msg_signal)
    
    def get_name_list(self, by_unique = True) :
        NumberNames = 0
        MyName = []
        ret = self.obj.GetNameList(NumberNames, MyName)
        # print(ret)
        print_log(f'Total Number of Points = {ret[0]}', self.msg_signal)
        
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
            print_log(f'Point {unique} set support successfully.', self.msg_signal)
            return unique
        else :
            print_log(f'Point {name} do Not set successfully.', self.msg_signal)
            return None

    def assign_spring(self, unique:str , spring_prop: str = '') :
        Name = str(unique)
        SpringProp = spring_prop
        ItemType = 0
        
        # returnValue = instance.SetSpringAssignment(Name, SpringProp, ItemType)
        ret = self.sapModel.PointObj.SetSpringAssignment(Name, SpringProp, ItemType)
        
        if ret == 0 :
            print_log(f'Point {unique} set spring successfully.', self.msg_signal)
            return ret
        else :
            print_log(f'Point {unique} do Not set spring successfully.', self.msg_signal)
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
 
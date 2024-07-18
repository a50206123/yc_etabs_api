from geometry import GeometryObj
import yc_print as print_log

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
            Point = input
            unique, returnValue = self.obj.AddByPoint(NumberPoints, 
                                        	Point, Name, PropName, UserName) # API
        else :
            returnValue = 1
        
        if returnValue == 0 :
            print_log(f'Area {unique} added successfully.', self.msg_signal)
            return unique
        else :
            print_log('No Area Added.', self.msg_signal)
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
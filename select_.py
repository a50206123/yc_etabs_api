# from etabs import ETABS

class Select() :
    def __init__(self, etabs, print_log, msg_signal) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel
        self.obj = self.sapModel.SelectObj

        self.print_log = print_log
        self.msg_signal = msg_signal
    
    def all(self, deselect = False) :
        ret = self.obj.All(deselect)
        # print(ret)

    def clear(self) :
        ret = self.obj.ClearSelection()

    def object_type(self, type_) :
        pass

    def by_group(self, name:str, deselect = False) :
        Name = name
        Deselect = deselect

        ret = self.obj.Group(Name, Deselect)
        # print(ret)

        if ret == 0 :
            if deselect :
                self.print_log(f'Object in group {name} is deselected', self.msg_signal)
            else :
                self.print_log(f'Object in group {name} is selected', self.msg_signal)

    def get(self, type_ = 'Frame') :
        NumberItems = 0
        ObjectType = []
        ObjectName = []

        NumberItems, ObjectType, ObjectName, ret = self.obj.GetSelected(
            NumberItems, ObjectType, ObjectName)

        name2type = {
            'Point' : 1,
            'Frame' : 2,
            'Area' : 5
        }

        results = []

        for i in range(NumberItems) :
            if ObjectType[i] == name2type[type_] :
                results.append(ObjectName[i])
        
        return results

if __name__ == '__main__' :
    from yc_etabs_api.etabs import ETABS

    etabs = ETABS()

    # print(etabs.Select.get())
    # etabs.Select.by_group("A")
    # print(etabs.Select.get_all())
    etabs.Select.clear()
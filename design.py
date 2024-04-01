from geometry import Frames

class Design :
    def __init__(self, etabs) -> None:
        self.ConcFrame = ConcFrame(etabs)
        self.ConcSlab = None
        self.Steel = None    


class ConcFrame :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.SapModel
        self.obj = etabs.sapModel.DesignConcrete
        self.Frame = Frames(self.etabs)

    def set_code(self, code = 'ACI318-14') :
        if code == 'ACI318-14' :
            code_name = 'ACI 318-14'
        elif code == 'ACI318-08' :
            code_name = 'ACI 318-08'

        ret = self.obj.SetCode(code_name)

        self.set_design_by_last_step()
    
    def get_code(self) :
        CodeName = ''
        ret = self.obj.GetCode(CodeName)
        # print(ret)
        return ret[0]
    
    def set_design_by_last_step(self) :
        code = self.get_code()

        if '318-14' in code :
            ret = self.obj.ACI318_14.SetPreference(18, 3)
        elif '318-08' in code :
            ret = self.obj.ACI318_08_IBC2009.SetPreference(13, 3)

    def set_overwrite(self, name:str, item:int, value:int, quick:str = None) :
        code = self.get_code()

        Name = name
        if quick is None :
            Item = item
            Value = value 
        elif quick == 'sway' :
            Item = 1
            Value = 1
        elif quick == 'nonsway' :
            Item = 1
            Value = 4
        elif quick == '0.6LL' :
            Item = 2
            Value = 0.6
        elif quick == '0.8LL' :
            Item = 2
            Value = 0.8

        if '318-14' in code :
            ret = self.obj.ACI318_14.SetOverwrite(Name, Item, Value)
        elif '318-08' in code :
            ret = self.obj.ACI318_08_IBC2009.SetOverwrite(Name, Item, Value)
        
        label, story = self.Frame.unique2label(name)
        if ret == 0 :
            print(f'Frame {name} ({story} {label}) sets overwrite successfully ({quick})')
        else :
            print(f'Frame {name} ({story} {label}) does not set overwrite successfully ')

    def get_overwrite(self, name:str, item:int, quick:str = None) :
        code = self.get_code()

        Name = name
        Value = ''
        if quick is None :
            Item = item

        elif quick == 'frame type' :
            Item = 1
             
        elif quick == 'live reduction' :
            Item = 2

        if '318-14' in code :
            ret = self.obj.ACI318_14.GetOverwrite(Name, Item)
        elif '318-08' in code :
            ret = self.obj.ACI318_08_IBC2009.GetOverwrite(Name, Item)

        # print(ret)

        val = ret[0]

        if Item == 1 :
            if val == 1 :
                return 'sway'
            elif val == 4 :
                return 'nonsway'


if __name__ == "__main__" :
    from yc_etabs_api.etabs import ETABS

    etabs = ETABS()

    # etabs.Design.ConcFrame.set_code('ACI318-14')
    # print(etabs.Design.ConcFrame.get_code())

    etabs.Design.ConcFrame.get_overwrite('4040', 0, quick='frame type')

    
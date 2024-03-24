class Design :
    def __init__(self, etabs) -> None:
        self.ConcFrame = ConcFrame(etabs)

class ConcFrame :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.SapModel
        self.obj = etabs.sapModel.DesignConcrete

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

if __name__ == "__main__" :
    from yc_etabs_api.etabs import ETABS

    etabs = ETABS()

    etabs.Design.ConcFrame.set_code('ACI318-14')
    print(etabs.Design.ConcFrame.get_code())
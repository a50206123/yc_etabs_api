class LoadComb :
    def __init__(self, etabs) :
        self.etabs = etabs
        self.sapModel = etabs.SapModel
        self.obj = self.sapModel.RespCombo

    def add(self, name:str, type_ = 'add') :
        if name in self.get_all_comb() :
            print(f'LoadComb {name} exists already !!')
            return None

        if type_ == 'add' :
            ComboType = 0
        elif type_ == 'envelope' :
            ComboType = 1

        ret = self.obj.Add(name, ComboType)
        # print(ret)

        if ret == 0 :
            print(f'LoadComb {name} is added successfully!!')
        else :
            print(f'LoadComb {name} is NOT added successfully!!')

    
    def get_all_comb(self) :
        NumberNames = 0
        MyName = ''
        ret = self.obj.GetNameList(NumberNames, MyName)
        # print(ret)
        return ret [1]

    def set_case_factor(self, name:str, case_name:str, factor:float, is_load_comb = False) :
        Name = name
        if is_load_comb :
            CNameType = 1
        else :
            CNameType = 0

        CName = case_name
        SF = factor

        ret = self.obj.SetCaseList(Name, CNameType, CName, SF)
        # print(ret)
        if ret[-1] == 0 :
            print(f'LoadComb {name} set {case_name} factor to {factor:.3f} successfully!!')
        else :
            print(f'LoadComb {name} do NOT set factor successfully !!!!!!!!')

if __name__ == '__main__' :
    from yc_etabs_api.etabs import ETABS
    etabs = ETABS()

    # etabs.LoadComb.add("TEST000")
    # etabs.LoadComb.set_case_factor('COMB000', 'DEAD', 1.6)
    # etabs.LoadComb.get_all_comb()
    # etabs.LoadComb.set_case_factor('SPEQX1', 'SPECPX1', 1.248)
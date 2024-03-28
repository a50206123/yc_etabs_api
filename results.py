class Results :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.SapModel
        self.obj = self.sapModel.Results
    
    def set_output_case_combo(self, cases:list = ["DEAD", "LIVE"], combos:list = [], is_replace:bool = True) :
        # Deselect all cases and combinations
        if is_replace :
            self.obj.Setup.DeselectAllCasesAndCombosForOutput()

        for case in cases :
            self.obj.Setup.SetCaseSelectedForOutput(case)
        for combo in combos :
            self.obj.Setup.SetComboSelectedForOutput(combo)



    def get_frame_force(self, name:str = '', type_:int = 3) :
        """
        type_ = 0 : ObjectElm  -> name is object element name
                1 : Element -> name is element name
                2 : GroupElm -> name is group name
                3 : SelectionElm -> name will be ignored
        """

        Name = name
        ItemTypeElm = type_
        NumberResults = 0
        Obj = []
        ObjSta = []
        Elm = []
        ElmSta = []
        LoadCase = []
        StepType = []
        StepNum = []
        P = []; V2 = []; V3 = [] 
        T = []; M2 = []; M3 = []

        ret = self.obj.FrameForce(Name, ItemTypeElm, NumberResults, Obj, ObjSta, Elm, ElmSta, 
                   LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3)
        
        # for i in ret :
        #     print(i)

        ele = []
        results = {}

        elements = ret[1]
        stations = ret[2]
        elements_meshed = ret[3]
        load_cases = ret[5]
        step_type = ret[6]
        steps = ret[7]
        P, V2, V3, T, M2, M3 = ret[8:14]
        
        for i in range(ret[0]) :
            force = {
                'P' : P[i],
                'V2' : V2[i], 
                'V3' : V3[i], 
                'T' : T[i], 
                'M2' : M2[i], 
                'M3' : M3[i]
            }

            load_case = load_cases[i]
            element = elements[i]

            if i == 0 :
                temp = {}
                temp[load_case] = {}
                temp[load_case][f'{stations[i] : .3f}'] = force

                ele.append(element)
                continue

            elif i == ret[0] - 1 :
                results[element] = temp
                continue
            
            if element in ele and load_case is load_cases[i-1]:
                temp[load_case][f'{stations[i] : .3f}'] = force
            elif elements in ele and load_case is not load_case[i-1] :
                temp[load_case] = {}
                temp[load_case][f'{stations[i] : .3f}'] = force
            else :
                results[element] = temp
                temp[load_case] = {}
                temp[load_case][f'{stations[i] : .3f}'] = force

                ele.append(element)
        
        return results

    def get_modal_mass_ratio(self, is_shear_building = True, max_ratio = 1, max_mode:int = 0) :
        NumberResults = 0
        LoadCase = []
        StepType = []; StepNum = []; Period = []
        UX = []; UY = []; UZ = []; SumUX = []; SumUY = []; SumUZ = [] 
        RX = []; RY = []; RZ = []; SumRX = []; SumRY = []; SumRZ = []

        ret = self.obj.ModalParticipatingMassRatios(NumberResults, LoadCase, StepType, StepNum, Period, 
                                              UX, UY, UZ, SumUX, SumUY, SumUZ, 
                                              RX, RY, RZ, SumRX, SumRY, SumRZ)
        # print(ret)
        NumberResults, LoadCase, StepType, StepNum, Period, UX, UY, UZ, SumUX, SumUY, SumUZ, \
            RX, RY, RZ, SumRX, SumRY, SumRZ, ret_val  = ret
        results = []

        if is_shear_building :
            for i in range(NumberResults) :
                results.append([i+1, Period[i], UX[i], UY[i], RZ[i], SumUX[i], SumUY[i], SumRZ[i]])

                if min(SumUX[i], SumUY[i], SumRZ[i]) > max_ratio :
                    break
                if max_mode > 0:
                    if i+1 == max_mode :
                        break
        else :
            for i in range(NumberResults) :
                results.append([i+1, Period[i], UX[i], UY[i], UZ[i], RX[i], RY[i], RZ[i], 
                                SumUX[i], SumUY[i], SumUZ[i], SumRX[i], SumRY[i], SumRZ[i]])
                if min(SumUX[i], SumUY[i], SumUZ[i], SumRX[i], SumRY[i], SumRZ[i]) > max_ratio :
                    break
                if max_mode > 0:
                    if i+1 == max_mode :
                        break

        return results

if __name__ == '__main__' :
    from yc_etabs_api.etabs import ETABS
    etabs = ETABS()

    etabs.Results.set_output_case_combo()

    # print(etabs.Results.get_frame_force(name = '', type_ = 3))

    # print(etabs.Results.get_modal_mass_ratio(is_shear_building=True, max_mode=0))
    # print(etabs.Results.get_modal_mass_ratio(is_shear_building=False, max_mode=5))
    print(etabs.Results.get_modal_mass_ratio(is_shear_building=True, max_ratio = .5, max_mode=5))
    
    pass
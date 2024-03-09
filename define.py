from yc_etabs_api import ETABS
import api_setting_numbers as nums

class Define() :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel

        self.FrameSect = None
        self.AreaSect = None
        self.Diaph = None
        self.PointSpring = None
        self.LineSpring = None
        self.AreaSpring = None

        self.LoadPattern = None
        self.LoadComb = None

        self.MassSource = None

    class Material() :
        def __init__(self, etabs) -> None:
            self.etabs = etabs
            self.sapModel = etabs.sapModel
        
        def add(self, name:str, type_:str) :
            type_int = nums.mtype2num[type_]
            sapModel = self.sapModel

            sapModel.PropMaterial.SetMaterial(name, type_int)

    class LoadCase() :
        def __init__(self, etabs) -> None:
            self.etabs = etabs
            self.sapModel = etabs.sapModel

            self.cases = etabs.sapModel.LoadCases.GetNameList(0, [])[1]
        
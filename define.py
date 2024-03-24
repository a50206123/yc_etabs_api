# from etabs import ETABS
import api_setting_numbers as nums
import math

class Define() :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel

        self.Material = Material(etabs)
        self.FrameSect = FrameSect(etabs)
        self.AreaSect = None
        self.Diaph = None
        self.PointSpring = None
        self.LineSpring = None
        self.AreaSpring = None

        self.LoadPattern = None
        self.LoadComb = None

        self.MassSource = None

    class LoadCase() :
        def __init__(self, etabs) -> None:
            self.etabs = etabs
            self.sapModel = etabs.sapModel

            self.cases = etabs.sapModel.LoadCases.GetNameList(0, [])[1]

class Material() :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel
        self.obj = self.sapModel.PropMaterial
    
    def add(self, name:str, type_:str) :
        if self.get(name) == 0 :
            print(f'Material {name} exists !!!!!!!!')
            return None
        
        MatType = nums.mtype2num(type_)
        Name = ''
        Region = ''
        Standard = ''
        Grade = ''
        UserName = name

        ret = self.obj.AddMaterial(Name, MatType, Region, 
                                                Standard, Grade, UserName)
        # print(ret)
        if ret[-1] == 0 :
            print(f'Material {name} is added successfully!!')
        else :
            print(f'Material {name} is NOT added !!!!!!!!')
    
    def get(self, name:str) : # OK
        Name = name
        MatType = 0
        Color = 0
        Notes = ''
        GUID = ''

        ret = self.obj.GetMaterial(Name, MatType, Color,
                                                     Notes, GUID)
        # print(ret
        
        return ret[-1]

    def set_conc_para(self, name, fc, conc_code = '113') :
        if self.get(name) != 0 :
            self.add(name, nums.mtype2num('concrete'))

        Name = name
        Fc = fc
        IsLightweight = False
        FcsFactor = 0
        SSType = 1
        SSHysType = 4
        StrainAtFc = 0.00221914
        StrainUltimate = 0.005

        ret = self.obj.SetOConcrete(Name, Fc*10, IsLightweight, FcsFactor, SSType, 
                                                SSHysType, StrainAtFc, StrainUltimate)
        if ret == 0 :
            print(f'Material {name} set fc\' = {fc} kgf/cm2 successfully!!')
        else :
            print(f'Material {name} do NOT set fc\' !!!!!!!!')

        if conc_code == '113' :
            Es = 12000
        else :
            Es = 15000

        E = round(Es*math.sqrt(fc)/100)*1000
        U = 0.17
        A = 0.0
        ret = self.obj.SetMPIsotropic(Name, E, U, A)
        # print(ret)
        if ret == 0 :
            print(f'Material {name} set E = {E} tf/m2 successfully!!')
        else :
            print(f'Material {name} do NOT set Young\'s modulus !!!!!!!!')
        
        W = 2.4
        MyOption = 1
        Value = W
        ret = self.obj.SetWeightAndMass(Name, MyOption,
                                                          Value)
        # print(ret)
        if ret == 0 :
            print(f'Material {name} set W = {W} tf/m3 successfully!!')
        else :
            print(f'Material {name} do NOT set Unit Weight !!!!!!!!')

class FrameSect :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel
        self.obj = self.sapModel.PropFrame

    def add(self, name:str, shape:str, geometry:dict, mat:str) :
        ####
        # shape = rect --> geometry = [H, B]
        ####
        if shape == 'rect' :
            if self.get(name, shape)['ret'] == 0 :
                isExist = True
                add_modify = 'modified'
            else :
                isExist = False
                add_modify = 'added'

            Name = name
            MatProp = mat
            T3, T2 = geometry
            ret = self.obj.SetRectangle(Name, MatProp, T3, T2)
            # print(ret)

            if ret == 0 :
                print(f'FrameSection {name} is {add_modify} successfully!!')
            else :
                print(f'FrameSection {name} is NOT {add_modify} !!!!!!!!')

    def get(self, name:str, shape:str) :
        if shape == 'rect' :
            Name = name
            FileName = ''
            MatProp = ''
            T3 = 0.0
            T2 = 0.0
            Color = 0
            Notes = ''
            GUID = ''
            ret = self.obj.GetRectangle(Name, FileName, MatProp, 
                                                       T3, T2, Color, Notes, GUID)
            # print(ret)
            return {
                'mat' : ret[1],
                'geometry' : ret[2:4],
                'ret' : ret[-1]
            }
        
    def set_beam_para(self, name:str, mat_rebar:str, mat_stir:str,
                       cover:list, As_top_i:float = 0, As_bot_i:float = 0, 
                       As_top_j:float = 0, As_bot_j:float = 0) :
        Name = name
        MatPropLong = mat_rebar
        MatPropConfine = mat_stir
        CoverTop, CoverBot = cover
        TopLeftArea, TopRightArea = As_top_i, As_top_j        
        BotLeftArea, BotRightArea = As_bot_i, As_bot_j

        ret = self.obj.SetRebarBeam(
            Name, MatPropLong, MatPropConfine, CoverTop, CoverBot, TopLeftArea, 
            TopRightArea, BotLeftArea, BotRightArea
        )
        # print(ret)
        if ret == 0 :
            print(f'FrameSection {name} set parameters of concrete beam successfully!!')
        else :
            print(f'FrameSection {name} do NOT set parameters of concrete beam !!!!!!!!')

    def set_col_para(self, name:str, mat_rebar:str, mat_stir:str, cover:float, shape = 'rect', 
                     confine_type = 'tie', rebar = [3, 3], rebar_size = '#10', tie_size = '#4',
                     num_tie = [2, 2], is_check = False) :
        Name = name
        MatPropLong = mat_rebar
        MatPropConfine = mat_stir

        if shape == 'rect' :
            Pattern = 1
        elif shape == 'circ' :
            Pattern = 2
        if confine_type == 'tie' :
            ConfineType = 1 # Tie
        else :
            ConfineType = 2 
        
        Cover = cover

        NumberCBars = 0

        NumberR3Bars, NumberR2Bars = rebar
        RebarSize = rebar_size
        TieSize = tie_size
        TieSpacingLongit = .15 # m
        Number2DirTieBars, Number3DirTieBars = num_tie
        ToBeDesigned = not is_check

        ret = self.obj.SetRebarColumn(Name, MatPropLong, MatPropConfine, 
                                                     Pattern, ConfineType, Cover, NumberCBars, 
                                                     NumberR3Bars, NumberR2Bars, RebarSize, TieSize, 
                                                     TieSpacingLongit, Number2DirTieBars, Number3DirTieBars, 
                                                     ToBeDesigned)
        # print(ret)
        if ret == 0 :
            print(f'FrameSection {name} set parameters of concrete column successfully!!')
        else :
            print(f'FrameSection {name} do NOT set parameters of concrete column !!!!!!!!')

if __name__ == '__main__' :
    from yc_etabs_api.etabs import ETABS

    etabs = ETABS()

    # print(etabs.Define.Material.get_material('123'))
    # etabs.Define.Material.add('test1', 'concrete')
    # etabs.Define.Material.set_conc_para('test1', 280, conc_code= '113')
    
    # etabs.Define.FrameSect.get('TestBeam', 'rect')
    # etabs.Define.FrameSect.get('TestBeam111', 'rect')
    etabs.Define.FrameSect.add('TestBeam', 'rect', [.70,.40], 'BEAM245')
    etabs.Define.FrameSect.add('TestCol', 'rect', [1.00,1.10], 'COL280')
    etabs.Define.FrameSect.set_beam_para('TestBeam', 'SD490', 'SD420', [.08,.08])
    etabs.Define.FrameSect.set_col_para('TestCol', 'SD490', 'SD420', .04)
    pass
from yc_etabs_api import ETABS

class Analyze() :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel

    def run(self) :
        self.sapModel.analyze.RunAnalysis()

    def set_case_to_run(self, load_cases:list =[]):
        ## load_cases = [] --> All case to run
        all_load_case = self.SapModel.Analyze.GetCaseStatus()[1]
        for lc in all_load_case:
            if not load_cases and not lc in load_cases:
                if lc in all_load_case:
                    self.SapModel.Analyze.SetRunCaseFlag(lc, False)
            else:
                self.SapModel.Analyze.SetRunCaseFlag(lc, True) 
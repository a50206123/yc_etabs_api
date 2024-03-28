
class Analyze() :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel
        self.obj = self.sapModel.Analyze

    def run(self) :
        print(f'{" Analysis STARTS ":-^30}')

        ret = self.obj.analyze.RunAnalysis()

        if ret == 0 :
            log = "Analysis is finished."
        else :
            log = "Analysis is NOT finished"
        
        print(f'{" " + log + " ":-^30}')
        # print(ret)

    def set_case_to_run(self, load_cases:list =[], is_replace = True):
        ## load_cases = [] --> All case to run
        NumberItems, CaseName, Run, ret = self.obj.GetRunCaseFlag()
        
        if load_cases == [] :
            load_cases = CaseName
        
        for i in range(NumberItems) :
            case = CaseName [i]
            run = Run[i]

            if case in load_cases :
                isRun = True
            else :
                if is_replace :
                    isRun = False
                else :
                    isRun = run

            ret = self.obj.SetRunCaseFlag(case, isRun)


if __name__ == '__main__' :
    from yc_etabs_api.etabs import ETABS

    etabs = ETABS()

    # etabs.Analyze.run()
    etabs.Analyze.set_case_to_run(['DEAD'], is_replace=False)
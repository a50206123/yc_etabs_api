class File :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel
    
    def openEDB(self, filename = 'TEST EDB\\TEST_API.EDB') :
        return self.sapModel.File.OpenFile(filename)

    def save(self, filename = None) :
        if filename :
            return self.sapModel.File.Save(filename)        
        else :
            return self.sapModel.File.Save()
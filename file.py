class File :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel
        self.obj = self.sapModel.File
    
    def openEDB(self, filename = 'TEST EDB\\TEST_API.EDB') :
        return self.obj.OpenFile(filename)

    def save(self, filename = None) :
        if filename :
            return self.obj.Save(filename)        
        else :
            return self.obj.File.Save()
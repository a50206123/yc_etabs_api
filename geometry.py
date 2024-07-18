import table as tb
from setting import *

class GeometryObj :
    def __init__(self, etabs) :
        sapModel = etabs.sapModel
        
        self.etabs = etabs
        self.sapModel = sapModel

        self.Table = tb.Table(etabs)

    def add(self) :
        pass
    
    def modify(self) :
        pass

    def delete(self) :
        pass

   
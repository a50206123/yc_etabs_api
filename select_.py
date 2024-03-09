from yc_etabs_api import ETABS

class Select() :
    def __init__(self, etabs) -> None:
        self.etabs = etabs
        self.sapModel = etabs.sapModel

    def object_type(self, type_) :
        pass

    def group(self, name) :
        pass
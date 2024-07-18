from geometry import GeometryObj

class Strips(GeometryObj) :
    def __init__(self, etabs, print_log) :
        super().__init__(etabs, print_log)
        # self.obj = self.sapModel.StripObj

    def add(self) :
        pass

    def assign_material(self) :
        pass
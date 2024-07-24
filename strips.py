from geometry import GeometryObj
import yc_print as print_log

class Strips(GeometryObj) :
    def __init__(self, etabs, print_log, msg_signal) :
        super().__init__(etabs, print_log, msg_signal)
        # self.obj = self.sapModel.StripObj

    def add(self) :
        pass

    def assign_material(self) :
        pass
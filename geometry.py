import table as tb
from setting import *

class GeometryObj :
    def __init__(self, etabs, print_log, msg_signal) :
        sapModel = etabs.sapModel
        
        self.etabs = etabs
        self.sapModel = sapModel

        self.print_log = print_log
        self.msg_signal = msg_signal

        self.Table = tb.Table(etabs, print_log, self.msg_signal)

    def add(self) :
        pass
    
    def modify(self) :
        pass

    def delete(self) :
        pass

   
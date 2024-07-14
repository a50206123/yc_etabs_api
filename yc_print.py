#### Import PyQt5
from PyQt5.QtCore import QObject, pyqtSignal
# Create a Signal
class MsgSignal(QObject):
    new_msg = pyqtSignal(str)

# For Printing Log to Console and Singal
def print_log(msg, add_mod = False):
    if add_mod :
        msg = f'- {msg:10s} modulus is loaded'

    msg_signal.new_msg.emit(msg) # Emit the signal to "new_msg"
    print(msg) # Print the "msg" to the console



msg_signal = MsgSignal()
from PyQt6.QtCore import QThread, pyqtSignal

class MATLABWorkerThread(QThread):

    eq_finished = pyqtSignal() # Signal to communicate with main UI

    def __init__(self, matlab_eng, input, gain_values, output):
        super().__init__()
        self.eng = matlab_eng
        self.input_name = input
        self.gains = gain_values
        self.output_name = output

    def run(self): # Function to run the EQ.m
        self.eng.EQ(self.input_name, self.gains, self.output_name, nargout=0)

        self.eq_finished.emit()

import matlab.engine
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, 
                             QPushButton, QVBoxLayout, QLineEdit, 
                             QGridLayout, QHBoxLayout, QSlider)

eng = matlab.engine.start_matlab() # Start MATLAB engine

# APP UI
class EQApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EQ")
        self.resize(400, 800)
        self.setMinimumSize(200, 200)

        self.mainLayout = QVBoxLayout() # Main Layout for the app
        self.sliderLayout = QHBoxLayout() # Layout for the sliders
        self.buttonLayout = QHBoxLayout() # Layout for the buttons

        self.sliderList = [] # Create list to hold sliders
        for i in range(7):
            slider = QSlider()
            slider.setSingleStep(1)
            slider.setTickInterval(1)
            slider.setMinimum(-20)
            slider.setMaximum(10)
            slider.setFixedHeight(200)
            self.sliderList.append(slider)
            self.sliderLayout.addWidget(slider)

        eqButton = QPushButton("Start EQ") # Create EQ Button 
        eqButton.setFixedSize(100, 50)
        self.buttonLayout.addWidget(eqButton)

        self.mainLayout.addLayout(self.sliderLayout, 0)
        self.mainLayout.addLayout(self.buttonLayout, 1)

        self.setLayout(self.mainLayout) # Use Main Layout for current window

        eqButton.clicked.connect(self.startEQ)


    def startEQ(self): # Function to start EQ process
        print("Start EQ button was clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQApp()
    window.show()
    sys.exit(app.exec())
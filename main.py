import matlab.engine
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, 
                             QPushButton, QVBoxLayout, QLineEdit, 
                             QGridLayout, QHBoxLayout, QSlider)

# APP UI
class EQApp(QWidget):
    def __init__(self):
        self.eng = matlab.engine.start_matlab() # Start MATLAB engine
        self.eng.addpath(r"C:\Users\jolea\OneDrive\Documents\MATLAB", nargout=0) # Add path to MATLAB functions
        super().__init__()
        self.setWindowTitle("EQ")
        self.resize(1000, 1000)
        self.setMinimumSize(200, 200)

        self.mainLayout = QVBoxLayout() # Main Layout for the app
        self.sliderLayout = QHBoxLayout() # Layout for the sliders
        self.labelLayout = QHBoxLayout() # Layout for the labels
        self.sliderLabelLayout = QVBoxLayout() # Layout for slider labels
        self.buttonLayout = QHBoxLayout() # Layout for the buttons

        self.sliderList = [] # Create list to hold sliders
        for i in range(7):
            slider = QSlider()
            slider.setSingleStep(1)
            slider.setTickInterval(1)
            slider.setMinimum(-20)
            slider.setMaximum(10)
            slider.setFixedHeight(150)
            slider.valueChanged.connect(self.sliderValues) # Connect slider to function
            self.sliderList.append(slider)
            self.sliderLayout.addWidget(slider)
        toneDownSlider = QSlider() # Create Tone Down Slider
        toneDownSlider.setSingleStep(1)
        toneDownSlider.setTickInterval(1)
        toneDownSlider.setMinimum(-10)
        toneDownSlider.setMaximum(0)
        toneDownSlider.setFixedHeight(100)
        toneDownSlider.valueChanged.connect(self.sliderValues) # Connect slider to function
        self.sliderList.append(toneDownSlider)
        self.sliderLayout.addWidget(toneDownSlider)

        eqButton = QPushButton("Start EQ") # Create EQ Button 
        eqButton.setFixedSize(100, 50)
        self.buttonLayout.addWidget(eqButton)

        sliderNames = ["Sub-Bass (20-60Hz)", "Bass (60-250Hz)", "Lower Mids (250-500Hz)",
                       "Midrange (500Hz-2kHz)", "Upper Mids (2kHz-4kHz)", "Presence (4kHz-6kHz)", 
                       "Brilliance/Air (6kHz-20kHz)", "Tone Down"]
        
        for i in range(8):
            label = QLabel(f"{sliderNames[i]}")
            self.labelLayout.addWidget(label)

        self.mainLayout.addLayout(self.sliderLayout) # Add slider layout to main layout
        self.mainLayout.addLayout(self.labelLayout, 7)
        self.mainLayout.addLayout(self.buttonLayout, 1)

        self.setLayout(self.mainLayout) # Use Main Layout for current window

        eqButton.clicked.connect(self.startEQ)

    def startEQ(self): # Function to start EQ process
        self.eng.EQ(r"C:\Users\jolea\Downloads\cokkie.mp3", self.gainValues, nargout=0)
        print("Start EQ button was clicked")

    def sliderValues(self): # Function to get slider values
        currentVals = []
        for i in range(8):
            currentVals.append(self.sliderList[i].value())
            print(f"Slider {i} value: {currentVals[i]}")
        self.gainValues = matlab.double(currentVals) # Convert to MATLAB double array

    def closeEvent(self, event):
        self.eng.quit() # or self.eng.exit()
        event.accept() # Confirms the window should actually close

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQApp()
    window.show()
    sys.exit(app.exec())
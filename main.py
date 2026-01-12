
import matlab.engine
import sys, os
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, 
                             QGridLayout, QHBoxLayout, QSlider, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# APP UI
class EQApp(QWidget):

    def __init__(self):
        self.eng = matlab.engine.start_matlab() # Start MATLAB engine
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.eng.addpath(script_dir, nargout=0) # Add path to MATLAB functions

        super().__init__()

        # Inside __init__
        script_dir_icon = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir_icon, "eq_icon.png") # Make sure the name matches your file
        self.setWindowIcon(QIcon(icon_path))

        self.sliderList = [] # Create list to hold sliders
        self.labelList = [] # Create list to hold labels
        self.gainValues = matlab.double([0, 0, 0, 0, 0, 0, 0, 0]) # Default gain values
        self.inputName = "" # Default input file name
        self.sliderNames = ["Sub-Bass (20-60Hz)", "Bass (60-250Hz)", "Lower Mids (250-500Hz)",
                       "Midrange (500Hz-2kHz)", "Upper Mids (2kHz-4kHz)", "Presence (4kHz-6kHz)", 
                       "Brilliance/Air (6kHz-20kHz)", "Tone Down"]

        self.setWindowTitle("EQ")
        self.resize(1000, 1000)
        self.setMinimumSize(200, 200)

        self.mainLayout = QVBoxLayout() # Main Layout for the app
        self.sliderLayout = QHBoxLayout() # Layout for the sliders
        self.sliderLabelLayout = QVBoxLayout() # Layout for slider labels
        self.buttonLayout = QHBoxLayout() # Layout for the buttons

        for i in range(8): # Create sliders and labels
            col = QVBoxLayout() # Create column layout for each slider/label pair
            slider = QSlider()

            slider.setSingleStep(1)
            slider.setTickInterval(1)
            slider.valueChanged.connect(self.sliderValues) # Connect slider to function
            if i != 7:
                slider.setMinimum(-20)
                slider.setMaximum(10)
                slider.setFixedHeight(150)
            else:
                slider.setMinimum(-10)
                slider.setMaximum(0)
                slider.setFixedHeight(100)

            label = QLabel(f"{self.sliderNames[i]} \nGain (dB): {0}") # Create label for slider
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            label.setWordWrap(True)
            self.labelList.append(label) # Add label to list

            col.addWidget(slider, alignment=Qt.AlignmentFlag.AlignHCenter)
            col.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

            self.sliderList.append(slider) # Add slider to list
            self.sliderLayout.addLayout(col) # Add column to slider layout

        eqButton = QPushButton("Start EQ") # Create EQ Button 
        eqButton.setFixedSize(100, 50)
        self.buttonLayout.addWidget(eqButton)
        eqButton.clicked.connect(self.startEQ) # Connect button to function

        fileButton = QPushButton("Select File") # Create File Select Button
        fileButton.setFixedSize(100, 50)
        self.buttonLayout.addWidget(fileButton)
        fileButton.clicked.connect(self.fileInput) # Connect button to function 
        
        self.fileNameLabel = QLabel("No file selected") # Label to show selected file
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addLayout(self.sliderLayout) # Add slider layout to main layout
        self.mainLayout.addWidget(self.fileNameLabel, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainLayout.addLayout(self.buttonLayout)

        self.setLayout(self.mainLayout) # Use Main Layout for current window

    def startEQ(self): # Function to start EQ process
        savedName = self.saveFileName()
        self.eng.EQ(self.inputName, self.gainValues, savedName, nargout=0)
        print(f"EQ processing complete. Saved as: {savedName}")

    def sliderValues(self): # Function to get slider values
        currentVals = []
        for i in range(8):
            currentVals.append(self.sliderList[i].value())
            self.labelList[i].setText(f"{self.sliderNames[i]} \nGain (dB): {currentVals[i]}") # Update label with current gain value
        self.gainValues = matlab.double(currentVals) # Convert to MATLAB double array

    def fileInput(self): # Function to select input file
        self.inputName, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav)")
        if self.inputName:
            self.fileNameLabel.setText(os.path.basename(self.inputName)) # Update label with selected file name

    def saveFileName(self): # Function to get save file name
        savedName, _ = QFileDialog.getSaveFileName(self,"Save Processed File","","WAV Files (*.wav);;All Files (*)", 
                                                   options=QFileDialog.Option.DontUseNativeDialog)
        if not savedName: # If no file name is provided, return None
            return None
        
        if not savedName.lower().endswith('.wav'): # Ensure .wav extension
            savedName += '.wav'

        return savedName 

    def closeEvent(self, event):
        self.eng.quit() # or self.eng.exit()
        event.accept() # Confirms the window should actually close

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQApp()
    window.show()
    sys.exit(app.exec())
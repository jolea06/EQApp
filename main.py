import matlab.engine
import sys, os, ctypes
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, 
                             QGridLayout, QHBoxLayout, QSlider, QFileDialog, QStackedWidget, QMainWindow)
from PyQt6.QtCore import (Qt, QThread, pyqtSignal)
from PyQt6.QtGui import (QIcon, QPixmap, QMovie)
from matlabworker import MATLABWorkerThread

myappid = 'mycompany.myproduct.subproduct.version' # Set a unique App ID, so app icon shows in taskbar
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# APP UI
class EQApp(QMainWindow):

    def __init__(self):
        self.eng = matlab.engine.start_matlab() # Start MATLAB engine
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.eng.addpath(script_dir, nargout=0) # Add path to MATLAB functions
        self.eng.cd(script_dir, nargout=0) # Tell MATLAB to "work" in this folder
        
        super().__init__() # Start init

        self.setWindowIcon(QIcon("eq_icon.ico")) # Set App Icon
        self.setWindowTitle("EQ") # Presey app window size
        self.resize(1200, 1000)
        self.setMinimumSize(200, 200)

        self.stacked_screens = QStackedWidget() # Create the stacked widget for the screens

        self.main_screen = self.setup_main_screen() # Create and add main screen
        self.stacked_screens.addWidget(self.main_screen)

        self.results_screen = self.setup_results_screen() # Create and add results screen
        self.stacked_screens.addWidget(self.results_screen)

        self.setCentralWidget(self.stacked_screens) 
        self.stacked_screens.setCurrentIndex(0) # Set default screen as main screen

    def setup_main_sliders(self): # Setup and create sliders

        self.slider_list = [] # Create list to hold sliders
        self.label_list = [] # Create list to hold labels
        self.gain_values = matlab.double([0, 0, 0, 0, 0, 0, 0, 0]) # Default gain values
        self.input_name = "" # Default input file name
        self.slider_names = ["Sub-Bass (20-60Hz)", "Bass (60-250Hz)", "Lower Mids (250-500Hz)",
                       "Midrange (500Hz-2kHz)", "Upper Mids (2kHz-4kHz)", "Presence (4kHz-6kHz)", 
                       "Brilliance/Air (6kHz-20kHz)", "Tone Down"]
        
        self.main_layout = QVBoxLayout() # Main Layout for the app
        self.slider_layout = QHBoxLayout() # Layout for the sliders
        # self.slider_label_layout = QVBoxLayout() # Layout for slider labels

        for i in range(8): # Create sliders and labels
            col = QVBoxLayout() # Create column layout for each slider/label pair
            slider = QSlider()

            slider.setSingleStep(1)
            slider.setTickInterval(1)
            slider.valueChanged.connect(self.sliderValues) # Connect slider to function

            if i != 7: # To create the tone down slider, different from other 7
                slider.setMinimum(-20)
                slider.setMaximum(10)
                slider.setFixedHeight(150)
            else:
                slider.setMinimum(-10)
                slider.setMaximum(0)
                slider.setFixedHeight(100)

            label = QLabel(f"{self.slider_names[i]} \nGain (dB): {0}") # Create label for slider
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            label.setWordWrap(True)
            self.label_list.append(label) # Add label to list

            col.addWidget(slider, alignment=Qt.AlignmentFlag.AlignHCenter)
            col.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

            self.slider_list.append(slider) # Add slider to list
            self.slider_layout.addLayout(col) # Add column to slider layout

        self.main_layout.addLayout(self.slider_layout) # Add slider layout to main layout

    def setup_main_buttons(self): # Setup and create buttons

        self.button_layout = QHBoxLayout() # Layout for the buttons

        eq_button = QPushButton("Start EQ") # Create EQ Button 
        eq_button.setFixedSize(100, 50)
        self.button_layout.addWidget(eq_button)
        eq_button.clicked.connect(self.startEQ) # Connect button to function

        file_button = QPushButton("Select File") # Create File Select Button
        file_button.setFixedSize(100, 50)
        self.button_layout.addWidget(file_button)
        file_button.clicked.connect(self.fileInput) # Connect button to function

        self.prev_button = QPushButton("See Previous")
        self.prev_button.setFixedSize(100, 50)
        self.prev_button.clicked.connect(self.prevResults)

        self.file_name_label = QLabel("No file selected") # Label to show selected file
        self.file_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        self.main_layout.addWidget(self.file_name_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addLayout(self.button_layout)

    def setup_main_screen(self): # Initialize the main screen
        page = QWidget() 

        self.setup_main_sliders()
        self.setup_main_buttons()
        
        page.setLayout(self.main_layout) 
        return page

    def setup_results_screen(self): # Initialize the results screen
        page = QWidget()

        self.setup_results()
        page.setLayout(self.results_layout)
        return page

    def setup_results(self): # Setup and create layouts for results screen
        self.results_layout = QVBoxLayout()
        self.image_with_title = QVBoxLayout()
        self.label_image = QLabel()

        self.image_with_title.setSpacing(20) # Removes the gap between title and image
        self.image_with_title.setContentsMargins(50, 50, 50, 50) # Removes padding around the group

        self.label_image.setPixmap(QPixmap())
        self.label_image.setFixedSize(800, 500)
        self.label_image.setScaledContents(True)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.image_title = QLabel() # Object for image title
        self.image_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.image_title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.image_with_title.addWidget(self.image_title, alignment=Qt.AlignmentFlag.AlignHCenter) # Alignment for widget
        self.image_with_title.addWidget(self.label_image, alignment=Qt.AlignmentFlag.AlignHCenter)

        back_button = QPushButton("back") # Back button
        back_button.setFixedSize(100, 50)
        back_button.clicked.connect(self.goBack)

        self.results_layout.addWidget(back_button)
        self.results_layout.addLayout(self.image_with_title)
        self.results_layout.addStretch(1)

    def startEQ(self): # Function to start EQ process
        self.refreshResultsScreen()
        self.saved_name = self.saveFileName()
        self.stacked_screens.setCurrentIndex(1)
        
        self.worker_thread = MATLABWorkerThread(self.eng, self.input_name, self.gain_values, self.saved_name)
        self.worker_thread.finished.connect(self.eqFinished)
        self.worker_thread.start()

    def sliderValues(self): # Function to get slider values
        current_vals = []
        for i in range(8):
            current_vals.append(self.slider_list[i].value())
            self.label_list[i].setText(f"{self.slider_names[i]} \nGain (dB): {current_vals[i]}") # Update label with current gain value
        self.gain_values = matlab.double(current_vals) # Convert to MATLAB double array

    def fileInput(self): # Function to select input file
        self.input_name, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav)")
        if self.input_name:
            self.file_name_label.setText(os.path.basename(self.input_name)) # Update label with selected file name

    def saveFileName(self): # Function to get save file name
        saved_name, _ = QFileDialog.getSaveFileName(self,"Save Processed File","","WAV Files (*.wav);;All Files (*)", 
                                                   options=QFileDialog.Option.DontUseNativeDialog)
        if not saved_name: # If no file name is provided, return None
            return None
        
        if not saved_name.lower().endswith('.wav'): # Ensure .wav extension
            saved_name += '.wav'

        return saved_name 

    def prevResults(self): # Function to show previous result screen
        self.stacked_screens.setCurrentIndex(1)

    def goBack(self): # Function to return to main screen
        self.button_layout.addWidget(self.prev_button)
        self.stacked_screens.setCurrentIndex(0)

    def eqFinished(self): # Function to update results screen once EQ has finished
        self.loading.stop()
        new_image = QPixmap('signal_comparison.png')
        self.label_image.setPixmap(new_image)
        self.label_image.update()
        self.image_title.setText("Equalized Audio Comparison")

    def refreshResultsScreen(self): # Function to refresh/reset the results screen with loading
        self.loading = QMovie('loading.gif')
        self.label_image.setMovie(self.loading)
        self.loading.start()
        self.image_title.setText("Loading...")

    def closeEvent(self, event): # Event handling the closing of the app
        self.eng.quit() # or self.eng.exit()
        event.accept() # Confirms the window should actually close

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQApp()
    window.show()
    sys.exit(app.exec())
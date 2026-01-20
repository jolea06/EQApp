# Audio Equalizer (PyQt & MATLAB)

A high-performance desktop application that integrates **Python (PyQt6)** with a **MATLAB Engine** to perform digital signal processing on audio files.

## Prerequisites

Before running the application, ensure the following are installed on your machine:

1. **MATLAB**: R2022a or newer (with the **Signal Processing Toolbox**).
2. **Python**: Version 3.9, 3.10, or 3.11 (64-bit).
   * *Note: Ensure Python is added to your system PATH during installation.*

---

## Installation & Setup

Follow these steps to set up the environment on a new machine:

### 1. Clone the Repository
Copy the project folder containing the `.py` source files and any associated `.m` MATLAB scripts.

### 2. Install Python Dependencies
Open your terminal or command prompt and install the required GUI and engine libraries:

```bash
pip install PyQt6
pip install matlabengine
```

### 3. Verify MATLAB Engine
The application requires the **MATLAB Engine API for Python** to communicate with the processing scripts. 

> **Note:** If `pip install matlabengine` fails, ensure your Python version is compatible with your installed MATLAB version. You may need to install it manually using the `setup.py` script located in your MATLAB `extern/engines/python` directory.

To verify that the bridge is installed correctly, run:

```bash
python -c "import matlab.engine; print('MATLAB Engine Ready')"
```

---

## Running the Application

### Option 1: VS Code (Recommended for Development)
To run and debug the app in VS Code, ensure you have the following installed:

* **Required Extensions:**
    * **Python** (by Microsoft): Required to execute and debug the Python source code.
    * **MATLAB** (by MathWorks): Provides syntax highlighting and snippet support for your `.m` filtering scripts.
    * **Qt for Python** (by its-pelle): Provides better intellisense and linting for **PyQt6** GUI components.

* **Execution Steps:** 1. Open the project folder in VS Code.
    2. Open `main.py`.
    3. Click the **Run** button (play icon) in the top-right corner, or press `F5` to debug.

### Option 2: Command Line
Navigate to the project directory using your terminal or command prompt and run:

```bash
python main.py
```
---

## Current Status: UI Polish

> **Note:** The application is **fully functional and stable**, performing all tasks as intended. I am currently in the final stages of the project, focusing on polishing the user interface and optimizing the layout for a more professional aesthetic.
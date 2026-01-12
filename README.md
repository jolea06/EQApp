# 🎚️ Digital Audio Equalizer

This application is an 8-band audio equalizer that uses a **Python (PyQt6)** interface to control a **MATLAB** DSP backend. It allows you to modify the frequency response of any audio file and export the result as a high-quality `.wav` file.

---

## 🎮 How to Use

1. **Select a File:** Click the **"Select File"** button to choose your input audio (`.mp3` or `.wav`).
2. **Adjust Gains:** Move the **8 Sliders** to change the volume of specific frequencies. Labels will update in real-time to show your current dB settings.
3. **Save File:** Click **"Start EQ"**. A window will appear for you to name your file and choose a save location. The app ensures the `.wav` extension is added automatically.

---

## 🛠️ Installation Requirements

To run this application, you must have **MATLAB** (R2020b or later) installed to support the DSP backend and the `matlabengine` package.

### 1. Prerequisites
* **Python**: Versions 3.9 through 3.12 are recommended.
* **System**: A 64-bit operating system to match the MATLAB architecture.

### 2. Install PyQt6
This library handles the graphical user interface. Open your terminal and run:
```bash
pip install PyQt6
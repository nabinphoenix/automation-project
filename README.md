# 📄 Notepad-Calculator Automation 🧮

A powerful Python-based automation tool that bridges the gap between text-based math problems and the Windows Calculator. This script automatically reads mathematical expressions from a Notepad file, solves them using the system calculator, and appends the results back to the original file.

## ✨ Features
- **Automated Text Parsing**: Automatically extracts labeled math expressions (e.g., `a. 1548-741`).
- **Seamless Window Management**: Uses `pygetwindow` to reliably switch between Notepad and Calculator.
- **Smart Calculation**: Leverages the Windows Calculator's Scientific Mode for accurate BODMAS/PEMDAS results.
- **Auto-Saving**: Automatically saves the updated Notepad file after processing.
- **Safety First**: Includes a fail-safe mechanism (move mouse to any corner to stop).

## 🖥️ Platform Compatibility
> [!IMPORTANT]
> **Windows Only**: This project is specifically designed for the Windows operating system. It relies on Windows-specific shortcuts (Win+R, Alt+Tab) and Windows-native applications (Notepad and Calculator). It will **not** run on macOS or Linux without significant modifications.

## 🛠️ Prerequisites
- **Python 3.x** installed.
- **Windows OS** (Notepad and Calculator must be available).

## 🚀 Installation

1. **Clone the repository** (or download the files).
2. **Install dependencies** using the provided `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 How to Use

1. Prepare a `.txt` file with math problems in this format:
   ```text
   a. 1548-741
   b. (500*2)/5
   c. 123+456-78
   ```
2. Run the script:
   ```bash
   python main.py
   ```
3. When prompted, provide the **Full Path** to your text file.
4. Press **ENTER** and watch the magic happen! (Avoid touching the mouse/keyboard during automation).

## 🛡️ Fail-Safe
If something goes wrong or you need to stop the automation immediately, simply **move your mouse cursor to any corner of your screen**. This will trigger the `pyautogui` fail-safe and stop the script.

---
*Created for Treeleaf AI Company*

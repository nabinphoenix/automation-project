# 📄 Notepad-Calculator Helper 🧮

This is a simple tool that solves math problems for you. It reads math questions from a Notepad file, finds the answers using the Windows Calculator, and writes those answers back into your file automatically.

---

## ✨ Features

* **Finding math in your text**
  It looks for questions that look like this:
  ```
  a. 1548-741
  b. (500*2)/5
  ```

* **Switching between apps**
  It is good at moving between your Notepad and the Calculator.

* **Using the right math mode**
  It uses the Calculator in a special mode to make sure the answers are correct.

* **Managing data**
  It copies the final answer and writes it right into your file.

* **Checking for mistakes**
  If something goes wrong while copying, it tries again to make sure it gets it right.

* **Writing answers at the end**
  It adds a neat list of all the answers to the bottom of your file.

* **Saving your work**
  The tool saves the file for you when it is finished.

* **Quickly stopping the tool**
  You can stop the program immediately by moving your mouse to the top left corner of your screen.

---

## ⚙️ How It Works

1. You give the program the location of your file.
2. It opens your file in Notepad.
3. It copies all the text to read it.
4. It finds only the math questions.
5. It opens the Windows Calculator.
6. It types and solves each math problem.
7. It copies the answer.
8. It double checks the result.
9. It writes all the answers at the end of your file.
10. It saves your file.

---

## 🖥️ Platform Compatibility

> ⚠️ **Windows Only**

This project is made only for Windows computers.

It uses:
* Windows keyboard shortcuts (like Win + R)
* Windows Notepad
* Windows Calculator

It will not work on Mac or Linux computers.

---

## 🛠️ Prerequisites

* Python installed on your computer.
* A Windows computer.
* The Notepad and Calculator apps.

---

## 📦 Dependencies

You will need to install these tools:

```bash
pip install -r requirements.txt
```

The tools it uses are:
* `pyautogui` (for moving the mouse and typing)
* `pyperclip` (for copying and pasting)
* `pygetwindow` (for finding the right apps)

---

## 🚀 Installation

1. Download the project files.
2. Install the tools using this command:

   ```bash
   pip install -r requirements.txt
   ```
3. Make sure you have Notepad and Calculator on your computer.

---

## 📖 Usage

### 1. Prepare a text file like this:

```text
You can write anything here. The program only looks for the questions.

a. 1548-741
b. (500*2)/5
c. 123+456-78
```

### 2. Run the program:

```bash
python main.py
```

### 3. When the program asks:

* Paste the full location of your file.
* Press **ENTER**.
* Do not touch the mouse or keyboard while it works!

The answers will appear at the bottom like this:

```
==================================================
RESULTS:
==================================================
a. 1548-741 = 807
b. (500*2)/5 = 200
c. 123+456-78 = 501
```

---

## 🛡️ Emergency Stop (Fail-Safe)

If you need to stop the program right away:

👉 Move your mouse cursor to the **top-left corner (0,0)** of your screen.

This will stop the program immediately.

---

## ⚠️ Limitations

* Only works on Windows.
* You cannot use your computer while it is running.
* If your screen looks different, the timing might be slightly off.
* It works best with labels like "a." or "1.".

---

## 🧠 Technical Highlights

This project shows how to:
* Control the screen and mouse with Python.
* Open and manage windows.
* Use the clipboard for copying data.
* Find patterns in text.
* Handle errors so the program does not crash.

---

## 📌 Conclusion

This tool is more than just a math solver. It shows how a computer can be programmed to do repetitive tasks for you by using different apps at the same time.

---

*Created for Treeleaf AI Company*

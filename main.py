"""
This tool is for people who has many math problems in Notepad.
It opens the Notepad file and reads all the math questions.
Then it opens the Windows Calculator and solves every math problem one by one.
Finally, it writes the answers back inside your Notepad file automatically.
"""

import pyautogui as pag   # This library helps to move mouse and type on keyboard.
import pyperclip        # This is used for copying and pasting text.
import time             # This is used to make computer wait for some time.
import os               # This is to check if your file is really there.
import re               # This helps computer to find math in long text.
import pygetwindow as gw # This helps to find and open the right app windows.


# These are settings for how fast the computer works.
pag.FAILSAFE = True
pag.PAUSE = 0.8
TYPING_INTERVAL = 0.05 


def get_file_path():
    """ this function ask you where is your file. 
    you type or paste the path and it check if file is real. 
    """
    print("=" * 70)
    print("ENTER FILE PATH")
    print("=" * 70)
    print("\nHow to get the path:")
    print("   1. Right-click your file")
    print("   2. Choose 'Copy as path'")
    print("   3. Paste it here")
    print("=" * 70)
    
    file_path = input("\nEnter file path: ").strip().strip('"')
    
    if os.path.exists(file_path):
        print(f"File found: {file_path}")
        return file_path
    else:
        print(f"File not found. Please check the path and try again.")
        return None


def extract_expressions(text):
    """ this function find math questions in your text. 
    it look for things like a. or 1. first. 
    if there is no numbering it just look for lines that has many numbers and math signs. 
    """
    expressions = []
    lines = text.split('\n')
    
    print("\nSearching for math problems...")
    fallback_counter = 1
    
    for line in lines:
        raw_line = line.strip()
        if not raw_line:
            continue
            
        """
        this look at line start 
        if line start with a label like a. or 1) 
        it keep that label and also keep the rest of the line after space
        """
        label_match = re.match(r'^([a-zA-Z0-9]+[.\)])\s*(.*)$', raw_line)
        
        if label_match:
            label = label_match.group(1)
            math_stuff = label_match.group(2)
        else:
            # if there is no numbering we check if the line look like math.
            # it must have at least one number to be math.
            if not any(c.isdigit() for c in raw_line):
                continue
            
            # we check if most characters are numbers or math symbols.
            math_chars = "0123456789+-*/()%. "
            score = sum(1 for c in raw_line if c in math_chars)
            
            # if more than half of the line is math then we take it.
            if score / len(raw_line) > 0.5:
                label = f"{fallback_counter}."
                math_stuff = raw_line
                fallback_counter += 1
            else:
                continue
            
        # this part pick only the math symbols and numbers.
        expression = ""
        for char in math_stuff:
            if char.isdigit() or char in ['+', '-', '*', '/', '(', ')', '.', ' ']:
                expression += char
        
        final_expr = expression.strip()
        if final_expr:
            # check if it actually has numbers so we don't calculate empty stuff.
            if any(c.isdigit() for c in final_expr):
                expressions.append({
                    'label': label,
                    'expression': final_expr
                })
                print(f"  Found: {label} {final_expr}")
    
    return expressions


def focus_notepad():
    """ this function find the notepad window. 
    it make it active so we can copy things from it. 
    """
    notepad_wins = [w for w in gw.getWindowsWithTitle('Notepad') if 'main.py' not in w.title]
    
    if notepad_wins:
        win = notepad_wins[0]
        try:
            if win.isMinimized:
                win.restore()
            win.activate()
            time.sleep(1)
            return True
        except:
            pass
    
    # if it fail it try to alt-tab to find it.
    pag.hotkey('alt', 'tab')
    time.sleep(1)
    return False


def focus_calculator():
    """ this function find and open calculator window. 
    this works so we can type math in it later. 
    """
    calc_wins = gw.getWindowsWithTitle('Calculator')
    
    if calc_wins:
        win = calc_wins[0]
        try:
            if win.isMinimized:
                win.restore()
            win.activate()
            time.sleep(1)
            return True
        except:
            pass
    return False


def open_file_in_notepad(file_path):
    """ this function open your file using windows run command. 
    it just type notepad and file name to open it fast. 
    """
    print(f"\nOpening your file in Notepad...")
    pag.hotkey('win', 'r')
    time.sleep(1)
    
    command = f'notepad "{file_path}"'
    pag.write(command, interval=0.01)
    time.sleep(0.5)
    pag.press('enter')
    time.sleep(3)


def copy_from_notepad():
    """ this function select all text and copy it. 
    it work like pressing ctrl+a then ctrl+c on keyboard. 
    """
    focus_notepad()
    pyperclip.copy("") 
    time.sleep(0.5)
    
    pag.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pag.hotkey('ctrl', 'c')
    time.sleep(1)
    
    return pyperclip.paste()


def open_calculator():
    """ this function open calculator app. 
    it also switch it to scientific mode so hard problems are correct. 
    """
    print("\nOpening Calculator...")
    pag.press('win')
    time.sleep(0.5)
    pag.write('calculator', interval=0.05)
    time.sleep(1)
    pag.press('enter')
    time.sleep(4)
    
    focus_calculator()
    # alt+2 is the shortcut for scientific mode.
    pag.hotkey('alt', '2')
    time.sleep(1)


def calculate_expression(expression):
    """ this function type math in calculator and get result. 
    it clear calculator first so old math does not mix up. 
    """
    # we remove spaces so calculator does not get confused.
    calc_input = expression.replace(" ", "")
    
    focus_calculator()
    pag.press('esc') # clear button
    time.sleep(0.5)
    
    pag.write(calc_input, interval=0.05)
    time.sleep(0.8)
    pag.press('enter')
    time.sleep(1.5)
    
    pyperclip.copy("")
    time.sleep(0.5)
    pag.hotkey('ctrl', 'c')
    time.sleep(1)
    
    result = pyperclip.paste().strip().replace(",", "")
    
    # if result is empty we try one more time to be sure.
    if not result or result == calc_input or any(c.isalpha() for c in result):
        focus_calculator()
        time.sleep(0.5)
        pag.press('enter') 
        time.sleep(0.8)
        pag.hotkey('ctrl', 'c')
        time.sleep(0.8)
        result = pyperclip.paste().strip().replace(",", "")
    
    return result


def append_results_to_notepad(results):
    """ this function write all answers at bottom of file. 
    it move cursor to end and then type everything. 
    """
    print("\nWriting results to Notepad...")
    focus_notepad()
    
    pag.hotkey('ctrl', 'end')
    time.sleep(1)
    
    pag.press('enter', presses=2)
    separator = "=" * 50
    pag.write(separator, interval=0.01)
    pag.press('enter')
    pag.write("RESULTS:", interval=0.01)
    pag.press('enter')
    pag.write(separator, interval=0.01)
    pag.press('enter')
    
    for item in results:
        line = f"{item['label']} {item['expression']} = {item['result']}"
        print(f"  Writing result for {item['label']}")
        pag.write(line, interval=0.02)
        pag.press('enter')
        time.sleep(0.2)


def save_notepad():
    """ this function save your file. 
    it just press ctrl+s like you do manually. 
    """
    focus_notepad()
    pag.hotkey('ctrl', 's')
    time.sleep(1)


def main():
    """ this function is the main logic. 
    it call other functions in right order to solve math. 
    """
    print("\n" + "=" * 70)
    print("NOTEPAD-CALCULATOR AUTO-SOLVER")
    print("=" * 70)
    
    try:
        path = get_file_path()
        if not path:
            return
        
        print("Emergency Stop: Move mouse to top-left corner anytime to stop.")
        
        input("\nPress ENTER to start... Then hands off the mouse!")
        
        open_file_in_notepad(path)
        time.sleep(1.5)
        
        content = copy_from_notepad()
        if not content:
            print("The file was empty. Stopping.")
            return
        
        problems = extract_expressions(content)
        if not problems:
            print("No math problems found. Check your file.")
            return
        
        open_calculator()
        
        final_list = []
        for i, p in enumerate(problems, 1):
            print(f"Solving {i} of {len(problems)}: {p['label']}")
            ans = calculate_expression(p['expression'])
            final_list.append({
                'label': p['label'],
                'expression': p['expression'],
                'result': ans if ans else "ERROR"
            })
        
        append_results_to_notepad(final_list)
        save_notepad()
        
        print("\nAll done! Your answers are saved in the file.")
        
    except pag.FailSafeException:
        print("\n!!! EMERGENCY STOP !!!")
        print("Stopped because you moved the mouse to the corner.")
    except Exception as e:
        print(f"\nThere was an error: {e}")


if __name__ == "__main__":
    main()
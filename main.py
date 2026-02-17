"""
Notepad-Calculator Automation
Properly switches between Notepad and Calculator
"""

import pyautogui as pag   # Controls mouse and keyboard
import pyperclip        # Handles clipboard (copy/paste)
import time             # For adding delays
import os               # For file and system operations
import re               # Regular Expressions for parsing text
import pygetwindow as gw # For window management (focus/activate)


# ===== CONFIGURATION =====
pag.FAILSAFE = True
pag.PAUSE = 0.8

# Typing speed
TYPING_INTERVAL = 0.05

# ===== FILE HANDLING =====

def get_file_path():
    """Ask user for file path"""
    print("=" * 70)
    print("ENTER FILE PATH")
    print("=" * 70)
    print("\n📁 How to get file path:")
    print("   1. Right-click on your file")
    print("   2. Select 'Copy as path'")
    print("   3. Paste it here")
    print("\n   OR just type/paste the full path")
    print("=" * 70)
    
    file_path = input("\nEnter file path: ").strip().strip('"')
    
    # Verify file exists
    if os.path.exists(file_path):
        print(f"✅ File found: {file_path}")
        return file_path
    else:
        print(f"❌ File not found: {file_path}")
        print("   Please check the path and try again")
        return None

# ===== EXPRESSION EXTRACTION =====

def extract_expressions(text):
    """Extract mathematical expressions from text"""
    expressions = []
    lines = text.split('\n')
    
    for line in lines:
        if not line.strip():
            continue
        
        # This regex looks for a label at the start (e.g., 'a.', '1.', 'a)')
        # It handles letters/numbers followed by a period or parenthesis
        label_match = re.match(r'^([a-zA-Z0-9]+[.\)])\s*(.*)$', line)
        
        if label_match:
            label = label_match.group(1)  # e.g., "a." or "1."
            rest_of_line = label_match.group(2)  # e.g., "1548-741"
            
            # Extract expression from the part AFTER the label
            expression = ""
            for char in rest_of_line:
                if char.isdigit() or char in ['+', '-', '*', '/', '(', ')']:
                    expression += char
            
            if expression:
                expressions.append({
                    'label': label,
                    'expression': expression,
                    'original_line': line.strip()
                })
                print(f"  Extracted: {label} → {expression}")
    
    return expressions

# ===== WINDOW MANAGEMENT =====

def focus_notepad():
    """
    Focus on Notepad window using pygetwindow
    Ensures it's the active window before copying/typing
    """
    print("  Switching to Notepad...")
    
    # Try to find Notepad window
    # Exclude this script's editor if it happens to have 'Notepad' in title
    notepad_wins = [w for w in gw.getWindowsWithTitle('Notepad') if 'new_main.py' not in w.title]
    
    if notepad_wins:
        win = notepad_wins[0]
        try:
            if win.isMinimized:
                win.restore()
            win.activate()
            time.sleep(1)
            print("  ✓ Notepad focused")
            return True
        except Exception as e:
            print(f"  ⚠️ Could not activate Notepad: {e}")
    else:
        print("  ❌ Notepad window not found!")
    
    # Fallback to Alt+Tab if pygetwindow fails
    pag.hotkey('alt', 'tab')
    time.sleep(1)
    return False

def focus_calculator():
    """
    Focus on Calculator window using pygetwindow
    Ensures Calculator is the active window before typing
    """
    print("  Switching to Calculator...")
    
    calc_wins = gw.getWindowsWithTitle('Calculator')
    
    if calc_wins:
        win = calc_wins[0]
        try:
            if win.isMinimized:
                win.restore()
            win.activate()
            time.sleep(1)
            print("  ✓ Calculator focused")
            return True
        except Exception as e:
            print(f"  ⚠️ Could not activate Calculator: {e}")
    else:
        print("  ❌ Calculator window not found!")
        # Try to open it if not found
        open_calculator()
    
    return False


# ===== AUTOMATION FUNCTIONS =====

def open_file_in_notepad(file_path):
    """Open file in Notepad"""
    print(f"\n📝 Opening file in Notepad...")
    
    # Use Win+R to run command
    pag.hotkey('win', 'r')
    time.sleep(1)
    
    # Type command
    command = f'notepad "{file_path}"'
    pag.write(command, interval=0.02)
    time.sleep(0.5)
    
    pag.press('enter')
    time.sleep(3)
    
    print("✓ Notepad opened")

def copy_from_notepad():
    """Copy content from Notepad"""
    print("\n📋 Copying content from Notepad...")
    
    # Make sure Notepad is focused
    focus_notepad()
    
    # Clear clipboard before copying
    pyperclip.copy("")
    time.sleep(0.5)
    
    # Select all text (Ctrl+A)
    pag.hotkey('ctrl', 'a')
    time.sleep(1)
    
    # Copy selected text (Ctrl+C)
    pag.hotkey('ctrl', 'c')
    time.sleep(1)
    
    # Get the raw text from the windows clipboard
    content = pyperclip.paste()
    
    if content:
        print(f"✓ Copied {len(content)} characters")
        return content
    else:
        print("❌ Failed to copy content")
        return ""

def open_calculator():
    """Open Calculator"""
    print("\n🧮 Opening Calculator...")
    
    pag.press('win')
    time.sleep(0.5)
    pag.write('calculator', interval=0.05)
    time.sleep(1)
    pag.press('enter')
    time.sleep(4)
    
    print("✓ Calculator opened")
    
    # Ensure Scientific Mode for complex calculations (BODMAS/PEMDAS)
    print("  Ensuring Scientific Mode...")
    focus_calculator()
    pag.hotkey('alt', '2')
    time.sleep(1)

def calculate_expression(expression):
    """
    Calculate expression in Calculator
    FIXED: Properly focuses Calculator before typing
    """
    print(f"  🔢 Calculating: {expression}")
    
    # IMPORTANT: Focus Calculator first!
    focus_calculator()
    
    # Clear calculator
    pag.press('esc')
    time.sleep(0.5)
    
    # Type the math expression into the Calculator display
    # We use write() because it handles numeric symbols and operators reliably
    pag.write(expression, interval=0.1)
    time.sleep(1)
    
    # Press ENTER to execute the calculation
    pag.press('enter')
    time.sleep(2)
    
    # Clear the clipboard first to ensure we don't accidentally get old data
    pyperclip.copy("")
    time.sleep(0.5)
    
    # Send Ctrl+C to the Calculator to copy the final result
    pag.hotkey('ctrl', 'c')
    time.sleep(1.5)
    
    # Pull the result from the clipboard into our Python variable
    result = pyperclip.paste().strip()
    
    # Clean result: remove commas and whitespace
    result = result.replace(",", "").strip()
    
    # Validate result: it shouldn't be the same as the expression and shouldn't contain letters
    if result and result != "" and not any(c.isalpha() for c in result):
        # Additional check: if result is still the expression, copying might have failed
        if result == expression:
            print("  ⚠️ Result matches expression, retrying...")
            return retry_calculate_copy()
        
        print(f"  ✅ Result: {result}")
        return result
    else:
        return retry_calculate_copy()

def retry_calculate_copy():
    """Fallback if first copy fails"""
    print("  Retrying copy...")
    focus_calculator()
    time.sleep(0.5)
    # Sometimes Esc or a small click helps refresh the UI state
    pag.press('enter') 
    time.sleep(1)
    pag.hotkey('ctrl', 'c')
    time.sleep(1)
    result = pyperclip.paste().strip().replace(",", "")
    print(f"  ✅ Result: {result}")
    return result

def append_results_to_notepad(results):
    """
    Append results to Notepad
    FIXED: Properly focuses Notepad before typing
    """
    print("\n📝 Appending results to Notepad...")
    
    # Switch to Notepad
    focus_notepad()
    
    # Go to end
    pag.hotkey('ctrl', 'end')
    time.sleep(1)
    
    # Add separator
    pag.press('enter')
    time.sleep(0.3)
    pag.press('enter')
    time.sleep(0.3)
    
    separator = "=" * 50
    pag.write(separator, interval=TYPING_INTERVAL)
    time.sleep(0.5)
    pag.press('enter')
    time.sleep(0.3)
    
    pag.write("RESULTS:", interval=TYPING_INTERVAL)
    time.sleep(0.5)
    pag.press('enter')
    time.sleep(0.3)
    
    pag.write(separator, interval=TYPING_INTERVAL)
    time.sleep(0.5)
    pag.press('enter')
    time.sleep(0.3)
    
    # Add each result
    for item in results:
        result_line = f"{item['label']} {item['expression']} = {item['result']}"
        print(f"  Writing: {result_line}")
        
        pag.write(result_line, interval=TYPING_INTERVAL)
        time.sleep(0.5)
        pag.press('enter')
        time.sleep(0.5)
    
    print("✓ Results appended")

def save_notepad():
    """Save Notepad file"""
    print("\n💾 Saving file...")
    
    # Make sure Notepad is focused
    focus_notepad()
    
    pag.hotkey('ctrl', 's')
    time.sleep(2)
    
    print("✓ File saved")

# ===== MAIN AUTOMATION =====

def main():
    """Main automation workflow"""
    
    print("\n" + "=" * 70)
    print("NOTEPAD-CALCULATOR AUTOMATION")
    print("=" * 70)
    print("\n📋 What this does:")
    print("   1. Opens your file in Notepad")
    print("   2. Reads math questions (a., b., c., etc.)")
    print("   3. Solves them in Calculator")
    print("   4. Appends results to the file")
    print("\n⚠️  EMERGENCY STOP: Move mouse to ANY corner of the screen")
    print("=" * 70)
    
    try:
        # Step 1: Get file path from user
        file_path = get_file_path()
        
        if not file_path:
            print("\n❌ Invalid file path. Exiting.")
            return
        
        
        print("\n✅ File verified!")
        input("\nPress ENTER to start automation...")
        
        # Step 2: Open in Notepad
        open_file_in_notepad(file_path)
        
        print("\n⏳ Starting in 2 seconds... Don't touch anything!")
        time.sleep(2)
        
        # Step 3: Copy content from Notepad
        content = copy_from_notepad()
        
        if not content:
            print("❌ No content found. Exiting.")
            return
        
        # Step 4: Extract expressions
        print("\n🔍 Extracting expressions...")
        expressions = extract_expressions(content)
        
        if not expressions:
            print("❌ No expressions found!")
            return
        
        print(f"\n✅ Found {len(expressions)} expressions")
        
        # Step 5: Open Calculator
        open_calculator()
        time.sleep(2)
        
        # Step 6: Calculate each expression
        print("\n🧮 Calculating expressions...")
        results = []
        
        for i, expr_data in enumerate(expressions, 1):
            print(f"\n[{i}/{len(expressions)}] {expr_data['label']}")
            
            try:
                # This will focus Calculator and calculate
                result = calculate_expression(expr_data['expression'])
                results.append({
                    'label': expr_data['label'],
                    'expression': expr_data['expression'],
                    'result': result
                })
            except Exception as e:
                print(f"  ❌ Error: {e}")
                results.append({
                    'label': expr_data['label'],
                    'expression': expr_data['expression'],
                    'result': 'ERROR'
                })
            
            time.sleep(1)
        
        # Step 7: Append results to Notepad
        append_results_to_notepad(results)
        
        # Step 8: Save
        save_notepad()
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ AUTOMATION COMPLETED!")
        print("=" * 70)
        print("\n📊 Results:")
        for item in results:
            print(f"   {item['label']} {item['expression']} = {item['result']}")
        print("\n💾 Results saved to:", file_path)
        print("=" * 70)
        
    except pag.FailSafeException:
        print("\n⚠️  EMERGENCY STOP ACTIVATED!")
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
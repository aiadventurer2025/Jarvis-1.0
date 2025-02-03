import pygetwindow as gw
import google.generativeai as genai
import psutil
import webbrowser
import os
from dotenv import dotenv_values
from colorama import Fore, init
# Initialize colorama
init(autoreset=True)
# Load environment variables
env_vars = dotenv_values(".env")
# Configure Gemini API
genai.configure(api_key=env_vars.get("Gemini_API_KEY"))  # Store API key in .env
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def get_active_window():
    """Returns the title of the currently active window using pygetwindow."""
    active_window = gw.getActiveWindow()
    return active_window.title if active_window else "Unknown"

def get_python_code(task, active_window):
    """Ask Gemini AI to generate clean and executable Python code for the task based on the active window."""
    
    prompt = f"""Hello, I am {Username}. You are {Assistantname}, a highly accurate and advanced AI specialized in automation.
    
        Currently, the active window title is: "{active_window}". Your task is to generate a Python script to automate the following command: "{task}".

        ## IMPORTANT INSTRUCTIONS:
        - DO NOT include Markdown formatting (No ```python or ```)
        - DO NOT include explanations or comments
        - The script should EXECUTE IMMEDIATELY upon running
        - The script should work with the active application, if relevant
        - If the task involves opening a website, use `webbrowser.open()`
        - If it requires keyboard shortcuts, use `pyautogui`
        - If it involves system commands, use `os.system()`

        ## EXAMPLES:
        If the task is "open YouTube", the correct output is:
            webbrowser.open("https://www.youtube.com")

        If the task is "close YouTube tab", the correct output is:
            import pyautogui
            pyautogui.hotkey('ctrl', 'w')

        If the task is "open a text file", the correct output is:
            import os
            os.system("notepad example.txt")

        Now, generate the required Python script for: "{task}".
        """

    response = model.generate_content(prompt)
    return response.text


def clean_code(code):
    """Remove Markdown formatting and unnecessary whitespace."""
    if code.startswith("```python") and code.endswith("```"):
        code = code[9:-3].strip()
    elif code.startswith("```") and code.endswith("```"):
        code = code[3:-3].strip()
    return code.strip()

def execute_code(task):
    """Gets AI-generated Python code and executes it."""
    active_window = get_active_window()    
    code = get_python_code(task, active_window)
    code = clean_code(code)
    exec(code)  # Executes the AI-generated script


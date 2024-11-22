import subprocess
import os
import time


current_working_dir = os.getcwd()
activate_script = os.path.join(".venv", "Scripts", "activate.bat")

def start_quiz_GUI():
    gui_script = "python LoginPage.py"
    # command = f'start cmd /k "{activate_script} && {gui_script}"'
    command = f'cmd /c "{activate_script} && {gui_script}"'
    try:
        subprocess.Popen(command, cwd=current_working_dir, shell=True , creationflags= subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Failed to start quiz GUI: {e}")


if __name__ == "__main__":
    start_quiz_GUI()
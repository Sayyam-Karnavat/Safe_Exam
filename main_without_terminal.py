import subprocess
import os
import time

#################################################################################################################################################


'''
 start cmd command with subprocess.Popen, the start command itself opens a new command window. The creationflags=subprocess.CREATE_NO_WINDOW flag you’re using only applies to the cmd.exe process, not the start command.

'''


#################################################################################################################################################

current_working_dir = os.getcwd()
activate_script = os.path.join(".venv", "Scripts", "activate.bat")

def run_script_in_background(script_command):
    command = f'{activate_script} && {script_command}'
    try:
        subprocess.Popen(command, cwd=current_working_dir, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Failed to run script: {e}")

def start_quiz_GUI():
    gui_script = "python LoginPage.py"
    run_script_in_background(gui_script)

def start_wireless_screen_AI_model():
    wireless_script = "python wireless_screencast_detection.py"
    run_script_in_background(wireless_script)

def start_wired_screen_AI_model():
    wired_script = "python wired_screencast_detection.py"
    run_script_in_background(wired_script)

def open_dashboard():
    working_dir = os.path.join(current_working_dir, "student-dashboard/")
    front_end_command = "npm run start"
    try:
        subprocess.Popen(front_end_command, cwd=working_dir, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Failed to start Dashboard: {e}")

def open_database_server():
    wired_script = "python quiz_socket.py"
    run_script_in_background(wired_script)


if __name__ == "__main__":
    open_dashboard()
    time.sleep(2)
    open_database_server()
    start_quiz_GUI()
    start_wireless_screen_AI_model()
    start_wired_screen_AI_model()

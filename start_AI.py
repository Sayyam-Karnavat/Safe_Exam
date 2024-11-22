import subprocess
import os


current_working_dir = os.getcwd()
activate_script = os.path.join(".venv", "Scripts", "activate.bat")

def start_wireless_screen_AI_model():
    wireless_script = "python wireless_screencast_detection.py"
    command = f'cmd /c "{activate_script} && {wireless_script}"'
    try:
        subprocess.Popen(command, cwd=current_working_dir, shell=True, creationflags= subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Failed to start wireless screen AI model: {e}")

def start_wired_screen_AI_model():
    wired_script = "python wired_screencast_detection.py"
    command = f'cmd /c "{activate_script} && {wired_script}"'
    try:
        subprocess.Popen(command, cwd=current_working_dir, shell=True, creationflags= subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Failed to start wired screen AI model: {e}")


if __name__ == "__main__":
    ## Start AI model ###
    start_wireless_screen_AI_model()
    start_wired_screen_AI_model()

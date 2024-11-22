from flask import Flask
from flask_socketio import SocketIO
import os
import sys
import subprocess



activate_environment = os.path.join(".venv", "Scripts", "activate.bat")
current_directory = os.getcwd()

app = Flask(__name__)
socket_app = SocketIO(app, cors_allowed_origins="*")  


def start_AI_models():
    print("Starting the AI models !!!")
    
    wireless_AI = "python wireless_screencast_detection.py"
    wired_AI = "python wired_screencast_detection.py"
    
    # Activate environment and run AI models in separate terminals
    wireless_command = f'start cmd /k "{activate_environment} && {wireless_AI}"'
    wired_command = f'start cmd /k "{activate_environment} && {wired_AI}"'
    try:
        subprocess.Popen(wireless_command, cwd=current_directory, shell=True)
        subprocess.Popen(wired_command, cwd=current_directory, shell=True)
    except Exception as e:
        print(f"Error starting AI models: {e}")




def kill_background_terminal():
    script_path = 'kill-conhost.ps1'
    if os.path.exists(script_path):
        command = [
            'powershell.exe',
            '-ExecutionPolicy', 'ByPass',
            '-File', script_path
        ]
        try:
            subprocess.Popen(command)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        sys.exit(0)
    else:
        print(f"Script not found: {script_path}")
        sys.exit(1)

@app.route("/emit_start_AI", methods=['GET'])
def emit_start_AI():
    start_AI_models()
    return "AI model started"

@app.route("/emit_end_AI", methods=['GET'])
def emit_end_AI():
    kill_background_terminal()
    return "AI model stopped !!!"


if __name__ == "__main__":
    socket_app.run(app, debug=False)

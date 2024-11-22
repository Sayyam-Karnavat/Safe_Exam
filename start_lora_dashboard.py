import subprocess
import os


# Go one directory up of parent directory
current_working_dir = os.getcwd()
activate_script = os.path.join(".venv", "Scripts", "activate.bat")


def open_dashboard():
    '''
    This function gets called after the exam is over and close button is clicked
    '''
    working_dir = os.path.join(current_working_dir, "student-dashboard/")
    front_end_command = "npm run start"
    command = f'start cmd /k "{front_end_command}"'
    try:
        subprocess.Popen(command, cwd=working_dir, shell=True, creationflags= subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Failed to start Dashboard: {e}")



def open_dappflow():
    dappflow_command = "algokit explore"
    subprocess.Popen(f'start cmd /k "{dappflow_command}"' , cwd= current_working_dir , shell=True)


if __name__  == "__main__":
    open_dashboard()
    open_dappflow()
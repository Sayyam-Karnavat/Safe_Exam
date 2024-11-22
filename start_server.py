import subprocess
import os



current_working_dir = os.getcwd()
activate_script = os.path.join(".venv", "Scripts", "activate.bat")



def reset_localnet_and_start_server():
    '''
    Modified the open database server function to run after the localnet has been resetted
    '''
    reset_command = "algokit localnet reset && python server.py"
    subprocess.Popen(f'start cmd /k "{activate_script} && {reset_command}"' , cwd= current_working_dir , shell=True)


def start_server_for_testnet():
    start_socket_command  = "python server.py"
    combined_command = f'start cmd /k "{activate_script} && {start_socket_command}"'
    subprocess.Popen(combined_command , cwd=current_working_dir , shell=True)


if __name__ == "__main__":
    start_server_for_testnet()
    
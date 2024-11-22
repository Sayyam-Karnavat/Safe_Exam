import wmi
import time
import pythoncom
import requests
import socket
import json
from metadata import Exam_Title , Booklet , exam_start_time , exam_end_time


class ScreenCastingMonitor:
    def __init__(self):
        self.c = None
        self.initialize_com()
        self.c = wmi.WMI()
        self.initial_monitors = self.get_connected_monitors()
        self.initial_count = len(self.initial_monitors)
        self.deviceIP = self.get_ip_address()
        self.message = "yes"

        self.api_url_blockchain = "http://127.0.0.1:2222/send_data_to_blockchain"

        self.student_json_data = {
            "student_id": "-",
            "wallet_address":"-",
            "exam_title": Exam_Title,
            "city": "-",
            "center_name": "-",
            "booklet": Booklet,
            "start_time": exam_start_time,
            "que_ans": "-",
            "suspicious_activity_detected": f"{self.message}-{self.deviceIP}",
            "end_time": exam_end_time,
            "transaction_id": "-",
        }

        try:

            with open("deployed_user_data.json" , "r") as f:
                # This will contain private_key, app_id etc of user who has already deployed the application
                self.user_json_data = json.load(fp=f)

                # Update the json for studnet ID and wallet address
                self.student_json_data['student_id'] = self.user_json_data['userID']
                self.student_json_data['wallet_address'] =self.user_json_data['user_wallet_address']
                f.close()
        except Exception as e :
            print(str(e))

    def get_ip_address(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("8.8.8.8", 80))  # Connect to a dummy socket 
                local_ip_address = sock.getsockname()[0]
            return local_ip_address
        except socket.error as e:
            print(f"Error occurred: {e}")
            return None

    def initialize_com(self):
        """Initialize COM for the current thread.""" 
        pythoncom.CoInitialize()

    def get_connected_monitors(self):
        monitors = self.c.Win32_PnPEntity(ConfigManagerErrorCode=0)
        connected_monitors = []

        for monitor in monitors:
            if 'DISPLAY' in monitor.PNPDeviceID:
                instance_name = monitor.PNPDeviceID
                description = monitor.Description
                connection_type = "Unknown"

                # Check if the monitor is connected via HDMI, DVI, DisplayPort, or VGA
                if "HDMI" in instance_name.upper():
                    connection_type = "HDMI"
                elif "DVI" in instance_name.upper():
                    connection_type = "DVI"
                elif "DISPLAYPORT" in instance_name.upper():
                    connection_type = "DisplayPort"
                elif "VGA" in instance_name.upper():
                    connection_type = "VGA"

                connected_monitors.append((instance_name, description, connection_type))

        return connected_monitors

    def detect_screen_casting(self):
        while True:
            current_monitors = self.get_connected_monitors()
            current_count = len(current_monitors)

            if current_count != self.initial_count:
                print("Display configuration changed!")
                
                # Update JSON data with the latest IP address
                self.student_json_data["suspicious_activity_detected"] = f"{self.message}-{self.deviceIP}"

                # Send POST request
                requests.post(url=self.api_url_blockchain, json=self.student_json_data)

                if current_count > self.initial_count:
                    print("Screen casting detected.")
                else:
                    print("Screen casting stopped.")

                # Update the state to the current configuration
                self.initial_monitors = current_monitors
                self.initial_count = current_count
            else:
                print("Display configuration is stable.")

            time.sleep(10)

    def main(self):
        print("Wired AI model monitoring enabled!")
        try:
            self.detect_screen_casting()
        finally:
            pythoncom.CoUninitialize()  # Clean up COM

if __name__ == "__main__":
    monitor = ScreenCastingMonitor()
    monitor.main()

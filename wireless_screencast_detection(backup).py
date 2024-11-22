import socket
import time
import win32api
from scapy.all import sniff, IP, UDP
import psutil
import pickle
from predictor import ModelPredictor
import screeninfo
import requests

class PacketMonitor:
    def __init__(self):
        self.traffic_dict = {}
        self.initial_display_devices = []
        self.program_start_time = time.time()
        self.deviceIP = self.get_ip_address()
        self.initial_display_devices = self.get_display_devices()
        self.all_ip_address = self.get_all_ip_addresses()

        self.api_url_blockchain = "http://127.0.0.1:2222/send_data_to_blockchain"
        self.message = "yes"
        self.student_json_data = {
            "student_id": "-", # Student ID yet to be implemented 
            # "wallet_address": f"{self.wallet_address}",
            "exam_title": "-",
            "city": "-",
            "center_name": "-",
            "booklet": "",
            "start_time": "-",
            "que_ans": "-",
            "suspicious_activity_detected": f"{self.message}-{self.deviceIP}",
            "end_time": "-",
            "transaction_id": "-",
        }

    def get_ip_address(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("8.8.8.8", 80))  # Connect to a dummy socket 
                local_ip_address = sock.getsockname()[0]
            return local_ip_address
        except socket.error as e:
            print(f"Error occurred: {e}")
            return None
        

    def create_filter_string(self,ip_addresses):
        # Create a filter string for multiple IP addresses
        if not ip_addresses:
            return ""
        filter_parts = [f"host {ip}" for ip in ip_addresses]
        return " or ".join(filter_parts)

    def get_all_ip_addresses(self):
        ip_addresses = []
        # Get all network interfaces
        interfaces = psutil.net_if_addrs()
        for interface in interfaces:
            for address in interfaces[interface]:
                if address.family == socket.AF_INET:
                    ip_addresses.append(address.address)
        return ip_addresses
        
    def get_display_devices(self):
        display_devices = []
        i = 0
        while True:
            try:
                display_device = win32api.EnumDisplayDevices(None, i)
                if display_device.DeviceName:
                    display_devices.append(display_device)
                i += 1
            except win32api.error:
                break
        return display_devices

    def process_packet(self, packet):
        #### Sleep the Model for 1-2 seconds after each packet received ####
        # Since when the screen is shared(on teams)/Screencasted every millisecond the packet is shared which slows down the entire GUI #
        time.sleep(1)
        try:
                
            
            if IP in packet and UDP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                packet_length = len(packet[UDP])

                # Traffic dictionary update
                if dst_ip not in self.traffic_dict:
                    print(f"Connection started between {self.deviceIP} - {dst_ip}")
                    self.traffic_dict[dst_ip] = {"starttime": time.time(), "packet_rate": 0}

                try:
                    elapsed_time = time.time() - self.traffic_dict[dst_ip]['starttime']
                    if elapsed_time > 0:
                        self.traffic_dict[dst_ip]['packet_rate'] += packet_length / elapsed_time
                except ZeroDivisionError:
                    pass


                ##############################################################################################################
                # Check packet rate every 15 seconds also after every 15 seconds the display device gets checked since it was
                # expensive to check after each loop
                ##############################################################################################################
                if time.time() - self.program_start_time > 15:


                    # Check if screen count becomes more than 1
                    after_screen_count = len(screeninfo.get_monitors())
                    if after_screen_count > 1:
                        print("Malicious activity detected: Screen count is more than 1")
                        print("Total Screen count is:", after_screen_count)
                        print("Device IP  :- ",self.deviceIP)
                        
                        # Send data to blockchain 
                        requests.post(url= self.api_url_blockchain , json=self.student_json_data)

                    # Check if display devices changed
                    current_display_devices = self.get_display_devices()
                    if len(current_display_devices) > len(self.initial_display_devices):
                        print("Malicious activity detected: Current screen is extended or duplicated")
                        print("Multiple screens found for device IP :- ", self.deviceIP)
                        # Send data to blockchain 
                        requests.post(url= self.api_url_blockchain , json=self.student_json_data)



                    print("Traffic dictionary :-" , self.traffic_dict)
                    print("10 Seconds Elapsed Checking")
                    print("Traffic dictiory:-" , self.traffic_dict)
                    self.program_start_time = time.time()

                    for key, value in self.traffic_dict.items():

                        ##### Lowered the packet rate to create dummy dataset for AI ####
                        if value['packet_rate'] > 512354:
                            print("High packet rate detected, sending data for AI prediction")
                            print(f"IP: {key}, Packet Rate: {value['packet_rate']}")
                            data_for_prediction = {
                                'protocol': 'UDP',
                                'packet_length': packet_length,
                                'flag': 0,
                                'sequence': 0,
                                'window_size': 0,
                                'ack': 0
                            }
                            res = predictor_obj.predict(data_for_prediction)
                            if res != 1:
                                print("Malicious activity detected !!! Device IP :- ", self.deviceIP)
                                # Send data to blockchain 
                                requests.post(url= self.api_url_blockchain , json=self.student_json_data)
                                ### Added this delay so that server doesn't gets overloaded with requests ####
                                time.sleep(2)
                            else:
                                print("Not a malicious activity")

                    self.traffic_dict.clear()
        except Exception as e:
            print("Error occured while processing packets \n" , e)

    def main(self):
        initial_screen_count = len(screeninfo.get_monitors())
        if initial_screen_count > 1:
            
            print("More than 1 screen connected to device")
            # Send data to blockchain 
            requests.post(url= self.api_url_blockchain , json=self.student_json_data)


        print("Wireless AI model monitoring enabled !!!!")
        print("Device IP address:", self.deviceIP)
        print("All ip address :-" , self.all_ip_address)

        if self.all_ip_address:
            filter_string = self.create_filter_string(self.all_ip_address)
            try:
                sniff(filter=filter_string, prn=self.process_packet, store=0)
            except KeyboardInterrupt:
                print("Exiting loop")
        elif self.deviceIP:
            try:
                sniff(filter=f"host {self.deviceIP}", prn=self.process_packet, store=0)
            except KeyboardInterrupt:
                print("Exiting loop")
        else:
            print("No Ip address found to Sniff packets !!!")




if __name__ == "__main__":
    predictor_obj = ModelPredictor()
    monitor = PacketMonitor()
    monitor.main()

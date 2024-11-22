from tkinter import messagebox
import customtkinter as ctk
import DefaultPage
from LoginPage import LoginApp
from collections import deque
import sys
import datetime
import subprocess
import metadata
import threading
import time
import requests
import os
from metadata import server_URL , insert_data_endpoint


login_obj = LoginApp()


###############################################################################################################################################################################

class TaskQueue:
    def __init__(self, blockchain_object):
        self.task_queue = deque()
        self.blockchain_obj = blockchain_object

    def add_task(self, student_json_data):
        self.task_queue.appendleft(student_json_data)
        return 1

    def write_data_to_blockchain(self):
        json_student_data = self.task_queue.pop()

        student_id = json_student_data.get('student_id', "-")
        exam_title = json_student_data.get('exam_title', "-")
        city = json_student_data.get('city', "-")
        center_name = json_student_data.get('center_name', "-")
        booklet = json_student_data.get('booklet', "-")
        start_time = json_student_data.get('start_time', "-")
        que_ans = json_student_data.get('que_ans', "-")
        end_time = json_student_data.get('end_time', "-")
        suspicious_activity_detected = json_student_data.get('suspicious_activity_detected', "-")
        wallet_address = json_student_data.get('wallet_address', "-")
        user_mnemonic = json_student_data.get("user_mnemonic" , "-")

        transaction_id, wallet_address = self.blockchain_obj.deploy_data(
            student_id=student_id,
            exam_title=exam_title,
            city=city,
            center_name=center_name,
            suspicious_activity_detected=suspicious_activity_detected,
            start_time=start_time,
            end_time=end_time,
            booklet=booklet,
            que_ans=que_ans,
            user_mnemonic=user_mnemonic
        )
        
        json_student_data['transaction_id'] = transaction_id
        json_student_data['wallet_address'] = wallet_address

        ##################################################################################################################
        # Retry logic by append the data again to queue.
        
        if transaction_id == -1 and wallet_address == -1:
            # Error occured (possibly timeout error ) , hence again append the data to queue
            self.add_task(student_json_data= json_student_data)
        else:
            #####################################################################################################################
            # If transaction is successfull send json data to server to store data in database in server for backup
            requests.post(url= server_URL + insert_data_endpoint , json=json_student_data)


###############################################################################################################################################################################


class QnaApp(DefaultPage.DefaultApp):
    

    def __init__(self,city,center, booklet_selected, previous_question_and_answers,valid_user_blockchain_object ,valid_user_details ,question_index=0):
        super().__init__()

        self.data = DefaultPage.DefaultApp()
        self.bgcolor = "#8cc4fc"
        self.fontcolor = "#1848a0"
        self.answer_changed = False
        self.current_question_index = int(question_index)
        self.previous_question_answers = previous_question_and_answers
        self.selected_booklet = booklet_selected
        self.city = city
        self.center = center

        self.valid_user_blockchain_object = valid_user_blockchain_object
        self.valid_user_details = valid_user_details
        # Used to write blockchain transaction
        self.queue_obj = TaskQueue(blockchain_object=self.valid_user_blockchain_object)


        self.stopEvent = threading.Event()
        self.complete_task_thread = threading.Thread(target=self.complete_tasks_from_Queue, args=(self.queue_obj,))
        self.complete_task_thread.start()
        
        self.Qna()

    def perform_cleanup(self, event=None):
        self.stopEvent.set()
        self.kill_background_terminal()
        self.destroy()
        sys.exit(0)



    ##################################################################################################################
    def complete_tasks_from_Queue(self, obj:TaskQueue):
        while not self.stopEvent.is_set():
            if len(obj.task_queue) >0 :
                obj.write_data_to_blockchain()
            else:
                time.sleep(1)
                continue

    ##################################################################################################################


    # As soon as exam ends the json file of user should be destroyed 

    def destroy_user_file(self):

        filename = "deployed_user_data.json"
        if os.path.exists(filename):
            os.remove(filename)
            print(f'{filename} has been deleted.')
        else:
            print(f'{filename} does not exist.')

    def kill_background_terminal(self):
        script_path = 'kill-conhost.ps1'  

        # Define the command to open PowerShell and execute the script
        command = [
            'powershell.exe',  # PowerShell executable
            '-ExecutionPolicy', 'ByPass',  # Temporarily bypass(or set it to Unrestricted) execution policy
            '-File', script_path  # Path to the PowerShell script
        ]
        try:
            # Use subprocess.Popen to start the process
            subprocess.Popen(command)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Exit the system after all terminals are closed
        sys.exit(0)
        

    def Qna(self):
        # Configure fullscreen based on DefaultApp
        self.screen_width = self.data.screen_width
        self.screen_height = self.data.screen_height
        # self.api_url = "http://127.0.0.1:2222"
        
        # IF app crashesh or escape key is pressed then 
        self.bind("<Escape>", self.perform_cleanup)
        
        #############################################################################################################
        
                            # Using static Json file for question answer for now #
        # try:
        #     quiz_data_api_url = "https://flask-quiz-app-xi.vercel.app/"
        #     response = requests.get(quiz_data_api_url)
        #     if response.status_code == 200:
        #         print("Questions Data Received !!!")
        #         quiz_question_data = json.loads(response.text)

        # except Exception as e:
        #     print("Cannot retrieve questions !!!", e)
        #     messagebox.showerror("Data Retrieval Error", "Unable to fetch quiz data. Please try again later.")
        #     return
        self.Exam_Title = metadata.Exam_Title
        quiz_question_data = metadata.quiz_data

        
        ################################################################################################################
        number_of_questions_to_ask = 30
        booklet_data = quiz_question_data['booklets'][self.selected_booklet]
        questions = booklet_data["questions"][:number_of_questions_to_ask]
        options = booklet_data["options"][:number_of_questions_to_ask]
        correct_answers = booklet_data["answers"][:number_of_questions_to_ask]
        user_answers = [""] * len(questions)
        

        option_mapping = {}
        for i, opts in enumerate(options):
            option_mapping[i] = {chr(65 + j): opt for j, opt in enumerate(opts)}

        reverse_mapping = {chr(65+i): i for i in range(len(options[0]))}

        #################################################################################################################
        # Logic to automatically select the answers of the exam if the app was crashed
        if self.previous_question_answers:
            for question_no_index, answer in self.previous_question_answers.items():
                user_answers[int(question_no_index)-1] = answer
        #################################################################################################################

        main_frame = ctk.CTkFrame(
            self,
            width=self.screen_width,
            height=self.screen_height,
            corner_radius=10,
            fg_color=self.bgcolor,
        )
        main_frame.pack(fill="both", expand=True, padx=50, pady=50)

        def auto_width(text, min_width=10):
            required_width = max(len(text), min_width)
            return required_width

        def widgets():
            for widget in main_frame.winfo_children():
                widget.destroy()

            question = questions[self.current_question_index]
            option = options[self.current_question_index]

            ctk.CTkLabel(
                main_frame,
                text=f"{self.Exam_Title} Questions",
                font=(self.data.header_font, self.data.headerfontsize, "bold"),
                text_color="#c35e6c",
                bg_color=self.bgcolor,
            ).pack(padx=20, pady=(10, 10), anchor="nw")
            ctk.CTkLabel(
                main_frame,
                text=f"({self.current_question_index + 1} of {len(questions)})",
                font=(self.data.header_font, self.data.fontsize),
                text_color=self.fontcolor,
                bg_color=self.bgcolor,
            ).pack(padx=(0, 20), pady=(10, 5), anchor="ne")

            upper_line = ctk.CTkCanvas(main_frame, height=1, width=self.screen_width)
            upper_line.pack(fill="both")

            que_label = ctk.CTkLabel(
                main_frame,
                text=f"Question {self.current_question_index + 1}:",
                font=(self.data.font, 22, "underline"),
                wraplength=self.screen_width,
                anchor="w",
                justify="left",
                bg_color=self.bgcolor,
                text_color=self.fontcolor,
            )
            que_label.pack(padx=20, pady=(10, 30), anchor="w")
            que_text = ctk.CTkLabel(
                main_frame,
                text=question,
                font=(self.data.font, 20),
                width=auto_width(question),
                wraplength=self.screen_width - 30,
                anchor="w",
                justify="left",
                bg_color=self.bgcolor,
                text_color=self.fontcolor,
            )
            que_text.pack(padx=20, pady=(5, 50), anchor="w")

            selected_option = ctk.StringVar(value=user_answers[self.current_question_index])

            def select_option(value):
                selected_option.set(value)
                user_answers[self.current_question_index] = value
                self.answer_changed = True
                widgets()

            for i, opt in enumerate(option):
                letter = chr(65 + i)
                ctk.CTkRadioButton(
                    main_frame,
                    text=f" {opt}",
                    font=(self.data.font, self.data.fontsize),
                    value=letter,
                    variable=selected_option,
                    text_color=self.fontcolor,
                    bg_color=self.bgcolor,
                    command=lambda val=letter: select_option(val),
                ).pack(padx=20, pady=10, anchor="w")

            button_frame = ctk.CTkFrame(main_frame, fg_color=self.bgcolor)
            button_frame.pack(fill="both", expand=True, pady=(50, 20), side="bottom")

            def prev_question():
                if self.current_question_index > 0:
                    self.current_question_index -= 1
                    selected_option.set(user_answers[self.current_question_index])
                    self.answer_changed = False
                    widgets()

            def next_question():
                if not selected_option.get():
                    messagebox.showerror("Error", "Please select an answer before proceeding.")
                    return
                if self.answer_changed:
                    user_answers[self.current_question_index] = selected_option.get()
                    selected_ans = user_answers[self.current_question_index]

                    student_data = {

                        "student_id":self.valid_user_details.get("userID"),
                        "wallet_address": self.valid_user_details.get("user_wallet_address"),
                        "exam_title" : self.Exam_Title,
                        "city" : f"{self.city}",
                        "center_name" : f"{self.center}",
                        "booklet": f"{self.selected_booklet}",
                        "start_time": "-",
                        "que_ans": f"{self.current_question_index+1}-{selected_ans}",
                        "end_time": "-",
                        "suspicious_activity_detected":"no",
                        "user_mnemonic" : self.valid_user_details.get("user_mnemonic"),
                    }

                    
                    self.queue_obj.add_task(student_json_data=student_data)
                    self.answer_changed = False

                if self.current_question_index < len(questions) - 1:
                    self.current_question_index += 1
                    selected_option.set(user_answers[self.current_question_index])
                    widgets()

            prev_button = ctk.CTkButton(
                button_frame,
                text="← Previous",
                bg_color=self.bgcolor,
                fg_color="#cf7582",
                hover_color="#f48b9c",
                text_color="#fff",
                font=(self.data.font, self.data.fontsize),
                height=40,
                command=prev_question,
                background_corner_colors=[self.bgcolor, self.bgcolor, self.bgcolor, self.bgcolor]
            )
            if self.current_question_index > 0:
                prev_button.pack(side="left", padx=20)

            next_button = ctk.CTkButton(
                button_frame,
                text="Next →",
                bg_color=self.bgcolor,
                fg_color="#84a921",
                hover_color="#99c226",
                text_color="#fff",
                height=40,
                font=(self.data.font, self.data.fontsize),
                command=next_question,
                background_corner_colors=[self.bgcolor, self.bgcolor, self.bgcolor, self.bgcolor]
            )
            if self.current_question_index < len(questions) - 1:
                next_button.pack(side="right", padx=20)
            else:
                def thank_you():
                    # This will delete the json file of deployed user
                    # For debuggin user file is not deleted
                    
                    self.destroy_user_file()



                    answer = messagebox.askquestion(
                    "Confirm", "Confirm you want to submit answers?"
                    )
                    if answer == "yes":
                        pass
                    else:
                        widget()

                    user_answers[self.current_question_index] = selected_option.get()
                    selected_ans = user_answers[self.current_question_index]
                    current_time = datetime.datetime.now()
                    date_str = f"{current_time.day}/{current_time.month}/{current_time.year}"
                    time_str = f"{current_time.hour}:{current_time.minute}:{current_time.second} {current_time.strftime('%p')} "
                    quiz_end_time = f"{date_str}-{time_str}"


                    student_data = {
                        "student_id":self.valid_user_details["userID"],
                        "wallet_address": self.valid_user_details["user_wallet_address"],
                        "exam_title" : self.Exam_Title,
                        "city" : f"{self.city}",
                        "center_name" : f"{self.center}",
                        "booklet": f"{self.selected_booklet}",
                        "start_time": "-",
                        "que_ans": f"{self.current_question_index+1}-{selected_ans}",
                        "end_time": "-",
                        "suspicious_activity_detected":"no",
                        "user_mnemonic" : self.valid_user_details["user_mnemonic"],
                    }

                    # Push json data for last question
                    self.queue_obj.add_task(student_json_data=student_data)
                    

                    endtime_data = {
                        "student_id":self.valid_user_details["userID"],
                        "wallet_address": self.valid_user_details["user_wallet_address"],
                        "exam_title" : self.Exam_Title,
                        "city" : f"{self.city}",
                        "center_name" : f"{self.center}",
                        "booklet": f"{self.selected_booklet}",
                        "start_time": "-",
                        "que_ans": "-",
                        "end_time": quiz_end_time,
                        "suspicious_activity_detected":"no",
                        "user_mnemonic" : self.valid_user_details["user_mnemonic"],
                    }
                    
                    self.queue_obj.add_task(student_json_data=endtime_data)


                    for widget in main_frame.winfo_children():
                        widget.destroy()


                    ctk.CTkLabel(
                        main_frame,
                        text="Thank you for taking the exam!",
                        font=(self.data.header_font, 22),
                        text_color=self.fontcolor,
                        bg_color=self.bgcolor,
                    ).pack(padx=20, pady=20, anchor="center")

                    def close_app():

                        while True:
                            if len(self.queue_obj.task_queue) > 0:
                                messagebox.showinfo("Wait" , "Transactions are being written!!")
                            else:
                                self.perform_cleanup()
                                messagebox.showinfo("Done" , "You can close this window now !!")
                                break


                        if self.winfo_exists():
                            self.destroy()
                            

                    # Create and display the close button
                    close_button = ctk.CTkButton(
                        main_frame,
                        text="Close",
                        bg_color=self.bgcolor,
                        fg_color="#ff5722",
                        hover_color="#ff7043",
                        text_color="#fff",
                        font=(self.data.font, self.data.fontsize),
                        command=close_app,
                    )
                    close_button.pack(pady=20, anchor="center")
                finish_button = ctk.CTkButton(
                    button_frame,
                    text="Submit Exam",
                    bg_color=self.bgcolor,
                    fg_color="#4caf50",
                    hover_color="#81c784",
                    text_color="#fff",
                    height=40,
                    font=(self.data.font, self.data.fontsize),
                    command=thank_you,
                    background_corner_colors=[self.bgcolor, self.bgcolor, self.bgcolor, self.bgcolor]
                )
                finish_button.pack(side="right", padx=20)  # This line was moved here
        widgets()


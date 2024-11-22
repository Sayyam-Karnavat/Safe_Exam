import requests
from tkinter import messagebox
from PIL import Image,ImageSequence
import customtkinter as ctk
from tkinter import ttk
import DefaultPage
import metadata
from deploy_file import Blockchain
import json
from start_AI import start_wired_screen_AI_model , start_wireless_screen_AI_model


class LoginApp(DefaultPage.DefaultApp):
 
    def __init__(self):
        # Test
        super().__init__()
        self.data = DefaultPage.DefaultApp()
        self.booklet_selected= metadata.Booklet
        self.cities = metadata.cities
        self.centers = metadata.centers

        
        self.selected_city = ""
        self.selected_center = []


        self.api_url = metadata.server_URL
        self.insert_data_endpoint = metadata.insert_data_endpoint
        self.validate_user_endpoint = metadata.validate_user_endpoint

        self.valid_user = "NAN"
        self.Exam_Title = metadata.Exam_Title

        self.Login()
 
    def Login(self):
        # Configure fullscreen based on DefaultApp
        self.screen_width = self.data.screen_width
        self.screen_height = self.data.screen_height
 
        # Load background image
        bg_img = ctk.CTkImage(Image.open("./Assets/bg_1.png"), size=(self.screen_width, self.screen_height))
        self.bg_image_label = ctk.CTkLabel(self, image=bg_img, text="")
        self.bg_image_label.image = bg_img  # Keep reference to avoid garbage collection
        self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Add login header
        date_title=ctk.CTkLabel(self, text=f"{self.Exam_Title}\n{self.data.date} {self.data.time_str}", font=(self.data.header_font, self.data.headerfontsize, "bold"), text_color=self.data.fontcolor, bg_color=self.data.bgcolor)
        date_title.pack(padx=30,pady=20,anchor="ne")

        opening_frame = ctk.CTkFrame(self, height=300,width=self.screen_width/2,bg_color=self.data.bgcolor,fg_color=self.data.bgcolor, background_corner_colors=[self.data.bgcolor,self.data.bgcolor,self.data.bgcolor,self.data.bgcolor])
        opening_frame.pack(padx=10,side="left")

        user_img = ctk.CTkImage(Image.open("./Assets/logo.png"), size=(100, 100))
        self.user_label = ctk.CTkLabel(opening_frame, image=user_img, text="")
        self.user_label.image = user_img  # Keep reference to avoid garbage collection
        self.user_label.pack(anchor="w")

        wlcm_label =  ctk.CTkLabel(opening_frame,text="Welcome,",font=(self.data.header_font, self.data.headerfontsize, "bold"),text_color=self.data.fontcolor)
        wlcm_label.pack(padx=20,anchor="w")

        title_label = ctk.CTkLabel(opening_frame,text="SafeExam Portal",font=(self.data.header_font, self.data.headerfontsize, "bold"),text_color=self.data.fontcolor)
        title_label.pack(padx=20,anchor="w")

        subtitle_label = ctk.CTkLabel(opening_frame,text="Login to start your exam with confidence.Your information is handled with the utmost care and securely stored to ensure it stays safe and protected every step of the way.",font=(self.data.font, 16),text_color="#a9afb2",wraplength=self.screen_width/2.5)
        subtitle_label.pack(padx=20,pady=(5,40),anchor="w")
        
        combo_lbl_frame = ctk.CTkFrame(opening_frame, fg_color=self.data.bgcolor,corner_radius=10)
        combo_lbl_frame.pack(anchor="w")

        self.city = ctk.CTkLabel(combo_lbl_frame,width=135,height=30,text="Select City",text_color=self.data.fontcolor, font=(self.data.font,16))
        self.city.pack(side="left",padx=(0,20))

        self.center = ctk.CTkLabel(combo_lbl_frame,width=135,height=30,text="Select Center",text_color=self.data.fontcolor, font=(self.data.font,16))
        self.center.pack(side="right",padx=20)

        combo_frame = ctk.CTkFrame(opening_frame, fg_color=self.data.bgcolor,corner_radius=10)
        combo_frame.pack(padx=10,anchor="w")

        self.city_lbl = ctk.CTkLabel(combo_frame,width=140,height=40,text="",fg_color=self.data.fontcolor, font=(self.data.font, self.data.fontsize),corner_radius=5)
        self.city_lbl.pack(side="left",padx=10,pady=(0,10))

        self.center_lbl = ctk.CTkLabel(combo_frame,width=140,height=40,text="",fg_color=self.data.fontcolor, font=(self.data.font, self.data.fontsize),corner_radius=5)
        self.center_lbl.pack(side="right",padx=20,pady=(0,10))

        self.city_combo = ttk.Combobox(combo_frame,height= 100, width= 10,values=self.cities,font=(self.data.font, self.data.fontsize))
        self.city_combo.set("City")
        self.city_combo.bind("<<ComboboxSelected>>",self.update_center)
        self.city_combo.place(in_=self.city_lbl, relx=0.5, rely=0.5, anchor="center")

        self.center_combo = ttk.Combobox(combo_frame,height=40,width=10,values=self.selected_center, font=(self.data.font, self.data.fontsize))
        self.center_combo.set("Center")
        self.center_combo.place(in_=self.center_lbl, relx=0.5, rely=0.5, anchor="center")

        # Add username/mobile number entry
        ctk.CTkLabel(opening_frame, text="Enter Username", bg_color=self.data.bgcolor, font=(self.data.font,16), text_color=self.data.fontcolor).pack(anchor="w",padx=20)
        self.mobile_entry = ctk.CTkEntry(opening_frame,placeholder_text="Username",width=315,height=40, font=(self.data.font, self.data.fontsize),border_width=0,corner_radius=5)
        self.mobile_entry.pack(anchor="w",padx=20,pady=(0,10))
 
        # Add password entry
        ctk.CTkLabel(opening_frame, text="Enter Password", bg_color=self.data.bgcolor, font=(self.data.font,16), text_color=self.data.fontcolor).pack(anchor="w",padx=20)
        self.password_entry = ctk.CTkEntry(opening_frame,placeholder_text="Password" ,width=315,height=40, font=(self.data.font, self.data.fontsize),border_width=0,corner_radius=5, show='*')
        self.password_entry.pack(anchor="w",padx=20,pady=(0,10))
 
        # Add login button
        ctk.CTkButton(opening_frame,hover_color="#7bb2ff", text="Login",fg_color="#007cff", width=120, height=50, command=self.check_credentials, font=(self.data.font, self.data.fontsize),border_width=0,corner_radius=5, text_color=self.data.fontcolor).pack(anchor="w",padx=110,pady=20)
        
             
    def update_center(self, event):
        self.selected_city = self.city_combo.get()
        self.selected_center = self.centers.get(self.selected_city, [])
        self.center_combo['values'] = self.selected_center
        self.city_value= self.city_combo.get()
        self.center_combo.bind("<<ComboboxSelected>>", self.on_center_selected)
       
    def on_center_selected(self, event):
        self.center_value = self.center_combo.get()  # Get the selected value from the center combo box
           
 
    def open_loading_window(self):
        # Create a pop-up window for loading
        loading_window = ctk.CTkToplevel(self)
        loading_window.title("Loading")
        loading_window.overrideredirect(True)
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()
 
        window_width = 300
        window_height = 180
        x_position = parent_x + (parent_width - window_width) // 2
        y_position = parent_y + (parent_height - window_height) // 2
 
        loading_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
 
        # Load the GIF and prepare frames
        gif_path = "./Assets/loading.gif"
        gif_image = Image.open(gif_path)
        frames = [ctk.CTkImage(frame.copy(),size=((200,100))) for frame in ImageSequence.Iterator(gif_image)]
        label = ctk.CTkLabel(loading_window,text="Loading, please wait...", compound="top",height=window_height,width=window_width,font=(self.data.font, self.data.fontsize),bg_color="#fff")
        label.pack(expand=True)
        # Function to update the frame
        def update_frame(frame_index):
            if loading_window.winfo_exists():  # Check if the window still exists
                label.configure(image=frames[frame_index])
                frame_index = (frame_index + 1) % len(frames)
                loading_window.after(100, update_frame, frame_index)  # Update every 100ms
 
        update_frame(0)
 
        # Simulate processing task
        # self.after(3000, lambda: self.finish_loading(loading_window))
 
    def finish_loading(self,loading_window=None):
        if loading_window and loading_window.winfo_exists():  # Check if the window still exists
            loading_window.destroy()
 
 
    def check_credentials(self):

        self.GUI_user_id = self.mobile_entry.get()
        self.GUI_password = self.password_entry.get()

        check_user_json = {
            "user_id" : self.GUI_user_id,
            "password" : self.GUI_password
        }

        validate_response = requests.post(url=self.api_url +self.validate_user_endpoint , json=check_user_json)

        

        if validate_response.status_code == 200:
            # Before creating blockchain object check if user has already logged in 
            try:
                with open("deployed_user_data.json" , "r") as f:
                    # This will contain private_key, app_id etc of user who has already deployed the application
                    self.user_json_data = json.load(fp=f)
                    f.close()
                
                # After validation set valid user so that further it can be used in QNA page as well for writing transactions
                self.valid_user_blockchain_object = Blockchain(user_id=self.GUI_user_id ,user_already_exist=True , user_json_data=self.user_json_data)
                # This will give deployed app id , userID , password etc. 
                self.valid_user_details = self.valid_user_blockchain_object.get_generated_user_details()

                print("User Already exists !!!")

            except Exception as e:
                print("User does not exist !!! \n" , e)

                # IF user logs in for first time then application will be deployed
                self.valid_user_blockchain_object = Blockchain(user_id=self.GUI_user_id , user_already_exist=False)
                self.valid_user_details = self.valid_user_blockchain_object.get_generated_user_details()

                with open("deployed_user_data.json","w") as f:
                    json.dump(obj=self.valid_user_details , fp=f)
                    f.close()


            if (self.city_value and self.center_value) :
                self.open_loading_window()
                self.after(100 , lambda : self.process_login())
            else:
                messagebox.showerror("Selection Error" , "Select both city and center !!!")
        else:
            messagebox.showerror("Login Error", "Invalid mobile number or password.")
 
    def process_login(self):
        # transaction_id = deploy_data("1234","Bank Exam",self.city_value,self.center_value,self.booklet_selected, self.data.start_time, "-", "No","-")
        #######################################################################################
        # Write data to blockchain via object created

        student_json_data = {
            "student_id" : self.valid_user_details['userID'],
            "exam_title" : self.Exam_Title,
            "city" : self.city_value,
            "center_name": self.center_value,
            "booklet": self.booklet_selected,
            "start_time" : self.data.start_time,
            "que_ans":"-",
            "end_time":"-",
            "suspicious_activity_detected" : "-",
            "user_mnemonic":self.valid_user_details['user_mnemonic'], # Not to be stored in server
            "transaction_id" : "-",
            "wallet_address" : "-"
        }


        transaction_id , wallet_address = self.valid_user_blockchain_object.deploy_data(
            student_id=student_json_data['student_id'],
            exam_title=student_json_data['exam_title'],
            city=student_json_data['city'],
            center_name=student_json_data['center_name'],
            booklet=student_json_data['booklet'] ,
            start_time=student_json_data['start_time'],
            que_ans=student_json_data['que_ans'],
            end_time=student_json_data['end_time'],
            suspicious_activity_detected="-",
            user_mnemonic=student_json_data['user_mnemonic']
        )

        student_json_data['transaction_id'] = transaction_id
        student_json_data['wallet_address'] = wallet_address
        
        #######################################################################################

        # Send the data to be written on database which is located at server

        
        requests.post(url= self.api_url + self.insert_data_endpoint , json=student_json_data)
        #######################################################################################
        self.destroy()
        self.open_quiz_page()
 
    def open_quiz_page(self):

        ############################################################################################
        # Start AI after user logs in
        start_wireless_screen_AI_model()
        start_wired_screen_AI_model()
        ############################################################################################
        try:
            import QnaPage # Do not move this import to start of code  it will give pyimage does not exist error because resources are already in use by LoginPage


            #####################################################################################
            # For debugging stopped resume quiz service #
            try:

                previous_question_answers = self.valid_user_blockchain_object.get_crash_exam_details(application_id=self.valid_user_details.get("app_id"))
            except Exception as e :
                print("Error getting crash data at Login Page !!!")

            if previous_question_answers:
                resume_question_index = max(previous_question_answers.keys(), key=lambda k: int(k))
            else:
                previous_question_answers = {}
                resume_question_index = 0
            #######################################################################################
            
            qna=QnaPage.QnaApp(city = self.city_value,center = self.center_value,booklet_selected=self.booklet_selected , question_index=resume_question_index , previous_question_and_answers=previous_question_answers , valid_user_blockchain_object = self.valid_user_blockchain_object , valid_user_details=self.valid_user_details)
            qna.mainloop()
        except IndexError as e:
            messagebox.showinfo("Exam already given!!!" , "Exam is Already completed")
        except Exception as e:
            print("Error :-" , e)
 
 
if __name__ == "__main__":
    # db.delete_all_records()
    app = LoginApp()
    app.mainloop()
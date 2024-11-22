import datetime
import customtkinter as ctk

class DefaultApp(ctk.CTk):

    def __init__(self):
        # Test
        super().__init__()
        self.default()

    def default(self):
        # Close Full screen
        self.bind("<Escape>", self.exit_fullscreen)

        # Full Screen
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.overrideredirect(True)

        self.header_font="Arial"
        self.font = "Arial"
        self.bgcolor = "#004aad"
        self.fontcolor = "#fff"
        self.fontsize=18
        self.headerfontsize=26
        self.time = datetime.datetime.now()
        self.date = f"{self.time.day}/{self.time.month}/{self.time.year}"
        self.time_str = f"{self.time.hour}:{self.time.minute}:{self.time.second} {self.time.strftime('%p')} "
        self.start_time = f"{self.date} {self.time_str}"
        self.credentials = {
            "user":"admin",
            "password":"admin"
        }

    def exit_fullscreen(self, event=None):
        self.overrideredirect(False)  
        self.attributes('-fullscreen', False)  
        self.quit() 

if __name__ == "__main__":
    app = DefaultApp()
    app.mainloop()

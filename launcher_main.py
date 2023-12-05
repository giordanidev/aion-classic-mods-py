#TODO LAUNCHER TO CHECK PROGRAM UPDATES
#DOWNLOAD AND INSTALL UPDATE? YES/NO.

from functions import *
import tkinter as tk, customtkinter as ctk, logging

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(translateText("app_title") + translateText("app_launcher_title") + translateText("app_launcher_version"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # System appearance
        ctk.set_appearance_mode(app_config.get('app', 'theme'))
        ctk.set_default_color_theme(app_config.get('app', 'color').lower())

        configJson()



        #center the app on screen
        window_width = 350
        window_height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        print(self.winfo_screenwidth())
        print(self.winfo_screenheight())
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

app = App()
app.iconbitmap("./config/img/AionClassicMods.ico")
app.resizable(0, 0)
app.mainloop()

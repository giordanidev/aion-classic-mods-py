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

        #center app on main screen 
        centerApp(350, 150, self)

app = App()
app.iconbitmap("./config/img/AionClassicMods.ico")
app.resizable(0, 0)
app.mainloop()

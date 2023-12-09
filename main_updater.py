#TODO
#ADD OWN FUNCTIONS FILE/LOGS

from functions import *
import tkinter as tk, customtkinter as ctk, logging

logging.debug(f"{sys._getframe().f_code.co_name}() -> Updater initialized.")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        global app_config

        self.title(translateText("app_title") + translateText("app_updater_title") + translateText("app_updater_version"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # System appearance
        ctk.set_appearance_mode(app_config['theme'])
        ctk.set_default_color_theme(app_config['color'].lower())

        #center app on main screen 
        centerApp(450, 150, self)

        if app_config['on_start'] == True:

            self.updaterFrame = ctk.CTkFrame(self)
            self.updaterFrame.grid(row=0, column=0, sticky="new")
            self.updaterFrame.configure(fg_color="transparent")
            self.updaterFrame.grid_columnconfigure(1, weight=1)

            self.infoLabel = ctk.CTkLabel(self.updaterFrame, text="Aguardando")
            self.infoLabel.grid(row=0, column=0, columnspan=2, padx=padx_both, pady=pady_both, sticky="we")
            
            cloud_version = checkUpdates()
            
            self.iconbitmap(app_icon)
            self.resizable(0, 0)
            self.mainloop()
        else:
            print("QUIT")
            self.destroy()

app = App()
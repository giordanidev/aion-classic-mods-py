#TODO UPDATER TO CHECK PROGRAM UPDATES
#DOWNLOAD AND INSTALL UPDATE? YES/NO.

from functions import *
import tkinter as tk, customtkinter as ctk, logging

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        def appConfigJson():
            with open(".\\config\\config.json", encoding='utf-8') as f:
                config_json = json.load(f)
            f.close
            return config_json
        app_config_json = appConfigJson()

        self.title(translateText("app_title") + translateText("app_updater_title") + translateText("app_updater_version"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # System appearance
        ctk.set_appearance_mode(app_config_json["theme"])
        ctk.set_default_color_theme(app_config_json["color"].lower())

        configJson()

        #center app on main screen 
        centerApp(450, 150, self)

        if app_config_json["on_start"] == True:

            self.updaterFrame = ctk.CTkFrame(self)
            self.updaterFrame.grid(row=0, column=0, sticky="new")
            self.updaterFrame.configure(fg_color="transparent")
            self.updaterFrame.grid_columnconfigure(1, weight=1)

            self.infoLabel = ctk.CTkLabel(self.updaterFrame, text="Aguardando")
            self.infoLabel.grid(row=0, column=0, columnspan=2, padx=padx_both, pady=pady_both, sticky="w")
            
            cloud_version = checkUpdates()

            
            self.iconbitmap("./config/img/AionClassicMods.ico")
            self.resizable(0, 0)
            self.mainloop()
        else:
            print("QUIT")
            self.destroy()

app = App()
import customtkinter as ctk
from app_config import appSettings

class mainTabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        appConfig = appSettings.appConfigRead()

        # System appearance
        ctk.set_appearance_mode(appConfig[0].get('app', 'theme'))
        ctk.set_default_color_theme(appConfig[0].get('app', 'color').lower())

        # create tabs
        self.add("App")
        appTab = self.tab("App")
        appTab.grid_rowconfigure(0, weight=1) 
        appTab.grid_columnconfigure(0, weight=1)

        self.add("Config")
        configTab = self.tab("Config")
        configTab.grid_rowconfigure(4, weight=1)
        configTab.grid_columnconfigure(1, weight=1)
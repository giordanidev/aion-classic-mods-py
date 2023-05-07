import customtkinter as ctk
from app_config import appSettings
from app_tabs import mainTabs
from app_functions import appFunctions

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aion Classic 'Mods' by Load")

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        # Read configs from file
        def appGetConfigs():
            global appConfigRead
            global configFullPath
            appConfigRead = appSettings.appConfigRead()[0]
            configFullPath = appSettings.appConfigRead()[1]
        appGetConfigs()

        ctk.set_default_color_theme(appConfigRead.get('app', 'color').lower())

        self.tabsView = mainTabs(self)
        self.tabsView.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")
        self.current_ui = []
        self.current_ui.append(self.tabsView)
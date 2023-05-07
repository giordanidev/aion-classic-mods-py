import tkinter as tk
import customtkinter as ctk
from app_tabs import mainTabs
from app_functions import appFunctions

class appConfigTab:
    def create_config_tab(self):
        # Config tab widgets > Left
        self.configLeftFrame = ctk.CTkFrame(mainTabs.configTab)
        self.configLeftFrame.grid(row=0, column=0, sticky="ns")
        self.configLeftFrame.configure(fg_color="transparent")

        self.themeLabel = ctk.CTkLabel(self.configLeftFrame, text="App Theme:")
        self.themeLabel.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="e")
        self.themeLabel.configure(font=("", 12, "bold"))
        self.colorLabel = ctk.CTkLabel(self.configLeftFrame, text="App Color:")
        self.colorLabel.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
        self.colorLabel.configure(font=("", 12, "bold"))
        self.regionLabel = ctk.CTkLabel(self.configLeftFrame, text="Region Selection:")
        self.regionLabel.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        self.regionLabel.configure(font=("", 12, "bold"))
        self.naPathLabel = ctk.CTkLabel(self.configLeftFrame, text="NA Path:")
        self.naPathLabel.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="e")
        self.naPathLabel.configure(font=("", 12, "bold"))
        self.euPathLabel = ctk.CTkLabel(self.configLeftFrame, text="EU Path:")
        self.euPathLabel.grid(row=4, column=0, padx=(0, 5), pady=5, sticky="e")
        self.euPathLabel.configure(font=("", 12, "bold"))

        # Config tab widgets > Right
        self.configRightFrame = ctk.CTkFrame(mainTabs.configTab)
        self.configRightFrame.grid(row=0, column=1, sticky="nsew")
        self.configRightFrame.configure(fg_color="transparent")
        self.configRightFrame.grid_columnconfigure((0, 1, 2), weight=1)  # configure grid system

        self.themeButton = ctk.CTkSegmentedButton(self.configRightFrame,values=["System", "Dark", "Light"], command=appFunctions.change_theme_event)
        self.themeButton.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), columnspan=3, sticky="ew")
        self.colorButton = ctk.CTkSegmentedButton(self.configRightFrame, values=["Blue", "Dark-blue", "Green"], command=appFunctions.change_color_event)
        self.colorButton.grid(row=1, column=0, padx=(5, 0), pady=(5, 5), columnspan=3, sticky="ew")
        
        self.regionRadio = tk.IntVar()
        #regionSelection() reference

        self.naRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text="Classic NA",
                                                    command=appFunctions.regionSelection,
                                                    variable=self.regionRadio,
                                                    value=0)
        self.naRadio.grid(row=2, column=0, padx=(5, 0), pady=8, sticky="w")
        self.euRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text="Classic EU",
                                                    command=appFunctions.regionSelection,
                                                    variable=self.regionRadio,
                                                    value=1)
        self.euRadio.grid(row=2, column=1, pady=8, sticky="w")
        self.bothRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text="Both",
                                                    command=appFunctions.regionSelection,
                                                    variable=self.regionRadio,
                                                    value=2)
        self.bothRadio.grid(row=2, column=2, pady=8, sticky="w")

        self.naPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="C:\Games\Aion Classic NA")
        self.naPathEntry.grid(row=3, column=0, padx=(5, 0), pady=(5, 5), columnspan=2, sticky="we")
        self.naPathButton = ctk.CTkButton(self.configRightFrame, text="Select Path", command="")
        self.naPathButton.grid(row=3, column=2, padx=(5, 0), pady=(5, 5))

        self.euPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="C:\Games\Aion Classic EU")
        self.euPathEntry.grid(row=4, column=0, padx=(5, 0), pady=(5, 5), columnspan=2, sticky="we")
        self.euPathButton = ctk.CTkButton(self.configRightFrame, text="Select Path", command="")
        self.euPathButton.grid(row=4, column=2, padx=(5, 0), pady=(5, 5))

        self.configTextbox = ctk.CTkTextbox(mainTabs.configTab)
        self.configTextbox.grid(row=5, column=0, columnspan=2, pady=(5, 0), sticky="nsew")
        self.configTextbox.configure(state="disabled")
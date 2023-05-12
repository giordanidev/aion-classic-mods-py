import tkinter as tk
import customtkinter as ctk
from app_functions import *

# Read configs from file
load_configs = app_config_read()
app_config = load_configs[0]
config_full_path = load_configs[0]

first_run()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aion Classic 'Mods' by Load")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        load_configs = app_config_read()
        app_config = load_configs[0]

        # System appearance
        ctk.set_appearance_mode(app_config.get('app', 'theme'))
        ctk.set_default_color_theme(app_config.get('app', 'color').lower())

        self.tabsView = createTabs(self, self.change_color_event)
        self.tabsView.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")

        self.current_ui = []
        self.current_ui.append(self.tabsView)

    def change_color_event(self, color):
        ctk.set_default_color_theme(color.lower())
        app_config = app_config_read()[0]
        app_config.set('app', 'color', color)
        app_config_write(app_config)
        self.reset_current_ui()

    def reset_current_ui(self):
        for widget in self.current_ui:
            widget.destroy()
        self.tabsView = createTabs(self, self.change_color_event)
        self.tabsView.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")
        createTabs.set(self.tabsView, "Config")

class createTabs(ctk.CTkTabview):
    def __init__(self, master, change_color_event, **kwargs):
        super().__init__(master=master, **kwargs)

        print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> createTabs() initialized.")

        app_config = app_config_read()[0]

        print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> app_config.items(): \n{app_config.items('app')}")

        # create tabs
        self.add("App")
        appTab = self.tab("App")
        appTab.grid_rowconfigure(0, weight=1)
        appTab.grid_columnconfigure(0, weight=1)

        self.add("Config")
        configTab = self.tab("Config")
        configTab.grid_rowconfigure(4, weight=1)
        configTab.grid_columnconfigure(1, weight=1)

        # App tab widgets
        self.appTopFrame = ctk.CTkFrame(appTab)
        self.appTopFrame.grid(row=0, column=0, sticky="new")
        self.appTopFrame.configure(fg_color="transparent")
        self.appTopFrame.grid_columnconfigure(1, weight=1)

        self.voiceButton = ctk.CTkButton(self.appTopFrame, text="Check Files", command="")
        self.voiceButton.grid(row=0, column=2, padx=(5, 0), pady=5)
        self.voiceButton.configure(font=("", 13, "bold"), state="disabled")

        self.voiceLabel = ctk.CTkLabel(self.appTopFrame, text="KR Voices:")
        self.voiceLabel.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
        self.voiceLabel.configure(font=("", 12, "bold"))
        self.filterLabel = ctk.CTkLabel(self.appTopFrame, text="Chat Filter:")
        self.filterLabel.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        self.filterLabel.configure(font=("", 12, "bold"))
        self.hitLabel = ctk.CTkLabel(self.appTopFrame, text="JP Fonts:")
        self.hitLabel.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="e")
        self.hitLabel.configure(font=("", 12, "bold"))

        self.voiceReturnLabel = ctk.CTkLabel(self.appTopFrame, text="Koren Voices are installed.")
        self.voiceReturnLabel.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.filterReturnLabel = ctk.CTkLabel(self.appTopFrame, text="Chat Filter is up to date.")
        self.filterReturnLabel.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.hitReturnLabel = ctk.CTkLabel(self.appTopFrame, text="JP Fonts are installed.")
        self.hitReturnLabel.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.voiceButton = ctk.CTkButton(self.appTopFrame, text="Install", command="")
        self.voiceButton.grid(row=1, column=2, padx=(5, 0), pady=5)
        self.filterButton = ctk.CTkButton(self.appTopFrame, text="Install", command="")
        self.filterButton.grid(row=2, column=2, padx=(5, 0), pady=5)
        self.hitButton = ctk.CTkButton(self.appTopFrame, text="Install", command="")
        self.hitButton.grid(row=3, column=2, padx=(5, 0), pady=5)

        """
        self.appTextbox = ctk.CTkTextbox(self.appTopFrame)
        self.appTextbox.grid(row=4, column=0, columnspan=3, pady=(5, 0), sticky="nsew")
        self.appTextbox.configure(state="disabled")
        """

        # Config tab widgets > Left
        self.configLeftFrame = ctk.CTkFrame(configTab)
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
        self.configRightFrame = ctk.CTkFrame(configTab)
        self.configRightFrame.grid(row=0, column=1, sticky="nsew")
        self.configRightFrame.configure(fg_color="transparent")
        self.configRightFrame.grid_columnconfigure((0, 1, 2), weight=1)

        self.themeButton = ctk.CTkSegmentedButton(self.configRightFrame,values=["System", "Dark", "Light"], command=self.change_theme_event)
        self.themeButton.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), columnspan=3, sticky="ew")
        self.colorButton = ctk.CTkSegmentedButton(self.configRightFrame, values=["Blue", "Dark-blue", "Green"], command=change_color_event)
        self.colorButton.grid(row=1, column=0, padx=(5, 0), pady=(5, 5), columnspan=3, sticky="ew")
        
        self.regionRadio = tk.IntVar()

        def region_selection():
            app_config = app_config_read()[0]
            app_config.set('app', 'region', str(self.regionRadio.get()))
            app_config_write(app_config)
            if (self.regionRadio.get() == 0):
                self.naPathLabel.configure(state="disabled")
                self.naPathEntry.configure(state="disabled")
                self.naPathButton.configure(state="disabled")
                self.euPathLabel.configure(state="disabled")
                self.euPathEntry.configure(state="disabled")
                self.euPathButton.configure(state="disabled")
            elif (self.regionRadio.get() == 1):
                self.naPathLabel.configure(state="normal")
                self.naPathEntry.configure(state="normal")
                self.naPathButton.configure(state="normal")
                self.euPathLabel.configure(state="disabled")
                self.euPathEntry.configure(state="disabled")
                self.euPathButton.configure(state="disabled")
            elif (self.regionRadio.get() == 2):
                self.naPathLabel.configure(state="disabled")
                self.naPathEntry.configure(state="disabled")
                self.naPathButton.configure(state="disabled")
                self.euPathLabel.configure(state="normal")
                self.euPathEntry.configure(state="normal")
                self.euPathButton.configure(state="normal")
            elif (self.regionRadio.get() == 3):
                self.naPathLabel.configure(state="normal")
                self.naPathEntry.configure(state="normal")
                self.naPathButton.configure(state="normal")
                self.euPathLabel.configure(state="normal")
                self.euPathEntry.configure(state="normal")
                self.euPathButton.configure(state="normal")

        self.naRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text="Classic NA",
                                                    command=region_selection,
                                                    variable=self.regionRadio,
                                                    value=1)
        self.naRadio.grid(row=2, column=0, padx=(5, 0), pady=8, sticky="w")
        self.euRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text="Classic EU",
                                                    command=region_selection,
                                                    variable=self.regionRadio,
                                                    value=2)
        self.euRadio.grid(row=2, column=1, pady=8, sticky="w")
        self.bothRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text="Both",
                                                    command=region_selection,
                                                    variable=self.regionRadio,
                                                    value=3)
        self.bothRadio.grid(row=2, column=2, pady=8, sticky="w")

        self.naPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="Game folder not found.")
        self.naPathEntry.grid(row=3, column=0, padx=(5, 0), pady=(5, 5), columnspan=2, sticky="we")
        self.naPathButton = ctk.CTkButton(self.configRightFrame, text="Select Folder", command="")
        self.naPathButton.grid(row=3, column=2, padx=(5, 0), pady=(5, 5))

        self.euPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="Game folder not found.")
        self.euPathEntry.grid(row=4, column=0, padx=(5, 0), pady=(5, 5), columnspan=2, sticky="we")
        self.euPathButton = ctk.CTkButton(self.configRightFrame, text="Select Folder", command="")
        self.euPathButton.grid(row=4, column=2, padx=(5, 0), pady=(5, 5))

        """
        self.configTextbox = ctk.CTkTextbox(configTab)
        self.configTextbox.grid(row=5, column=0, columnspan=2, pady=(5, 0), sticky="nsew")
        self.configTextbox.configure(state="disabled")
        """

        #DEFAULT VALUES
        app_config = app_config_read()[0]
        if app_config.get('app', 'theme'): self.themeButton.set(app_config.get('app', 'theme'))
        if app_config.get('app', 'region'): self.regionRadio.set(app_config.get('app', 'region'))
        if app_config.get('app', 'napath'): self.naPathEntry.insert(0, app_config.get('app', 'napath'))
        if app_config.get('app', 'eupath'): self.euPathEntry.insert(0, app_config.get('app', 'eupath'))
        if app_config.get('app', 'color'): self.colorButton.set(app_config.get('app', 'color'))

    def change_theme_event(self, value):
        app_config = app_config_read()[0]
        app_config.set('app', 'theme', value)
        app_config_write(app_config)
        ctk.set_appearance_mode(value)

app = App()
app.geometry("500x250")
app.resizable(0, 0)
app.eval("tk::PlaceWindow . center")
app.mainloop()
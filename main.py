import tkinter as tk
import customtkinter as ctk
from functools import partial
from app_functions import *
import logging

# Read configs from file
load_configs = app_config_read()
app_config = load_configs[0]
config_full_path = load_configs[0]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        logging.debug(f"{sys._getframe().f_code.co_name}() -> App() initialized.")

        self.title("Aion Classic 'Mods' by Load")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # System appearance
        ctk.set_appearance_mode(app_config.get('app', 'theme'))
        ctk.set_default_color_theme(app_config.get('app', 'color').lower())

        self.tabsView = createTabs(self, self.change_color_event, self.reset_current_ui)
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
        self.tabsView = createTabs(self, self.change_color_event, self.reset_current_ui)
        self.tabsView.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")
        createTabs.set(self.tabsView, "Config")

class createTabs(ctk.CTkTabview):
    def __init__(self, master, change_color_event, reset_current_ui, **kwargs):
        super().__init__(master=master, **kwargs)

        logging.debug(f"{sys._getframe().f_code.co_name}() -> createTabs() initialized.")

        app_config = app_config_read()[0]

        logging.debug(f"{sys._getframe().f_code.co_name}() -> app_config.items(): {app_config.items('app')}")

        # create tabs
        self.add("App")
        appTab = self.tab("App")
        appTab.grid_rowconfigure(0, weight=1)
        appTab.grid_columnconfigure(0, weight=1)

        self.add("Config")
        configTab = self.tab("Config")
        configTab.grid_rowconfigure(4, weight=1)
        configTab.grid_columnconfigure(1, weight=1)

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Tabs created.")
        
        if first_run(): reset_current_ui

        # App tab widgets
        self.appTopFrame = ctk.CTkFrame(appTab)
        self.appTopFrame.grid(row=0, column=0, sticky="new")
        self.appTopFrame.configure(fg_color="transparent")
        self.appTopFrame.grid_columnconfigure(1, weight=1)

        self.voiceLabel = ctk.CTkLabel(self.appTopFrame, text="KR Voices:")
        self.voiceLabel.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
        self.voiceLabel.configure(font=("", 12, "bold"))
        self.filterLabel = ctk.CTkLabel(self.appTopFrame, text="Chat Filter:")
        self.filterLabel.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        self.filterLabel.configure(font=("", 12, "bold"))
        self.fontLabel = ctk.CTkLabel(self.appTopFrame, text="JP Fonts:")
        self.fontLabel.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="e")
        self.fontLabel.configure(font=("", 12, "bold"))

        self.checkAllButton = ctk.CTkButton(self.appTopFrame, text="Check All Files")
        self.checkAllButton.grid(row=0, column=2, padx=(5, 0), pady=5)
        self.checkAllButton.configure(font=("", 13, "bold"))

        self.voiceReturnLabel = ctk.CTkLabel(self.appTopFrame, text=f"Please press '{self.checkAllButton.cget('text')}' to start.")
        self.voiceReturnLabel.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.filterReturnLabel = ctk.CTkLabel(self.appTopFrame, text=f"Please press '{self.checkAllButton.cget('text')}' to start.")
        self.filterReturnLabel.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.fontReturnLabel = ctk.CTkLabel(self.appTopFrame, text=f"Please press '{self.checkAllButton.cget('text')}' to start.")
        self.fontReturnLabel.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        def copy_files_button(file_type, return_label, return_button):
            """
            
            """
            return_label.configure(text=f"Verifying '{file_type.capitalize()}' files.")

            copy_files_return = copy_files(file_type)

            if copy_files_return:
                return_label.configure(text=f"Success! '{file_type.capitalize()}' files have been updated.", text_color="#00E30A")
                return_button.configure(text=f"Up to date", state="disabled")
            elif not copy_files_return:
                return_label.configure(text=f"There are no new '{file_type}' files to update.")
                return_button.configure(text=f"Up to date", state="disabled")
        
        self.voiceButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled")
        self.voiceButton.configure(command=partial(copy_files_button, "voice", self.voiceReturnLabel, self.voiceButton))
        self.voiceButton.grid(row=1, column=2, padx=(5, 0), pady=5)

        self.filterButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled")
        self.filterButton.configure(command=partial(copy_files_button, "filter", self.filterReturnLabel, self.filterButton))
        self.filterButton.grid(row=2, column=2, padx=(5, 0), pady=5)

        self.fontButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled")
        self.fontButton.configure(command=partial(copy_files_button, "font", self.fontReturnLabel, self.fontButton))
        self.fontButton.grid(row=3, column=2, padx=(5, 0), pady=5)

        def check_files_button(file_type_list, install_buttons_list, file_type_label_list):
            """
            
            """
            start_button = 0
            for file_type in file_type_list:
                file_type_label_list[start_button].configure(text=f"Verifying '{file_type}' files.")
                check_files_return = check_files(file_type)
                if check_files_return:
                    install_buttons_list[start_button].configure(text=f"Install", state="normal")
                    file_type_label_list[start_button].configure(text=f"'{file_type.capitalize()}' files are ready to update. Press install.", text_color="red")
                elif not check_files_return:
                    install_buttons_list[start_button].configure(text=f"Up to date", state="disabled")
                    file_type_label_list[start_button].configure(text=f"There are no new '{file_type}' files to update.", text_color="#00E30A")
                start_button += 1

        self.checkAllButton.configure(command=partial(check_files_button, 
                                                   ["voice", "filter", "font"], 
                                                   [self.voiceButton, self.filterButton, self.fontButton], 
                                                   [self.voiceReturnLabel, self.filterReturnLabel, self.fontReturnLabel]))

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
                classic_na_path()
                self.naPathLabel.configure(state="normal")
                self.naPathEntry.configure(state="normal")
                self.naPathButton.configure(state="normal")
                self.euPathLabel.configure(state="disabled")
                self.euPathEntry.configure(state="disabled")
                self.euPathButton.configure(state="disabled")
            elif (self.regionRadio.get() == 2):
                classic_eu_path()
                self.naPathLabel.configure(state="disabled")
                self.naPathEntry.configure(state="disabled")
                self.naPathButton.configure(state="disabled")
                self.euPathLabel.configure(state="normal")
                self.euPathEntry.configure(state="normal")
                self.euPathButton.configure(state="normal")
            elif (self.regionRadio.get() == 3):
                classic_na_path()
                classic_eu_path()
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

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Tabs populated.")

        # DEFAULT VALUES
        if app_config.get('app', 'theme'): self.themeButton.set(app_config.get('app', 'theme'))
        if app_config.get('app', 'region'): self.regionRadio.set(app_config.get('app', 'region'))
        if app_config.get('app', 'napath'): self.naPathEntry.insert(0, app_config.get('app', 'napath'))
        if app_config.get('app', 'eupath'): self.euPathEntry.insert(0, app_config.get('app', 'eupath'))
        if app_config.get('app', 'color'): self.colorButton.set(app_config.get('app', 'color'))
        region_selection()

        # Runs file check at start
        """
        check_files_button(["voice", "filter", "font"], 
                           [self.voiceButton, self.filterButton, self.fontButton], 
                           [self.voiceReturnLabel, self.filterReturnLabel, self.fontReturnLabel])
        """

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values read.")

        #copy_files("filter")
        #copy_files("font")
        #copy_files("voice")

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
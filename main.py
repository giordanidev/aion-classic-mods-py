from app_functions import *
import tkinter as tk, customtkinter as ctk, logging
from functools import partial

logging.debug(f"{sys._getframe().f_code.co_name}() -> main.py imported.")

# Read configs from file
load_configs = app_config_read()
app_config = load_configs[0]
config_full_path = load_configs[0]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        logging.debug(f"{sys._getframe().f_code.co_name}() -> App() class initialized.")

        self.title(translated_text["app_title"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # System appearance
        ctk.set_appearance_mode(app_config.get('app', 'theme'))
        ctk.set_default_color_theme(app_config.get('app', 'color').lower())

        self.tabsView = createTabs(self, self.change_color_event)
        self.tabsView.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")

        self.current_ui = []
        self.current_ui.append(self.tabsView)

    def change_color_event(self, color):

        en_color = get_english_name(color)

        ctk.set_default_color_theme(en_color.lower())
        app_config = app_config_read()[0]
        app_config.set('app', 'color', en_color)
        app_config_write(app_config)
        self.reset_current_ui()
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Color changed to '{color.capitalize()}'.")

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

        logging.debug(f"{sys._getframe().f_code.co_name}() -> createTabs() class initialized.")

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
        
        first_run()

        # App tab widgets
        self.appTopFrame = ctk.CTkFrame(appTab)
        self.appTopFrame.grid(row=0, column=0, sticky="new")
        self.appTopFrame.configure(fg_color="transparent")
        self.appTopFrame.grid_columnconfigure(1, weight=1)

        self.infoLabel = ctk.CTkLabel(self.appTopFrame, text=translated_text["app_info_label"])
        self.infoLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.infoLabel.grid_remove()

        self.voiceLabel = ctk.CTkLabel(self.appTopFrame, text=translated_text["app_voice_label"], font=font_regular_bold)
        self.voiceLabel.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
        self.filterLabel = ctk.CTkLabel(self.appTopFrame, text=translated_text["app_filter_label"], font=font_regular_bold)
        self.filterLabel.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        self.fontLabel = ctk.CTkLabel(self.appTopFrame, text=translated_text["app_font_label"], font=font_regular_bold)
        self.fontLabel.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="e")

        self.voiceReturnLabel = ctk.CTkLabel(self.appTopFrame, text=translated_text["app_return_label_waiting"])
        self.voiceReturnLabel.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        self.filterReturnLabel = ctk.CTkLabel(self.appTopFrame, text=translated_text["app_return_label_waiting"])
        self.filterReturnLabel.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        self.fontReturnLabel = ctk.CTkLabel(self.appTopFrame, text=translated_text["app_return_label_waiting"])
        self.fontReturnLabel.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        
        self.voiceButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_install"], state="disabled", width=120)
        self.voiceButton.grid(row=1, column=2, padx=(5, 0), pady=5)

        self.filterButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_install"], state="disabled", width=120)
        self.filterButton.grid(row=2, column=2, padx=(5, 0), pady=5)

        self.fontButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_install"], state="disabled", width=120)
        self.fontButton.grid(row=3, column=2, padx=(5, 0), pady=5)


        self.voiceBackupButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_create"], state="disabled", width=85)
        self.voiceBackupButton.grid(row=1, column=3, padx=(5, 0), pady=5)

        self.filterBackupButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_create"], state="disabled", width=85)
        self.filterBackupButton.grid(row=2, column=3, padx=(5, 0), pady=5)

        self.fontBackupButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_create"], state="disabled", width=85)
        self.fontBackupButton.grid(row=3, column=3, padx=(5, 0), pady=5)


        self.voiceDeleteButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_delete"], state="disabled", width=67)
        self.voiceDeleteButton.grid(row=1, column=4, padx=(5, 0), pady=5)

        self.filterDeleteButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_delete"], state="disabled", width=67)
        self.filterDeleteButton.grid(row=2, column=4, padx=(5, 0), pady=5)

        self.fontDeleteButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_delete"], state="disabled", width=67)
        self.fontDeleteButton.grid(row=3, column=4, padx=(5, 0), pady=5)
        
        
        self.voiceButton.configure(command=partial(copy_files_button,
                                                   "voice",
                                                   "copy",
                                                   self.voiceReturnLabel,
                                                   self.voiceButton,
                                                   self.voiceDeleteButton))
        self.filterButton.configure(command=partial(copy_files_button,
                                                    "filter",
                                                    "copy",
                                                    self.filterReturnLabel,
                                                    self.filterButton,
                                                    self.filterDeleteButton))
        self.fontButton.configure(command=partial(copy_files_button,
                                                  "font",
                                                  "copy",
                                                  self.fontReturnLabel,
                                                  self.fontButton,
                                                  self.fontDeleteButton))
        
        self.voiceBackupButton.configure(command=partial(copy_files_button,
                                                         "voice",
                                                         "create",
                                                         self.voiceReturnLabel,
                                                         self.voiceBackupButton,
                                                         self.voiceDeleteButton))
        self.filterBackupButton.configure(command=partial(copy_files_button,
                                                          "filter",
                                                          "create",
                                                          self.filterReturnLabel,
                                                          self.filterBackupButton,
                                                          self.filterDeleteButton))
        self.fontBackupButton.configure(command=partial(copy_files_button,
                                                        "font",
                                                        "create",
                                                        self.fontReturnLabel,
                                                        self.fontBackupButton,
                                                        self.fontDeleteButton))
        
        self.voiceDeleteButton.configure(command=partial(copy_files_button,
                                                         "voice",
                                                         "delete",
                                                         self.voiceReturnLabel,
                                                         self.voiceBackupButton,
                                                         self.voiceDeleteButton))
        self.filterDeleteButton.configure(command=partial(copy_files_button,
                                                          "filter",
                                                          "delete",
                                                          self.filterReturnLabel,
                                                          self.filterBackupButton,
                                                          self.filterDeleteButton))
        self.fontDeleteButton.configure(command=partial(copy_files_button,
                                                        "font",
                                                        "delete",
                                                        self.fontReturnLabel,
                                                        self.fontBackupButton,
                                                        self.fontDeleteButton))


        self.checkAllButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_check_all"], font=font_big_bold, width=120)
        self.checkAllButton.grid(row=0, column=2, padx=(5, 0), pady=5)

        self.checkBackupButton = ctk.CTkButton(self.appTopFrame, text=translated_text["app_button_check_all_backups"], font=font_big_bold, width=157)
        self.checkBackupButton.grid(row=0, column=3, columnspan=2, padx=(5, 0), pady=5)
        
        self.checkAllButton.configure(command=partial(check_files_button, 
                                                   ["filter", "font", "voice"], 
                                                   [self.filterButton, self.fontButton, self.voiceButton],
                                                   "",
                                                   [self.filterReturnLabel, self.fontReturnLabel, self.voiceReturnLabel],
                                                   self.checkAllButton,
                                                   "check_all",
                                                   self))
        
        self.checkBackupButton.configure(command=partial(check_files_button, 
                                                   ["filter", "font", "voice"],
                                                   [self.filterBackupButton, self.fontBackupButton, self.voiceBackupButton],
                                                   [self.filterDeleteButton, self.fontDeleteButton, self.voiceDeleteButton],
                                                   [self.filterReturnLabel, self.fontReturnLabel, self.voiceReturnLabel],
                                                   self.checkBackupButton,
                                                   "check_backup",
                                                   self))

        # Config tab widgets > Left
        self.configLeftFrame = ctk.CTkFrame(configTab, fg_color="transparent")
        self.configLeftFrame.grid(row=0, column=0, sticky="ns")

        self.themeLabel = ctk.CTkLabel(self.configLeftFrame, text=translated_text["config_theme_label"], font=font_regular_bold)
        self.themeLabel.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="e")
        self.colorLabel = ctk.CTkLabel(self.configLeftFrame, text=translated_text["config_color_label"], font=font_regular_bold)
        self.colorLabel.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
        self.regionLabel = ctk.CTkLabel(self.configLeftFrame, text=translated_text["config_region_label"], font=font_regular_bold)
        self.regionLabel.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        self.naPathLabel = ctk.CTkLabel(self.configLeftFrame, text=translated_text["config_na_label"], font=font_regular_bold)
        self.naPathLabel.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="e")
        self.euPathLabel = ctk.CTkLabel(self.configLeftFrame, text=translated_text["config_eu_label"], font=font_regular_bold)
        self.euPathLabel.grid(row=4, column=0, padx=(0, 5), pady=5, sticky="e")

        # Config tab widgets > Right
        self.configRightFrame = ctk.CTkFrame(configTab, fg_color="transparent")
        self.configRightFrame.grid(row=0, column=1, sticky="nsew")
        self.configRightFrame.grid_columnconfigure((0, 1, 2), weight=1)

        theme_variable = ctk.StringVar(value="System")
        self.themeButton = ctk.CTkSegmentedButton(self.configRightFrame, command=self.change_theme_event, variable=theme_variable,
                                                  values=[translated_text["config_theme_system"],
                                                          translated_text["config_theme_dark"],
                                                          translated_text["config_theme_light"]])
        self.themeButton.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), columnspan=4, sticky="ew")
        color_variable = ctk.StringVar(value="Blue")
        self.colorButton = ctk.CTkSegmentedButton(self.configRightFrame, command=change_color_event, variable=color_variable,
                                                  values=[translated_text["config_color_blue"],
                                                          translated_text["config_color_darkblue"],
                                                          translated_text["config_color_green"]])
        self.colorButton.grid(row=1, column=0, padx=(5, 0), pady=(5, 5), columnspan=4, sticky="ew")
        
        self.regionRadio = tk.IntVar()

        self.naRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text=translated_text["config_region_radio_na"],
                                                    command=partial(region_selection, self),
                                                    variable=self.regionRadio,
                                                    value=1)
        self.naRadio.grid(row=2, column=0, padx=(5, 0), pady=8, sticky="w")
        self.euRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text=translated_text["config_region_radio_eu"],
                                                    command=partial(region_selection, self),
                                                    variable=self.regionRadio,
                                                    value=2)
        self.euRadio.grid(row=2, column=1, pady=8, sticky="w")
        self.bothRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text=translated_text["config_region_radio_both"],
                                                    command=partial(region_selection, self),
                                                    variable=self.regionRadio,
                                                    value=3)
        self.bothRadio.grid(row=2, column=2, pady=8, sticky="w")

        self.naPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="C:\\NA\\Game\\Folder")
        self.naPathEntry.grid(row=3, column=0, padx=(5, 0), pady=(5, 5), columnspan=3, sticky="we")
        self.naPathButton = ctk.CTkButton(self.configRightFrame, text=translated_text["config_select_folder_button"], command=partial(select_directory, self.naPathEntry), width=120)
        self.naPathButton.grid(row=3, column=3, padx=(5, 0), pady=(5, 5))

        self.euPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="C:\\EU\\Game\\Folder")
        self.euPathEntry.grid(row=4, column=0, padx=(5, 0), pady=(5, 5), columnspan=3, sticky="we")
        self.euPathButton = ctk.CTkButton(self.configRightFrame, text=translated_text["config_select_folder_button"], command=partial(select_directory, self.euPathEntry), width=120)
        self.euPathButton.grid(row=4, column=3, padx=(5, 0), pady=(5, 5))

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Tabs populated.")

        # DEFAULT VALUES
        app_config = app_config_read()[0]
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values -> "+
                      f"theme: {app_config.get('app', 'theme')} | "+
                      f"region: {app_config.get('app', 'region')} | "+
                      f"napath: {app_config.get('app', 'napath')} | "+
                      f"eupath: {app_config.get('app', 'eupath')} | "+
                      f"color: {app_config.get('app', 'color')}")
        if app_config.get('app', 'theme'):
            lang_theme = get_lang_name(app_config.get('app', 'theme'))
            self.themeButton.set(lang_theme)
        if app_config.get('app', 'color'):
            lang_color = get_lang_name(app_config.get('app', 'color'))
            self.colorButton.set(lang_color)
        if app_config.get('app', 'region'): self.regionRadio.set(app_config.get('app', 'region'))
        if app_config.get('app', 'napath'): self.naPathEntry.insert(0, app_config.get('app', 'napath'))
        if app_config.get('app', 'eupath'): self.euPathEntry.insert(0, app_config.get('app', 'eupath'))

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values read.")

    def change_theme_event(self, value):

        en_theme = get_english_name(value)

        app_config = app_config_read()[0]
        app_config.set('app', 'theme', en_theme)
        app_config_write(app_config)
        ctk.set_appearance_mode(en_theme)
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Theme changed to '{value.capitalize()}'.")

app = App()
app.iconbitmap("./config/img/Aion-Classic-Mods.ico")
app.geometry("650x245")
app.resizable(0, 0)
app.eval("tk::PlaceWindow . center")
app.mainloop()
from app_functions import *
import tkinter as tk, customtkinter as ctk, logging
from functools import partial

logging.debug(f"{sys._getframe().f_code.co_name}() -> main.py imported.")

# Read configs from file
load_configs = appConfigLoad()
app_config = load_configs[0]
config_full_path = load_configs[0]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        logging.debug(f"{sys._getframe().f_code.co_name}() -> App() class initialized.")

        self.title(translateText("app_title") + translateText("app_version"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # System appearance
        ctk.set_appearance_mode(app_config.get('app', 'theme'))
        ctk.set_default_color_theme(app_config.get('app', 'color').lower())

        self.tabsView = createTabs(self, self.changeColorEvent)
        self.tabsView.grid(row=0, column=0, padx=padx_both, pady=pady_both, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")

        self.current_ui = []
        self.current_ui.append(self.tabsView)

    def changeColorEvent(self, color):

        en_color = getEnglishTranslation(color)

        ctk.set_default_color_theme(en_color.lower())
        app_config = appConfigLoad()[0]
        app_config.set('app', 'color', en_color)
        appConfigSave(app_config)
        self.resetCurrentUi()
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Color changed to '{color.capitalize()}'.")

    def resetCurrentUi(self):
        for widget in self.current_ui:
            widget.destroy()
        self.tabsView = createTabs(self, self.changeColorEvent)
        self.tabsView.grid(row=0, column=0, padx=padx_both, pady=pady_both, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")
        createTabs.set(self.tabsView, "Config")

class createTabs(ctk.CTkTabview):
    def __init__(self, master, changeColorEvent, **kwargs):
        super().__init__(master=master, **kwargs)

        logging.debug(f"{sys._getframe().f_code.co_name}() -> createTabs() class initialized.")

        app_config = appConfigLoad()[0]

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
        
        firstRun()

        # App tab widgets
        self.appTopFrame = ctk.CTkFrame(appTab)
        self.appTopFrame.grid(row=0, column=0, sticky="new")
        self.appTopFrame.configure(fg_color="transparent")
        self.appTopFrame.grid_columnconfigure(1, weight=1)

        self.infoLabel = ctk.CTkLabel(self.appTopFrame, text=translateText("app_info_label"))
        self.infoLabel.grid(row=0, column=0, columnspan=2, padx=padx_both, pady=pady_both, sticky="w")
        self.infoLabel.grid_remove()

        self.voiceLabel = ctk.CTkLabel(self.appTopFrame, text=translateText("app_voice_label"), height=30, font=font_regular_bold)
        self.voiceLabel.grid(row=1, column=0, padx=padx_both, pady=pady_both, sticky="e")
        self.filterLabel = ctk.CTkLabel(self.appTopFrame, text=translateText("app_filter_label"), height=30, font=font_regular_bold)
        self.filterLabel.grid(row=2, column=0, padx=padx_both, pady=pady_both, sticky="e")
        self.fontLabel = ctk.CTkLabel(self.appTopFrame, text=translateText("app_font_label"), height=30, font=font_regular_bold)
        self.fontLabel.grid(row=3, column=0, padx=padx_both, pady=pady_both, sticky="e")

        self.voiceReturnLabel = ctk.CTkLabel(self.appTopFrame, text=translateText("app_return_label_waiting"), justify="left")
        self.voiceReturnLabel.grid(row=1, column=1, columnspan=2, padx=padx_both, pady=pady_both, sticky="w")
        self.filterReturnLabel = ctk.CTkLabel(self.appTopFrame, text=translateText("app_return_label_waiting"), justify="left")
        self.filterReturnLabel.grid(row=2, column=1, columnspan=2, padx=padx_both, pady=pady_both, sticky="w")
        self.fontReturnLabel = ctk.CTkLabel(self.appTopFrame, text=translateText("app_return_label_waiting"), justify="left")
        self.fontReturnLabel.grid(row=3, column=1, columnspan=2, padx=padx_both, pady=pady_both, sticky="w")

        
        self.voiceButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_install"), state="disabled", width=90)
        self.voiceButton.grid(row=1, column=2, padx=padx_both, pady=pady_both)

        self.filterButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_install"), state="disabled", width=90)
        self.filterButton.grid(row=2, column=2, padx=padx_both, pady=pady_both)

        self.fontButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_install"), state="disabled", width=90)
        self.fontButton.grid(row=3, column=2, padx=padx_both, pady=pady_both)

        self.voiceDeleteButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_delete"), state="disabled", width=90)
        self.voiceDeleteButton.grid(row=1, column=3, padx=padx_both, pady=pady_both)

        self.filterDeleteButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_delete"), state="disabled", width=90)
        self.filterDeleteButton.grid(row=2, column=3, padx=padx_both, pady=pady_both)

        self.fontDeleteButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_delete"), state="disabled", width=90)
        self.fontDeleteButton.grid(row=3, column=3, padx=padx_both, pady=pady_both)
        
        
        
        self.voiceButton.configure(command=partial(copyFilesButton,
                                                   "voice",
                                                   "copy",
                                                   self.voiceReturnLabel,
                                                   self.voiceButton,
                                                   self.voiceDeleteButton))
        self.filterButton.configure(command=partial(copyFilesButton,
                                                    "filter",
                                                    "copy",
                                                    self.filterReturnLabel,
                                                    self.filterButton,
                                                    self.filterDeleteButton))
        self.fontButton.configure(command=partial(copyFilesButton,
                                                  "font",
                                                  "copy",
                                                  self.fontReturnLabel,
                                                  self.fontButton,
                                                  self.fontDeleteButton))

        self.voiceDeleteButton.configure(command=partial(copyFilesButton,
                                                         "voice",
                                                         "delete",
                                                         self.voiceReturnLabel,
                                                         self.voiceButton,
                                                         self.voiceDeleteButton))
        self.filterDeleteButton.configure(command=partial(copyFilesButton,
                                                          "filter",
                                                          "delete",
                                                          self.filterReturnLabel,
                                                          self.filterButton,
                                                          self.filterDeleteButton))
        self.fontDeleteButton.configure(command=partial(copyFilesButton,
                                                        "font",
                                                        "delete",
                                                        self.fontReturnLabel,
                                                        self.fontButton,
                                                        self.fontDeleteButton))


        self.verifyAllButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_verify_all"), font=font_big_bold, width=184)
        self.verifyAllButton.grid(row=0, column=2, columnspan=2, padx=padx_both, pady=pady_both)
        
        self.verifyAllButton.configure(command=partial(verifyFilesButton, 
                                                   ["filter", "font", "voice"], 
                                                   [self.filterButton, self.fontButton, self.voiceButton],
                                                   [self.filterDeleteButton, self.fontDeleteButton, self.voiceDeleteButton],
                                                   [self.filterReturnLabel, self.fontReturnLabel, self.voiceReturnLabel],
                                                   self.verifyAllButton,
                                                   self))

        # Config tab widgets > Left
        self.configLeftFrame = ctk.CTkFrame(configTab, fg_color="transparent")
        self.configLeftFrame.grid(row=0, column=0, sticky="ns")

        self.themeLabel = ctk.CTkLabel(self.configLeftFrame, text=translateText("config_theme_label"), font=font_regular_bold)
        self.themeLabel.grid(row=0, column=0, padx=padx_both, pady=pady_both, sticky="e")
        self.colorLabel = ctk.CTkLabel(self.configLeftFrame, text=translateText("config_color_label"), font=font_regular_bold)
        self.colorLabel.grid(row=1, column=0, padx=padx_both, pady=pady_both, sticky="e")
        self.regionLabel = ctk.CTkLabel(self.configLeftFrame, text=translateText("config_region_label"), font=font_regular_bold)
        self.regionLabel.grid(row=2, column=0, padx=padx_both, pady=pady_both, sticky="e")
        self.naPathLabel = ctk.CTkLabel(self.configLeftFrame, text=translateText("config_na_label"), font=font_regular_bold)
        self.naPathLabel.grid(row=3, column=0, padx=padx_both, pady=pady_both, sticky="e")
        self.euPathLabel = ctk.CTkLabel(self.configLeftFrame, text=translateText("config_eu_label"), font=font_regular_bold)
        self.euPathLabel.grid(row=4, column=0, padx=padx_both, pady=pady_both, sticky="e")

        # Config tab widgets > Right
        self.configRightFrame = ctk.CTkFrame(configTab, fg_color="transparent")
        self.configRightFrame.grid(row=0, column=1, sticky="nsew")
        self.configRightFrame.grid_columnconfigure((0, 1, 2), weight=1)

        theme_variable = ctk.StringVar(value="System")
        self.themeButton = ctk.CTkSegmentedButton(self.configRightFrame, command=self.change_theme_event, variable=theme_variable,
                                                  values=[translateText("config_theme_system"),
                                                          translateText("config_theme_dark"),
                                                          translateText("config_theme_light")])
        self.themeButton.grid(row=0, column=0, padx=padx_both, pady=pady_both, columnspan=4, sticky="ew")
        color_variable = ctk.StringVar(value="Blue")
        self.colorButton = ctk.CTkSegmentedButton(self.configRightFrame, command=changeColorEvent, variable=color_variable,
                                                  values=[translateText("config_color_blue"),
                                                          translateText("config_color_darkblue"),
                                                          translateText("config_color_green")])
        self.colorButton.grid(row=1, column=0, padx=padx_both, pady=pady_both, columnspan=4, sticky="ew")
        
        self.regionRadio = tk.IntVar()

        self.naRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text=translateText("config_region_radio_na"),
                                                    command=partial(regionSelection, self),
                                                    variable=self.regionRadio,
                                                    value=1)
        self.naRadio.grid(row=2, column=0, padx=padx_both, pady=pady_both, sticky="w")
        self.euRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text=translateText("config_region_radio_eu"),
                                                    command=partial(regionSelection, self),
                                                    variable=self.regionRadio,
                                                    value=2)
        self.euRadio.grid(row=2, column=1, pady=pady_both, sticky="w")
        self.bothRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text=translateText("config_region_radio_both"),
                                                    command=partial(regionSelection, self),
                                                    variable=self.regionRadio,
                                                    value=3)
        self.bothRadio.grid(row=2, column=2, pady=pady_both, sticky="w")

        self.naPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="C:\\NA\\Game\\Folder")
        self.naPathEntry.grid(row=3, column=0, padx=padx_both, pady=pady_both, columnspan=3, sticky="we")
        self.naPathButton = ctk.CTkButton(self.configRightFrame, text=translateText("config_select_folder_button"), command=partial(selectDirectory, self.naPathEntry), width=120)
        self.naPathButton.grid(row=3, column=3, padx=padx_both, pady=pady_both)

        self.euPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="C:\\EU\\Game\\Folder")
        self.euPathEntry.grid(row=4, column=0, padx=padx_both, pady=pady_both, columnspan=3, sticky="we")
        self.euPathButton = ctk.CTkButton(self.configRightFrame, text=translateText("config_select_folder_button"), command=partial(selectDirectory, self.euPathEntry), width=120)
        self.euPathButton.grid(row=4, column=3, padx=padx_both, pady=pady_both)

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Tabs populated.")

        # DEFAULT VALUES
        app_config = appConfigLoad()[0]
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values -> "+
                      f"theme: {app_config.get('app', 'theme')} | "+
                      f"region: {app_config.get('app', 'region')} | "+
                      f"napath: {app_config.get('app', 'napath')} | "+
                      f"eupath: {app_config.get('app', 'eupath')} | "+
                      f"color: {app_config.get('app', 'color')}")
        if app_config.get('app', 'theme'):
            lang_theme = getLangTranslation(app_config.get('app', 'theme'))
            self.themeButton.set(lang_theme)
        if app_config.get('app', 'color'):
            lang_color = getLangTranslation(app_config.get('app', 'color'))
            self.colorButton.set(lang_color)
        if app_config.get('app', 'region'): self.regionRadio.set(app_config.get('app', 'region'))
        if app_config.get('app', 'napath'): self.naPathEntry.insert(0, app_config.get('app', 'napath'))
        if app_config.get('app', 'eupath'): self.euPathEntry.insert(0, app_config.get('app', 'eupath'))

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values read.")

    def change_theme_event(self, value):

        en_theme = getEnglishTranslation(value)

        app_config = appConfigLoad()[0]
        app_config.set('app', 'theme', en_theme)
        appConfigSave(app_config)
        ctk.set_appearance_mode(en_theme)
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Theme changed to '{value.capitalize()}'.")

app = App()
app.iconbitmap("./config/img/Aion-Classic-Mods.ico")
app.geometry("570x245")
app.resizable(0, 0)
app.eval("tk::PlaceWindow . center")
app.mainloop()
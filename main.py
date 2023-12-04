from functions import *
import tkinter as tk, customtkinter as ctk, logging
from functools import partial

logging.debug(f"{sys._getframe().f_code.co_name}() -> main.py imported.")

# Read configs from file
load_configs = appConfigLoad()
app_config = load_configs[0]
config_full_path = load_configs[0]
        
gerar_campos = ["translation", "translation_eu", "filter", "font", "voice", "asmo_skin"]

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

        self.infoLabel = ctk.CTkLabel(self.appTopFrame, text="")
        self.infoLabel.grid(row=0, column=0, columnspan=2, padx=padx_both, pady=pady_both, sticky="w")

        self.closeClientButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_close_client"), state="disabled", width=90)
        self.closeClientButton.grid(row=0, column=1, padx=padx_both, pady=pady_both, sticky="e")

        self.closeClientButton.configure(command=partial(forceCloseAion, "close", "client", self.closeClientButton, self.infoLabel))

        self.closeGameButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_close_game"), state="disabled", width=90)
        self.closeGameButton.grid(row=0, column=2, padx=padx_both, pady=pady_both)

        self.closeGameButton.configure(command=partial(forceCloseAion, "close", "game", self.closeGameButton, self.infoLabel))



        linha = 1
        all_buttons = []
        all_deleteButtons = []
        all_returnLabels = []
        #GERAR CAMPOS/BOTÕES DRY
        for campo in gerar_campos:
            self.nome_campoLabel = f"{campo}Label"
            self.nome_campoReturnLabel = f"{campo}ReturnLabel"
            self.nome_campoButton = f"{campo}Button"
            self.nome_campoDeleteButton = f"{campo}DeleteButton"
            
            self.nome_campoLabel = ctk.CTkLabel(self.appTopFrame, text=translateText(f"app_{campo}_label"), height=30, font=font_regular_bold)
            self.nome_campoLabel.grid(row=linha, column=0, padx=padx_both, pady=pady_both, sticky="e")
            self.nome_campoReturnLabel = ctk.CTkLabel(self.appTopFrame, text=translateText("app_return_label_waiting"), justify="left")
            self.nome_campoReturnLabel.grid(row=linha, column=1, columnspan=2, padx=padx_both, pady=pady_both, sticky="w")
            self.nome_campoButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_install"), state="disabled", width=90)
            self.nome_campoButton.grid(row=linha, column=3, padx=padx_both, pady=pady_both)
            self.nome_campoDeleteButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_delete"), state="disabled", width=90)
            self.nome_campoDeleteButton.grid(row=linha, column=4, padx=padx_both, pady=pady_both)
            self.nome_campoButton.configure(command=partial(copyFilesButton,
                                                    campo,
                                                    "copy",
                                                    self.nome_campoReturnLabel,
                                                    self.nome_campoButton,
                                                    self.nome_campoDeleteButton))
            self.nome_campoDeleteButton.configure(command=partial(copyFilesButton,
                                                            campo,
                                                            "delete",
                                                            self.nome_campoReturnLabel,
                                                            self.nome_campoButton,
                                                            self.nome_campoDeleteButton))
            all_buttons.append(self.nome_campoButton)
            all_deleteButtons.append(self.nome_campoDeleteButton)
            all_returnLabels.append(self.nome_campoReturnLabel)
            linha += 1
            


        self.verifyAllButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_verify_all"), font=font_big_bold, width=184)
        self.verifyAllButton.grid(row=0, column=3, columnspan=2, padx=padx_both, pady=pady_both)
        self.verifyAllButton.configure(command=partial(verifyFilesButton, 
                                                   gerar_campos, 
                                                   all_buttons,
                                                   all_deleteButtons,
                                                   all_returnLabels,
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
        self.euLauncherLabel = ctk.CTkLabel(self.configLeftFrame, text=translateText("config_eulauncher_label"), font=font_regular_bold)
        self.euLauncherLabel.grid(row=5, column=0, padx=padx_both, pady=pady_both, sticky="e")

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

        self.euLauncherPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="C:\\EU\\Launcher\\Folder", state="disabled")
        self.euLauncherPathEntry.grid(row=5, column=0, padx=padx_both, pady=pady_both, columnspan=3, sticky="we")
        self.euLauncherPathButton = ctk.CTkButton(self.configRightFrame, text=translateText("config_select_folder_button"), command=partial(selectDirectory, self.euLauncherPathEntry), width=120, state="disabled")
        self.euLauncherPathButton.grid(row=5, column=3, padx=padx_both, pady=pady_both)

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Tabs populated.")

        # DEFAULT VALUES
        app_config = appConfigLoad()[0]
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values -> "+
                      f"theme: {app_config.get('app', 'theme')} | "+
                      f"region: {app_config.get('app', 'region')} | "+
                      f"napath: {app_config.get('app', 'napath')} | "+
                      f"eupath: {app_config.get('app', 'eupath')} | "+
                      f"eulauncherpath: {app_config.get('app', 'eulauncherpath')} | "+
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
        if app_config.get('app', 'eulauncherpath'): self.euLauncherPathEntry.insert(0, app_config.get('app', 'eulauncherpath'))

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values read.")

    def change_theme_event(self, value):

        en_theme = getEnglishTranslation(value)

        app_config = appConfigLoad()[0]
        app_config.set('app', 'theme', en_theme)
        appConfigSave(app_config)
        ctk.set_appearance_mode(en_theme)
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Theme changed to '{value.capitalize()}'.")

app = App()
app.iconbitmap("./config/img/AionClassicMods.ico")
app.geometry("570x300")
app.resizable(0, 0)
app.eval("tk::PlaceWindow . center")
app.mainloop()
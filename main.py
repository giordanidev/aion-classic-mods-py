from functions import *
import tkinter as tk, customtkinter as ctk, logging
from functools import partial

logging.debug(f"{sys._getframe().f_code.co_name}() -> main.py imported.")

gerar_campos = ["translation", "translation_eu", "filter", "font", "voice", "asmo_skin"]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        global app_config

        logging.debug(f"{sys._getframe().f_code.co_name}() -> App() class initialized.")

        self.title(translateText("app_title") + " - v" +local_version["app_version"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # System appearance
        ctk.set_appearance_mode(app_config['theme'])
        ctk.set_default_color_theme(app_config['color'].lower())

        self.tabsView = createTabs(self, self.changeColorEvent)
        self.tabsView.grid(row=0, column=0, padx=padx_both, pady=pady_both, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")

        self.current_ui = []
        self.current_ui.append(self.tabsView)
        
        # DEFINES APP SIZE AND POSITION ON MAIN SCREEN
        centerApp(580, 305, self)
        
        self.iconbitmap(app_icon)
        self.resizable(0, 0)
        self.mainloop()

    def changeColorEvent(self, color):
        global app_config
        en_color = getEnglishTranslation(color)

        ctk.set_default_color_theme(en_color.lower())
        app_config['color'] = en_color
        appConfigSave(app_config)
        self.resetCurrentUi()
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Color changed to '{color.capitalize()}'.")

    def resetCurrentUi(self):
        global app_config
        for widget in self.current_ui:
            widget.destroy()
        self.tabsView = createTabs(self, self.changeColorEvent)
        self.tabsView.grid(row=0, column=0, padx=padx_both, pady=pady_both, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")
        createTabs.set(self.tabsView, "Config")

class createTabs(ctk.CTkTabview):
    def __init__(self, master, changeColorEvent, **kwargs):
        super().__init__(master=master, **kwargs)

        global app_config

        logging.debug(f"{sys._getframe().f_code.co_name}() -> createTabs() class initialized.")

        logging.debug(f"{sys._getframe().f_code.co_name}() -> app_config: {app_config}")

        # START CREATE TABS
        self.add("App")
        appTab = self.tab("App")
        appTab.grid_rowconfigure(0, weight=1)
        appTab.grid_columnconfigure(0, weight=1)

        self.add("Config")
        configTab = self.tab("Config")
        configTab.grid_rowconfigure(4, weight=1)
        configTab.grid_columnconfigure(1, weight=1)

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Tabs created.")
        # END CREATE TABS
        
        # DO FIRST RUN THINGS (CHECK COMMAND FOR MORE INFO)
        firstRun()

        ## START APP MAIN FRAME
        self.appTopFrame = ctk.CTkFrame(appTab)
        self.appTopFrame.grid(row=0, column=0, sticky="nsew")
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

        # START GENERATE LABELS/BUTTONS FOR ASSETS
        linha = 1
        all_buttons = []
        all_deleteButtons = []
        all_returnLabels = []
        for campo in gerar_campos:
            #self.nome_campoLabel = f"{campo}Label"
            #self.nome_campoReturnLabel = f"{campo}ReturnLabel"
            #self.nome_campoButton = f"{campo}Button"
            #self.nome_campoDeleteButton = f"{campo}DeleteButton"
            
            self.nome_campoLabel = ctk.CTkLabel(self.appTopFrame, text=translateText(f"app_{campo}_label")+":", height=30, font=font_regular_bold)
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
        # END GENERATE LABELS/BUTTONS FOR ASSETS


        self.verifyAllButton = ctk.CTkButton(self.appTopFrame, text=translateText("app_button_verify_all"), font=font_big_bold, width=184)
        self.verifyAllButton.grid(row=0, column=3, columnspan=2, padx=padx_both, pady=pady_both)
        self.verifyAllButton.configure(command=partial(verifyFilesButton, 
                                                   gerar_campos, 
                                                   all_buttons,
                                                   all_deleteButtons,
                                                   all_returnLabels,
                                                   self.verifyAllButton,
                                                   self))
        ## END APP MAIN FRAME

        ## START CONFIG SCROLLABLE FRAME
        self.configScrollableFrame = ctk.CTkScrollableFrame(configTab, fg_color="transparent", height=245)
        self.configScrollableFrame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.configScrollableFrame.grid_columnconfigure(4, weight=1)

        theme_variable = ctk.StringVar(value="System")
        self.themeLabel = ctk.CTkLabel(self.configScrollableFrame, text=translateText("config_theme_label"), font=font_regular_bold)
        self.themeLabel.grid(row=0, column=0, padx=padx_both, pady=2, sticky="e")
        self.themeButton = ctk.CTkSegmentedButton(self.configScrollableFrame, command=self.change_theme_event, variable=theme_variable,
                                                  values=[translateText("config_theme_system"),
                                                          translateText("config_theme_dark"),
                                                          translateText("config_theme_light")])
        self.themeButton.grid(row=0, column=1, padx=padx_both, pady=pady_both, columnspan=4, sticky="ew")

        color_variable = ctk.StringVar(value="Blue")
        self.colorLabel = ctk.CTkLabel(self.configScrollableFrame, text=translateText("config_color_label"), font=font_regular_bold)
        self.colorLabel.grid(row=1, column=0, padx=padx_both, pady=2, sticky="e")
        self.colorButton = ctk.CTkSegmentedButton(self.configScrollableFrame, command=changeColorEvent, variable=color_variable,
                                                  values=[translateText("config_color_blue"),
                                                          translateText("config_color_darkblue"),
                                                          translateText("config_color_green")])
        self.colorButton.grid(row=1, column=1, padx=padx_both, pady=pady_both, columnspan=4, sticky="ew")

        self.eu_launcherLabel = ctk.CTkLabel(self.configScrollableFrame, text=translateText("config_eu_launcher_label"), font=font_regular_bold)
        self.eu_launcherLabel.grid(row=2, column=0, padx=padx_both, pady=2, sticky="e")
        self.eu_launcherPathEntry = ctk.CTkEntry(self.configScrollableFrame, placeholder_text=translateText("config_eu_launcher_folder"))
        self.eu_launcherPathEntry.grid(row=2, column=1, padx=padx_both, pady=pady_both, columnspan=2, sticky="we")
        self.eu_launcherPathButton = ctk.CTkButton(self.configScrollableFrame, text=translateText("config_select_folder_button"), command=partial(selectDirectory, self.eu_launcherPathEntry), font=font_regular_bold, width=120)
        self.eu_launcherPathButton.grid(row=2, column=3, padx=padx_both, pady=pady_both, sticky="w")

        linha = 3
        for region in app_config['regions']:
            self.region_selectionLabel = ctk.CTkLabel(self.configScrollableFrame, text=region[1], font=font_regular_bold)
            self.region_selectionLabel.grid(row=linha, column=0, padx=padx_both, pady=2, sticky="e")
            linha += 1
            regions = []
            for lang in app_config['langs']:
                if lang[0] == region[0]:
                    # TODO
                    regions = []
        
        """
        self.regionRadio = tk.IntVar()

        self.naRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text="",
                                                    command=partial(regionSelection, self),
                                                    variable=self.regionRadio,
                                                    value=1)
        self.naRadio.grid(row=2, column=0, padx=padx_both, pady=pady_both, sticky="w")
        self.euRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text="",
                                                    command=partial(regionSelection, self),
                                                    variable=self.regionRadio,
                                                    value=2)
        self.euRadio.grid(row=2, column=1, pady=pady_both, sticky="w")
        self.bothRadio = ctk.CTkRadioButton(self.configRightFrame,
                                                    text="",
                                                    command=partial(regionSelection, self),
                                                    variable=self.regionRadio,
                                                    value=3)
        self.bothRadio.grid(row=2, column=2, pady=pady_both, sticky="w")
        """

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Tabs populated.")

        # DEFAULT VALUES
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values -> "+
                      f"theme: {app_config['theme']} | "+
                      f"color: {app_config['color']}"+
                      f"eu_launcher_path: {app_config['eu_launcher_path']} | ")
        if app_config['theme']:
            lang_theme = getLangTranslation(app_config['theme'])
            self.themeButton.set(lang_theme)
        if app_config['color']:
            lang_color = getLangTranslation(app_config['color'])
            self.colorButton.set(lang_color)
        if app_config['eu_launcher_path']: self.eu_launcherPathEntry.insert(0, app_config['eu_launcher_path'][0])

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values read.")

        

    def change_theme_event(self, value):

        en_theme = getEnglishTranslation(value)

        global app_config
        app_config['theme'] = en_theme
        appConfigSave(app_config)
        ctk.set_appearance_mode(en_theme)
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Theme changed to '{value.capitalize()}'.")
        

app = App()
from functions import *
import tkinter as tk, customtkinter as ctk, logging
from functools import partial

logging.debug(f"{sys._getframe().f_code.co_name}() :: Reading main.py.")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logging.debug(f"{sys._getframe().f_code.co_name}() :: App() class initialized.")

        self.title(translateText("app_title") + " - " +local_version["app_version"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.set_appearance_mode(app_config['theme']) # System appearance
        ctk.set_default_color_theme(app_config['color'].lower())

        self.tabsView = createTabs(self, self.changeColorEvent, self.checkUpdate)
        self.tabsView.grid(row=0, column=0, padx=padx_both, pady=pady_both, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")

        self.current_ui = []
        self.current_ui.append(self.tabsView)
        
        centerApp(580, 305, self) # DEFINES APP SIZE AND POSITION ON MAIN SCREEN

        self.checkupdate_window = None
        
        if app_config["check_updates_startup"] == True:
            self.checkUpdate()
    
    def checkUpdate(self):
        if self.checkupdate_window is None or not self.checkupdate_window.winfo_exists():
            self.checkupdate_window = checkUpdateWindow(self)  # create window if its None or destroyed
        else:
            self.checkupdate_window.focus()  # if window exists focus it

    def changeColorEvent(self, color):
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Changing color to '{color.capitalize()}'.")
        global app_config
        en_color = getEnglishTranslation(color)

        ctk.set_default_color_theme(en_color.lower())
        app_config['color'] = en_color
        appConfigSave(app_config)
        self.resetCurrentUi()

    def resetCurrentUi(self):
        global app_config
        for widget in self.current_ui:
            widget.destroy()
        self.tabsView = createTabs(self, self.changeColorEvent, self.checkUpdate)
        self.tabsView.grid(row=0, column=0, padx=padx_both, pady=pady_both, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")
        createTabs.set(self.tabsView, "Config")

class createTabs(ctk.CTkTabview):
    def __init__(self, master, changeColorEvent, checkUpdate, **kwargs):
        super().__init__(master=master, **kwargs)

        global app_config

        logging.debug(f"{sys._getframe().f_code.co_name}() :: createTabs() class initialized.")

        # START CREATE TABS
        self.add("App")
        appTab = self.tab("App")
        appTab.grid_rowconfigure(0, weight=1)
        appTab.grid_columnconfigure(0, weight=1)

        self.add("Config")
        configTab = self.tab("Config")
        configTab.grid_rowconfigure(4, weight=1)
        configTab.grid_columnconfigure(1, weight=1)
        # END CREATE TABS
        
        # DO FIRST RUN THINGS (CHECK COMMAND FOR MORE INFO)
        firstRun()

        ## START APP MAIN FRAME
        self.appMainFrame = ctk.CTkFrame(appTab)
        self.appMainFrame.grid(row=0, column=0, sticky="nsew")
        self.appMainFrame.configure(fg_color="transparent")
        self.appMainFrame.grid_columnconfigure(1, weight=1)
        
        linha_main = 0

        self.infoLabel = ctk.CTkLabel(self.appMainFrame, text="")
        self.infoLabel.grid(row=linha_main, column=0, columnspan=2, padx=padx_both, pady=pady_both, sticky="w")

        self.closeClientButton = ctk.CTkButton(self.appMainFrame, text=translateText("app_button_close_client"), state="disabled", width=90)
        self.closeClientButton.grid(row=linha_main, column=1, padx=padx_both, pady=pady_both, sticky="e")

        self.closeClientButton.configure(command=partial(forceCloseAion, "close", "client", self.closeClientButton, self.infoLabel))

        self.closeGameButton = ctk.CTkButton(self.appMainFrame, text=translateText("app_button_close_game"), state="disabled", width=90)
        self.closeGameButton.grid(row=linha_main, column=2, padx=padx_both, pady=pady_both)

        self.closeGameButton.configure(command=partial(forceCloseAion, "close", "game", self.closeGameButton, self.infoLabel))
        
        self.verifyAllButton = ctk.CTkButton(self.appMainFrame, text=translateText("app_button_verify_all"), font=font_big_bold, width=184)
        self.verifyAllButton.grid(row=linha_main, column=3, columnspan=2, padx=padx_both, pady=pady_both)

        linha_main += 1
        all_buttons = []
        all_deleteButtons = []
        all_returnLabels = []
        for campo in file_types:
            self.nome_campoLabel = ctk.CTkLabel(self.appMainFrame, text=translateText(f"app_{campo}_label")+":", height=30, font=font_regular_bold)
            self.nome_campoLabel.grid(row=linha_main, column=0, padx=padx_both, pady=pady_both, sticky="e")
            self.nome_campoReturnLabel = ctk.CTkLabel(self.appMainFrame, text=translateText("app_return_label_waiting"), justify="left")
            self.nome_campoReturnLabel.grid(row=linha_main, column=1, columnspan=2, padx=padx_both, pady=pady_both, sticky="w")
            self.nome_campoButton = ctk.CTkButton(self.appMainFrame, text=translateText("app_button_install"), state="disabled", width=90)
            self.nome_campoButton.grid(row=linha_main, column=3, padx=padx_both, pady=pady_both)
            self.nome_campoDeleteButton = ctk.CTkButton(self.appMainFrame, text=translateText("app_button_delete"), state="disabled", width=90)
            self.nome_campoDeleteButton.grid(row=linha_main, column=4, padx=padx_both, pady=pady_both)
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
            linha_main += 1

            if campo in local_version["disabled_fields"]:
                self.nome_campoLabel.configure(state="disabled")
                self.nome_campoReturnLabel.configure(state="disabled")
                self.nome_campoButton.configure(state="disabled")
                self.nome_campoDeleteButton.configure(state="disabled")

        self.verifyAllButton.configure(command=partial(verifyFilesButton, 
                                                   file_types, 
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

        linha_configs = 0
        self.generalLabel = ctk.CTkLabel(self.configScrollableFrame, text=translateText("config_general_label"), font=font_big_bold)
        self.generalLabel.grid(row=linha_configs, column=0, columnspan=5, padx=padx_both, pady=2, sticky="we")
        
        linha_configs += 1
        var_verif_files_startup = ctk.BooleanVar()
        var_verif_files_startup.set(app_config["verify_files_startup"])
        self.verifyCheckbox = ctk.CTkCheckBox(self.configScrollableFrame, variable=var_verif_files_startup, onvalue=True, offvalue=False)
        self.verifyCheckbox.configure(command=partial(checkboxEvent, self.verifyCheckbox, "verify"), text=translateText("config_verify_files_startup"))
        self.verifyCheckbox.grid(row=linha_configs, column=1, columnspan=2, padx=padx_both, pady=2, sticky="we")

        linha_configs += 1
        var_check_updates_startup = ctk.BooleanVar()
        var_check_updates_startup.set(app_config["check_updates_startup"])
        self.updateCheckbox = ctk.CTkCheckBox(self.configScrollableFrame, variable=var_check_updates_startup, onvalue=True, offvalue=False)
        self.updateCheckbox.configure(command=partial(checkboxEvent, self.updateCheckbox, "update"), text=translateText("config_check_updates_startup"))
        self.updateCheckbox.grid(row=linha_configs, column=1, columnspan=2, padx=padx_both, pady=2, sticky="we")

        self.checkUpdateButton = ctk.CTkButton(self.configScrollableFrame, text='Update', command=checkUpdate, font=font_regular_bold, width=120)
        self.checkUpdateButton.grid(row=linha_configs, column=4, padx=padx_both, pady=pady_both, sticky="w")

        linha_configs += 1
        theme_variable = ctk.StringVar(value="System")
        self.themeLabel = ctk.CTkLabel(self.configScrollableFrame, text=translateText("config_theme_label")+":", font=font_regular_bold)
        self.themeLabel.grid(row=linha_configs, column=0, padx=padx_both, pady=2, sticky="e")
        self.themeButton = ctk.CTkSegmentedButton(self.configScrollableFrame, command=self.change_theme_event, variable=theme_variable,
                                                  values=[translateText("config_theme_system"),
                                                          translateText("config_theme_dark"),
                                                          translateText("config_theme_light")])
        self.themeButton.grid(row=linha_configs, column=1, padx=padx_both, pady=pady_both, columnspan=4, sticky="ew")

        linha_configs += 1
        color_variable = ctk.StringVar(value="Blue")
        self.colorLabel = ctk.CTkLabel(self.configScrollableFrame, text=translateText("config_color_label")+":", font=font_regular_bold)
        self.colorLabel.grid(row=linha_configs, column=0, padx=padx_both, pady=2, sticky="e")
        self.colorButton = ctk.CTkSegmentedButton(self.configScrollableFrame, command=changeColorEvent, variable=color_variable,
                                                  values=[translateText("config_color_blue"),
                                                          translateText("config_color_darkblue"),
                                                          translateText("config_color_green")])
        self.colorButton.grid(row=linha_configs, column=1, padx=padx_both, pady=pady_both, columnspan=4, sticky="ew")

        linha_configs += 1
        self.eu_launcherLabel = ctk.CTkLabel(self.configScrollableFrame, text=translateText("config_eu_launcher_label")+":", font=font_regular_bold, state="disabled")
        self.eu_launcherLabel.grid(row=linha_configs, column=0, padx=padx_both, pady=2, sticky="e")
        self.eu_launcherPathEntry = ctk.CTkEntry(self.configScrollableFrame, placeholder_text=translateText("config_eu_launcher_folder"), state="disabled")
        self.eu_launcherPathEntry.grid(row=linha_configs, column=1, columnspan=3, padx=padx_both, pady=pady_both, sticky="we")
        self.eu_launcherPathButton = ctk.CTkButton(self.configScrollableFrame, text=translateText("config_select_folder_button"), command=partial(selectDirectory, self.eu_launcherPathEntry), font=font_regular_bold, width=120, state="disabled")
        self.eu_launcherPathButton.grid(row=linha_configs, column=4, padx=padx_both, pady=pady_both, sticky="w")

        linha_configs += 1
        self.regionLabel = ctk.CTkLabel(self.configScrollableFrame, text=translateText("config_regions_label"), font=font_big_bold)
        self.regionLabel.grid(row=linha_configs, column=0, columnspan=5, padx=padx_both, pady=2, sticky="we")
        self.eu_launcherPathButton = ctk.CTkButton(self.configScrollableFrame, text=translateText("config_regions_button"), command="#TODO", font=font_regular_bold, state="disabled", width=120)
        self.eu_launcherPathButton.grid(row=linha_configs, column=4, padx=padx_both, pady=pady_both, sticky="w")

        linha_configs += 1
        for region in app_config['regions']:
            self.region_selectionLabel = ctk.CTkLabel(self.configScrollableFrame, text=region[1]+":", font=font_regular_bold)
            self.region_selectionLabel.grid(row=linha_configs, column=0, padx=padx_both, pady=2, sticky="e")
            coluna = 1
            for lang in app_config['langs']:
                if coluna >= 5:
                    coluna = 1
                    linha_configs += 1
                if lang[0] == region[0]:
                    if lang[2] == True:
                        check_var = ctk.BooleanVar(value=True)
                    else:
                        check_var = ctk.BooleanVar(value=False)
                    self.checkbox = ctk.CTkCheckBox(self.configScrollableFrame, variable=check_var, onvalue=True, offvalue=False)
                    self.checkbox.configure(command=partial(checkboxEvent, self.checkbox, lang[0]), text=lang[1])
                    self.checkbox.grid(row=linha_configs, column=coluna, padx=padx_both, pady=2)
                    coluna += 1
            linha_configs += 1

        # DEFAULT VALUES
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Reading default values.")
        if app_config['theme']: self.themeButton.set(getLangTranslation(app_config['theme']))
        if app_config['color']: self.colorButton.set(getLangTranslation(app_config['color']))
        if app_config['eu_launcher_path']: self.eu_launcherPathEntry.insert(0, app_config['eu_launcher_path'][0])
        ## END CONFIG SCROLLABLE FRAME

    def change_theme_event(self, value):
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Changing theme to '{value.capitalize()}'.")
        en_theme = getEnglishTranslation(value)
        global app_config
        app_config['theme'] = en_theme
        appConfigSave(app_config)
        ctk.set_appearance_mode(en_theme)

class checkUpdateWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("creating")
        self.after(210, lambda: self.iconbitmap(app_icon))
        self.after(230, lambda: self.focus())
        self.resizable(0, 0)
        self.title("Updater")
        
        centerApp(280, 155, self)

        linha_configs = 0
        self.label = ctk.CTkLabel(self, text="Checking for updates...\nThe window will close automatically\nif no updates are found.")
        self.label.grid(row=linha_configs, column=1, columnspan=2, padx=padx_both, pady=2, sticky="we")

        linha_configs += 5
        var_check_updates_startup = ctk.BooleanVar()
        var_check_updates_startup.set(app_config["check_updates_startup"])
        self.updateCheckbox = ctk.CTkCheckBox(self, variable=var_check_updates_startup, onvalue=True, offvalue=False)
        self.updateCheckbox.configure(command=partial(checkboxEvent, self.updateCheckbox, "update"), text=translateText("config_check_updates_startup"))
        self.updateCheckbox.grid(row=linha_configs, column=1, columnspan=2, padx=padx_both, pady=2, sticky="we")

app = App()
app.iconbitmap(app_icon)
app.resizable(0, 0)
app.mainloop()
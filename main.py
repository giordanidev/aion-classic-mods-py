import tkinter as tk, customtkinter as ctk, logging, threading
from tkinter import filedialog
from functools import partial
from app_functions import *

logging.debug(f"{sys._getframe().f_code.co_name}() -> main.py imported.")

# Read configs from file
load_configs = app_config_read()
app_config = load_configs[0]
config_full_path = load_configs[0]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        logging.debug(f"{sys._getframe().f_code.co_name}() -> App() class initialized.")

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
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Color changed to '{color.capitalize()}'.")

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
        
        if first_run(): change_color_event

        text_color_success = ("#007514", "#7EFF93")
        text_color_fail = ("#D80000", "#FF6969")
        text_color_verifying = ("black", "white")
        font_regular = ("", 12)
        font_regular_bold = ("", 12, "bold")
        font_big_bold = ("", 13, "bold")

        # App tab widgets
        self.appTopFrame = ctk.CTkFrame(appTab)
        self.appTopFrame.grid(row=0, column=0, sticky="new")
        self.appTopFrame.configure(fg_color="transparent")
        self.appTopFrame.grid_columnconfigure(1, weight=1)

        self.voiceLabel = ctk.CTkLabel(self.appTopFrame, text="KR Voices:")
        self.voiceLabel.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
        self.voiceLabel.configure(font=font_regular_bold)
        self.filterLabel = ctk.CTkLabel(self.appTopFrame, text="Chat Filter:")
        self.filterLabel.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        self.filterLabel.configure(font=font_regular_bold)
        self.fontLabel = ctk.CTkLabel(self.appTopFrame, text="JP Fonts:")
        self.fontLabel.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="e")
        self.fontLabel.configure(font=font_regular_bold)

        self.checkAllButton = ctk.CTkButton(self.appTopFrame, text="Check Files", width=120)
        self.checkAllButton.grid(row=0, column=2, padx=(5, 0), pady=5)
        self.checkAllButton.configure(font=font_big_bold)

        self.checkBackupButton = ctk.CTkButton(self.appTopFrame, text="Check Backup Files", width=157)
        self.checkBackupButton.grid(row=0, column=3, columnspan=2, padx=(5, 0), pady=5)
        self.checkBackupButton.configure(font=font_big_bold)

        press_to_start = f"Please press '{self.checkAllButton.cget('text')}' to start."
        self.voiceReturnLabel = ctk.CTkLabel(self.appTopFrame, text=press_to_start)
        self.voiceReturnLabel.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        self.filterReturnLabel = ctk.CTkLabel(self.appTopFrame, text=press_to_start)
        self.filterReturnLabel.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        self.fontReturnLabel = ctk.CTkLabel(self.appTopFrame, text=press_to_start)
        self.fontReturnLabel.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        def copy_files_button(file_type, copy_backup, return_label, return_button):
            """
            
            """
            logging.debug(f"{sys._getframe().f_code.co_name}() -> {return_button.cget('text')} {copy_backup.capitalize()} ({file_type.capitalize()}) button pressed.")
            return_label.configure(text=f"Verifying '{file_type.capitalize()}' files.")

            copy_files_return = copy_files(file_type, copy_backup)

            if copy_files_return:
                return_label.configure(text=f"Success! '{file_type.capitalize()}' files have been updated.", text_color=text_color_success)
                return_button.configure(text=f"Up to date", state="disabled", font=font_regular)
            else:
                return_label.configure(text=f"There are no new '{file_type}' files to update.")
                return_button.configure(text=f"Up to date", state="disabled", font=font_regular)
        
        self.voiceButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled", width=120)
        self.voiceButton.configure(command=partial(copy_files_button, "voice", "copy", self.voiceReturnLabel, self.voiceButton))
        self.voiceButton.grid(row=1, column=2, padx=(5, 0), pady=5)

        self.filterButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled", width=120)
        self.filterButton.configure(command=partial(copy_files_button, "filter", "copy", self.filterReturnLabel, self.filterButton))
        self.filterButton.grid(row=2, column=2, padx=(5, 0), pady=5)

        self.fontButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled", width=120)
        self.fontButton.configure(command=partial(copy_files_button, "font", "copy", self.fontReturnLabel, self.fontButton))
        self.fontButton.grid(row=3, column=2, padx=(5, 0), pady=5)

        self.voiceBackupButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled", width=85)
        self.voiceBackupButton.configure(command=partial(copy_files_button, "voice", "create", self.voiceReturnLabel, self.voiceButton))
        self.voiceBackupButton.grid(row=1, column=3, padx=(5, 0), pady=5)

        self.filterBackupButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled", width=85)
        self.filterBackupButton.configure(command=partial(copy_files_button, "filter", "create", self.filterReturnLabel, self.filterButton))
        self.filterBackupButton.grid(row=2, column=3, padx=(5, 0), pady=5)

        self.fontBackupButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled", width=85)
        self.fontBackupButton.configure(command=partial(copy_files_button, "font", "create", self.fontReturnLabel, self.fontButton))
        self.fontBackupButton.grid(row=3, column=3, padx=(5, 0), pady=5)

        self.voiceDeleteButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled", width=67)
        self.voiceDeleteButton.configure(command=partial(copy_files_button, "voice", "delete", self.voiceReturnLabel, self.voiceButton))
        self.voiceDeleteButton.grid(row=1, column=4, padx=(5, 0), pady=5)

        self.filterDeleteButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled", width=67)
        self.filterDeleteButton.configure(command=partial(copy_files_button, "filter", "delete", self.filterReturnLabel, self.filterButton))
        self.filterDeleteButton.grid(row=2, column=4, padx=(5, 0), pady=5)

        self.fontDeleteButton = ctk.CTkButton(self.appTopFrame, text="Waiting", state="disabled", width=67)
        self.fontDeleteButton.configure(command=partial(copy_files_button, "font", "delete", self.fontReturnLabel, self.fontButton))
        self.fontDeleteButton.grid(row=3, column=4, padx=(5, 0), pady=5)

        # file_type_list: filter, font, voice | install_backup_buttons_list: filter, font, voice buttons
        # delete_buttons_list: filter, font, voice -> delete buttons -> Only used when Checking Backups
        # file_type_label_list: filter, font, voice labels | check_all_backup_button: filter, font, voice
        # check_all_delete "check_all" or "check_backup" -> Used to identify if we are checking for game files or backup files
        def check_files_button(file_type_list, install_backup_buttons_list, delete_buttons_list, file_type_label_list, check_all_backup_button, check_all_backup):
            """
            
            """
            # TODO VERIFY BACKUP FILES
            logging.debug(f"{sys._getframe().f_code.co_name}() -> {check_all_backup_button.cget('text')} button pressed.")
            try:
                if check_game_path() == True:

                    type_count = 0
                    for file_type in file_type_list:
                        def check_files_thread(file_type, type_count):
                            logging.debug(f"{sys._getframe().f_code.co_name}() -> thread started.")
                            file_type_label_list[type_count].configure(text=f"Checking '{file_type}' files, please wait!", text_color=text_color_verifying)
                            install_backup_buttons_list[type_count].configure(text=f"Checking", state="disabled")
                            install_backup_buttons_list[type_count].configure(font=font_regular)
                            if check_all_backup == "check_backup":
                                delete_buttons_list[type_count].configure(text=f"Checking", state="disabled")
                                delete_buttons_list[type_count].configure(font=font_regular)
                            # Sends the file type and check for regular or backup files
                            # check_files() has to know which files it is going to look for
                            check_files_return = check_files(file_type, check_all_backup)
                            if check_files_return:
                                file_type_label_list[type_count].configure(text=f"'{file_type.capitalize()}' files are ready to update.", text_color=text_color_fail)
                                file_type_label_list[type_count].configure(font=font_regular)
                                install_backup_buttons_list[type_count].configure(text=f"Install", state="normal")
                                install_backup_buttons_list[type_count].configure(font=font_big_bold)
                                if check_all_backup == "check_backup":
                                    delete_buttons_list[type_count].configure(text=f"Install", state="normal")
                                    delete_buttons_list[type_count].configure(font=font_big_bold)
                            elif not check_files_return:
                                file_type_label_list[type_count].configure(text=f"There are no new '{file_type}' files to update.", text_color=text_color_success)
                                file_type_label_list[type_count].configure(font=font_regular)
                                install_backup_buttons_list[type_count].configure(text=f"Up to date", state="disabled")
                                #install_backup_buttons_list[type_count].configure(font=font_regular)
                                if check_all_backup == "check_backup":
                                    delete_buttons_list[type_count].configure(text=f"Up to date", state="disabled")
                                    #delete_buttons_list[type_count].configure(font=font_regular)
                        check_files_thread_func = threading.Thread(target=check_files_thread, args=(file_type, type_count))
                        check_files_thread_func.start()
                        #check_files_thread_func.join() # crashes the app =(
                        type_count += 1

                else:
                    self.set("Config")
                    #TODO ADD ERROR

            except Exception as e:
                get_exception(e)
                return False

        self.checkAllButton.configure(command=partial(check_files_button, 
                                                   ["filter", "font", "voice"], 
                                                   [self.filterButton, self.fontButton, self.voiceButton], 
                                                   "",
                                                   [self.filterReturnLabel, self.fontReturnLabel, self.voiceReturnLabel],
                                                   self.checkAllButton,
                                                   "check_all"))
        self.checkBackupButton.configure(command=partial(check_files_button, 
                                                   ["filter", "font", "voice"],
                                                   [self.filterBackupButton, self.fontBackupButton, self.voiceBackupButton],
                                                   [self.filterDeleteButton, self.fontDeleteButton, self.voiceDeleteButton],
                                                   [self.filterReturnLabel, self.fontReturnLabel, self.voiceReturnLabel],
                                                   self.checkBackupButton,
                                                   "check_backup"))

        # Config tab widgets > Left
        self.configLeftFrame = ctk.CTkFrame(configTab)
        self.configLeftFrame.grid(row=0, column=0, sticky="ns")
        self.configLeftFrame.configure(fg_color="transparent")

        self.themeLabel = ctk.CTkLabel(self.configLeftFrame, text="App Theme:")
        self.themeLabel.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="e")
        self.themeLabel.configure(font=font_regular_bold)
        self.colorLabel = ctk.CTkLabel(self.configLeftFrame, text="App Color:")
        self.colorLabel.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
        self.colorLabel.configure(font=font_regular_bold)
        self.regionLabel = ctk.CTkLabel(self.configLeftFrame, text="Region Selection:")
        self.regionLabel.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        self.regionLabel.configure(font=font_regular_bold)
        self.naPathLabel = ctk.CTkLabel(self.configLeftFrame, text="NA Game Folder:")
        self.naPathLabel.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="e")
        self.naPathLabel.configure(font=font_regular_bold)
        self.euPathLabel = ctk.CTkLabel(self.configLeftFrame, text="EU Game Folder:")
        self.euPathLabel.grid(row=4, column=0, padx=(0, 5), pady=5, sticky="e")
        self.euPathLabel.configure(font=font_regular_bold)

        # Config tab widgets > Right
        self.configRightFrame = ctk.CTkFrame(configTab)
        self.configRightFrame.grid(row=0, column=1, sticky="nsew")
        self.configRightFrame.configure(fg_color="transparent")
        self.configRightFrame.grid_columnconfigure((0, 1, 2), weight=1)

        self.themeButton = ctk.CTkSegmentedButton(self.configRightFrame,values=["System", "Dark", "Light"], command=self.change_theme_event)
        self.themeButton.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), columnspan=4, sticky="ew")
        self.colorButton = ctk.CTkSegmentedButton(self.configRightFrame, values=["Blue", "Dark-blue", "Green"], command=change_color_event)
        self.colorButton.grid(row=1, column=0, padx=(5, 0), pady=(5, 5), columnspan=4, sticky="ew")
        
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
                if classic_na_path():
                    self.naPathEntry.delete(0, 'end')
                    self.naPathEntry.insert(0, app_config.get('app', 'napath'))
                self.naPathLabel.configure(state="normal")
                self.naPathEntry.configure(state="normal")
                self.naPathButton.configure(state="normal")
                self.euPathLabel.configure(state="disabled")
                self.euPathEntry.configure(state="disabled")
                self.euPathButton.configure(state="disabled")
            elif (self.regionRadio.get() == 2):
                if classic_eu_path():
                    self.euPathEntry.delete(0, 'end')
                    self.euPathEntry.insert(0, app_config.get('app', 'eupath'))
                self.naPathLabel.configure(state="disabled")
                self.naPathEntry.configure(state="disabled")
                self.naPathButton.configure(state="disabled")
                self.euPathLabel.configure(state="normal")
                self.euPathEntry.configure(state="normal")
                self.euPathButton.configure(state="normal")
            elif (self.regionRadio.get() == 3):
                if classic_na_path():
                    self.naPathEntry.delete(0, 'end')
                    self.naPathEntry.insert(0, app_config.get('app', 'napath'))
                if classic_eu_path():
                    self.euPathEntry.delete(0, 'end')
                    self.euPathEntry.insert(0, app_config.get('app', 'eupath'))
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

        def select_directory(path_entry):
            logging.debug(f"{sys._getframe().f_code.co_name}() -> {path_entry} ({path_entry}) button pressed.")
            game_directory = filedialog.askdirectory().replace("/","\\")
            logging.debug(f"{sys._getframe().f_code.co_name}() -> game_directory: {game_directory}.")

            if game_directory:
                placeholder_text = path_entry.cget("placeholder_text")
                validate_directory_return = validate_directory(game_directory, placeholder_text)
                logging.debug(f"{sys._getframe().f_code.co_name}() -> validate_directory_return: {validate_directory_return}.")

                if validate_directory_return:
                    path_entry.delete(0, 'end')
                    path_entry.insert(0, game_directory)
                    return

            else:
                if not check_game_path():
                    logging.debug(f"ERROR -> {sys._getframe().f_code.co_name}() -> Wrong game directory.")
                    return
                return

        self.naPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="C:\\NA\\Game\\Folder")
        self.naPathEntry.grid(row=3, column=0, padx=(5, 0), pady=(5, 5), columnspan=3, sticky="we")
        self.naPathButton = ctk.CTkButton(self.configRightFrame, text="Select Folder", command=partial(select_directory, self.naPathEntry), width=120)
        self.naPathButton.grid(row=3, column=3, padx=(5, 0), pady=(5, 5))

        self.euPathEntry = ctk.CTkEntry(self.configRightFrame, placeholder_text="C:\\EU\\Game\\Folder")
        self.euPathEntry.grid(row=4, column=0, padx=(5, 0), pady=(5, 5), columnspan=3, sticky="we")
        self.euPathButton = ctk.CTkButton(self.configRightFrame, text="Select Folder", command=partial(select_directory, self.euPathEntry), width=120)
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
        if app_config.get('app', 'theme'): self.themeButton.set(app_config.get('app', 'theme'))
        if app_config.get('app', 'color'): self.colorButton.set(app_config.get('app', 'color'))
        if app_config.get('app', 'region'): self.regionRadio.set(app_config.get('app', 'region'))
        if app_config.get('app', 'napath'): self.naPathEntry.insert(0, app_config.get('app', 'napath'))
        if app_config.get('app', 'eupath'): self.euPathEntry.insert(0, app_config.get('app', 'eupath'))

        logging.debug(f"{sys._getframe().f_code.co_name}() -> Default values read.")

    def change_theme_event(self, value):
        app_config = app_config_read()[0]
        app_config.set('app', 'theme', value)
        app_config_write(app_config)
        ctk.set_appearance_mode(value)
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Theme changed to '{value.capitalize()}'.")

app = App()
app.iconbitmap("./config/img/Aion-Classic-Mods.ico")
app.geometry("600x245")
app.resizable(0, 0)
app.eval("tk::PlaceWindow . center")
app.mainloop()

# TODO 
# REORGANIZE FUNCTIONS
#
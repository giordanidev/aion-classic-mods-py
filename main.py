import tkinter as tk
import customtkinter as ctk
from configparser import ConfigParser
import winreg
import hashlib
import os.path

# Read configs from file
def app_config_read():
    try:
        app_config = ConfigParser()
        config_path = 'config/'
        config_file = 'config.ini'
        config_full_path = config_path + config_file
        app_config.read(config_full_path)

        return (app_config, config_full_path)
    except: ""
app_config = app_config_read()[0]
config_full_path = app_config_read()[1]

def app_config_write():
    try:
        with open(config_full_path, 'w') as config_write:
            app_config.write(config_write)

    except: ""

def classic_eu_path():
    try:
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        aKey = winreg.OpenKey(aReg, r'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall')

        notFound = True
        for i in range(1024):
            try:
                aValue_name = winreg.EnumKey(aKey, i)
                oKey = winreg.OpenKey(aKey, aValue_name)
                sValue = winreg.QueryValueEx(oKey, "DisplayName")
                classicEuPublisher = winreg.QueryValueEx(oKey, "Publisher")
                if (sValue[0] == "AION Classic"):
                    if (classicEuPublisher[0] == "Gameforge"):
                        classicEuPath = winreg.QueryValueEx(oKey, "InstallLocation")
                        notFound = False

            except: "" #print(EnvironmentError)

        if (notFound == False):
            print("Client found: "+classicEuPath[0])
            app_config.set('app', 'eupath', classicEuPath[0])
            app_config_write()
        else:
            print("Client not found. Please select manually.")

    except:
        print("Client not found. Please select manually.")

def classic_na_path():
    try:
        app_config_read()
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        aKey = winreg.OpenKey(aReg, r'SOFTWARE\\WOW6432Node\\NCWest\\AION_CLASSIC')

        if aKey:
            sValue = winreg.QueryValueEx(aKey, "BaseDir")
            na_dir = sValue[0]
            if na_dir[len(na_dir)-1] == "\\":
                na_dir = na_dir.rstrip(na_dir[-1])
            app_config.set('app', 'napath', na_dir)
            app_config_write()
            
    except:
        print("Client not found. Please select manually.")

def define_region():
    try:
        count_region = 0
        app_config_read()

        if app_config.get('app', 'napath'): count_region += 1
        if app_config.get('app', 'eupath'): count_region += 2

        app_config.set('app', 'region', str(count_region))
        app_config_write()
    except: ""

def check_filter_hash(filter_files):
    app_config_read()
    count = 0
    check_hash = []
    for filter in filter_files:
        if filter == "original":
            filter_path = "assets\\l10n\\enu\\data\\Strings\\aionfilterline.pak"
        elif filter == "enu":
            filter_path = f"{app_config.get('app', 'napath')}\\l10n\\{filter}\\data\\Strings\\aionfilterline.pak"
        else:
            filter_path = f"{app_config.get('app', 'eupath')}\\l10n\\{filter}\\data\\Strings\\aionfilterline.pak"

        if os.path.isfile(filter_path):
            with open(filter_path, 'rb', buffering=0) as f:
                print(f"FILTER {filter_path} PASSED. {count} {hashlib.file_digest(f, 'sha256').hexdigest()}")
                check_hash.append(hashlib.file_digest(f, 'sha256').hexdigest())
        else:
            print(f"FILTER {filter_path} NOT FOUND. {count}")
            check_hash.append(False)
        count += 1
    return check_hash

def check_files():
#try:
    filter_files = ["original", "enu", "eng", "deu", "fra"]
    check_hash = check_filter_hash(filter_files)
    print(check_hash)

def first_run():
    if not app_config.get('app', 'region'):
        try:
            classic_na_path()
            classic_eu_path()
            define_region()
            check_files()

        except: ""
first_run()


class mainTabs(ctk.CTkTabview):
    def __init__(self, master, change_color_event, **kwargs):
        super().__init__(master=master, **kwargs)

        app_config_read()

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

        self.voiceButton = ctk.CTkButton(self.appTopFrame, text="Check Updates", command="")
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
            app_config.set('app', 'region', str(self.regionRadio.get()))
            app_config_write()
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
        app_config_read()
        if app_config.get('app', 'theme'): self.themeButton.set(app_config.get('app', 'theme'))
        if app_config.get('app', 'region'): self.regionRadio.set(app_config.get('app', 'region'))
        if app_config.get('app', 'napath'): self.naPathEntry.insert(0, app_config.get('app', 'napath'))
        if app_config.get('app', 'eupath'): self.euPathEntry.insert(0, app_config.get('app', 'eupath'))
        if app_config.get('app', 'color'): self.colorButton.set(app_config.get('app', 'color'))
        region_selection()

    def change_theme_event(self, value):
        app_config.set('app', 'theme', value)
        app_config_write()
        ctk.set_appearance_mode(value)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aion Classic 'Mods' by Load")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        app_config_read()

        # System appearance
        ctk.set_appearance_mode(app_config.get('app', 'theme'))
        ctk.set_default_color_theme(app_config.get('app', 'color').lower())

        self.tabsView = mainTabs(self, self.change_color_event)
        self.tabsView.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")

        self.current_ui = []
        self.current_ui.append(self.tabsView)

    def change_color_event(self, color):
        ctk.set_default_color_theme(color.lower())
        app_config.set('app', 'color', color)
        app_config_write()
        app_config_read()
        self.reset_current_ui()

    def reset_current_ui(self):
        for widget in self.current_ui:
            widget.destroy()
        self.tabsView = mainTabs(self, self.change_color_event)
        self.tabsView.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")
        mainTabs.set(self.tabsView, "Config")

app = App()
app.geometry("500x250")
app.resizable(0, 0)
app.eval("tk::PlaceWindow . center")
app.mainloop()
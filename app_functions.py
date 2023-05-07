import winreg
import customtkinter as ctk
from app_config import appSettings
from app_tabs import mainTabs

class appFunctions:
    # ENABLE/DISABLE NA/EU fields configs
    def regionSelection(self, region):
        appSettings.appConfigRead.set('app', 'region', str(self.regionRadio.get()))
        appSettings.appConfigWrite(appSettings.appConfigRead, appSettings.configFullPath)
        if (self.regionRadio.get() == 0):
            self.naPathLabel.configure(state="normal")
            self.naPathEntry.configure(state="normal")
            self.naPathButton.configure(state="normal")
            self.euPathLabel.configure(state="disabled")
            self.euPathEntry.configure(state="disabled")
            self.euPathButton.configure(state="disabled")
        elif (self.regionRadio.get() == 1):
            self.naPathLabel.configure(state="disabled")
            self.naPathEntry.configure(state="disabled")
            self.naPathButton.configure(state="disabled")
            self.euPathLabel.configure(state="normal")
            self.euPathEntry.configure(state="normal")
            self.euPathButton.configure(state="normal")
        elif (self.regionRadio.get() == 2):
            self.naPathLabel.configure(state="normal")
            self.naPathEntry.configure(state="normal")
            self.naPathButton.configure(state="normal")
            self.euPathLabel.configure(state="normal")
            self.euPathEntry.configure(state="normal")
            self.euPathButton.configure(state="normal")

    def change_theme_event(self, value):
        appSettings.appConfigRead.set('app', 'theme', value)
        appSettings.appOptions.appConfigWrite(appSettings.appConfigRead, appSettings.configFullPath)
        ctk.set_appearance_mode(value)

    def change_color_event(self, color):
        ctk.set_default_color_theme(color.lower())
        appSettings.appConfigRead.set('app', 'color', color)
        appSettings.appConfigWrite(appSettings.appConfigRead, appSettings.configFullPath)
        self.reset_current_ui()

    def reset_current_ui(self):
        for widget in self.current_ui:
            widget.destroy()
        self.tabsView = mainTabs(self, self.change_color_event)
        self.tabsView.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.tabsView._segmented_button.grid(sticky="w")
        mainTabs.set(self.tabsView, "Config")

    # Get EU Classic installation path
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

                except: print(EnvironmentError)

            if (notFound == False):
                print("Client found: "+classicEuPath[0])
            else:
                print("Client not found. Please select manually.")
        except: print("Client not found. Please select manually.")

    # Get NA Classic installation path
    def classic_na_path():
        try:
            aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            aKey = winreg.OpenKey(aReg, r'SOFTWARE\\WOW6432Node\\NCWest\\AION_CLASSIC')

            if aKey:
                sValue = winreg.QueryValueEx(aKey, "BaseDir")
                print("Client found: "+sValue[0])
                
        except: print("Client not found. Please select manually.")
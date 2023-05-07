import winreg

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
classic_eu_path()
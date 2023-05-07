import winreg

def classic_na_path():
    try:
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        aKey = winreg.OpenKey(aReg, r'SOFTWARE\\WOW6432Node\\NCWest\\AION_CLASSIC')

        if aKey:
            sValue = winreg.QueryValueEx(aKey, "BaseDir")
            na_dir = sValue[0]
            if na_dir[len(na_dir)-1] == "\\":
                na_dir = na_dir.rstrip(na_dir[-1])
            print("Client found: "+na_dir)
            
    except: print("Client not found. Please select manually.")
classic_na_path()
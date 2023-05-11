from configparser import ConfigParser
import os, os.path, hashlib, winreg

def app_config_read():
    try:
        app_config = ConfigParser()
        config_path = 'config/'
        config_file = 'config.ini'
        config_full_path = config_path + config_file
        app_config.read(config_full_path)

        return (app_config, config_full_path)
    except Exception as e:
        print("ERROR -> app_config_read() :: "+str(e))
app_config = app_config_read()[0]
config_full_path = app_config_read()[1]

def app_config_write():
    try:
        with open(config_full_path, 'w') as config_write:
            app_config.write(config_write)

    except Exception as e:
        print("ERROR -> app_config_write() :: "+str(e))

def classic_eu_path():
    try:
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall')

        not_found = True
        for i in range(1024):
            try:
                a_value_name = winreg.EnumKey(a_key, i)
                o_key = winreg.OpenKey(a_key, a_value_name)
                s_value = winreg.QueryValueEx(o_key, "DisplayName")
                classic_eu_publisher = winreg.QueryValueEx(o_key, "Publisher")
                if (s_value[0] == "AION Classic"):
                    if (classic_eu_publisher[0] == "Gameforge"):
                        classic_eu_path = winreg.QueryValueEx(o_key, "InstallLocation")
                        eu_dir = classic_eu_path[0]
                        not_found = False

            except Exception as e:
                print("ERROR -> classic_eu_path() :: "+str(e))

        if (not_found == False):
            print("Client found: "+eu_dir)
            app_config.set('app', 'eupath', eu_dir)
            app_config_write()
        else:
            print("Client not found. Please select manually.")

    except:
        print("Client not found. Please select manually.")

def classic_na_path():
    try:
        app_config_read()
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\NCWest\\AION_CLASSIC')

        if a_key:
            s_value = winreg.QueryValueEx(a_key, "BaseDir")
            na_dir = s_value[0]
            if na_dir[len(na_dir)-1] == "\\":
                na_dir = na_dir.rstrip(na_dir[-1])
            app_config.set('app', 'napath', na_dir)
            app_config_write()
            
    except Exception as e:
        print("ERROR -> classic_na_path() :: "+str(e))

def define_region():
        count_region = 0
        check_game_path()
        app_config_read()

        if app_config.get('app', 'napath'): count_region += 1
        if app_config.get('app', 'eupath'): count_region += 2

        app_config.set('app', 'region', str(count_region))
        app_config_write()

def get_game_file_type(game_file_type):
    if (game_file_type == "filter"):
        game_file_type = "Data\\Strings\\aionfilterline.pak"
    elif (game_file_type == "font"):
        game_file_type = "textures\\ui\\hit_number.pak"
    elif (game_file_type == "voice"):
        game_file_type = "sounds\\voice\\attack\\attack.pak"
    return game_file_type

def get_file_path(lang, game_file_type):
    app_config = app_config_read()[0]

    if lang == "assets":
        file_path = f"assets\{game_file_type}"
    elif lang == "enu":
        file_path = f"{app_config.get('app', 'napath')}\\l10n\\{lang}\\{game_file_type}"
    else:
        file_path = f"{app_config.get('app', 'eupath')}\\l10n\\{lang}\\{game_file_type}"
    return file_path

def check_files_hash(game_lang, game_file_type):
    """
    Returns the files' Hashes as requested by check_files()
    """
    try:
        game_file_type = get_game_file_type(game_file_type)

        check_hash = []
        for lang in game_lang:
            file_path = get_file_path(lang, game_file_type)

            if os.path.isfile(file_path):
                with open(file_path, 'rb', buffering=0) as f:
                    hashed = hashlib.file_digest(f, 'sha256').hexdigest()
                    check_hash.append(hashed)
            else:
                check_hash.append(False)

        return [check_hash, game_file_type]
    except Exception as e:
        print("ERROR -> check_files_hash() :: "+str(e))

def check_files():
    """
    This function returns the HASH of all files that the app can modify
    depending on the installed game versions and the LANG information
    of the versions.
    If any of the files return a False, then all of them will be replaced
    when you call the 'copy_files()' function.
    If a directory is not found or a HASH does not match the assets' file,
    it returns a boolean "False" statement.
    """
    try:
        app_config = app_config_read()[0]
        game_lang = ["assets", "enu", "eng", "deu", "fra"] # Define all possible game LANG
        filter_hash = check_files_hash(game_lang, "filter") # Get all filter pak hashes
        font_hash = check_files_hash(game_lang, "font") # Get all font pak hashes
        voice_hash = check_files_hash(game_lang, "voice") # Get all voice pak hashes

        #print(filter_hash)
        #print(font_hash)
        #print(voice_hash)

        check_filter_pass = True
        check_font_pass = True
        check_voice_pass = True

        # Checks if we are missing any Original files in the "assets" folder
        if (filter_hash[0][0] != False) and (font_hash[0][0] != False) and (voice_hash[0][0] != False):
            app_region = app_config.get('app', 'region')
            # Checks if the NA region is eligible for hash validation
            if (app_region == "1") or (app_region == "3"):
                # Matches original file hash against all NA hashes
                if (filter_hash[0][1] != filter_hash[0][0]):
                    check_filter_pass = False
                if (font_hash[0][1] != font_hash[0][0]):
                    check_font_pass = False
                if (voice_hash[0][1] != voice_hash[0][0]):
                    check_voice_pass = False
                    
            # Checks if the EU region is eligible for hash validation
            if (app_region == "2") or (app_region == "3"):
                # Matches assets file hash against all EU hashes
                if (filter_hash[0][2] != filter_hash[0][0]) or (filter_hash[0][3] != filter_hash[0][0]) or (filter_hash[0][4] != filter_hash[0][0]):
                    check_filter_pass = False
                if (font_hash[0][2] != font_hash[0][0]) or (font_hash[0][3] != font_hash[0][0]) or (font_hash[0][4] != font_hash[0][0]):
                    check_font_pass = False
                if (voice_hash[0][2] != voice_hash[0][0]) or (voice_hash[0][3] != voice_hash[0][0]) or (voice_hash[0][4] != voice_hash[0][0]):
                    check_voice_pass = False
        
        # Returns the validation + game LANGS
        print([check_filter_pass, check_font_pass, check_voice_pass, game_lang])
        return [check_filter_pass, check_font_pass, check_voice_pass, game_lang]
    except Exception as e:
        print("ERROR -> check_files() :: "+str(e))

def check_game_path():
    app_config = app_config_read()[0]
    na_path = app_config.get('app', 'napath')
    eu_path = app_config.get('app', 'eupath')

    #print(f"APP CONFIG NA PATH #1: {na_path}")
    if not na_path:
        classic_na_path()
        app_config = app_config_read()[0]
        na_path = app_config.get('app', 'napath')

        #print(f"APP CONFIG NA PATH #2: {na_path}")
        if not na_path:
            #print("COULD'NT FIND NA GAME DIRECTORY.")
            return
    if na_path:
        game_path = f"{na_path}\\bin64\\Aion.bin"
        if not os.path.isfile(game_path):
            app_config.set('app', 'napath', "")
            app_config_write()

    #print(f"APP CONFIG EU PATH #1: {eu_path}")
    if not eu_path:
        classic_eu_path()
        app_config = app_config_read()[0]
        eu_path = app_config.get('app', 'eupath')

        #print(f"APP CONFIG EU PATH #2: {eu_path}")
        if not eu_path:
            #print("COULD'NT FIND EU GAME DIRECTORY.")
            return
        
    if eu_path:
        game_path = f"{eu_path}\\bin64\\aionclassic.bin"
        if not os.path.isfile(game_path):
            app_config.set('app', 'eupath', "")
            app_config_write()

def copy_files_exec(game_file_type, langs):
    file_path = get_game_file_type(game_file_type)

    #TODO move all voice from assets to game folder

    for lang in langs:
        if lang != "assets":
            assets_path = f"assets\\{file_path}"
            dest_path = get_file_path(lang, file_path)
            
            print(f"ASSETS: {assets_path} DEST: {dest_path}")
            if not os.path.isdir(os.path.dirname(dest_path)):
                print(f"MKDIR: {os.path.dirname(dest_path)}")
                try:
                    os.makedirs(os.path.dirname(dest_path))
                except Exception as e:
                    print("ERROR -> copy_files_exec() -> os.makedirs() :: " +str(e))
            if os.path.isfile(dest_path):
                print(f"REMOVE: {dest_path} ISFILE? {os.path.isfile(dest_path)}")
                try:
                    os.remove(dest_path)
                except Exception as e:
                    print("ERROR -> copy_files_exec() -> os.remove() :: " +str(e))
            try:
                print("COPY")
                os.system(f'copy {assets_path} {dest_path}')
            except Exception as e:
                print("ERROR -> copy_files_exec() -> os.system() :: " +str(e))

def copy_files(game_file_type):
        app_config = app_config_read()[0]
        check_files_result = check_files()
        langs = check_files_result[3]

        current_dir = f"{os.getcwd()}\\assets\\sounds\\{game_file_type}"
        print(os.listdir(current_dir))

        print(f"GAME FILE TYPE: {game_file_type}")

        if game_file_type == "filter":
            if (check_files_result[0] == False):
                check_game_path()
                copy_files_exec(game_file_type, langs)
        elif game_file_type == "font":
            if (check_files_result[1] == False):
                check_game_path()
                copy_files_exec(game_file_type, langs)
        elif game_file_type == "voice":
            if (check_files_result[2] == False):
                check_game_path()
                copy_files_exec(game_file_type, langs)

#copy_files("filter")
#copy_files("font")
copy_files("voice")
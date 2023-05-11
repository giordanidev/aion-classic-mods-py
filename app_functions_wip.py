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
        get_exception(e)
        return
    
app_config = app_config_read()[0]
config_full_path = app_config_read()[1]

def first_run():
    if not app_config.get('app', 'region'):
        try:
            classic_na_path()
            classic_eu_path()
            define_region()
            check_files()

        except: ""

def app_config_write():
    try:
        with open(config_full_path, 'w') as config_write:
            app_config.write(config_write)

    except Exception as e:
        get_exception(e)
        return

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
                get_exception(e)
                return

        if (not_found == False):
            print("Client found: "+eu_dir)
            app_config.set('app', 'eupath', eu_dir)
            app_config_write()
        else:
            print("Client not found. Please select manually.")

    except:
        print("Client not found. Please select manually.")
        return

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
        get_exception(e)
        return

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

def define_region():
    count_region = 0
    check_game_path()
    app_config_read()

    if app_config.get('app', 'napath'): count_region += 1
    if app_config.get('app', 'eupath'): count_region += 2

    app_config.set('app', 'region', str(count_region))
    app_config_write()

def check_files(game_file_type):
    """
    This function returns the Hash and Full Path of all files that the
    app can modify depending on the installed game versions, considering
    the given File Type.

    If any of the files doesn't exists it returns a 'False' boolean that
    will be used to validate the copying of the files.

    If the returned value is a Hash, then all of the files will be replaced
    when it calls the 'copy_files_exec()' function.
    """
    try:
        app_config = app_config_read()[0]
        app_region = app_config.get('app', 'region')
        print(f"DEBUG :: check_files() -> app_region: {app_region}.")
        game_lang = []

        if not app_region in ("1", "2", "3"):
            print("ERROR -> app_region :: Region is not set.")
            return

        if app_region  in ("1", "3"):
            game_lang.append("enu")
        if app_region in ("2", "3"):
            game_lang.extend(["eng", "fra", "deu"])

        if game_file_type in ("filter", "font", "voice"):
            print(f"DEBUG -> check_files() :: game_lang: {game_lang}")
            files_hash = get_files_hash(game_lang, game_file_type) # Get all files' hashes
        else:
            print("ERROR -> check_files() :: Unknown file type.")
            return

        print(f"DEBUG :: check_files() -> files_hash: {files_hash} {len(files_hash)}.")
        return files_hash
    
    except Exception as e:
        get_exception(e)
        return

def get_files_hash(game_lang, game_file_type):
    """
    Returns the files' Hashes as requested by check_files()
    """
    try:
        file_path = get_game_file_path(game_file_type)
        print(f"DEBUG :: get_files_hash() -> file_path: {file_path} {len(file_path)}.")

        assets_full_file_path = [f"assets\{file_path}"]

        all_assets_files = get_all_files(assets_full_file_path)
        print(f"DEBUG -> get_files_hash() -> all_assets_files: {all_assets_files} {len(all_assets_files)}")

        full_file_path = get_full_file_path(game_lang, file_path)
        all_game_files = get_all_files(full_file_path)
        print(f"DEBUG -> get_files_hash() -> all_game_files: {all_game_files} {len(all_game_files)}")

        all_assets_files_hash = get_files_hash_exec(all_assets_files)
        all_game_files_hash = get_files_hash_exec(all_game_files)

        print(f"DEBUG :: check_files_hash() -> \n\nall_assets_files_hash: {len(all_assets_files_hash)} \n{all_assets_files_hash} -> \n\nall_game_files_hash: {len(all_game_files_hash)}\n{all_game_files_hash} -> \n\ngame_file_type: {game_file_type}.")
        return [all_assets_files_hash, all_game_files_hash]
    
    except Exception as e:
        get_exception(e)
        return
    
def get_files_hash_exec(all_files):
    #TODO validate destinations for 'False' if file not found

    print(f"DEBUG :: get_files_hash_exec() -> all_files: {all_files} {len(all_files)}.")
    full_hash = []
    for list in all_files:
        print(f"DEBUG :: get_files_hash_exec() -> list: {list} {len(list)}.")
        files_hash = []
        for file in list:
            print(f"DEBUG :: get_files_hash_exec() -> file: {file}.")
            with open(file, 'rb', buffering=0) as f:
                hashed = hashlib.file_digest(f, 'sha256').hexdigest()
                files_hash.extend([[hashed, file]])
        full_hash.extend([files_hash])
    print(f"DEBUG :: get_files_hash_exec() -> files_hash: {files_hash} {len(files_hash)}.")
    return full_hash

def get_game_file_path(game_file_type):
    if (game_file_type == "filter"):
        file_path = "data\\Strings"
    elif (game_file_type == "font"):
        file_path = "textures\\ui"
    elif (game_file_type == "voice"):
        file_path = "sounds\\voice"
    else:
        print("ERROR -> get_game_file_path() :: Unknown file type.")
        return
    return file_path

def get_full_file_path(game_lang, file_path):
    app_config = app_config_read()[0]
    na_path = app_config.get('app', 'napath')
    eu_path = app_config.get('app', 'eupath')

    full_file_path = []

    for lang in game_lang:
        if lang == "enu":
            full_file_path.append(f"{na_path}\\l10n\\{lang}\\{file_path}")
        elif lang in ("eng", "fra", "deu"):
            full_file_path.append(f"{eu_path}\\l10n\\{lang}\\{file_path}")
        else:
            print("ERROR -> get_full_file_path() :: Unknown region.")
            return
    return full_file_path
        
def get_all_files(file_path):
    all_game_files = []
    print(f"DEBUG :: get_all_files() -> file_path: {file_path} {len(file_path)}.")
    for path in file_path:
        game_files = []
        print(f"DEBUG :: get_all_files() -> path: {path} {len(path)}.")
        for root, dirs, files in os.walk(path):
            for file in files:
                print(f"DEBUG :: get_all_files() -> file: {os.path.join(root, file)}.")
                game_files.extend([os.path.join(root, file)])
        all_game_files.extend([game_files])
    return all_game_files

def copy_files(game_file_type):
        print(f"DEBUG -> copy_files() -> GAME FILE TYPE: {game_file_type}")

        check_files_result = check_files(game_file_type) # Returns [[[[assets_hash, assets_path]]],[[lang[[file_hash, file_path]]]]
        asset_files_hash = check_files_result[0]
        game_files_hash = check_files_result[1]

        #TODO compare and validate destinations

        #copy_files_exec(check_files_result)
        
        """
        current_dir = f"{os.getcwd()}\\assets\\sounds\\{game_file_type}"
        print(os.listdir(current_dir))
        if os.path.isdir(os.path.dirname(current_dir)):
                print(f"REMOVE: {os.path.dirname(current_dir)} ISFILE? {os.path.isfile(current_dir)}")
                try:
                    os.remove(os.path.dirname(current_dir))
                except Exception as e:
                    get_exception(e)

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
        """

def copy_files_exec(check_files_result):
    
    #TODO move all files from assets to game folder

    try:
        assets_result = check_files_result[0]
        print(f"DEBUG :: copy_files_exec() -> assets_result: {assets_result}.")
        files_result = check_files_result[1]
        print(f"DEBUG :: copy_files_exec() -> files_result: {files_result}.")

        for file in files_result:
            print(f"DEBUG -> ASSETS: {assets_result[1]} DEST: {file[1]}")
            if not os.path.isdir(os.path.dirname(file[1])):
                print(f"DEBUG -> MKDIR: {os.path.dirname(file[1])}")
                try:
                    os.makedirs(os.path.dirname(file[1]))
                except Exception as e:
                    get_exception(e)
                    return
            if os.path.isfile(file[1]):
                print(f"DEBUG -> REMOVE: {file[1]} ISFILE? {os.path.isfile(file[1])}")
                try:
                    os.remove(file[1])
                except Exception as e:
                    get_exception(e)
                    return
            try:
                print("DEBUG -> COPY")
                os.system(f'copy {assets_result[1]} {file[1]}')
            except Exception as e:
                get_exception(e)
                return
    except Exception as e:
        get_exception(e)
        return
    
def get_exception(e):
    trace = []
    tb = e.__traceback__
    while tb is not None:
        trace.append({
            "filename": tb.tb_frame.f_code.co_filename,
            "function name": tb.tb_frame.f_code.co_name,
            "line": tb.tb_lineno
        })
        tb = tb.tb_next
    print({
        'ERROR': type(e).__name__,
        'message': str(e),
        'trace': trace
    })


#copy_files("filter")
#copy_files("font")
copy_files("voice")
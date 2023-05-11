from configparser import ConfigParser
import os, os.path, hashlib, winreg, ntpath

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
        except Exception as e:
            get_exception(e)
            return

def app_config_write():
    try:
        with open(config_full_path, 'w') as config_write:
            app_config.write(config_write)

    except Exception as e:
        get_exception(e)
        return

def classic_eu_path():
    """
    This function will attempt to get the installation path for
    the AION Classic Europe and save it to the 'config.ini' file.

    If it fails it will prompt the user to select a path manually.
    """
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

    except Exception as e:
        get_exception(e)
        return

def classic_na_path():
    """
    This function will attempt to get the installation path for
    the AION Classic North America and save it to the 'config.ini' file.

    If it fails it will prompt the user to select a path manually.
    """
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
    """
    This function verifies if the client path is correct
    before trying to download and copy files.
    """
    app_config = app_config_read()[0]
    na_path = app_config.get('app', 'napath')
    eu_path = app_config.get('app', 'eupath')

    #print(f"APP CONFIG NA PATH #1: {na_path}")
    if not na_path:
        classic_na_path()

    if na_path:
        game_path = f"{na_path}\\bin64\\Aion.bin"
        if not os.path.isfile(game_path):
            app_config.set('app', 'napath', "")
            app_config_write()

    #print(f"APP CONFIG EU PATH #1: {eu_path}")
    if not eu_path:
        classic_eu_path()
        
    if eu_path:
        game_path = f"{eu_path}\\bin64\\aionclassic.bin"
        if not os.path.isfile(game_path):
            app_config.set('app', 'eupath', "")
            app_config_write()

def define_region():
    """
    This function defines the region that is used to define
    which versions of the game will have files replaced on
    request.
    """
    count_region = 0
    check_game_path()
    app_config_read()

    if app_config.get('app', 'napath'): count_region += 1
    if app_config.get('app', 'eupath'): count_region += 2

    app_config.set('app', 'region', str(count_region))
    app_config_write()

def get_game_file_path(game_file_type):
    """
    
    """
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
    """
    
    """
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
        #print(f"DEBUG :: check_files() -> app_region: {app_region}.")
        game_lang = []

        if not app_region in ("1", "2", "3"):
            print("ERROR -> app_region :: Region is not set.")
            return

        if app_region  in ("1", "3"):
            game_lang.append("enu")
        if app_region in ("2", "3"):
            game_lang.extend(["eng", "fra", "deu"])

        if game_file_type in ("filter", "font", "voice"):
            #print(f"DEBUG -> check_files() :: game_lang: {game_lang}")
            full_files = get_full_files(game_lang, game_file_type) # Get files' hashes when files already exist in game path
        else:
            print("ERROR -> check_files() :: Unknown file type.")
            return

        #print(f"DEBUG :: check_files() -> files_hash: {files_hash} {len(files_hash)}.")
        return full_files
    
    except Exception as e:
        get_exception(e)
        return

def get_full_files(game_lang, game_file_type):
    """
    Returns the list of files that should be copied or replaced
    in the game path.
    """
    try:
        file_path = get_game_file_path(game_file_type)
        #print(f"DEBUG :: get_full_files() -> file_path: {file_path} {len(file_path)}.")

        assets_full_file_path = [f"assets\{file_path}"] # Defines assets path
        full_file_path = get_full_file_path(game_lang, file_path) # Returns [full_file_path]. It can be multiple paths depending on regions selected

        compared_files = compare_files(assets_full_file_path, full_file_path) # Returns [[check_hash_list], [copy_files_list]]

        copy_files_check = compare_files_hash(compared_files)

        #print(f"DEBUG :: get_full_files() -> copy_files_check: {len(copy_files_check)} \n{copy_files_check}")
        return copy_files_check
    
    except Exception as e:
        get_exception(e)
        return
    
def compare_files_hash(compared_files):
    """
    
    """
    #print(f"DEBUG :: compare_files_hash() -> compared_files: {len(compared_files)} \n{compared_files}.")
    check_hash_list = compared_files[0]
    copy_files_list = compared_files[1]

    for list in check_hash_list:
        asset_file = list[0]
        game_file = list[1]
        #print(f"DEBUG :: compare_files_hash() -> asset_file: {asset_file}.")
        with open(asset_file, 'rb', buffering=0) as f:
            asset_file_hashed = hashlib.file_digest(f, 'sha256').hexdigest()

        #print(f"DEBUG :: compare_files_hash() -> game_file: {game_file}.")
        with open(game_file, 'rb', buffering=0) as f:
            game_file_hashed = hashlib.file_digest(f, 'sha256').hexdigest()
        if asset_file_hashed != game_file_hashed:
            copy_files_list.extend([[asset_file, game_file]])

    #print(f"DEBUG :: compare_files_hash() -> copy_files_list: {len(copy_files_list)} \n{copy_files_list}.")
    return copy_files_list
        
def compare_files(assets_full_file_path, full_file_path):
    #print(f"DEBUG :: compare_files() -> assets_full_file_path: \n{assets_full_file_path}.\nDEBUG :: compare_files() -> full_file_path: \n{full_file_path}.")

    try:
        copy_files_list = []
        check_hash_list = []
        for assets_dir in assets_full_file_path:
            #print(f"DEBUG :: compare_files() -> assets_dir: {assets_dir}.")
            for (dirpath, dirnames, filenames) in os.walk(assets_dir):
                for filename in filenames:
                    relative_path = dirpath.replace(assets_dir, "")
                    for files_dir in full_file_path:
                        asset_path = assets_dir+'\\'+filename
                        file_path = files_dir+relative_path+'\\'+filename
                        if not os.path.exists(file_path):
                            #print(f"DEBUG :: compare_files() -> file_path -> copy_files_list[]: NAY {file_path}")
                            copy_files_list.extend([[asset_path, file_path]])
                        else:
                            #print(f"DEBUG :: compare_files() -> file_path -> check_hash_list[]: AY {file_path}")
                            check_hash_list.extend([[asset_path, file_path]])

            #print(f"DEBUG :: compare_files() -> check_hash_list: \n{check_hash_list}")
            #print(f"DEBUG :: compare_files() -> copy_files_list: \n{copy_files_list}")
            return [check_hash_list, copy_files_list]

    except Exception as e:
        get_exception(e)
        return
    
def copy_files(game_file_type):
    """

    """
    try:
        #print(f"DEBUG -> copy_files() -> GAME FILE TYPE: {game_file_type}")
        copy_files_list = check_files(game_file_type) # Returns [[asset_path, file_path]] ready to copy!

        """
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
        """

    except Exception as e:
        get_exception(e)
        return
    
def get_exception(e):
    """
    This function keeps track of Exception errors.
    """
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


copy_files("filter")
#copy_files("font")
#copy_files("voice")
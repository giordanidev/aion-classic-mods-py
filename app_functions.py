from configparser import ConfigParser
import os, os.path, hashlib, winreg, sys

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

load_configs = app_config_read()
app_config = load_configs[0]
config_full_path = load_configs[1]

def app_config_write(app_config):
    try:
        with open(config_full_path, 'w') as config_write:
            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> config_write: \n{app_config.items('app')}")
            app_config.write(config_write)

    except Exception as e:
        get_exception(e)
        return

def first_run():
    app_config = app_config_read()[0]
    if not app_config.get('app', 'region'):
        try:
            #print(f"DEBUG -> {sys._getframe().f_code.co_name}() :: First run!")
            classic_na_path()
            classic_eu_path()
            check_game_path()
            define_region()
        except Exception as e:
            get_exception(e)
            return
        return True
    else:
        ""
        #print(f"DEBUG -> {sys._getframe().f_code.co_name}() :: Not the first run!")

def classic_na_path():
    """
    Attempts to get the installation path for the AION Classic North
    America and save it to the 'config.ini' file.

    If it fails it will prompt the user to select a path manually.
    """
    try:
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\NCWest\\AION_CLASSIC')
        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> a_key: {a_key}")

        if a_key:
            classic_na_path = winreg.QueryValueEx(a_key, "BaseDir")[0]
            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> na_dir: {classic_na_path}")
            if classic_na_path[len(classic_na_path)-1] == "\\":
                classic_na_path = classic_na_path.rstrip(classic_na_path[-1])
            app_config = app_config_read()[0]
            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> app_config_read(): \n{app_config}")
            app_config.set('app', 'napath', classic_na_path)
            app_config_write(app_config)
            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> app_config_write()")
            
    except Exception as e:
        get_exception(e)
        return

def classic_eu_path():
    """
    Attempts to get the installation path for the AION Classic Europe
    and save it to the 'config.ini' file.

    If it fails it will prompt the user to select a path manually.
    """
    try:
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall')
        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> a_key: {a_key}")

        not_found = True
        for i in range(1024):
            try:
                key_name = winreg.EnumKey(a_key, i)
                #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> key_name: {key_name}")
                o_key = winreg.OpenKey(a_key, key_name)
                #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> o_key: {o_key}")
                display_name = winreg.QueryValueEx(o_key, "DisplayName")[0]
                #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> display_name: {display_name}")
                if display_name == "AION Classic":
                    game_publisher = winreg.QueryValueEx(o_key, "Publisher")[0]
                    if (game_publisher == "Gameforge"):
                        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> classic_eu_publisher[0]: {game_publisher}")
                        classic_eu_path = winreg.QueryValueEx(o_key, "InstallLocation")
                        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> classic_eu_path: {classic_eu_path}")
                        eu_dir = classic_eu_path[0]
                        not_found = False

            except:
                ""

        if (not_found == False):
            app_config = app_config_read()[0]
            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> app_config_read(): \n{app_config}")
            app_config.set('app', 'eupath', eu_dir)
            app_config_write(app_config)
            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> app_config_write()")
        else:
            print("Client not found. Please select manually.")

    except Exception as e:
        get_exception(e)
        return

def define_region():
    """
    Defines the region that is used to set which versions of
    the game will have files replaced on request.
    """
    count_region = 0
    check_game_path() # Checks if game path selected is accurate.
    app_config = app_config_read()[0] # Reloads config.

    if app_config.get('app', 'napath'): count_region += 1
    if app_config.get('app', 'eupath'): count_region += 2

    app_config.set('app', 'region', str(count_region))
    app_config_write(app_config)

def check_game_path():
    """
    Verifies if the client path is correct before trying to
    copy files. If it cannot reach the game executable file
    using the saved path it removes it from config and prompts
    the user to select a new path.
    """
    app_config = app_config_read()[0]
    #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> app_config_read(): \n{app_config}")
    na_path = app_config.get('app', 'napath')
    eu_path = app_config.get('app', 'eupath')

    if na_path:
        game_path = f"{na_path}\\bin64\\Aion.bin"
        if not os.path.isfile(game_path):
            app_config.set('app', 'napath', "")
            app_config_write(app_config)

    if eu_path:
        game_path = f"{eu_path}\\bin64\\aionclassic.bin"
        if not os.path.isfile(game_path):
            app_config.set('app', 'eupath', "")
            app_config_write(app_config)

def get_game_file_path(game_file_type):
    """
    Sets the base path for each asset/file type.
    """
    if (game_file_type == "filter"):
        file_path = "data\\Strings"
    elif (game_file_type == "font"):
        file_path = "textures\\ui"
    elif (game_file_type == "voice"):
        file_path = "sounds\\voice"
    else:
        print(f"ERROR -> {sys._getframe().f_code.co_name}() :: Unknown file type.")
        return
    return file_path

def get_full_file_path(game_lang, file_path):
    """
    Gets the full file paths for the selected regions using the
    previously set base file path.
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
            print(f"ERROR -> {sys._getframe().f_code.co_name}() :: Unknown region.")
            return
    return full_file_path

def check_files(game_file_type):
    """
    Defines regions and languages of which the app will use to
    look for files.

    Calls 'get_full_files()' to finish processing the request.
    """
    try:
        app_config = app_config_read()[0]
        app_region = app_config.get('app', 'region')
        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> app_region: {app_region}.")
        game_lang = []

        if not app_region in ("1", "2", "3"):
            print(f"ERROR -> {sys._getframe().f_code.co_name}() -> app_region :: Region is not set.")
            return

        if app_region  in ("1", "3"):
            game_lang.append("enu")
        if app_region in ("2", "3"):
            game_lang.extend(["eng", "fra", "deu"])

        if game_file_type in ("filter", "font", "voice"):
            #print(f"DEBUG -> {sys._getframe().f_code.co_name}() :: game_lang: {game_lang}")
            # Gets all files and hashes them when files already exist in game path
            copy_files_check = get_full_files(game_lang, game_file_type)
        else:
            print(f"ERROR -> {sys._getframe().f_code.co_name}() :: Unknown file type.")
            return

        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> files_hash: {files_hash} {len(files_hash)}.")
        return copy_files_check
    
    except Exception as e:
        get_exception(e)
        return

def get_full_files(game_lang, game_file_type):
    """
    Returns the list of files that should be copied or replaced
    in the game path.

    #1 - Calls 'get_game_file_path()' to get the base directories of files;

    #2 - Sets the assets full path directory;

    #3 - Calls 'get_full_file_path' to set the full path of the installed
    versions/regions of the game files.

    #4 - Calls 'compare_files()' that checks for missing files in the game
    path that are stored in the assets path and returns two lists:
    - One list contains duplicated files that should be hashed;
    - The second list contains the files that should be copied because
    the app could not find them in the game path.

    #5 - Calls 'compare_files_hash()' to determine if the duplicated
    files are equal or differ from the asset files path.
    - If the files are different, then it adds the files to the
    list of files that should be copied. If hashes match, ignores
    those files.

    #6 - Returns the final list of files that should be copied, even if
    they are already in the game path but are different files.

    #7 - Stores the files on the const 'copy_files_check' variable to be
    used by the 'copy_files()' command when requested.
    """
    try:
        file_path = get_game_file_path(game_file_type)
        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> file_path: {file_path} {len(file_path)}.")

        # Defines assets path
        assets_full_file_path = [f"assets\{file_path}"]
        # Returns [full_file_path]. It can be multiple paths depending on regions selected
        full_file_path = get_full_file_path(game_lang, file_path)

        # Returns [[check_hash_list], [copy_files_list]]
        compared_files = compare_files(assets_full_file_path, full_file_path) 

        # Compares duplicated files hashes and adds them to the copy_files_check list if hashes differ
        copy_files_check = compare_files_hash(compared_files) 

        
        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> copy_files_check: {len(copy_files_check)} \n{copy_files_check}")
        return copy_files_check
    
    except Exception as e:
        get_exception(e)
        return
    
def compare_files_hash(compared_files):
    """
    Compares duplicated files hashes and adds them to the
    copy_files_check list if hashes differ.
    Returns a single list of files with both assets and game
    file paths ready to be replaced in [[asset_file, game_file]]
    format.
    """
    #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> compared_files: {len(compared_files)} \n{compared_files}.")
    check_hash_list = compared_files[0]
    copy_files_list = compared_files[1]

    for list in check_hash_list:
        asset_file = list[0]
        game_file = list[1]
        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> asset_file: {asset_file}.")
        with open(asset_file, 'rb', buffering=0) as f:
            asset_file_hashed = hashlib.file_digest(f, 'sha256').hexdigest()

        #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> game_file: {game_file}.")
        with open(game_file, 'rb', buffering=0) as f:
            game_file_hashed = hashlib.file_digest(f, 'sha256').hexdigest()
        if asset_file_hashed != game_file_hashed:
            copy_files_list.extend([[asset_file, game_file]])

    #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> copy_files_list: {len(copy_files_list)} \n{copy_files_list}.")
    return copy_files_list
        
def compare_files(assets_full_file_path, full_file_path):
    #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> assets_full_file_path: \n{assets_full_file_path}.\nDEBUG :: compare_files() -> full_file_path: \n{full_file_path}.")

    try:
        copy_files_list = []
        check_hash_list = []
        for assets_dir in assets_full_file_path:
            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> assets_dir: {assets_dir}.")
            for (dirpath, dirnames, filenames) in os.walk(assets_dir):
                for filename in filenames:
                    relative_path = dirpath.replace(assets_dir, "")
                    for files_dir in full_file_path:
                        asset_path = assets_dir+'\\'+filename
                        file_path = files_dir+relative_path+'\\'+filename
                        if not os.path.exists(file_path):
                            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> file_path -> copy_files_list[]: NAY {file_path}")
                            copy_files_list.extend([[asset_path, file_path]])
                        else:
                            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> file_path -> check_hash_list[]: AY {file_path}")
                            check_hash_list.extend([[asset_path, file_path]])

            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> check_hash_list: \n{check_hash_list}")
            #print(f"DEBUG :: {sys._getframe().f_code.co_name}() -> copy_files_list: \n{copy_files_list}")
            return [check_hash_list, copy_files_list]

    except Exception as e:
        get_exception(e)
        return
    
def copy_files(copy_files_check):
    """
    Creates directories, removes old/different files, copies
    new files.
    """
    try:
        print(f"DEBUG -> {sys._getframe().f_code.co_name}() -> copy_files_check: \n{copy_files_check}")

        """
        assets_result = check_files_result[0]
        print(f"DEBUG -> {sys._getframe().f_code.co_name}() -> assets_result: {assets_result}.")
        files_result = check_files_result[1]
        print(f"DEBUG -> {sys._getframe().f_code.co_name}() -> files_result: {files_result}.")

        for file in files_result:
            print(f"DEBUG -> ASSETS: {assets_result[1]} DEST: {file[1]}")
            if not os.path.isdir(os.path.dirname(file[1])):
                print(f"DEBUG -> {sys._getframe().f_code.co_name}() -> MKDIR: {os.path.dirname(file[1])}")
                try:
                    os.makedirs(os.path.dirname(file[1]))
                except Exception as e:
                    get_exception(e)
                    return
            if os.path.isfile(file[1]):
                print(f"DEBUG -> {sys._getframe().f_code.co_name}() -> REMOVE: {file[1]} ISFILE? {os.path.isfile(file[1])}")
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

#check_files("filter")
#check_files("font")
#check_files("voice")
#copy_files(copy_files_check)
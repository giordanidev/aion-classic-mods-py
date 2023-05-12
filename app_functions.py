from configparser import ConfigParser
import os, os.path, hashlib, winreg, sys, json, logging

logging.basicConfig(filename='.\\config\\logs\\logs.log', format='%(asctime)s [%(levelname)s] -> :: %(message)s', encoding='utf-8', level=logging.DEBUG, filemode='w')
logging.getLogger().addHandler(logging.StreamHandler())

def app_config_read():
    try:
        app_config = ConfigParser()
        config_path = 'config/'
        config_file = 'config.ini'
        config_full_path = config_path + config_file
        app_config.read(config_full_path)
        logging.info(f"{sys._getframe().f_code.co_name}() -> app_config_read: {app_config.items('app')}")
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
            logging.info(f"{sys._getframe().f_code.co_name}() -> app_config_write: {app_config.items('app')}")
            app_config.write(config_write)

    except Exception as e:
        get_exception(e)
        return

def first_run():
    app_config = app_config_read()[0]
    if not app_config.get('app', 'region'):
        try:
            logging.info(f"{sys._getframe().f_code.co_name}() :: First run!")
            classic_na_path()
            classic_eu_path()
            check_game_path()
            define_region()
        except Exception as e:
            get_exception(e)
            return
        return True
    else:
        logging.info(f"{sys._getframe().f_code.co_name}() :: Not the first run anymore!")
        return False

def classic_na_path():
    """
    Attempts to get the installation path for the AION Classic North
    America and save it to the 'config.ini' file.

    If it fails it will prompt the user to select a path manually.
    """
    try:
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\NCWest\\AION_CLASSIC')

        if a_key:
            classic_na_path = winreg.QueryValueEx(a_key, "BaseDir")[0]
            logging.debug(f"{sys._getframe().f_code.co_name}() -> na_dir: {classic_na_path}")
            if classic_na_path[len(classic_na_path)-1] == "\\":
                classic_na_path = classic_na_path.rstrip(classic_na_path[-1])
            app_config = app_config_read()[0]
            app_config.set('app', 'napath', classic_na_path)
            app_config_write(app_config)
            
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

        not_found = True
        for i in range(1024):
            try:
                key_name = winreg.EnumKey(a_key, i)
                o_key = winreg.OpenKey(a_key, key_name)
                display_name = winreg.QueryValueEx(o_key, "DisplayName")[0]
                if display_name == "AION Classic":
                    game_publisher = winreg.QueryValueEx(o_key, "Publisher")[0]
                    if (game_publisher == "Gameforge"):
                        logging.debug(f"{sys._getframe().f_code.co_name}() -> display_name: {display_name}")
                        logging.debug(f"{sys._getframe().f_code.co_name}() -> game_publisher: {game_publisher}")
                        classic_eu_path = winreg.QueryValueEx(o_key, "InstallLocation")[0]
                        logging.debug(f"{sys._getframe().f_code.co_name}() -> classic_eu_path: {classic_eu_path}")
                        not_found = False
                if not_found == False:
                    if classic_eu_path[len(classic_eu_path)-1] == "\\":
                        classic_eu_path = classic_eu_path.rstrip(classic_eu_path[-1])
                    app_config = app_config_read()[0]
                    app_config.set('app', 'eupath', classic_eu_path)
                    app_config_write(app_config)
                    return

            except:
                continue

        if not_found == True:
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
        logging.warning(f"ERROR -> {sys._getframe().f_code.co_name}() :: Unknown file type.")
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
            logging.warning(f"ERROR -> {sys._getframe().f_code.co_name}() :: Unknown region.")
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
        #print(f"{sys._getframe().f_code.co_name}() -> app_region: {app_region}.")
        game_lang = []

        if not app_region in ("1", "2", "3"):
            logging.warning(f"ERROR -> {sys._getframe().f_code.co_name}() -> app_region :: Region is not set.")
            return

        if app_region  in ("1", "3"):
            game_lang.append("enu")
        if app_region in ("2", "3"):
            game_lang.extend(["eng", "fra", "deu"])

        if game_file_type in ("filter", "font", "voice"):
            # Gets all files and hashes them when files already exist in game path
            copy_files_check = get_full_files(game_lang, game_file_type)
        else:
            logging.warning(f"ERROR -> {sys._getframe().f_code.co_name}() -> game_file_type: {game_file_type} :: Unknown file type.")
            return

        logging.debug(f"{sys._getframe().f_code.co_name}() -> copy_files_check: {len(copy_files_check)} {copy_files_check}.")
        if len(copy_files_check) <= 0:
            return False
        elif len(copy_files_check) >= 1:
            return True
        else:
            logging.warning(f"{sys._getframe().f_code.co_name}() -> copy_files_check type: {type(copy_files_check)}.")
        
    
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

    #7 - Stores the files in a JSON file at './assets/lists/{type}_files.json'
    to be used by the 'copy_files()' command when requested.
    """
    try:
        file_path = get_game_file_path(game_file_type)
        logging.debug(f"{sys._getframe().f_code.co_name}() -> file_path: {file_path}.")

        # Defines assets path
        assets_full_file_path = [f".\\assets\\{file_path}"]
        # Returns [full_file_path]. It can be multiple paths depending on regions selected
        full_file_path = get_full_file_path(game_lang, file_path)

        # Returns [[check_hash_list], [copy_files_list]]
        compared_files = compare_files(assets_full_file_path, full_file_path) 

        # Compares duplicated files hashes and adds them to the copy_files_check list if hashes differ
        copy_files_check = compare_files_hash(compared_files) 

        with open(f'.\\config\\lists\\{game_file_type}_files.json', 'w', encoding='utf-8') as f:
            json.dump(copy_files_check, f, ensure_ascii=False, indent=4)
            f.close

        logging.debug(f"{sys._getframe().f_code.co_name}() -> copy_files_check: {len(copy_files_check)} {copy_files_check}")
        return copy_files_check
    
    except Exception as e:
        get_exception(e)
        return
        
def compare_files(assets_full_file_path, full_file_path):
    logging.debug(f"{sys._getframe().f_code.co_name}() -> assets_full_file_path: {assets_full_file_path}. compare_files() -> full_file_path: {full_file_path}.")

    try:
        copy_files_list = []
        check_hash_list = []
        for assets_dir in assets_full_file_path:
            logging.debug(f"{sys._getframe().f_code.co_name}() -> assets_dir: {assets_dir}.")
            for (dirpath, dirnames, filenames) in os.walk(assets_dir):
                for filename in filenames:
                    relative_path = dirpath.replace(assets_dir, "")
                    for files_dir in full_file_path:
                        asset_path = assets_dir+relative_path+'\\'+filename
                        file_path = files_dir+relative_path+'\\'+filename
                        if not os.path.exists(file_path):
                            logging.debug(f"{sys._getframe().f_code.co_name}() -> file_path -> copy_files_list[]: NAY {file_path}")
                            copy_files_list.extend([[asset_path, file_path]])
                        else:
                            logging.debug(f"{sys._getframe().f_code.co_name}() -> file_path -> check_hash_list[]: AY {file_path}")
                            check_hash_list.extend([[asset_path, file_path]])

            logging.debug(f"{sys._getframe().f_code.co_name}() -> check_hash_list: {check_hash_list}")
            logging.info(f"{sys._getframe().f_code.co_name}() -> check_hash_list: {len(check_hash_list)} files need to be compared.")
            logging.debug(f"{sys._getframe().f_code.co_name}() -> copy_files_list: {copy_files_list}")
            return [check_hash_list, copy_files_list]

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
    logging.debug(f"{sys._getframe().f_code.co_name}() -> compared_files: {len(compared_files)} {compared_files}.")
    check_hash_list = compared_files[0]
    copy_files_list = compared_files[1]

    for list in check_hash_list:
        asset_file = list[0]
        game_file = list[1]
        logging.debug(f"{sys._getframe().f_code.co_name}() -> asset_file: {asset_file}.")
        with open(asset_file, 'rb', buffering=0) as f:
            asset_file_hashed = hashlib.file_digest(f, 'sha256').hexdigest()

        logging.debug(f"{sys._getframe().f_code.co_name}() -> game_file: {game_file}.")
        with open(game_file, 'rb', buffering=0) as f:
            game_file_hashed = hashlib.file_digest(f, 'sha256').hexdigest()
        if asset_file_hashed != game_file_hashed:
            copy_files_list.extend([[asset_file, game_file]])

    logging.debug(f"{sys._getframe().f_code.co_name}() -> copy_files_list: {len(copy_files_list)} {copy_files_list}.")
    logging.info(f"{sys._getframe().f_code.co_name}() -> copy_files_list: {len(copy_files_list)} files need to be moved.")
    return copy_files_list
    
def copy_files(game_file_type):
    """
    Creates directories, removes old/different files, copies
    new files.
    """
    try:
        with open(f'.\\config\\lists\\{game_file_type}_files.json') as f:
            copy_files_list = json.load(f)
            f.close
        if not copy_files_list == []:
            logging.debug(f"{sys._getframe().f_code.co_name}() -> copy_files -> type: {game_file_type}: {copy_files_list}")

            for files in copy_files_list:
                try:
                    logging.debug(f"{sys._getframe().f_code.co_name}() -> files: {len(files)} {files}.")
                    asset_file = files[0]
                    game_file = files[1]
                    if not os.path.isdir(os.path.dirname(game_file)):
                        logging.debug(f"{sys._getframe().f_code.co_name}() -> MKDIR: {os.path.dirname(game_file)}")
                        try:
                            os.makedirs(os.path.dirname(game_file))
                        except Exception as e:
                            get_exception(e)
                            return
                    if os.path.isfile(game_file):
                        logging.debug(f"{sys._getframe().f_code.co_name}() -> REMOVE: {game_file}")
                        try:
                            os.remove(game_file)
                        except Exception as e:
                            get_exception(e)
                            return
                    try:
                        logging.debug(f"{sys._getframe().f_code.co_name}() -> COPY :: {asset_file} -> {game_file}")
                        os.system(f'copy {asset_file} {game_file}')
                    except Exception as e:
                        get_exception(e)
                        return

                except Exception as e:
                    get_exception(e)
                    return
            with open(f'.\\config\\lists\\{game_file_type}_files.json', 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
                f.close
            return True
        else:
            logging.warning(f"ERROR -> {sys._getframe().f_code.co_name}() :: Nothing to copy from '.\\config\\lists\\{game_file_type}_files.json'")
            return False
    
    except Exception as e:
        get_exception(e)
        return False
    
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
    logging.error({
        'ERROR': type(e).__name__,
        'message': str(e),
        'trace': trace
    })
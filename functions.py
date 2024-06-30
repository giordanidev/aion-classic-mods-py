from __future__ import (division, absolute_import, print_function, unicode_literals)
from configparser import ConfigParser
from tkinter import messagebox, filedialog
import os, os.path, hashlib, winreg, sys, json, logging, threading, ctypes, locale, shutil, time, tempfile, zipfile, psutil
import urllib.request as urllib2
import urllib.parse as urlparse

# GLOBAL VARIABLES
file_types = ["translation", "translation_eu", "filter", "font", "voice", "asmo_skin"]
copy_delete_files = ""
config_path = "./config/config.json"
version_path = "./config/version.json"
logs_path = "./logs/logs.log"
app_icon = "./config/img/AionClassicMods.ico"
update_url = "https://github.com/giordanidev/aion-classic-mods-py/raw/master/download/update.json"
filter_url = "https://github.com/giordanidev/aion-classic-mods-py/raw/master/download/aionfilter.zip"
font_url = "https://github.com/giordanidev/aion-classic-mods-py/raw/master/download/hit_number.zip"
voice_url = "https://github.com/giordanidev/aion-classic-mods-py/raw/master/download/voice.zip"
translation_url = "https://github.com/giordanidev/aion-classic-ptbr/raw/main/_arquivo/z_Data_na_ptBR.zip"
translation_eu_url = "https://github.com/giordanidev/aion-classic-ptbr/raw/main/_arquivo/z_data_eu_ptBR.zip"
asmo_skin_url = "https://github.com/giordanidev/aion-classic-mods-py/raw/master/download/asmo_skin.zip"

def setLogLevel():
    try:
        arg_count = 0
        arg_found = False
        for arg in sys.argv:
            if arg == "--DEBUG":
                log_level = logging.DEBUG
                arg_found = True
            arg_count += 1
        if arg_found == False:
            #TODO DEBUGGING
            log_level = logging.DEBUG
        return log_level
    except Exception as e:
        getException(e)
        return False
log_level = setLogLevel() # GLOBAL VARIABLE

if not os.path.isdir(os.path.dirname(logs_path)):
    os.makedirs(os.path.dirname(logs_path))
    
logging.basicConfig(filename=logs_path, format='%(asctime)s [%(threadName)s] -> [%(levelname)s] -> :: %(message)s', encoding='utf-8', level=log_level, filemode="w")
logging.getLogger().addHandler(logging.StreamHandler())

logging.info(f"{sys._getframe().f_code.co_name}() :: App initialized.")
logging.debug(f"{sys._getframe().f_code.co_name}() :: app_functions.py imported.")

def appConfigJson():
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Reading configs.")
        with open(config_path, encoding='utf-8') as f:
            config_json = json.load(f)
        f.close
        return config_json
    except Exception as e:
        getException(e)
        return False
app_config = appConfigJson() # GLOBAL VARIABLE

def appConfigSave(app_config):
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Saving configs.")
        with open(config_path, 'w') as config_write:
            json_object = json.dumps(app_config, indent=4)
            config_write.write(json_object)
    except Exception as e:
        getException(e)
        return False

def appVersion():
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Reading local app version.")
        with open(version_path, encoding='utf-8') as f:
            local_version = json.load(f)
            f.close
        return local_version
    except Exception as e:
        getException(e)
        return False
local_version = appVersion() # GLOBAL VARIABLE

def getLang():
    """
    Gets system language to load the correct "lang" file for app's translation.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Loading translation.")
        windll = ctypes.windll.kernel32
        app_lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        lang_path = f"./config/lang/{app_lang}.json"
        with open("./config/lang/en_US.json", encoding='utf-8') as f:
            en_translated_text = json.load(f)
            f.close
        if os.path.isfile(lang_path):
            with open(lang_path, encoding='utf-8') as f:
                translated_text = json.load(f)
                f.close
        else:
            translated_text = en_translated_text
            logging.debug(f"{sys._getframe().f_code.co_name}() :: ({app_lang}) translation not found. Loaded default (en_US).")
        return translated_text, en_translated_text
    except Exception as e:
        getException(e)
        return False
load_translated_text = getLang()
translated_text = load_translated_text[0]
en_translated_text = load_translated_text[1]

def translateText(key):
    try:
        if key in translated_text:
            return translated_text[key]
        else:
            return en_translated_text[key]
    except Exception as e:
        getException(e)
        return False

def getEnglishTranslation(value):
    try:
        for key in translated_text:
            if translated_text[key] == value:
                english_name = en_translated_text[key]
                return english_name
        return False
    except Exception as e:
        getException(e)
        return False

def getLangTranslation(value):
    try:
        for key in en_translated_text:
            if en_translated_text[key] == value:
                return translated_text[key]
        return False
    except Exception as e:
        getException(e)
        return False

###########################################################
###########                                     ###########
###########   START  MAIN.PY FUNCTIONS          ###########
###########                                     ###########
###########################################################

# GLOBAL VARIABLES
text_color_success = ("#007514", "#7EFF93")
text_color_fail = ("#D80000", "#FF6969")
text_color_verifying = ("black", "white")
font_regular = ("", 12)
font_regular_bold = ("", 12, "bold")
font_big_bold = ("", 14, "bold")
padx_both = 2.5
pady_both = 2.5

def centerApp(width, height, self):
    """
    Centers the app in the computer's main screen on start.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Centering app on main window.")
        window_width = width
        window_height = height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2) - 50)
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
    except Exception as e:
        getException(e)
        return False

def checkboxEvent(checkbox_get, checkbox_lang):
    print(f"{sys._getframe().f_code.co_name}() Changing '{checkbox_get.cget('text')}' checkbox setting to '{checkbox_get.get()}'.")

    global app_config
    if checkbox_lang == "update":
        app_config["check_updates_startup"] = checkbox_get.get()
    elif checkbox_lang == "verify":
        app_config["verify_files_startup"] = checkbox_get.get()
    else:
        count = 0
        for lang in app_config['langs']:
            if lang[0] == checkbox_lang:
                if lang[1] == checkbox_get.cget('text'):
                    app_config["langs"][count][2] = checkbox_get.get()
            count += 1

    appConfigSave(app_config)

def selectDirectory(path_entry, region): #TODO
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Setting game folder.")
        game_directory = filedialog.askdirectory().replace("\\","/")
        if game_directory is not None:
            validate_directory_return = validateDirectory(game_directory, region)

            if validate_directory_return:
                path_entry.delete(0, 'end')
                path_entry.insert(0, game_directory)
                global app_config
                app_config['TODO'] = game_directory
                appConfigSave(app_config)
                return True

        else:
            if not verifyGamePath():
                logging.debug(f"{sys._getframe().f_code.co_name}() :: Wrong game folder.")
                return False
    except Exception as e:
        getException(e)
        return False

# file_type_list :: [filter, font, voice] list
# install_buttons_list :: filter, font, voice buttons (Returns install for Verify All, Backup/Restore for Backup buttons)
# remove_restore_buttons_list :: filter, font, voice buttons (Returns Remove for Vrify All/Restore for Backup buttons)
# delete_buttons_list :: filter, font, voice -> delete buttons -> Only used when verifying Backups
# file_type_label_list :: filter, font, voice labels widgets
# verify_all_backup_button :: button widget that was pressed
# verify_all_backup :: "verify_all" or "verify_backup" -> Used to identify if we are verifying for game files or backup files
def verifyFilesButton(file_type_list,
                      install_buttons_list,
                      delete_buttons_list,
                      file_type_label_list,
                      verify_all_button,
                      self):
    """
    
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Verifying files.")
        verify_path = verifyGamePath()
        if verify_path is not False:
            type_count = 0
            for file_type in file_type_list:
                def verifyFilesThreaded(file_type, type_count):
                    file_type_label_list[type_count].configure(text=translateText("app_return_label_verifying"), text_color=text_color_verifying)
                    install_buttons_list[type_count].configure(text=translateText("app_button_verifying"), state="disabled", font=font_regular)

                    # Sends the file type and verify
                    if file_type not in local_version["disabled_fields"]:
                        verify_files_return = verifyFiles(file_type)
                        if verify_files_return in ["both", "game"]:
                            file_type_label_list[type_count].configure(text=translateText("app_return_label_update"), text_color=text_color_success)
                            install_buttons_list[type_count].configure(text=translateText("app_button_update"), state="normal", font=font_regular_bold)
                            delete_buttons_list[type_count].configure(state="normal", font=font_regular_bold)
                        elif verify_files_return in ["assets", True]:
                            file_type_label_list[type_count].configure(text=translateText("app_return_label_install"), text_color=text_color_success)
                            install_buttons_list[type_count].configure(text=translateText("app_button_install"), state="normal", font=font_regular_bold)
                            delete_buttons_list[type_count].configure(state="disabled", font=font_regular)
                        elif verify_files_return == False:
                            file_type_label_list[type_count].configure(text=translateText("app_return_label_download"), text_color=text_color_success)
                            install_buttons_list[type_count].configure(text=translateText("app_button_download"), state="normal", font=font_regular_bold)
                            delete_buttons_list[type_count].configure(state="disabled", font=font_regular)
                        else:
                            file_type_label_list[type_count].configure(text=translateText("app_return_label_install"), text_color=text_color_success)
                            install_buttons_list[type_count].configure(text=translateText("app_button_install"), state="disabled", font=font_regular)
                            delete_buttons_list[type_count].configure(state="disabled", font=font_regular)

                        if file_type in local_version["disable_fields"]:
                            file_type_label_list[type_count].configure(state="disabled", font=font_regular)
                            install_buttons_list[type_count].configure(state="disabled", font=font_regular)
                            
                    verifyFilesThreaded_func = threading.Thread(target=verifyFilesThreaded, args=(file_type, type_count))
                    verifyFilesThreaded_func.start()
                    #verifyFilesThreaded_func.join() # crashes the app =(
                    type_count += 1
        else:
            self.set("Config")
            print(f"verifyGamePath() == False")
    except Exception as e:
        getException(e)
        return False
    
# copy :: used to copy files to the game folder
## if there is no backup, one will be created before
## copying the new files.
## if files are up to date and backup already exists,
## turns into a Restore button to replace current files
## with the backed up files.
# create :: used to create backup files
# delete :: used to delete backups
def copyFilesButton(file_type, copy_delete, return_label, return_button, delete_button):
    """
    
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: {copy_delete.capitalize()} ({file_type.capitalize()}) files.")
        return_label.configure(text=translateText("app_return_label_verifying"))
        def copyFilesThreaded():
            copy_files_return = copyDeleteFiles(file_type, copy_delete, return_label)
            if copy_files_return == False:
                return_label.configure(text=translateText("app_return_label_success"), text_color=text_color_success)
                return_button.configure(text=translateText("app_button_update"), state="enabled", font=font_regular_bold)
                delete_button.configure(state="normal", font=font_regular_bold)
                return False
            elif copy_files_return == True:
                if copy_delete == "copy":
                    return_label.configure(text=translateText("app_return_label_success"), text_color=text_color_success)
                    return_button.configure(text=translateText("app_button_update"), state="enabled", font=font_regular_bold)
                    delete_button.configure(state="normal", font=font_regular_bold)
                elif copy_delete == "delete":
                    return_label.configure(text=translateText("app_return_label_deleted"), text_color=text_color_success)
                    return_button.configure(text=translateText("app_button_download"), state="normal", font=font_regular_bold)
                    delete_button.configure(state="disabled", font=font_regular)
        copyFilesThreaded_func = threading.Thread(target=copyFilesThreaded)
        copyFilesThreaded_func.start()
    except Exception as e:
        getException(e)
        return False

###########################################################
###########                                     ###########
###########   END    MAIN.PY FUNCTIONS          ###########
###########                                     ###########
###########################################################

def firstRun():
    """
    List of tasks to be executed on the app's first run. Such as:
    - Try to locate NA's and EU's client and launcher installation paths;
    - Try to identify region's translation folders;
    - Confirm that paths found are current being used.
    """
    try:
        global app_config
        if app_config['first_run'] == True:
            logging.info(f"{sys._getframe().f_code.co_name}() :: First run! The program will try to configure some basic settings.")
            getClassicNaPath()
            getClassicEuPath()
            getClassicEuLauncherPath()
            verifyGamePath()
            return True
        else:
            logging.debug(f"{sys._getframe().f_code.co_name}() :: Not the first run anymore!")
            return False
    except Exception as e:
        getException(e)
        return False

def getClassicNaPath():
    """
    Attempts to get the installation path for the AION Classic North
    America and save it to the 'config.ini' file.

    If it fails it will prompt the user to select a path manually.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Searching for the Classic NA path.")
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\NCWest\\AION_CLASSIC')
        if a_key:
            classic_na_path = winreg.QueryValueEx(a_key, "BaseDir")[0]
            if classic_na_path[len(classic_na_path)-1] == "\\":
                classic_na_path = classic_na_path.rstrip(classic_na_path[-1])
            global app_config
            return_index = getRegionIndex("NA")
            region_index = return_index[0]
            region_exists = return_index[1]
            classic_na_path.replace("\\","/")
            if region_exists == True:
                app_config['regions'][region_index][2] = classic_na_path
                app_config['regions'][region_index][3] = True
            else:
                na_settings = ["NA", "Classic NA", classic_na_path, True]
                app_config['regions'].append(na_settings)
            addGameLang(classic_na_path, "NA")
            appConfigSave(app_config)
            return True
        else:
            return False
    except Exception as e:
        getException(e)
        return False

def getClassicEuPath():
    """
    Attempts to get the installation path for the AION Classic Europe
    and save it to the 'config.ini' file.

    If it fails it will prompt the user to select a path manually.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Searching for the Classic EU path.")
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall')
        found = False
        for i in range(1024):
            try:
                key_name = winreg.EnumKey(a_key, i)
                o_key = winreg.OpenKey(a_key, key_name)
                display_name = winreg.QueryValueEx(o_key, "DisplayName")[0]
                if display_name == "AION Classic":
                    game_publisher = winreg.QueryValueEx(o_key, "Publisher")[0]
                    if (game_publisher == "Gameforge"):
                        classic_eu_path = winreg.QueryValueEx(o_key, "InstallLocation")[0]
                        found = True
                if found == True:
                    if classic_eu_path[len(classic_eu_path)-1] == "\\":
                        classic_eu_path = classic_eu_path.rstrip(classic_eu_path[-1])
                        classic_eu_path.replace("\\","/")
                    global app_config
                    return_index = getRegionIndex("EU")
                    region_index = return_index[0]
                    region_exists = return_index[1]
                    if region_exists == True:
                        app_config['regions'][region_index][2] = classic_eu_path
                        app_config['regions'][region_index][3] = True
                    else:
                        eu_settings = ["EU", "Classic EU", classic_eu_path, True]
                        app_config['regions'].append(eu_settings)
                    appConfigSave(app_config)
                    addGameLang(classic_eu_path, "EU")
                    return True
            except:
                continue
        if found == False:
            return False
    except Exception as e:
        getException(e)
        return False

def getRegionIndex(region):
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Getting region index.")
        global app_config
        count = 0
        bool_var = False
        for regions in app_config['regions']:
            if regions[0] == region:
                bool_var = True
                return count, bool_var
            count += 1
        return count, bool_var
    except Exception as e:
        getException(e)
        return False
    
def getClassicEuLauncherPath():
    """
    Attempts to get the installation path for the Gameforge Client (Launcher)
    and save it to the 'config.ini' file.

    If it fails it will prompt the user to select a path manually.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Searching for the EU Launcher path.")
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        try:
            a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\Gameforge4d\\GameforgeClient\\MainApp\\Libraries\\c')
        except:
            return False
        if a_key:
            classic_eu_launcher_path = winreg.QueryValueEx(a_key, "LibraryLocation")[0]
            if classic_eu_launcher_path[len(classic_eu_launcher_path)-1] == "\\":
                classic_eu_launcher_path = classic_eu_launcher_path.rstrip(classic_eu_launcher_path[-1])
            global app_config
            app_config['eu_launcher_path'] = [classic_eu_launcher_path.replace("\\","/"), True]
            appConfigSave(app_config)
            return True
        else:
            return False
    except Exception as e:
        getException(e)
        return False
    
def addGameLang(game_path, game_short):
    try:
        global app_config
        dir_path = f"{game_path}\\l10n"
        if os.path.isdir(os.path.dirname(dir_path)):
            dir_list = [ f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f)) ]
            for dir in dir_list:
                dir = dir.upper()
                found = False
                for lang in app_config['langs']:
                    if lang[0] == game_short and lang[1] == dir:
                        found = True
                if found == False:
                    lang_settings = [game_short, dir, True]
                    app_config['langs'].append(lang_settings)
    except Exception as e:
        getException(e)
        return False
    
# alert_type = showinfo | showwarning | showerror | askquestion | askokcancel | askyesno 
def showAlert(alert_type, message):
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Sending alert message.")
        if alert_type == "showinfo": # returns "ok"
            alert_return = messagebox.showinfo(translateText("functions_alert_info"), message)
        elif alert_type == "showwarning": # returns "ok"
            alert_return = messagebox.showwarning(translateText("functions_alert_warning"), message)
        elif alert_type == "showerror": # returns "ok"
            alert_return = messagebox.showerror(translateText("functions_alert_error"), message)
        elif alert_type == "askquestion": # returns "yes" or "no"
            alert_return = messagebox.askquestion(translateText("functions_alert_question"), message)
        elif alert_type == "askokcancel": # returns "True" or "False"
            alert_return = messagebox.askokcancel(translateText("functions_alert_okcancel"), message)
        elif alert_type == "askyesno": # returns "True" or "False"
            alert_return = messagebox.askyesno(translateText("functions_alert_yesno"), message)
        else:
            logging.error(f"{sys._getframe().f_code.co_name}() :: Unknown alert type.")
            return
        return alert_return
    except Exception as e:
        getException(e)
        return False

def validateDirectory(game_directory, region):
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Validating directory for the {region} region.")
        wrong_directory = translateText("functions_wrong_directory")
        if region == "NA":
            game_path = f"{game_directory}\\bin64\\aion.bin"
            if not os.path.isfile(game_path):
                showAlert("showerror", wrong_directory.replace("{VERSION}","NA"))
                return False
            else:
                return True
        if region == "EU":
            game_path = f"{game_directory}\\bin64\\aionclassic.bin"
            if not os.path.isfile(game_path):
                showAlert("showerror", wrong_directory.replace("{VERSION}","EU"))
                return False
            else:
                return True
    except Exception as e:
        getException(e)
        return False

def verifyFiles(game_file_type):
    """
    Verifies if files exist in the game directory or not.
    If they do not exist, then the Remove button will not be anabled.
    If they exist, both the Download and Remove buttons will be anabled.
    """
    try:
        logging.debug(f"({game_file_type}) {sys._getframe().f_code.co_name}() :: Verifying files.")
        global app_config
        game_lang = []
        for lang in app_config['langs']:
            if lang[2] == True:
                game_lang.append(lang)
        if game_lang == []:
            logging.error(f"{sys._getframe().f_code.co_name}() :: Select at least one language to modify files.")
            return False
        
        files_path = getFilePath(game_file_type)
        verifyGamePath()
        game_paths = getGameFilePath(game_lang) # Returns [full_file_path]. It can be multiple paths depending on regions selected
        all_files = getFiles(files_path[0], files_path[1], game_paths) # assets path | game file | file names
        if not all_files:
            logging.error(f"({game_file_type}) {sys._getframe().f_code.co_name}() :: Files not available.")
            return False
        elif len(all_files) >= 1:
            for files in all_files:
                assets_file = files[0]
                game_file = files[1]
                if os.path.isfile(assets_file):
                    if os.path.isfile(game_file):
                        return "both"
                    else:
                        return "assets"
                elif os.path.isfile(game_file):
                    return "game"
            return False
        
    except Exception as e:
        getException(e)
        return False

def getFilePath(game_file_type):
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Getting file path.")
        with open("./config/files.json", encoding='utf-8') as f:
            download_files = json.load(f)
            f.close
        files = download_files[game_file_type]
        curr_dir = os.getcwd()
        assets_path = f"{curr_dir}\\assets"
        return assets_path, files
    except Exception as e:
        getException(e)
        return False

def verifyGamePath():
    """
    Verifies if the client path is correct before trying to
    copy files. If it cannot reach the game executable file
    using the saved path it removes it from config and prompts
    the user to select a new path.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Verifying game path.")
        global app_config
        game_paths = []
        count = 0
        for region in app_config['regions']:
            found = False
            for executable in ["aion.bin", "aiononline.bin", "aionclassic.bin"]:
                if os.path.isfile(f"{region[2]}\\bin64\\{executable}"):
                    found = True
                    game_paths.append(region[1])
            if found == False:
                app_config['regions'][count][2] = ""
                app_config['regions'][count][3] = False
                appConfigSave(app_config)
            count += 1
        return game_paths

    except Exception as e:
        getException(e)
        return False

def getGameFilePath(game_lang):
    """
    Gets the full file paths for the selected regions using the
    previously set base file path.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Getting game path.")
        global app_config
        full_file_path = []
        for lang in game_lang:
            if lang[0] is not None:
                for region in app_config["regions"]:
                    if region[0] == lang[0]:
                        region_replace = region[2].replace("/", "\\")
                        full_file_path.append(f"{region_replace}\\l10n\\{lang[1]}")
            else:
                logging.error(f"{sys._getframe().f_code.co_name}() :: Unknown language: {lang[0]}")
                return
        return full_file_path
    except Exception as e:
        getException(e)
        return False
    
def getFiles(assets_path, file_names, game_paths):
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Getting files.")
        copy_files_list = []
        for game_dir in game_paths:
            for filename in file_names:
                assets_file = assets_path+filename
                game_file = game_dir+filename
                """
                if os.path.isfile(assets_file) or os.path.isfile(game_file):
                    logging.debug(f"{sys._getframe().f_code.co_name}() -> assets_file: {os.path.isfile(assets_file)} game_file: {os.path.isfile(game_file)}.")
                else:
                    logging.debug(f"{sys._getframe().f_code.co_name}() -> assets_file and game_file NOT FOUND.")
                """
                copy_files_list.extend([[assets_file, game_file]])
        return copy_files_list
    except Exception as e:
        getException(e)
        return False
    
def copyDeleteFiles(game_file_type, copy_delete, return_label):
    """
    Creates directories; removes old/different files, copies
    and deletes files.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Copying/deleting files ({copy_delete}).")
        global app_config
        game_lang = []
        for lang in app_config['langs']:
            if lang[2] == True:
                game_lang.append(lang)
        if game_lang == []:
            return False
        
        files_path = getFilePath(game_file_type)
        verifyGamePath()
        game_paths = getGameFilePath(game_lang) # Returns [full_file_path]. It can be multiple paths depending on regions selected
        all_files = getFiles(files_path[0], files_path[1], game_paths) # assets path | game file | file names

        if not all_files:
            logging.warning(f"{sys._getframe().f_code.co_name}() :: Nothing to {copy_delete}.")
            return False
        
        if copy_delete == "copy":
            downloaded_files = downloadFiles(game_file_type, return_label)
            extractFiles(downloaded_files[0], downloaded_files[1]) # file path | destination in app assets folder
        show_delete_warning = True
        for files in all_files: # [0] = asset | [1] = game
            asset_file = files[0]
            game_file = files[1]
            if copy_delete == "copy":
                #TODO ADD EU/NA VERIFICATION
                if game_file_type == "translation":
                    for idioma in ["eng", "fra", "deu"]:
                        if idioma in game_file.split("/"):
                            pass
                elif game_file_type == "translation_eu" and "enu" in game_file.split("/"):
                    pass
                if not os.path.isdir(os.path.dirname(game_file)):
                    os.makedirs(os.path.dirname(game_file))
                shutil.copy2(asset_file, game_file)

            elif copy_delete == "delete":
                files_path = getFilePath(game_file_type)
                copy_delete_files = getFiles(files_path[0], files_path[1], files_path[2]) # assets path | game files path)
                if not copy_delete_files:
                    return False
                if show_delete_warning == True:
                    alert = showAlert("askquestion", translateText("functions_show_delete").replace('{FILETYPE}', translateText(f"app_{game_file_type}_label")))
                    if alert == "no":
                        return False
                    else:
                        show_delete_warning = False
                if os.path.isfile(game_file):
                    os.remove(game_file)
                if os.path.isfile(asset_file):
                    os.remove(asset_file)

        copy_delete_files = []
        return True
    except Exception as e:
        getException(e)
        return False
    
def downloadFiles(file_type, return_label):
    """ 
    Download and save a file specified by url to 'dest' directory.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Downloading files.")
        file_path = getFilePath(file_type)[0]
        # Defines assets path
        if file_type == "filter":
            assets_dir = "\\data\\Strings"
        if file_type == "font":
            assets_dir = "\\textures\\ui"
        if file_type == "voice":
            assets_dir = "\\sounds\\voice"
        if file_type in ["translation", "translation_eu"]:
            assets_dir = "\\data"
        if file_type == "asmo_skin":
            assets_dir = "\\data\\custompreset"
        file_path = file_path+assets_dir
        dest = file_path
        if not os.path.isdir(dest):
            logging.debug(f"{sys._getframe().f_code.co_name}() -> MKDIR: {dest}")
            os.makedirs(dest)
        if (file_type == "filter"):
            url = filter_url
        elif (file_type == "font"):
            url = font_url
        elif (file_type == "voice"):
            url = voice_url
        elif (file_type == "translation"):
            url = translation_url
        elif (file_type == "translation_eu"):
            url = translation_eu_url
        elif (file_type == "asmo_skin"):
            url = asmo_skin_url

        u = urllib2.urlopen(url)
        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        filename = os.path.basename(path)

        if dest:
            filepath = os.path.join(dest, filename)
        else:
            return False
        
        with open(filepath, 'wb') as f:
            meta = u.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func("Content-Length")
            file_size = None
            if meta_length:
                file_size = int(meta_length[0])
                
            #print("Downloading: {0} Bytes: {1}".format(url, file_size))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)

                status = f"{translateText('app_button_downloading')} {filename}:"
                if file_size:
                    status += " {0:3.0f}%".format(file_size_dl * 100 / file_size)
                status += chr(13)
                #print(status, end="")
                return_label.configure(text=status, text_color=text_color_success)
            #print()
        return filepath, dest
    except Exception as e:
        getException(e)
        return False

def extractFiles(filepath, dest):
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Extracting files.")
        with zipfile.ZipFile(filepath, 'r') as zip_files:
            zip_files.extractall(dest)
    except Exception as e:
        getException(e)
        return False

def checkUpdate():
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Checking for update.")
        global local_version
        cloud_json = urllib2.urlopen(update_url)
        cloud_version = json.loads(cloud_json.read())

        with open("./config/version.json", encoding='utf-8') as f:
            local_json = json.load(f)
            f.close

        file_types.append("disabled_fields_version")
        for arquivo in file_types:
            for cloud in cloud_version:
                if arquivo == cloud:
                    for local in local_json:
                        if cloud == local:
                            print("teste")
        return cloud_version
    except Exception as e:
        getException(e)
        return False
#latest_version = checkUpdate() # GLOBAL VARIABLE
update_test = checkUpdate()

def getException(e):
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
    logging.error({
        'ERROR': type(e).__name__,
        'message': str(e),
        'trace': trace
    })
    showAlert("showerror", translateText("functions_show_critical_error")+"\n\n"+str(e))

####### MAY USE IT IN THE FUTURE AGAIN!

def forceCloseAion(action, game_client, close_button, return_label):        
    try: #deleting the app if asked app is running.(It raises error for some windows apps)3
        logging.debug(f"{sys._getframe().f_code.co_name}() :: Force-closing all Aion clients.")
        running_apps = psutil.process_iter(['pid','name']) #returns names of running processes

        if game_client == "game":
            app_name = ["aion", "aionclassic"]
            app_extension = "bin"
            app_check_phrase = translateText("app_return_label_game_found")
            app_close_phrase = translateText("app_return_label_game_closed")
        elif game_client == "client":
            app_name = ["gfservice", "gfclient"]
            app_extension = "exe"
            app_check_phrase = translateText("app_return_label_launcher_found")
            app_close_phrase = translateText("app_return_label_launcher_closed")

        found = False
        for app in running_apps:
            sys_app = app.info.get('name').split('.')
            sys_app_name = sys_app[0].lower()

            if sys_app_name in app_name and app_extension in sys_app:
                if action == "close":
                    pid = app.info.get('pid') #returns PID of the given app if found running
                    app_pid = psutil.Process(pid)
                    app_pid.terminate()
                    logging.debug(f"{sys._getframe().f_code.co_name}() -> Process '{sys_app_name}.{app_extension} ({app_pid})' closed!")
                    close_button.configure(state="disabled", font=font_regular)
                    return_label.configure(text=app_close_phrase, text_color=text_color_success, font=font_regular)
                    found = True
                elif action == "check":
                    close_button.configure(state="normal", font=font_regular_bold)
                    return_label.configure(text=app_check_phrase, text_color=text_color_success, font=font_regular)
            else: pass
        
        if found == False:
            logging.debug(f"{sys._getframe().f_code.co_name}() -> Aion process not found!")
            close_button.configure(state="disabled", font=font_regular)
            return_label.configure(text=translateText("app_info_aion_notfound"), font=font_regular)
    
    except Exception as e:
        getException(e)
        return False

def forceCloseAion_thread(action, game_client, close_button, return_label):
    while 1:
        forceCloseAion(action, game_client, close_button, return_label)
        time.sleep(10)

def compareFilesHash(compared_files):
    """
    Compares duplicated files hashes and adds them to the
    copy_files_verify list if hashes differ.
    Returns a single list of files with both assets and game
    file paths ready to be replaced in [[asset_file, game_file]]
    format.
    """
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() -> compared_files: {len(compared_files)} {compared_files}.")
        verify_hash_list = compared_files[0]
        copy_files_list = compared_files[1]
        for list in verify_hash_list:
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
        logging.info(f"{sys._getframe().f_code.co_name}() -> copy_files_list: {len(copy_files_list)} {copy_files_list} files need to be moved.")
        return copy_files_list, verify_hash_list
    except Exception as e:
        getException(e)
        return False
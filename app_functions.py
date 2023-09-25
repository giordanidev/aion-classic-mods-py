from __future__ import (division, absolute_import, print_function, unicode_literals)
from configparser import ConfigParser
from tkinter import messagebox, filedialog
import os, os.path, hashlib, winreg, sys, json, logging, threading, ctypes, locale, shutil, psutil, time, tempfile
import urllib.request as urllib2
import urllib.parse as urlparse

logging.basicConfig(filename='.\\logs\\logs.log', format='%(asctime)s [%(threadName)s] -> [%(levelname)s] -> :: %(message)s', encoding='utf-8', level=logging.DEBUG, filemode='w')
logging.getLogger().addHandler(logging.StreamHandler())

logging.debug(f"{sys._getframe().f_code.co_name}() -> App initialized.")
logging.debug(f"{sys._getframe().f_code.co_name}() -> app_functions.py imported.")

# Gets system language to load the correct "lang" file for app translation
def getLang():
    try:
        windll = ctypes.windll.kernel32
        app_lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        lang_path = f".\\config\\lang\\{app_lang}.json"
        with open(".\\config\\lang\\en_US.json", encoding='utf-8') as f:
            en_translated_text = json.load(f)
            f.close
        if os.path.isfile(lang_path):
            with open(lang_path, encoding='utf-8') as f:
                translated_text = json.load(f)
                f.close
            logging.debug(f"{sys._getframe().f_code.co_name}() -> ({app_lang}) translation loaded.")
        else:
            translated_text = en_translated_text
            logging.debug(f"{sys._getframe().f_code.co_name}() -> ({app_lang}) translation not found. Loaded default (en_US).")
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
                lang_name = translated_text[key]
                return lang_name
        return False
    except Exception as e:
        getException(e)
        return False

def appConfigLoad():
    try:
        app_config = ConfigParser()
        config_path = 'config/'
        config_file = 'config.ini'
        config_full_path = config_path + config_file
        app_config.read(config_full_path)
        logging.debug(f"{sys._getframe().f_code.co_name}() -> appConfigLoad: {app_config.items('app')}")
        return (app_config, config_full_path)
    except Exception as e:
        getException(e)
        return False

load_configs = appConfigLoad()
app_config = load_configs[0]
config_full_path = load_configs[1]

def appConfigSave(app_config):
    try:
        with open(config_full_path, 'w') as config_write:
            logging.debug(f"{sys._getframe().f_code.co_name}() -> appConfigSave: {app_config.items('app')}")
            app_config.write(config_write)
    except Exception as e:
        getException(e)
        return False

"""
def get_langs():
    with open('./config/config.json') as config_file:
        data = json.load(config_file)
    if "langs" in data:
        langs = data["langs"]
    else:
        langs = False
    return langs

def get_regions():
    with open('./config/config.json') as config_file:
        data = json.load(config_file)
    regions = data["regions"]
    return regions
"""

###########################################################
###########                                     ###########
###########   START  MAIN.PY FUNCTIONS          ###########
###########                                     ###########
###########################################################

text_color_success = ("#007514", "#7EFF93")
text_color_fail = ("#D80000", "#FF6969")
text_color_verifying = ("black", "white")
font_regular = ("", 12)
font_regular_bold = ("", 12, "bold")
font_big_bold = ("", 13, "bold")
padx_both = 2.5
pady_both = 2.5

def regionSelection(self):
    try:
        app_config = appConfigLoad()[0]
        app_config.set('app', 'region', str(self.regionRadio.get()))
        appConfigSave(app_config)
        if (self.regionRadio.get() == 0):
            self.naPathLabel.configure(state="disabled")
            self.naPathEntry.configure(state="disabled")
            self.naPathButton.configure(state="disabled")
            self.euPathLabel.configure(state="disabled")
            self.euPathEntry.configure(state="disabled")
            self.euPathButton.configure(state="disabled")
        elif (self.regionRadio.get() == 1):
            if getClassicNaPath():
                self.naPathEntry.delete(0, 'end')
                self.naPathEntry.insert(0, app_config.get('app', 'napath'))
            self.naPathLabel.configure(state="normal")
            self.naPathEntry.configure(state="normal")
            self.naPathButton.configure(state="normal")
            self.euPathLabel.configure(state="disabled")
            self.euPathEntry.configure(state="disabled")
            self.euPathButton.configure(state="disabled")
        elif (self.regionRadio.get() == 2):
            if getClassicEuPath():
                self.euPathEntry.delete(0, 'end')
                self.euPathEntry.insert(0, app_config.get('app', 'eupath'))
            self.naPathLabel.configure(state="disabled")
            self.naPathEntry.configure(state="disabled")
            self.naPathButton.configure(state="disabled")
            self.euPathLabel.configure(state="normal")
            self.euPathEntry.configure(state="normal")
            self.euPathButton.configure(state="normal")
        elif (self.regionRadio.get() == 3):
            if getClassicNaPath():
                self.naPathEntry.delete(0, 'end')
                self.naPathEntry.insert(0, app_config.get('app', 'napath'))
            if getClassicEuPath():
                self.euPathEntry.delete(0, 'end')
                self.euPathEntry.insert(0, app_config.get('app', 'eupath'))
            self.naPathLabel.configure(state="normal")
            self.naPathEntry.configure(state="normal")
            self.naPathButton.configure(state="normal")
            self.euPathLabel.configure(state="normal")
            self.euPathEntry.configure(state="normal")
            self.euPathButton.configure(state="normal")
    except Exception as e:
        getException(e)
        return False

def selectDirectory(path_entry):
    try:
        logging.debug(f"{sys._getframe().f_code.co_name}() -> 'Select Folder' ({path_entry.cget('placeholder_text')}) button pressed.")

        game_directory = filedialog.askdirectory().replace("/","\\")
        logging.debug(f"{sys._getframe().f_code.co_name}() -> game_directory: {game_directory}.")

        if game_directory:
            placeholder_text = path_entry.cget("placeholder_text")
            if "NA" in placeholder_text.split("\\"):
                region = "NA"
                path = "napath"
            elif "EU" in placeholder_text.split("\\"):
                region = "EU"
                path = "eupath"
            validate_directory_return = validateDirectory(game_directory, region)
            logging.debug(f"{sys._getframe().f_code.co_name}() -> validate_directory_return: {validate_directory_return}.")

            if validate_directory_return:
                path_entry.delete(0, 'end')
                path_entry.insert(0, game_directory)
                load_configs = appConfigLoad()
                app_config = load_configs[0]
                app_config.set('app', path, game_directory)
                appConfigSave(app_config)
                return True

        else:
            if not verifyGamePath():
                logging.debug(f"ERROR -> {sys._getframe().f_code.co_name}() -> Wrong game folder.")
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
    logging.debug(f"{sys._getframe().f_code.co_name}() -> {verify_all_button.cget('text')} button pressed.")
    try:
        if verifyGamePath() == True:
            type_count = 0
            for file_type in file_type_list:
                def verifyFilesThreaded(file_type, type_count):
                    logging.debug(f"({file_type}) {sys._getframe().f_code.co_name}() -> thread started.")
                    file_type_label_list[type_count].configure(text=translateText("app_return_label_verifying"), text_color=text_color_verifying)
                    install_buttons_list[type_count].configure(text=translateText("app_button_verifying"), state="disabled", font=font_regular)

                    # Sends the file type and verify
                    verify_files_return = verifyFiles(file_type)
                    if verify_files_return == True:
                        file_type_label_list[type_count].configure(text=translateText("app_return_label_install_ready"), text_color=text_color_fail)
                        install_buttons_list[type_count].configure(text=translateText("app_button_install"), state="normal", font=font_regular_bold)
                        delete_buttons_list[type_count].configure(state="disabled", font=font_regular)
                    else:
                        file_type_label_list[type_count].configure(text=translateText("app_return_label_update"), text_color=text_color_success)
                        install_buttons_list[type_count].configure(text=translateText("app_button_download"), state="normal", font=font_regular)
                        delete_buttons_list[type_count].configure(state="normal", font=font_regular_bold)
                        
                verifyFilesThreaded_func = threading.Thread(target=verifyFilesThreaded, args=(file_type, type_count))
                verifyFilesThreaded_func.start()
                #verifyFilesThreaded_func.join() # crashes the app =(
                type_count += 1
        else:
            self.set("Config")
            #TODO ADD ERROR
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
        logging.debug(f"{sys._getframe().f_code.co_name}() -> {copy_delete.capitalize()} ({file_type.capitalize()}) button pressed.")
        return_label.configure(text=translateText("app_return_label_verifying"))
        def copyFilesThreaded():
            copy_files_return = copyFiles(file_type, copy_delete, return_label)
            if copy_files_return == False:
                return False
            elif copy_files_return == True:
                if copy_delete == "copy":
                    return_label.configure(text=translateText("app_return_label_install"), text_color=text_color_success)
                    return_button.configure(text=translateText("app_button_uptodate"), state="disabled", font=font_regular)
                    delete_button.configure(state="normal", font=font_regular_bold)
                    if (file_type == "translation"):
                        return_button.configure(text=translateText("app_button_download"), state="normal", font=font_regular_bold)
                elif copy_delete == "delete":
                    return_label.configure(text=translateText("app_return_label_deleted"), text_color=text_color_success)
                    return_button.configure(state="disabled", font=font_regular)
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
    try:
        app_config = appConfigLoad()[0]
        if not app_config.get('app', 'region'):
            logging.info(f"{sys._getframe().f_code.co_name}() :: First run!")
            logging.debug(f"{sys._getframe().f_code.co_name}() -> getClassicNaPath() initialized.")
            getClassicNaPath()
            logging.debug(f"{sys._getframe().f_code.co_name}() -> getClassicEuPath() initialized.")
            getClassicEuPath()
            logging.debug(f"{sys._getframe().f_code.co_name}() -> getClassicEuLauncherPath() initialized.")
            getClassicEuLauncherPath()
            logging.debug(f"{sys._getframe().f_code.co_name}() -> verifyGamePath() initialized.")
            verifyGamePath()
            logging.debug(f"{sys._getframe().f_code.co_name}() -> defineRegion() initialized.")
            defineRegion()
            return True
        else:
            logging.info(f"{sys._getframe().f_code.co_name}() :: Not the first run anymore!")
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
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        try:
            a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\NCWest\\AION_CLASSIC')
        except:
            logging.debug(f"{sys._getframe().f_code.co_name}(): Installation path not found. Select manually.")
            return False
        if a_key:
            classic_na_path = winreg.QueryValueEx(a_key, "BaseDir")[0]
            logging.debug(f"{sys._getframe().f_code.co_name}() -> na_dir: {classic_na_path}")
            if classic_na_path[len(classic_na_path)-1] == "\\":
                classic_na_path = classic_na_path.rstrip(classic_na_path[-1])
            app_config = appConfigLoad()[0]
            app_config.set('app', 'napath', classic_na_path)
            appConfigSave(app_config)
            return True
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
                    app_config = appConfigLoad()[0]
                    app_config.set('app', 'eupath', classic_eu_path)
                    appConfigSave(app_config)
                    return True
            except:
                continue
        if not_found == True:
            logging.debug(f"{sys._getframe().f_code.co_name}(): Installation path not found. Select manually.")
            return False
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
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        try:
            a_key = winreg.OpenKey(a_reg, r'SOFTWARE\\WOW6432Node\\Gameforge4d\\GameforgeClient\\MainApp\\Libraries\\c')
        except:
            logging.debug(f"{sys._getframe().f_code.co_name}(): Installation path not found. Select manually.")
            return False
        if a_key:
            classic_eu_launcher_path = winreg.QueryValueEx(a_key, "LibraryLocation")[0]
            logging.debug(f"{sys._getframe().f_code.co_name}() -> classic_eu_launcher_path: {classic_eu_launcher_path}")
            if classic_eu_launcher_path[len(classic_eu_launcher_path)-1] == "\\":
                classic_eu_launcher_path = classic_eu_launcher_path.rstrip(classic_eu_launcher_path[-1])
            app_config = appConfigLoad()[0]
            app_config.set('app', 'eulauncherpath', classic_eu_launcher_path)
            appConfigSave(app_config)
            return True
    except Exception as e:
        getException(e)
        return False

def defineRegion():
    """
    #TODO redo region handling wish JSON

    Defines the region that is used to set which versions of
    the game will have files replaced on request.
    """
    try:
        count_region = 0
        verifyGamePath() # verifys if game path selected is accurate.
        app_config = appConfigLoad()[0] # Reloads config.
        if app_config.get('app', 'napath'): count_region += 1
        if app_config.get('app', 'eupath'): count_region += 2
        app_config.set('app', 'region', str(count_region))
        appConfigSave(app_config)
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
        app_config = appConfigLoad()[0]
        na_path = app_config.get('app', 'napath')
        eu_path = app_config.get('app', 'eupath')
        app_region = app_config.get('app', 'region')
        if not app_region == "0":
            wrong_directory = translateText("functions_wrong_directory")
            wrong_directory_logs = "Selected folder is not the correct {VERSION} game folder. Please select the root {VERSION} game folder."
            if app_region in ("1", "3"):
                logging.debug(f"{sys._getframe().f_code.co_name}() -> na_path: {na_path}")
                if na_path:
                    game_path = f"{na_path}\\bin64\\Aion.bin"
                    if not os.path.isfile(game_path):
                        app_config.set('app', 'napath', "")
                        appConfigSave(app_config)
                        logging.error(f"ERROR -> {sys._getframe().f_code.co_name}() :: {wrong_directory_logs.replace('{VERSION}', 'NA')}")
                        showAlert("showerror", wrong_directory.replace("{VERSION}","NA"))
                        return False
                else:
                    logging.debug(f"{sys._getframe().f_code.co_name}() -> NA game directory is not set.")
                    logging.error(f"ERROR -> {sys._getframe().f_code.co_name}() :: {wrong_directory_logs.replace('{VERSION}', 'NA')}")
                    showAlert("showerror", wrong_directory.replace("{VERSION}","NA"))
                    return False
            if app_region in ("2", "3"):
                logging.debug(f"{sys._getframe().f_code.co_name}() -> eu_path: {eu_path}")
                if eu_path:
                    game_path = f"{eu_path}\\bin64\\aionclassic.bin"
                    if not os.path.isfile(game_path):
                        app_config.set('app', 'eupath', "")
                        appConfigSave(app_config)
                        logging.error(f"ERROR -> {sys._getframe().f_code.co_name}() :: {wrong_directory_logs.replace('{VERSION}', 'EU')}")
                        showAlert("showerror", wrong_directory.replace("{VERSION}","EU"))
                        return False
                else:
                    logging.error(f"ERROR -> {sys._getframe().f_code.co_name}() :: {wrong_directory_logs.replace('{VERSION}', 'EU')}")
                    showAlert("showerror", wrong_directory.replace("{VERSION}","EU"))
                    return False
            return True
        else:
            showAlert("showerror", translateText("functions_show_game_region"))
            return False
    except Exception as e:
        getException(e)
        return False
    
# alert_type = showinfo | showwarning | showerror | askquestion | askokcancel | askyesno 
def showAlert(alert_type, message):
    try:
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
            logging.error(f"ERROR -> {sys._getframe().f_code.co_name}() :: Unknown alert type.")
            return
        logging.debug(f"{sys._getframe().f_code.co_name}() -> alert_return: {alert_return}.")
        return alert_return
    except Exception as e:
        getException(e)
        return False

def validateDirectory(game_directory, region):
    try:
        wrong_directory = translateText("functions_wrong_directory")
        if region == "NA":
            game_path = f"{game_directory}\\bin64\\Aion.bin"
            logging.debug(f"{sys._getframe().f_code.co_name}() -> game_path: {game_path}.")
            if not os.path.isfile(game_path):
                showAlert("showerror", wrong_directory.replace("{VERSION}","NA"))
                return False
            else:
                return True
        if region == "EU":
            game_path = f"{game_directory}\\bin64\\aionclassic.bin"
            logging.debug(f"{sys._getframe().f_code.co_name}() -> game_path: {game_path}.")
            if not os.path.isfile(game_path):
                showAlert("showerror", wrong_directory.replace("{VERSION}","EU"))
                return False
            else:
                return True
    except Exception as e:
        getException(e)
        return False

def getRelativeFilePath(game_file_type):
    """
    Sets the base path for each asset/file type.
    """
    try:
        if (game_file_type == "filter"):
            file_path = "data\\Strings"
        elif (game_file_type == "font"):
            file_path = "textures\\ui"
        elif (game_file_type == "voice"):
            file_path = "sounds\\voice"
        elif (game_file_type == "translation"):
            file_path = "data"
        else:
            logging.error(f"ERROR -> {sys._getframe().f_code.co_name}() :: Unknown file type.")
            return
        return file_path
    except Exception as e:
        getException(e)
        return False

# TODO change region/language config methods to JSON

def getFullFilePath(game_lang, file_path):
    """
    Gets the full file paths for the selected regions using the
    previously set base file path.
    """
    try:
        verifyGamePath()
        app_config = appConfigLoad()[0]
        na_path = app_config.get('app', 'napath')
        eu_path = app_config.get('app', 'eupath')
        full_file_path = []
        for lang in game_lang:
            if lang == "enu":
                full_file_path.append(f"{na_path}\\l10n\\{lang}\\{file_path}")
            elif lang in ("eng", "fra", "deu"):
                full_file_path.append(f"{eu_path}\\l10n\\{lang}\\{file_path}")
            else:
                logging.error(f"ERROR -> {sys._getframe().f_code.co_name}() :: Unknown region.")
                return
        return full_file_path
    except Exception as e:
        getException(e)
        return False

def getFilePath(game_file_type):
    try:
        app_config = appConfigLoad()[0]
        app_region = app_config.get('app', 'region')
        game_lang = []
        if not app_region in ("1", "2", "3"):
            logging.error(f"ERROR -> {sys._getframe().f_code.co_name}() -> app_region :: Region is not set.")
            return
        if app_region in ("1", "3"):
            game_lang.append("enu")
        if app_region in ("2", "3"):
            game_lang.extend(["eng", "fra", "deu"])
        # Gets all files and hashes them when files already exist in game path
        file_path = getRelativeFilePath(game_file_type)
        logging.debug(f"{sys._getframe().f_code.co_name}() -> file_path: {file_path}.")
        # Defines assets path
        assets_full_file_path = [f".\\assets\\{file_path}"]
        # Returns [full_file_path]. It can be multiple paths depending on regions selected
        full_file_path = getFullFilePath(game_lang, file_path)
        return assets_full_file_path, full_file_path
    except Exception as e:
        getException(e)
        return False

def verifyFiles(game_file_type):
    """
    Defines regions and languages of which the app will use to
    look for files.

    Calls 'get_full_files()' to finish processing the request.
    """
    try:
        if game_file_type in ("filter", "font", "voice", "translation"):
            # Returns [[verify_hash_list], [copy_files_list]]
            files_path = getFilePath(game_file_type)
            assets_full_file_path = files_path[0]
            full_file_path = files_path[1]

            compared_files = getFiles(assets_full_file_path, full_file_path, game_file_type) #compared_files[0] = hash | compared_files[1] = all files
            logging.debug(f"({game_file_type}) {sys._getframe().f_code.co_name}() -> compared_files: {len(compared_files)} - {compared_files}")
            
            def saveFilesJson(copy_files_verify):
                install_files = copy_files_verify[0]
                delete_files = copy_files_verify[1]
                if len(install_files) == 0:
                    install_files = {}
                with open(f'.\\config\\lists\\{game_file_type}_install.json', 'w', encoding='utf-8') as f:
                    json.dump(install_files, f, ensure_ascii=False, indent=4)
                    f.close

                if len(delete_files) == 0:
                    delete_files = {}
                with open(f'.\\config\\lists\\{game_file_type}_delete.json', 'w', encoding='utf-8') as f:
                    json.dump(delete_files, f, ensure_ascii=False, indent=4)
                    f.close

            # Compares duplicated files hashes and adds them to the copy_files_verify list if hashes differ
            copy_files_verify = compareFilesHash(compared_files)
            saveFilesJson(copy_files_verify)

            logging.debug(f"({game_file_type}) {sys._getframe().f_code.co_name}() -> copy_files_verify: {len(copy_files_verify)} - {copy_files_verify}")
            
        else:
            logging.error(f"ERROR -> ({game_file_type}) {sys._getframe().f_code.co_name}() -> game_file_type: {game_file_type} :: Unknown file type.")
            copy_files_verify = {}
            
        logging.debug(f"({game_file_type}) {sys._getframe().f_code.co_name}() -> copy_files_verify: {len(copy_files_verify)} {copy_files_verify}.")
        if len(copy_files_verify[0]) <= 0:
            return False
        elif len(copy_files_verify[0]) >= 1:
            return True
        else:
            logging.warning(f"({game_file_type}) {sys._getframe().f_code.co_name}() -> copy_files_verify type: {type(copy_files_verify)}.")
            return False
    except Exception as e:
        getException(e)
        return False
    
def getFiles(assets_full_file_path, full_file_path, game_file_type):
    logging.debug(f"{sys._getframe().f_code.co_name}() -> assets_full_file_path: {assets_full_file_path} - full_file_path: {full_file_path}")
    try:
        copy_files_list = []
        verify_hash_list = []
        for assets_dir in assets_full_file_path:
            logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> assets_dir: {assets_dir}.")
            if (game_file_type == "translation"):
                for file in os.listdir(assets_dir):
                    logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> os.listdir(assets_dir): {os.listdir(assets_dir)} type(file)): {type(file)} NOT file:{file}.")
                    logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> os.listdir(assets_dir): {os.listdir(assets_dir)} type(file)): {type(file)} file: {file}.")
                    if (file.endswith('.pak')):
                        logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> file: {file}.")
                        for files_dir in full_file_path:
                            file_path = files_dir+'\\'+file
                            asset_path = assets_dir+'\\'+file
                            if not os.path.exists(file_path):
                                logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> file_path -> copy_files_list[]: NAY {file_path}")
                                copy_files_list.extend([[asset_path, file_path]])
                            else:
                                logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> file_path -> verify_hash_list[]: AY {file_path}")
                                verify_hash_list.extend([[asset_path, file_path]])
                                copy_files_list.extend([[asset_path, file_path]])
            else:
                for (dirpath, dirnames, filenames) in os.walk(assets_dir):
                    for filename in filenames:
                        relative_path = dirpath.replace(assets_dir, "")
                        for files_dir in full_file_path:
                            file_path = files_dir+relative_path+'\\'+filename
                            asset_path = assets_dir+relative_path+'\\'+filename
                            if not os.path.exists(file_path):
                                logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> file_path -> copy_files_list[]: NAY {file_path}")
                                copy_files_list.extend([[asset_path, file_path]])
                            else:
                                logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> file_path -> verify_hash_list[]: AY {file_path}")
                                verify_hash_list.extend([[asset_path, file_path]])
            logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> verify_hash_list: {verify_hash_list}")
            logging.info(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> verify_hash_list: {len(verify_hash_list)} files need to be compared.")
            logging.debug(f"({assets_dir}) {sys._getframe().f_code.co_name}() -> copy_files_list: {copy_files_list}")
            return verify_hash_list, copy_files_list
    except Exception as e:
        getException(e)
        return False
    
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
    
def copyFiles(game_file_type, copy_delete, return_label):
    """
    Creates directories, removes old/different files, copies
    new files.
    """
    try:
        if copy_delete == "copy":
            downloadFile(game_file_type, return_label)
            with open(f'.\\config\\lists\\{game_file_type}_install.json') as files_list:
                copy_files_list = json.load(files_list)
                files_list.close
            if len(copy_files_list) < 1:
                logging.warning(f"ERROR -> {sys._getframe().f_code.co_name}() :: Nothing to {copy_delete} from '.\\config\\lists\\{game_file_type}_install.json'")
                return False
        elif copy_delete == "delete":
            with open(f'.\\config\\lists\\{game_file_type}_delete.json') as files_list:
                copy_files_list = json.load(files_list)
                files_list.close
            if len(copy_files_list) < 1:
                logging.warning(f"ERROR -> {sys._getframe().f_code.co_name}() :: Nothing to {copy_delete} from '.\\config\\lists\\{game_file_type}_delete.json'")
                return False
        logging.debug(f"{sys._getframe().f_code.co_name}() -> files -> type: {game_file_type}: {copy_files_list}")
        show_delete_warning = True
        for files in copy_files_list:
            logging.debug(f"FOR START - {sys._getframe().f_code.co_name}() -> files: {len(files)} {files} - FOR START :: show_delete_warning: {show_delete_warning}")
            asset_file = files[0]
            game_file = files[1]

            if copy_delete == "copy":
                if not os.path.isdir(os.path.dirname(game_file)):
                    logging.debug(f"{sys._getframe().f_code.co_name}() -> MKDIR: {os.path.dirname(game_file)}")
                    os.makedirs(os.path.dirname(game_file))
                logging.debug(f"{sys._getframe().f_code.co_name}() -> COPY :: {asset_file} -> {game_file}")
                shutil.copy2(asset_file, game_file)
            elif copy_delete == "delete":
                if show_delete_warning == True:
                    alert = showAlert("askquestion", translateText("functions_show_delete").replace('{FILETYPE}', translateText(f"{game_file_type}")))
                    if alert == "no":
                        return False
                    else:
                        show_delete_warning = False
                remove_file = game_file
                logging.debug(f"{sys._getframe().f_code.co_name}() -> REMOVE????????? {remove_file}")
                if os.path.isfile(remove_file):
                    logging.debug(f"{sys._getframe().f_code.co_name}() -> REMOVE: {remove_file}")
                    os.remove(remove_file)
            logging.debug(f"{sys._getframe().f_code.co_name}() -> copy_backup: {copy_delete}")
            logging.debug(f"FOR END - {sys._getframe().f_code.co_name}() -> files: {len(files)} {files} - FOR END :: show_delete_warning: {show_delete_warning}")
        return True
    except Exception as e:
        getException(e)
        return False
    
def downloadFile(file_type, return_label):
    """ 
    Download and save a file specified by url to dest directory,
    """
    file_path = getFilePath(file_type)[0]
    dest = file_path[0]
    logging.debug(f"{sys._getframe().f_code.co_name}() -> file_path: {file_path}")

    if (file_type == "filter"):
        urls = ["https://github.com/giordanidev/aion-classic-mods-py/raw/master/assets/Data/Strings/aionfilterline_load.pak"]
    elif (file_type == "font"):
        urls = ["https://github.com/giordanidev/aion-classic-mods-py/raw/master/assets/textures/ui/hit_number_jp.pak"]
    elif (file_type == "voice"):
        urls = ["https://github.com/giordanidev/aion-classic-mods-py/raw/master/assets/sounds/voice/attack/attack_kr.pak",
                "https://github.com/giordanidev/aion-classic-mods-py/raw/master/assets/sounds/voice/cast/cast_kr.pak",
                "https://github.com/giordanidev/aion-classic-mods-py/raw/master/assets/sounds/voice/damage/damage_kr.pak",
                "https://github.com/giordanidev/aion-classic-mods-py/raw/master/assets/sounds/voice/defence/defence_kr.pak",
                "https://github.com/giordanidev/aion-classic-mods-py/raw/master/assets/sounds/voice/login/login_kr.pak",
                "https://github.com/giordanidev/aion-classic-mods-py/raw/master/assets/sounds/voice/motion/motion_kr.pak"]
    elif (file_type == "translation"):
        urls = ["https://github.com/giordanidev/aion-classic-ptbr/raw/main/teste/data_ptbr.pak"]

    for url in urls:
        u = urllib2.urlopen(url)

        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        
        filename = os.path.basename(path)
        logging.debug(f"{sys._getframe().f_code.co_name}() -> filename: {filename}")

        logging.debug(f"{sys._getframe().f_code.co_name}() -> dest: {dest}")
        if dest:
            filepath = os.path.join(dest, filename)

        with open(filepath, 'wb') as f:
            meta = u.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func("Content-Length")
            file_size = None
            if meta_length:
                file_size = int(meta_length[0])
                
            print(f"Testing with {file_size} Bytes download")
            print("Downloading: {0} Bytes: {1}".format(url, file_size))

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
                print(status, end="")
                return_label.configure(text=status, text_color=text_color_success)
            print()

    return filepath

"""
def forceCloseAion(action, game_client, close_button, return_label):
    running_apps = psutil.process_iter(['pid','name']) #returns names of running processes
    found = False

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

    for app in running_apps:
        sys_app = app.info.get('name').split('.')
        sys_app_name = sys_app[0].lower()

        if sys_app_name in app_name and app_extension in sys_app:
            if action == "close":
                pid = app.info.get('pid') #returns PID of the given app if found running
            
                try: #deleting the app if asked app is running.(It raises error for some windows apps)
                    app_pid = psutil.Process(pid)
                    app_pid.terminate()
                    logging.debug(f"{sys._getframe().f_code.co_name}() -> Process '{sys_app_name}.{app_extension} ({app_pid})' closed!")
                    close_button.configure(state="disabled", font=font_regular)
                    return_label.configure(text=app_close_phrase, text_color=text_color_success, font=font_regular)
                    found = True
                except Exception as e:
                    getException(e)
                    return False
            elif action == "check":
                close_button.configure(state="normal", font=font_regular_bold)
                return_label.configure(text=app_check_phrase, text_color=text_color_success, font=font_regular)
        else: pass
    
    if found == False:
        logging.debug(f"{sys._getframe().f_code.co_name}() -> Aion process not found!")
        close_button.configure(state="disabled", font=font_regular)
        return_label.configure(text=translateText("app_info_aion_notfound"), font=font_regular)

def forceCloseAion_thread(action, game_client, close_button, return_label):
    while 1 :
        forceCloseAion(action, game_client, close_button, return_label)
        time.sleep(10)
"""

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

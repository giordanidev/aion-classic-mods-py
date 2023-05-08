from configparser import ConfigParser
import hashlib
import os.path

def app_config_read():
    try:
        app_config = ConfigParser()
        config_path = 'config/'
        config_file = 'config.ini'
        config_full_path = config_path + config_file
        app_config.read(config_full_path)

        return (app_config, config_full_path)
    except: ""
app_config = app_config_read()[0]
config_full_path = app_config_read()[1]

def check_files_hash(game_lang, game_file_type):
    try:
        app_config = app_config_read()[0]

        if (game_file_type == "filter"):
            game_file_type = "Data\\Strings\\aionfilterline.pak"
        elif (game_file_type == "font"):
            game_file_type = "textures\\ui\\hit_number.pak"
        elif (game_file_type == "voice"):
            game_file_type = "sounds\\voice\\attack\\attack.pak"

        count = 0
        check_hash = []
        for file_check in game_lang:
            if file_check == "original":
                filter_path = f"assets\\{game_file_type}"
            elif file_check == "enu":
                filter_path = f"{app_config.get('app', 'napath')}\\l10n\\{file_check}\\{game_file_type}"
            else:
                filter_path = f"{app_config.get('app', 'eupath')}\\l10n\\{file_check}\\{game_file_type}"

            if os.path.isfile(filter_path):
                with open(filter_path, 'rb', buffering=0) as f:
                    hashed = hashlib.file_digest(f, 'sha256').hexdigest()
                    check_hash.append(hashed)
            else:
                check_hash.append(False)
            count += 1
        return check_hash
    except: print("ERRO")

def check_files():
    try:
        app_config = app_config_read()[0]
        game_lang = ["original", "enu", "eng", "deu", "fra"]
        filter_hash = check_files_hash(game_lang, "filter")
        font_hash = check_files_hash(game_lang, "font")
        voice_hash = check_files_hash(game_lang, "voice")

        print(filter_hash)
        print(font_hash)
        print(voice_hash)

        check_filter_pass = True
        check_font_pass = True
        check_voice_pass = True

        if (filter_hash[0] != False) and (font_hash[0] != False):
            if (app_config.get('app', 'region') == "1") or (app_config.get('app', 'region') == "3"):
                if (filter_hash[1] != filter_hash[0]):
                    check_filter_pass = False
                if (font_hash[1] != font_hash[0]):
                    check_font_pass = False
                if (font_hash[1] != font_hash[0]):
                    check_voice_pass = False
                    
            if (app_config.get('app', 'region') == "2") or (app_config.get('app', 'region') == "3"):
                if (filter_hash[2] != filter_hash[0]) or (filter_hash[3] != filter_hash[0]) or (filter_hash[4] != filter_hash[0]):
                    check_filter_pass = False
                if (font_hash[2] != font_hash[0]) or (font_hash[3] != font_hash[0]) or (font_hash[4] != font_hash[0]):
                    check_font_pass = False
                if (voice_hash[2] != voice_hash[0]) or (voice_hash[3] != voice_hash[0]) or (voice_hash[4] != voice_hash[0]):
                    check_voice_pass = False
        
        return (check_filter_pass, check_font_pass, check_voice_pass)
    except: print("ERRO")
check_files()

def copy_files(game_lang, game_file_type):
    try: ""

    except: ""
from configparser import ConfigParser
import hashlib
import os.path

def app_config_read():
    try:
        global app_config
        global config_full_path
        app_config = ConfigParser()
        config_path = 'config/'
        config_file = 'config.ini'
        config_full_path = config_path + config_file
        app_config.read(config_full_path)
        
        global config_theme, config_color, config_region, config_na_path
        global config_font_version, config_filter_version, config_eu_path

        config_theme = app_config.get('app', 'theme')
        config_color = app_config.get('app', 'color')
        config_region = app_config.get('app', 'region')
        config_na_path = app_config.get('app', 'napath')
        config_eu_path = app_config.get('app', 'eupath')
        config_font_version = app_config.get('app', 'fontversion')
        config_filter_version = app_config.get('app', 'filterversion')

        return app_config
    except: ""
app_config_read()

def check_filter_hash(filter_files):
    app_config_read()
    count = 0
    check_hash = []
    for filter in filter_files:
        if filter == "original":
            filter_path = "assets\\l10n\\enu\\data\\Strings\\aionfilterline.pak"
        elif filter == "enu":
            filter_path = f"{config_na_path}\\l10n\\{filter}\\data\\Strings\\aionfilterline.pak"
        else:
            filter_path = f"{config_eu_path}\\l10n\\{filter}\\data\\Strings\\aionfilterline.pak"

        if os.path.isfile(filter_path):
            with open(filter_path, 'rb', buffering=0) as f:
                print(f"FILTER {filter_path} PASSED. {count} {hashlib.file_digest(f, 'sha256').hexdigest()}")
                check_hash.append(hashlib.file_digest(f, 'sha256').hexdigest())
        else:
            print(f"FILTER {filter_path} NOT FOUND. {count}")
            check_hash.append(False)
        count += 1
    return check_hash

def check_files():
#try:
    filter_files = ["original", "enu", "eng", "deu", "fra"]
    check_hash = check_filter_hash(filter_files)
    print(check_hash)
check_files()
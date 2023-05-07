from configparser import ConfigParser

class appSettings:
    def appConfigRead():
        appConfig = ConfigParser()
        configPath = 'config/'
        configFile = 'config.ini'
        configFullPath = configPath + configFile
        appConfig.read(configFullPath)
        return appConfig, configFullPath

    def appConfigWrite(appConfig, configFullPath):
        with open(configFullPath, 'w') as configWrite:
                appConfig.write(configWrite)

    """
    #DEFAULT VALUES
    self.themeButton.set(appConfigRead.get('app', 'theme')) # Modes: "System" (standard), "Dark", "Light"
    self.colorButton.set(appConfigRead.get('app', 'color'))
    self.regionRadio.set(appConfigRead.get('app', 'region'))
    configTab.regionSelection()
    """
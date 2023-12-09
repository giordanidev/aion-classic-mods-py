#TODO
#ADD OWN FUNCTIONS FILE/LOGS

from functions import *
import tkinter as tk, customtkinter as ctk, logging

logging.debug(f"{sys._getframe().f_code.co_name}() -> Updater initialized.")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        global app_config

        if app_config['on_start'] == True:

            self.title(translateText("app_title") + translateText("app_updater_title") + translateText("app_updater_version"))

            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            # System appearance
            ctk.set_appearance_mode(app_config['theme'])
            ctk.set_default_color_theme(app_config['color'].lower())

            #center app on main screen 
            centerApp(450, 150, self)

            self.updaterFrame = ctk.CTkFrame(self)
            self.updaterFrame.grid(row=0, column=0, sticky="ew")
            self.updaterFrame.configure(fg_color="transparent")
            self.updaterFrame.grid_columnconfigure(0, weight=1)
            self.updaterFrame.grid_rowconfigure(3, weight=1)

            self.infoLabel = ctk.CTkLabel(self.updaterFrame, text=translateText("app_updater_searching"))
            self.infoLabel.grid(row=0, column=0, columnspan=4, padx=padx_both, pady=pady_both)

            self.installButton = ctk.CTkButton(self.updaterFrame, text=translateText("app_button_update"), state="disabled", width=90)
            self.installButton.grid(row=1, column=1, padx=padx_both, pady=pady_both, sticky="ew")

            self.ignoreButton = ctk.CTkButton(self.updaterFrame, text=translateText("app_button_updater_ignore"), state="disabled", width=90)
            self.ignoreButton.grid(row=1, column=2, padx=padx_both, pady=pady_both, sticky="ew")
            
            self.progressbar = ctk.CTkProgressBar(self.updaterFrame, orientation="horizontal", width=280, mode="indeterminate")
            self.progressbar.grid(row=2, column=0, columnspan=4, padx=padx_both, pady=pady_both)
            self.progressbar.start()

            def checkbox_event():
                print("checkbox toggled, current value:", self.on_startCheckbox.get())
                
                if self.on_startCheckbox.get() == False:
                    self.on_startCheckbox.deselect()
                    self.progressbar.stop()
                    self.progressbar.configure(mode="determinate")
                    self.progressbar.set(0)
                else:
                    self.on_startCheckbox.select()
                    self.progressbar.configure(mode="indeterminate")
                    self.progressbar.start()
            self.on_startCheckbox = ctk.CTkCheckBox(self.updaterFrame, text=translateText("app_updater_on_start"), command=checkbox_event, onvalue=True, offvalue=False)
            self.on_startCheckbox.grid(row=3, column=3, padx=padx_both, pady=pady_both, sticky="s")
            self.on_startCheckbox.select()
            
            cloud_version = checkUpdates()
            
            self.iconbitmap(app_icon)
            self.resizable(0, 0)
            self.mainloop()
        else:
            print("QUIT")
            self.destroy()

app = App()
import customtkinter as ctk
from functools import partial

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(4, weight=1)
        
        def centerApp(width, height, self):
            """
            Centers the app in the computer's main screen on start.
            """
            window_width = width
            window_height = height
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x_cordinate = int((screen_width/2) - (window_width/2))
            y_cordinate = int((screen_height/2) - (window_height/2) - 50)
            self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        # DEFINES APP SIZE AND POSITION ON MAIN SCREEN
        centerApp(400, 90, self)

        linha_configs = 0
        font_regular_bold = ("", 12, "bold")
        padx_both = 2.5

        def checkbox_event(checkbox_get, checkbox_lang):
            # TODO
            # SAVE NEW CONFIGS
            print(f"CHECKBOX ({checkbox_get})> {checkbox_lang}>{checkbox_get.cget('text')}: {checkbox_get.get()}")

        regions = [['NA', 'Classic NA', 'E:/JOGOS/AION_CLASSIC', True], ['EU', 'Classic EU', 'E:/JOGOS/aionclassic', True]]
        langs = [['NA', 'ENU', True], ['NA', 'BRA', False], ['EU', 'DEU', False], ['EU', 'ENG', True], ['EU', 'FRA', False]]

        print(regions)
        for region in regions:
            self.region_selectionLabel = ctk.CTkLabel(self, text=region[1]+":", font=font_regular_bold)
            self.region_selectionLabel.grid(row=linha_configs, column=0, padx=padx_both, pady=2, sticky="e")
            coluna = 1
            for lang in langs:
                if lang[0] == region[0]:
                    if lang[2] == True:
                        check_var = ctk.StringVar(value="on")
                    else:
                        check_var = ctk.StringVar(value="off")
                    self.checkbox = ctk.CTkCheckBox(self, variable=check_var, onvalue="on", offvalue="off")
                    self.checkbox.configure(command=partial(checkbox_event, self.checkbox, lang[0]))
                    self.checkbox.configure(text=lang[1])
                    self.checkbox.grid(row=linha_configs, column=coluna, padx=padx_both, pady=2)
                    coluna += 1
            linha_configs += 1

        #self.iconbitmap(app_icon)
        self.resizable(0, 0)
        self.mainloop()

app = App()
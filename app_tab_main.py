import customtkinter as ctk
from app_tabs import mainTabs

class appMainTab():
    # App tab widgets
    def create_main_tab(self):
        self.appTopFrame = ctk.CTkFrame(mainTabs.appTab)
        self.appTopFrame.grid(row=0, column=0, sticky="new")
        self.appTopFrame.configure(fg_color="transparent")
        self.appTopFrame.grid_columnconfigure(1, weight=1)  # configure grid system

        self.voiceButton = ctk.CTkButton(self.appTopFrame, text="Check Updates", command="")
        self.voiceButton.grid(row=0, column=2, padx=(5, 0), pady=5)
        self.voiceButton.configure(font=("", 13, "bold"), state="disabled")

        self.voiceLabel = ctk.CTkLabel(self.appTopFrame, text="KR Voices:")
        self.voiceLabel.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="e")
        self.voiceLabel.configure(font=("", 12, "bold"))
        self.filterLabel = ctk.CTkLabel(self.appTopFrame, text="Chat Filter:")
        self.filterLabel.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        self.filterLabel.configure(font=("", 12, "bold"))
        self.hitLabel = ctk.CTkLabel(self.appTopFrame, text="JP Fonts:")
        self.hitLabel.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="e")
        self.hitLabel.configure(font=("", 12, "bold"))

        self.voiceReturnLabel = ctk.CTkLabel(self.appTopFrame, text="Koren Voices are installed.")
        self.voiceReturnLabel.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.filterReturnLabel = ctk.CTkLabel(self.appTopFrame, text="Chat Filter is up to date.")
        self.filterReturnLabel.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.hitReturnLabel = ctk.CTkLabel(self.appTopFrame, text="JP Fonts are installed.")
        self.hitReturnLabel.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.voiceButton = ctk.CTkButton(self.appTopFrame, text="Install", command="")
        self.voiceButton.grid(row=1, column=2, padx=(5, 0), pady=5)
        self.filterButton = ctk.CTkButton(self.appTopFrame, text="Install", command="")
        self.filterButton.grid(row=2, column=2, padx=(5, 0), pady=5)
        self.hitButton = ctk.CTkButton(self.appTopFrame, text="Install", command="")
        self.hitButton.grid(row=3, column=2, padx=(5, 0), pady=5)

        self.appTextbox = ctk.CTkTextbox(self.appTopFrame)
        self.appTextbox.grid(row=4, column=0, columnspan=3, pady=(5, 0), sticky="nsew")
        self.appTextbox.configure(state="disabled")
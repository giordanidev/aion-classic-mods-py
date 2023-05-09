from app import App

if __name__ == '__main__':
    app = App()
    app.geometry("500x300")
    app.resizable(0, 0)
    app.eval("tk::PlaceWindow . center")
    app.mainloop()
# TODO
# START THE APP OBVIOUSLY.

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MainScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        nomes = ["Marga Rida", "João Silva", "Fábio Araújo", "Giordani Sarturi", "Marco Polo", "Luana Pavão", "Maria Isabela", "Gabriela Marinho", "Caudio Toscano"]
        self.cols = 4
        for nome in nomes:
            self.add_widget(Label(text=nome))
            self.username = TextInput(multiline=False)
            self.add_widget(self.username)
            
            self.add_widget(Label(text='Senha'))
            self.password = TextInput(password=True, multiline=False)
            self.add_widget(self.password)

class MyApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()
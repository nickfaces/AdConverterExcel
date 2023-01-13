from kivy.uix.screenmanager import Screen
import pandas as pd
from plyer import filechooser

class HomeScreen(Screen):
    pass

    def check_file(self):
        # input_file = pd.read_excel('Клиенты. Пример импорта.xlsx')
        current_path = self.ids.input_file.text
        try:
            input_file = pd.read_excel(current_path)

            out = input_file.columns.values.tolist()
            print('ok ok ok')
            print(current_path)
            print(out)
            self.goto_settings_screen()
        except Exception as e:
            print(e)


    # changing screens also can be done in python
    def goto_settings_screen(self):
        self.manager.set_current("settings")

    def filechoose(self):
        path = filechooser.open_file()[0]
        self.ids.input_file.text = path

from kivy.uix.screenmanager import Screen
import pandas as pd

class HomeScreen(Screen):

    # changing screens also can be done in python
    # def goto_settings_screen(self):
    #     self.manager.set_current("settings")
    pass

    def check_connection(self):
        # input_file = pd.read_excel('Клиенты. Пример импорта.xlsx')
        current_path = self.ids.input_file.text
        input_file = pd.read_excel(current_path)

        out = input_file.columns.values.tolist()
        print('ok ok ok')
        print(current_path)
        print(out)

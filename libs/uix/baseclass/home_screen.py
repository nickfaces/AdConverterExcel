from kivy.uix.screenmanager import Screen
import pandas as pd
from kivymd.uix.screen import MDScreen
from plyer import filechooser
from kivymd.app import MDApp

class HomeScreen(MDScreen):
    pass

    def check_file(self):
        # input_file = pd.read_excel('Клиенты. Пример импорта.xlsx')
        current_path = self.ids.input_file.text
        try:
            input_file = pd.read_excel(current_path)

            out = input_file.columns.values.tolist()
            app = MDApp.get_running_app()
            app.amount_items = len(input_file.index)
            app.input_file = input_file
            self.goto_settings_screen()
        except Exception as e:
            print(e)


    # changing screens also can be done in python
    def goto_settings_screen(self):
        self.manager.set_current("clients")

    def filechoose(self):
        try:
            path = filechooser.open_file(filters = ["*.xlsx", "*.xls"])[0]
            self.ids.input_file.text = path
        except Exception as e:
            print(e)
    
    def directory_choose(self):
        try:
            path = filechooser.choose_dir()[0]
            self.ids.output_dir.text = path
        except Exception as e:
            print(e)

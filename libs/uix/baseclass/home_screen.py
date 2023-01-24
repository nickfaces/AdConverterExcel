import os
import pandas as pd
from kivymd.uix.screen import MDScreen
from plyer import filechooser
from kivymd.app import MDApp

class HomeScreen(MDScreen):

    check_all_flag = True
    def on_enter(self, *args):

        path = os.getcwd()
        self.ids.output_dir.text = path

    def check_file(self):
        current_path = self.ids.clients_file.text
        try:
            clients_file = pd.read_excel(current_path)

            out = clients_file.columns.values.tolist()
            app = MDApp.get_running_app()
            app.amount_items = len(clients_file.index)
            app.clients_file = clients_file
            self.goto_settings_screen()
        except Exception as e:
            print(e)


    def goto_settings_screen(self):
        self.manager.set_current("clients")

    def clients_filechoose(self):
        try:
            path = filechooser.open_file(filters = ["*.xlsx", "*.xls"])[0]
            self.ids.clients_file.text = path
        except Exception as e:
            print(e)
    
    def nomenclature_filechoose(self):
        try:
            path = filechooser.open_file(filters = ["*.xlsx", "*.xls"])[0]
            self.ids.nomenclature_file.text = path
        except Exception as e:
            print(e)
    
    def work_filechoose(self):
        try:
            path = filechooser.open_file(filters = ["*.xlsx", "*.xls"])[0]
            self.ids.work_file.text = path
        except Exception as e:
            print(e)
    
    def directory_choose(self):
        try:
            path = filechooser.choose_dir()[0]
            self.ids.output_dir.text = path
        except Exception as e:
            print(e)


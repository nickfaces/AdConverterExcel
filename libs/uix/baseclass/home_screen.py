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



    def check_choices_to_import(self):
        screen_list = []
        if (self.ids.clients_check.active == True and self.ids.clients_file.text != ''):
            screen_list.append('clients')
        if (self.ids.nomenclature_check.active == True and self.ids.nomenclature_file.text != ''):
            screen_list.append('nomenclature')
        if (self.ids.work_check.active == True and self.ids.work_file.text != ''):
            screen_list.append('work')
        app = MDApp.get_running_app()
        app.screen_list = screen_list



    def check_file(self):
        clients_path = self.ids.clients_file.text
        try:
            clients_file = pd.read_excel(clients_path)
            app = MDApp.get_running_app()
            app.amount_items = len(clients_file.index)
            app.clients_file = clients_file
        except Exception as e:
            print(e)
        nomenclature_path = self.ids.nomenclature_file.text
        try:
            nomenclature_file = pd.read_excel(nomenclature_path)
            app = MDApp.get_running_app()
            app.amount_items = len(nomenclature_file.index)
            app.nomenclature_file = nomenclature_file
        except Exception as e:
            print(e)
        work_path = self.ids.work_file.text
        try:
            work_file = pd.read_excel(work_path)
            app = MDApp.get_running_app()
            app.amount_items = len(work_file.index)
            app.work_file = work_file
        except Exception as e:
            print(e)

        self.goto_import_screen()


    def goto_import_screen(self):
        app = MDApp.get_running_app()
        screen_list = app.screen_list
        app.current_screen = 0
        self.manager.set_current(screen_list[0])

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


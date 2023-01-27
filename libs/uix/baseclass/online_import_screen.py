import json
import os
import threading

import requests
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class OnlineImportScreen(Screen):

    def on_enter(self, *args):
        try:
            app = MDApp.get_running_app()
            owner = app.owner
            if owner == False:
                self.ids.online_import_start.disabled = True
                self.ids.clients_online_check.disabled = True
                self.ids.nomenclature_online_check.disabled = True
                self.ids.work_online_check.disabled = True
                self.ids.owner_status.opacity = 1
            else:
                self.ids.online_import_start.disabled = False
                self.ids.owner_status.opacity = 0
                self.check_files()
        except:
            self.ids.online_import_start.disabled = True
            self.ids.clients_online_check.disabled = True
            self.ids.nomenclature_online_check.disabled = True
            self.ids.work_online_check.disabled = True
            self.ids.owner_status.opacity = 1

    def check_files(self):
        app = MDApp.get_running_app()
        path = app.path
        os.chdir(path)
        if os.path.isfile('clients.xlsx'):
            print('clients')
            self.ids.clients_online_check.disabled = False
        else:
            self.ids.clients_online_check.disabled = True

        if os.path.isfile('nomenclature.xlsx'):
            self.ids.nomenclature_online_check.disabled = False
        else:
            self.ids.nomenclature_online_check.disabled = True

        if os.path.isfile('work.xlsx'):
            self.ids.work_online_check.disabled = False
        else:
            self.ids.work_online_check.disabled = True

    def import_online_thread(self):
        threading.Thread(target=self.import_online)

    def import_online(self):
        app = MDApp.get_running_app()
        path = app.path
        os.chdir(path)
        with open('clients.xlsx', 'rb') as f:
            r = app.session
            headers = {'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Connection': 'keep-alive',
                        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryhwIhGUgh7owjR96x',}
                        # 'sec-ch-ua': "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"
                        # 'sec-ch-ua-mobile': '?0'
                        # 'sec-ch-ua-platform': "Linux"}
            sadasd = r.post('https://online.autodealer.ru/api/back/files',headers=headers, files={'clients.xlsx': f})
            jsans = json.loads(sadasd.text)
            print(jsans)


        pass
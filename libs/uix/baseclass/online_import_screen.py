import json
import os
import threading
from pathlib import Path

from kivy.clock import mainthread, Clock
from kivy.properties import BooleanProperty, NumericProperty
from kivymd.uix.dialog import MDDialog
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp




class OnlineImportScreen(Screen):

    dialog = None
    progress = NumericProperty(0)

    def on_enter(self, *args):
        try:
            app = MDApp.get_running_app()
            owner = app.owner
            if owner == False:
                # self.ids.online_import_start.disabled = True
                self.ids.clients_online_check.disabled = True
                self.ids.nomenclature_online_check.disabled = True
                self.ids.work_online_check.disabled = True
                self.ids.owner_status.opacity = 1
            else:
                self.ids.online_import_start.disabled = False
                self.ids.owner_status.opacity = 0
                self.check_files()
        except:
            # self.ids.online_import_start.disabled = True
            self.ids.clients_online_check.disabled = True
            self.ids.nomenclature_online_check.disabled = True
            self.ids.work_online_check.disabled = True
            self.ids.owner_status.opacity = 1

    def check_files(self):
        app = MDApp.get_running_app()
        path = app.path
        os.chdir(path)
        if os.path.isfile('clients.xlsx'):
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
        if self.ids.clients_online_check.active == True:
            self.spinner_toggle('clients_online_import_spin')
        if self.ids.clients_online_check.active == True:
            clients_path = self.manager.get_screen("home").ids.clients_file.text
            if clients_path == '':
                clients_path = 'clients.xlsx'
            part_url = 'contragents'
            spin_name = 'clients_online_import_spin'
            file_name = 'clients.xlxs'
            threading.Thread(target=self.upload_file, kwargs={'path': clients_path, 'part_url': part_url, 'spin': spin_name, 'file_name': file_name}).start()

        if self.ids.nomenclature_online_check.active == True:
            self.spinner_toggle('nomenclature_online_import_spin')
        if self.ids.nomenclature_online_check.active == True:
            nomenclatures_path = self.manager.get_screen("home").ids.nomenclature_file.text
            if nomenclatures_path == '':
                nomenclatures_path = 'nomenclature.xlsx'
            part_url = 'nomenclatures'
            spin_name = 'nomenclature_online_import_spin'
            file_name = 'nomenclature.xlxs'
            threading.Thread(target=self.upload_file,
                             kwargs={'path': nomenclatures_path, 'part_url': part_url, 'spin': spin_name, 'file_name': file_name}).start()

        if self.ids.work_online_check.active == True:
            self.spinner_toggle('work_online_import_spin')
        if self.ids.work_online_check.active == True:
            work_path = self.manager.get_screen("home").ids.work_file.text
            if work_path == '':
                work_path = 'work.xlsx'
            part_url = 'work'
            spin_name = 'work_online_import_spin'
            file_name = 'work.xlxs'
            threading.Thread(target=self.upload_file,
                             kwargs={'path': work_path, 'part_url': part_url, 'spin': spin_name,
                                     'file_name': file_name}).start()


    def import_online(self):
        app = MDApp.get_running_app()

        if self.ids.nomenclature_online_check.active == True:
            clients_path = self.manager.get_screen("home").ids.nomenclature_file.text
            self.upload_file(clients_path, 'nomenclatures')

        if self.ids.nomenclature_online_check.active == True:
            clients_path = self.manager.get_screen("home").ids.work_file.text
            self.upload_file(clients_path, 'commonWorks')


    def upload_file(self, path, part_url, spin, file_name):
        upload_url = 'https://online.autodealer.ru/api/back/files'
        filepath = path
        path = Path(filepath)
        total_size = path.stat().st_size
        filename = path.name
        fields = {
            "files": file_name,
        }


        with tqdm(
            desc=filename,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            with open(filepath, "rb") as f:
                fields["files"] = (file_name, f)
                e = MultipartEncoder(fields=fields)
                m = MultipartEncoderMonitor(
                    e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
                )
                app = MDApp.get_running_app()
                r = app.session
                headers = r.headers
                old_headers = r.headers
                headers["Content-Type"] = str(m.content_type)
                headers['Content-Length'] = str(total_size)
                answer = r.post(upload_url, data=m, headers=headers)
                print(answer)
                print(answer.content)
                print(json.loads(answer.content))
                print('sdfsf')
                id = json.loads(answer.text)[0]['id']
                print(id)

        r = app.session
        r.headers = {}
        url = 'https://online.autodealer.ru/api/' + part_url + '/import/check/' + str(id)
        answer = r.get(url)
        print(answer.text)
        try:
            if json.loads(answer.text)['errorRowCount'] == 0:
                url = 'https://online.autodealer.ru/api/' + part_url + '/import/process/' + str(id)
                answer = r.post(url)
                print(answer.text)
            else:
                print('ne zbs')
        except Exception as e:
            print(e)
            self.show_error_dialog(e)

        self.spinner_toggle(spin)

    @mainthread
    def show_error_dialog(self, text_error):
        if not self.dialog:
            self.dialog = MDDialog(
                text='[color=ff0000]' + str(text_error) + '[/color]',
            )
        self.dialog.open()


    @mainthread
    def spinner_toggle(self, name):
        if self.ids[name].active == False:
            self.ids[name].active = True
        else:
            self.ids[name].active = False

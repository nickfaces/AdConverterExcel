import threading
import json
import requests
from kivy.clock import mainthread, Clock
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from requests.auth import HTTPBasicAuth


class AccountScreen(Screen):


    @mainthread
    def spinner_toggle(self):
        if self.ids.auth_spin.active == False:
            self.ids.auth_spin.active = True
        else:
            self.ids.auth_spin.active = False

    def auth_thread(self):
        self.spinner_toggle()
        threading.Thread(target=(self.auth)).start()

    def auth(self):
        Clock.schedule_interval(lambda dt: self.spinner_toggle, 1)
        r = requests.Session()
        url = 'https://online.autodealer.ru/api/simple/auth'
        headers = {'Content-type': 'application/json',  # Определение типа данных
                   'Accept': '*/*',
                   'Content-Encoding': 'utf-8'}
        try:

            listitem = r.get(url, auth=HTTPBasicAuth(self.ids.login.text, self.ids.password.text))
            # app = App.get_running_app()
            # app.cookies = listitem.cookies
            i = 0
            if listitem.status_code == 204:
                i = 0
            elif listitem.status_code == 401:
                i = 3
            elif listitem.status_code == 400:
                i = 1
            else:
                i = 2
        except:
            i = 2
        if i == 0:
            url = 'https://online.autodealer.ru/api/tenantUsers/current'
            current = r.get(url)
            print(current.status_code)
            current_json = json.loads(current.text)
            app = MDApp.get_running_app()
            app.owner = current_json['owner']
            app.session = r
        print(i)
        self.spinner_toggle()
        self.success_icon(i)

    @mainthread
    def success_icon(self, status):
        layout = self.ids.screen_layout
        if status == 0:
            icon = "check-circle"
            text_color = 'green'
        else:
            icon = "cancel"
            text_color = 'red'
        self.ids.status.icon = icon
        self.ids.status.text_color = text_color
        self.ids.status.opacity = 1

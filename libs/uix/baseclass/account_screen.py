import threading
import json
import time

import requests
from kivy.clock import mainthread, Clock
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from requests.auth import HTTPBasicAuth


class AccountScreen(MDScreen):


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
            current_json = json.loads(current.text)
            app = MDApp.get_running_app()
            if current.status_code == 400:
                i = 1
                app.owner = False
                app.NomenclatureAttributesItemD = []
                app.ContragentAttributesItemD = []
                self.snackbar_status('400: Bad request')
            else:
                app.owner = current_json['owner']
                app.session = r
                self.get_attributes()
        self.spinner_toggle()
        self.success_icon(i)

    @mainthread
    def success_icon(self, status):
        layout = self.ids.screen_layout
        if status == 0:
            app = MDApp.get_running_app()
            if app.owner == True:
                icon = 'crown'
                text_color = 'gold'
                snackbar_text = 'Вы вошли с правами владельца'
            else:
                icon = "check-circle"
                text_color = 'green'
                snackbar_text = 'Вы вошли с правами обычного пользователя. Импорт файлов недоступен.'
        else:
            icon = "cancel"
            text_color = 'red'
            snackbar_text = 'Ошибка авторизации. Попробуйте еще раз.'
        self.ids.status.icon = icon
        self.ids.status.text_color = text_color
        self.ids.status.opacity = 1
        self.snackbar_status(snackbar_text)

    @mainthread
    def snackbar_status(self, snackbar_text):
        snackbar = Snackbar(
            text=snackbar_text,
        )
        snackbar.open()


    def get_attributes(self):
        url = 'https://online.autodealer.ru/api/contragents/attributesSettings'
        app = MDApp.get_running_app()
        session = app.session
        attributes_get = session.get(url=url)
        attributes = json.loads(attributes_get.text)
        attribute_list = []
        for attribute in attributes:
            if attribute['freeInput'] == True:
                attribute_list.append({'label_text': 'Атрибут: ' + str(attribute['name']), 'label_text_color': 'black',
                                       'dropdown_item_id': 'attribute_client' + str(attribute['id']), 'textfield_id': 'attribute_client_' + str(attribute['id']) + '_value'})

        app.ContragentAttributesItemD = attribute_list

        url = 'https://online.autodealer.ru/api/nomenclatures/attributesSettings'
        attributes_get = session.get(url=url)
        attributes = json.loads(attributes_get.text)
        attribute_list = []
        for attribute in attributes:
            if attribute['freeInput'] == True:
                attribute_list.append({'label_text': 'Атрибут: ' + str(attribute['name']), 'label_text_color': 'black',
                                       'dropdown_item_id': 'attribute_nomenclature' + str(attribute['id']), 'textfield_id': 'attribute_nomenclature_' + str(attribute['id']) + '_value'})
        app.NomenclatureAttributesItemD = attribute_list

        url = 'https://online.autodealer.ru/api/nomenclaturePriceColumns/'
        prices_get = session.get(url=url)
        prices = json.loads(prices_get.text)
        prices_list = []
        for price in prices:
            if price['active'] == True:
                prices_list.append({'label_text': str(price['fullName']), 'label_text_color': 'black',
                                       'dropdown_item_id': 'price_' + str(price['id']), 'textfield_id': 'price_' + str(price['id']) + '_value'})
        app.PricesItemD = prices_list

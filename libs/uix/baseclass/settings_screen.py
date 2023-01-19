import threading
from kivymd.app import MDApp
from kivy.clock import mainthread, Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
import pandas as pd
from kivy.properties import StringProperty, NumericProperty
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import time

class SettingsScreen(Screen):

    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.goback()
    dialog = None
    progress = StringProperty('')
    progress_value = NumericProperty(0)

    def drop(self, name):
        current_path = self.manager.get_screen("home").ids.input_file.text
        input_file = pd.read_excel(current_path)
        out = input_file.columns.values.tolist()
        items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.menu_callback(x, name)
            }
            for i in out
        ]
        caller = self.ids[name]
        self.menu = MDDropdownMenu(
            caller= caller,
            items=items,
            position="center",
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, text_item, name):
        self.menu.dismiss()
        self.ids[name].text = text_item


    def set_current_item_label(self, i):
        app = MDApp.get_running_app()
        amount_items = app.amount_items
        progress_proc = ((i + 1) / amount_items) * 100
        self.progress = 'Обрабатывается ' + str(i+1) + ' из ' + str(amount_items) + ' (' + str(round(progress_proc)) + \
                        '%)'
        self.progress_value = progress_proc
    def import_file(self):
        start = time.time()
        current_path = self.manager.get_screen("home").ids.input_file.text
        input_file = pd.read_excel(current_path)
        kol = len(input_file.index)
        start_dataframe = pd.read_excel(r'empty.xlsx')
        df3 = pd.DataFrame()
        for i, row in input_file.iterrows():
            Clock.schedule_interval(lambda dt: self.set_current_item_label(i), 1)

            if self.ids.clients_type_value.text != '':
                clients_type = self.ids.clients_type_value.text
            else:
                if self.ids.clients_type.text != '':
                    clients_type = input_file.iloc[i][self.ids.clients_type.text]
                else:
                    clients_type = ''

            if self.ids.full_name_value.text != '':
                full_name = self.ids.full_name_value.text
            else:
                if self.ids.full_name.text != '':
                    full_name = input_file.iloc[i][self.ids.full_name.text]
                else:
                    full_name = ''

            if self.ids.short_name_value.text != '':
                short_name = self.ids.short_name_value.text
            else:
                if self.ids.short_name.text != '':
                    short_name = input_file.iloc[i][self.ids.short_name.text]
                else:
                    short_name = ''

            if self.ids.inn_value.text != '':
                inn = self.ids.inn_value.text
            else:
                if self.ids.inn.text != '':
                    inn = input_file.iloc[i][self.ids.inn.text]
                else:
                    inn = ''

            if self.ids.kpp_value.text != '':
                kpp = self.ids.kpp_value.text
            else:
                if self.ids.kpp.text != '':
                    kpp = input_file.iloc[i][self.ids.kpp.text]
                else:
                    kpp = ''

            if self.ids.ogrn_value.text != '':
                ogrn = self.ids.ogrn_value.text
            else:
                if self.ids.ogrn.text != '':
                    ogrn = input_file.iloc[i][self.ids.ogrn.text]
                else:
                    ogrn = ''

            if self.ids.number_ip_value.text != '':
                number_ip = self.ids.number_ip_value.text
            else:
                if self.ids.number_ip.text != '':
                    number_ip = input_file.iloc[i][self.ids.number_ip.text]
                else:
                    number_ip = ''

            if self.ids.date_ip_value.text != '':
                date_ip = self.ids.date_ip_value.text
            else:
                if self.ids.number_ip.text != '':
                    date_ip = input_file.iloc[i][self.ids.date_ip.text]
                else:
                    date_ip = ''

            if self.ids.folder_value.text != '':
                folder = self.ids.folder_value.text
            else:
                if self.ids.number_ip.text != '':
                    folder = input_file.iloc[i][self.ids.folder.text]
                else:
                    folder = ''

            if self.ids.folder_value.text != '':
                folder = self.ids.folder_value.text
            else:
                if self.ids.number_ip.text != '':
                    folder = input_file.iloc[i][self.ids.folder.text]
                else:
                    folder = ''

            if self.ids.comment_value.text != '':
                comment = self.ids.comment_value.text
            else:
                if self.ids.comment.text != '':
                    comment = input_file.iloc[i][self.ids.comment.text]
                else:
                    comment = ''

            if self.ids.legal_address_value.text != '':
                legal_address = self.ids.legal_address_value.text
            else:
                if self.ids.legal_address.text != '':
                    legal_address = input_file.iloc[i][self.ids.legal_address.text]
                else:
                    legal_address = ''

            if self.ids.fact_address_value.text != '':
                fact_address = self.ids.fact_address_value.text
            else:
                if self.ids.fact_address.text != '':
                    fact_address = input_file.iloc[i][self.ids.fact_address.text]
                else:
                    fact_address = ''

            if self.ids.post_address_value.text != '':
                post_address = self.ids.post_address_value.text
            else:
                if self.ids.post_address.text != '':
                    post_address = input_file.iloc[i][self.ids.post_address.text]
                else:
                    post_address = ''


            if i != 0:
                start_dataframe = df3
            else:
                start_dataframe = start_dataframe

            df2 = pd.DataFrame({'Полное наименование': full_name, 'Краткое наименование': short_name, 'ИНН': inn,
                                'КПП': kpp, 'Тип клиента': clients_type, 'Примечание': comment, 'ОГРН': ogrn,
                                'Номер свидетельства ИП': number_ip, 'Дата выдачи ИП': date_ip,
                                'Папка': folder, 'Юридический адрес': legal_address,
                                'Фактический адрес': fact_address, 'Почтовый адрес': post_address}, index=[0])

            #df3 = start_dataframe.append(df2)
            df3 = pd.concat([start_dataframe, df2])
        writer = pd.ExcelWriter(r'output.xlsx')
        df3.to_excel(writer, index=False)
        end = time.time() - start
        print('END: ', end)
        writer.save()
        self.show_alert_dialog()


    def import_file_thread(self):
        threading.Thread(target=(self.import_file)).start()

    @mainthread
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Открыть файл?",
                buttons=[
                    MDFlatButton(
                        text="Открыть",
                        on_release=self.open_file
                    ),
                    MDFlatButton(
                        text="Отмена",
                        on_release=self.dialog_close
                    ),
                ],
            )
        self.dialog.open()

    @mainthread
    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def open_file(self, *args):
        import platform
        from subprocess import call
        if platform.system() == 'Windows':
            self.dialog_close()
            call('output.xlsx', shell=True)
        if platform.system() == 'Linux':
            call(['xdg-open', 'output.xlsx'])
            self.dialog_close()

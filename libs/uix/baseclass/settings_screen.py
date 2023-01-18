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
from kivy.properties import StringProperty
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import time

class SettingsScreen(Screen):

    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.goback()
    dialog = None
    progress = StringProperty('')

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

    @mainthread
    def spinner_toggle(self):
        if self.ids.progress_spinner.active == False:
            self.ids.progress_spinner.active = True
        else:
            self.ids.progress_spinner.active = False



    def set_current_item_label(self, i):
        app = MDApp.get_running_app()
        amount_items = app.amount_items
        # self.current_item = str(i)
        self.progress = 'Обрабатывается ' + str(i+1) + ' из ' + str(amount_items)

    def import_file(self):
        start = time.time()
        current_path = self.manager.get_screen("home").ids.input_file.text
        input_file = pd.read_excel(current_path)
        kol = len(input_file.index)
        start_dataframe = pd.read_excel(r'C:\Users\Владимир\Downloads\AdConverterExcel-main\AdConverterExcel-main\empty.xlsx')
        df3 = pd.DataFrame()
        for i, row in input_file.iterrows():
            Clock.schedule_interval(lambda dt: self.set_current_item_label(i), 1)
            clients_type = input_file.iloc[i][self.ids.clients_type.text] if self.ids.clients_type.text != '' else ''
            full_name = input_file.iloc[i][self.ids.full_name.text] if self.ids.full_name.text != '' else ''
            short_name = input_file.iloc[i][self.ids.short_name.text] if self.ids.short_name.text != '' else ''
            inn = input_file.iloc[i][self.ids.inn.text] if self.ids.inn.text != '' else ''
            kpp = input_file.iloc[i][self.ids.kpp.text] if self.ids.kpp.text != '' else ''
            ogrn = input_file.iloc[i][self.ids.ogrn.text] if self.ids.ogrn.text != '' else ''
            number_ip = input_file.iloc[i][self.ids.number_ip.text] if self.ids.number_ip.text != '' else ''
            date_ip = input_file.iloc[i][self.ids.date_ip.text] if self.ids.date_ip.text != '' else ''
            folder = input_file.iloc[i][self.ids.folder.text] if self.ids.folder.text != '' else ''
            comment = input_file.iloc[i][self.ids.comment.text] if self.ids.comment.text != '' else ''
            legal_address = input_file.iloc[i][self.ids.legal_address.text] if self.ids.legal_address.text != '' else ''
            fact_address = input_file.iloc[i][self.ids.fact_address.text] if self.ids.fact_address.text != '' else ''
            post_address = input_file.iloc[i][self.ids.post_address.text] if self.ids.post_address.text != '' else ''

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
        writer = pd.ExcelWriter(r'C:\Users\Владимир\Downloads\AdConverterExcel-main\AdConverterExcel-main\output.xlsx')
        df3.to_excel(writer, index=False)
        end = time.time() - start
        print('END: ', end)
        writer.save()
        self.show_alert_dialog()
        self.spinner_toggle()

    def import_file_thread(self):
        self.spinner_toggle()
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

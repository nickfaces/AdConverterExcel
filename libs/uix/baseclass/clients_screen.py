import threading
from kivymd.app import MDApp
from kivy.clock import mainthread, Clock
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
import pandas as pd
from kivy.properties import StringProperty, NumericProperty, ColorProperty, BooleanProperty
import time

class ClientsScreen(MDScreen):

    dialog = None
    progress = StringProperty('')
    progress_value = NumericProperty(0)
    app = MDApp.get_running_app()
    app.import_button = BooleanProperty(True)


    def __init__(self, **kwargs):
        super(ClientsScreen, self).__init__(**kwargs)
        my_grid = self.ids.my_grid
        ItemListD = [
         {'label_text': 'Тип клиента', 'label_text_color': 'red', 'dropdown_item_id': 'clients_type', 'textfield_id': 'clients_type_value'},
        {'label_text': 'Полное наименование', 'label_text_color': 'red', 'dropdown_item_id': 'full_name', 'textfield_id': 'full_name_value'},
        {'label_text': 'Краткое наименование', 'label_text_color': 'red', 'dropdown_item_id': 'short_name', 'textfield_id': 'short_name_value'},
        {'label_text': 'ИНН', 'label_text_color': 'black', 'dropdown_item_id': 'inn', 'textfield_id': 'inn_value'},
        {'label_text': 'КПП', 'label_text_color': 'black', 'dropdown_item_id': 'kpp', 'textfield_id': 'kpp_value'},
        {'label_text': 'ОГРН', 'label_text_color': 'black', 'dropdown_item_id': 'ogrn', 'textfield_id': 'ogrn_value'},
        {'label_text': 'Номер свидетельства ИП', 'label_text_color': 'black', 'dropdown_item_id': 'number_ip', 'textfield_id': 'number_ip_value'},
        {'label_text': 'Дата выдачи ИП', 'label_text_color': 'black', 'dropdown_item_id': 'date_ip', 'textfield_id': 'date_ip_value'},
        {'label_text': 'Папка', 'label_text_color': 'black', 'dropdown_item_id': 'folder', 'textfield_id': 'folder_value'},
        {'label_text': 'Примечание', 'label_text_color': 'black', 'dropdown_item_id': 'comment', 'textfield_id': 'comment_value'},
        {'label_text': 'Юридический адрес', 'label_text_color': 'black', 'dropdown_item_id': 'legal_address', 'textfield_id': 'legal_address_value'},
        {'label_text': 'Фактический адрес', 'label_text_color': 'black', 'dropdown_item_id': 'fact_address', 'textfield_id': 'fact_address_value'},
        {'label_text': 'Почтовый адрес', 'label_text_color': 'black', 'dropdown_item_id': 'post_address', 'textfield_id': 'post_address_value'},
        {'label_text': 'Категория цены на товары', 'label_text_color': 'black', 'dropdown_item_id': 'price_category', 'textfield_id': 'price_category_value'},
        {'label_text': 'Скидка на товары', 'label_text_color': 'black', 'dropdown_item_id': 'legal_address', 'textfield_id': 'legal_address_value'},
        {'label_text': 'Стоимость нормочаса', 'label_text_color': 'black', 'dropdown_item_id': 'fact_address', 'textfield_id': 'fact_address_value'},
        {'label_text': 'Скидка на работы', 'label_text_color': 'black', 'dropdown_item_id': 'post_address', 'textfield_id': 'post_address_value'}
        ]
        app = MDApp.get_running_app()
        app.contact_count = 1

        ContactListD = [
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Фамилия', 'label_text_color': 'black', 'dropdown_item_id': 'last_name', 'textfield_id': 'last_name_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Имя', 'label_text_color': 'black', 'dropdown_item_id': 'first_name', 'textfield_id': 'first_name_value'},
        {'label_text': 'Контактная персонах' + str(app.contact_count) +'].Отчество', 'label_text_color': 'black', 'dropdown_item_id': 'middle_name', 'textfield_id': 'middle_name_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Дата рождения', 'label_text_color': 'black', 'dropdown_item_id': 'birthday', 'textfield_id': 'birthday_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Пол', 'label_text_color': 'black', 'dropdown_item_id': 'gender', 'textfield_id': 'gender_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Контакты[1].Тип', 'label_text_color': 'black', 'dropdown_item_id': 'type', 'textfield_id': 'type_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Контакты[1].Значение', 'label_text_color': 'black', 'dropdown_item_id': 'contact_value', 'textfield_id': 'contact_value_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Контакты[1].Примечание', 'label_text_color': 'black', 'dropdown_item_id': 'contact_comment', 'textfield_id': 'contact_comment_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Контакты[1].Рассылка', 'label_text_color': 'black', 'dropdown_item_id': 'mailing', 'textfield_id': 'mailing_value'}]
        
        app.auto_count = 1

        AutoListD = [
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Марка', 'label_text_color': 'black', 'dropdown_item_id': 'mark', 'textfield_id': 'mark_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Модель', 'label_text_color': 'black', 'dropdown_item_id': 'model', 'textfield_id': 'model_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].VIN', 'label_text_color': 'black', 'dropdown_item_id': 'vin', 'textfield_id': 'vin_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Госномер', 'label_text_color': 'black', 'dropdown_item_id': 'number', 'textfield_id': 'number_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Год выпуска', 'label_text_color': 'black', 'dropdown_item_id': 'year', 'textfield_id': 'year_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Цвет', 'label_text_color': 'black', 'dropdown_item_id': 'color', 'textfield_id': 'color_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Примечание', 'label_text_color': 'black', 'dropdown_item_id': 'auto_comment', 'textfield_id': 'auto_comment_value'}]

        app.bank_count = 1

        BankListD = [
        {'label_text': 'Банковский счет[' + str(app.bank_count) +'].БИК', 'label_text_color': 'black', 'dropdown_item_id': 'bik', 'textfield_id': 'bik_value'},
        {'label_text': 'Банковский счет[' + str(app.bank_count) +'].Расчётный счёт', 'label_text_color': 'black', 'dropdown_item_id': 'bank_account', 'textfield_id': 'bank_account_value'},
        {'label_text': 'Банковский счет[' + str(app.bank_count) +'].Примечание', 'label_text_color': 'black', 'dropdown_item_id': 'bank_comment', 'textfield_id': 'bank_comment_value'}]



        app = MDApp.get_running_app()
        app.ItemListD = ItemListD
        app.ContactListD = ContactListD
        app.AutoListD = AutoListD
        app.BankListD = BankListD

        # for i in range(2):
        for i in range(len(ItemListD + ContactListD + AutoListD + BankListD)):
            item_list = ItemListD + ContactListD + AutoListD + BankListD
            item = item_list[i]
            my_vid = MyWidget()
            my_vid.label_text = item['label_text']
            my_vid.label_text_color = item['label_text_color']
            my_vid.dropdown_item_id = item['dropdown_item_id']
            my_vid.textfield_id = item['textfield_id']
            my_grid.add_widget(my_vid)

    def add_auto(self):
        app = MDApp.get_running_app()
        app.auto_count = app.auto_count + 1
        AutoListD = [
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Марка', 'label_text_color': 'black', 'dropdown_item_id': 'mark', 'textfield_id': 'mark_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Модель', 'label_text_color': 'black', 'dropdown_item_id': 'model', 'textfield_id': 'model_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].VIN', 'label_text_color': 'black', 'dropdown_item_id': 'vin', 'textfield_id': 'vin_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Госномер', 'label_text_color': 'black', 'dropdown_item_id': 'number', 'textfield_id': 'number_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Год выпуска', 'label_text_color': 'black', 'dropdown_item_id': 'year', 'textfield_id': 'year_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Цвет', 'label_text_color': 'black', 'dropdown_item_id': 'color', 'textfield_id': 'color_value'},
        {'label_text': 'Автомобиль[' + str(app.auto_count) +'].Примечание', 'label_text_color': 'black', 'dropdown_item_id': 'auto_comment', 'textfield_id': 'auto_comment_value'}]
        
        for i in range(len(AutoListD)):
            item_list = AutoListD
            item = item_list[i]
            my_vid = MyWidget()
            my_vid.label_text = item['label_text']
            my_vid.label_text_color = item['label_text_color']
            my_vid.dropdown_item_id = item['dropdown_item_id']
            my_vid.textfield_id = item['textfield_id']
            my_grid = self.ids.my_grid
            my_grid.add_widget(my_vid)

    def add_contact(self):
        app = MDApp.get_running_app()
        app.contact_count = app.contact_count + 1
        ContactListD = [
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Фамилия', 'label_text_color': 'black', 'dropdown_item_id': 'last_name', 'textfield_id': 'last_name_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Имя', 'label_text_color': 'black', 'dropdown_item_id': 'first_name', 'textfield_id': 'first_name_value'},
        {'label_text': 'Контактная персонах' + str(app.contact_count) +'].Отчество', 'label_text_color': 'black', 'dropdown_item_id': 'middle_name', 'textfield_id': 'middle_name_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Дата рождения', 'label_text_color': 'black', 'dropdown_item_id': 'birthday', 'textfield_id': 'birthday_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Пол', 'label_text_color': 'black', 'dropdown_item_id': 'gender', 'textfield_id': 'gender_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Контакты[1].Тип', 'label_text_color': 'black', 'dropdown_item_id': 'type', 'textfield_id': 'type_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Контакты[1].Значение', 'label_text_color': 'black', 'dropdown_item_id': 'contact_value', 'textfield_id': 'contact_value_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Контакты[1].Примечание', 'label_text_color': 'black', 'dropdown_item_id': 'contact_comment', 'textfield_id': 'contact_comment_value'},
        {'label_text': 'Контактная персона[' + str(app.contact_count) +'].Контакты[1].Рассылка', 'label_text_color': 'black', 'dropdown_item_id': 'mailing', 'textfield_id': 'mailing_value'}]
        for i in range(len(ContactListD)):
            item_list = ContactListD
            item = item_list[i]
            my_vid = MyWidget()
            my_vid.label_text = item['label_text']
            my_vid.label_text_color = item['label_text_color']
            my_vid.dropdown_item_id = item['dropdown_item_id']
            my_vid.textfield_id = item['textfield_id']
            my_grid = self.ids.my_grid
            my_grid.add_widget(my_vid)

    def add_bank(self):
        app = MDApp.get_running_app()
        app.bank_count = app.bank_count + 1
        BankListD = [
        {'label_text': 'Банковский счет[' + str(app.bank_count) +'].БИК', 'label_text_color': 'black', 'dropdown_item_id': 'bik', 'textfield_id': 'bik_value'},
        {'label_text': 'Банковский счет[' + str(app.bank_count) +'].Расчётный счёт', 'label_text_color': 'black', 'dropdown_item_id': 'bank_account', 'textfield_id': 'bank_account_value'},
        {'label_text': 'Банковский счет[' + str(app.bank_count) +'].Примечание', 'label_text_color': 'black', 'dropdown_item_id': 'bank_comment', 'textfield_id': 'bank_comment_value'}]
        for i in range(len(BankListD)):
            item_list = BankListD
            item = item_list[i]
            my_vid = MyWidget()
            my_vid.label_text = item['label_text']
            my_vid.label_text_color = item['label_text_color']
            my_vid.dropdown_item_id = item['dropdown_item_id']
            my_vid.textfield_id = item['textfield_id']
            my_grid = self.ids.my_grid
            my_grid.add_widget(my_vid)



    def menu_callback(self, text_item, name):
        self.menu.dismiss()
        self.ids[name].text = text_item
        self.check_minimal_value()

    def set_current_item_label(self, i):
        app = MDApp.get_running_app()
        amount_items = app.amount_items
        progress_proc = ((i + 1) / amount_items) * 100
        self.progress = 'Обрабатывается ' + str(i+1) + ' из ' + str(amount_items) + ' (' + str(round(progress_proc)) + \
                        '%)'
        self.progress_value = progress_proc

    def import_file(self):
        start = time.time()
        current_path = self.manager.get_screen("home").ids.clients_file.text
        clients_file = pd.read_excel(current_path)
        kol = len(clients_file.index)
        df3 = pd.DataFrame()

        pol = self.ids.my_grid.children

        plo_out = []
        for p in pol:
            plo_out.append({'label': p.ids.label_id.text, 'dropdown_item': p.ids.dropdown_item_id.text,
                            'textfield': p.ids.textfield_id.text})

        for pl in plo_out:
            try:
                if pl['dropdown_item'] != '' and pl['textfield'] == '':
                    df3[pl['label']] = clients_file[pl['dropdown_item']]
            except Exception as e:
                print(e)

        for pl in plo_out:
            try:
                if pl['textfield'] != '':
                    df4 = pd.DataFrame({pl['label']: pl['textfield']}, index=range(0, kol))
                    df3[pl['label']] = df4
                    print(df3)
            except Exception as e:
                print(e)


        print(df3)



        for i, row in clients_file.iterrows():
            Clock.schedule_interval(lambda dt: self.set_current_item_label(i), 1)


        writer = pd.ExcelWriter(r'output.xlsx')
        df3.to_excel(writer, index=False)
        end = time.time() - start
        writer.save()
        print('END: ', end)
        self.show_alert_dialog()
        self.add_next_button()


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

    @mainthread
    def add_next_button(self):
        btn = MDRaisedButton(
            text="Далее",
            size_hint=(.1, .7),
            pos_hint={'center_x': .9, 'center_y': .5},
        )
        layout = self.ids.float
        layout.add_widget(btn)


class MyWidget(MDCard):
    label_text = StringProperty()
    label_text_color = ColorProperty()
    dropdown_item_id = StringProperty()
    textfield_id = StringProperty()

    def drop(self, name):
        app = MDApp.get_running_app()
        clients_file = app.clients_file
        out = clients_file.columns.values.tolist()
        items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.menu_callback(x, name)
            }
            for i in out
        ]
        caller = self.ids.dropdown_item_id
        self.menu = MDDropdownMenu(
            caller= caller,
            items=items,
            position="center",
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, text_item, name):
        self.menu.dismiss()
        self.ids.dropdown_item_id.text = text_item
        self.check_minimal_value()

    @mainthread
    def check_minimal_value(self):
        app = MDApp.get_running_app()
        ItemListD = app.ItemListD
        ContactListD = app.ContactListD
        AutoListD = app.AutoListD
        BankListD = app.BankListD
        for i in range(len(ItemListD + ContactListD + AutoListD + BankListD)):
            item_list = ItemListD + ContactListD + AutoListD + BankListD
            item = item_list[i]
            if (item['label_text'] == 'Тип клиента' and (item['dropdown_item_id'] == '' or item['textfield_id'] == '')):
                app.import_button = False
            else:
                True


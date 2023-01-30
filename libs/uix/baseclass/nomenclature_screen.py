import os
import threading
from kivymd.app import MDApp
from kivy.clock import mainthread
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
import pandas as pd
from kivy.properties import StringProperty, NumericProperty, ColorProperty, BooleanProperty


class NomenclatureScreen(MDScreen):
    dialog = None
    progress = StringProperty('')
    progress_value = NumericProperty(0)
    app = MDApp.get_running_app()
    app.import_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(NomenclatureScreen, self).__init__(**kwargs)
        my_nomeclature_grid = self.ids.my_nomeclature_grid
        ItemListD = [
            {'label_text': 'Наименование', 'label_text_color': 'red', 'dropdown_item_id': 'detail_name',
             'textfield_id': 'detail_name_value'},
            {'label_text': 'Наименование в чеке', 'label_text_color': 'red', 'dropdown_item_id': 'detail_name_fiscal',
             'textfield_id': 'detail_name_fiscal_value'},
            {'label_text': 'Группа', 'label_text_color': 'black', 'dropdown_item_id': 'detail_group',
             'textfield_id': 'detail_group_value'},
            {'label_text': 'Метка', 'label_text_color': 'black', 'dropdown_item_id': 'detail_label', 'textfield_id': 'detail_label_value'},
            {'label_text': 'Примечание', 'label_text_color': 'black', 'dropdown_item_id': 'detail_comment', 'textfield_id': 'detail_comment_value'},
            {'label_text': 'Единица измерения', 'label_text_color': 'red', 'dropdown_item_id': 'unit',
             'textfield_id': 'unit_value'},
            {'label_text': 'Категория', 'label_text_color': 'black', 'dropdown_item_id': 'detail_category',
             'textfield_id': 'detail_category_value'},
            {'label_text': 'Страна', 'label_text_color': 'black', 'dropdown_item_id': 'country',
             'textfield_id': 'country_value'},
            {'label_text': 'Производитель', 'label_text_color': 'black', 'dropdown_item_id': 'manufacturer',
             'textfield_id': 'manufacturer_value'},
            {'label_text': 'Приход', 'label_text_color': 'black', 'dropdown_item_id': 'consumption',
             'textfield_id': 'consumption_value'},
            {'label_text': 'Расход', 'label_text_color': 'black', 'dropdown_item_id': 'consumption',
             'textfield_id': 'consumption_value'},
            {'label_text': 'Минимальный остаток', 'label_text_color': 'black', 'dropdown_item_id': 'minimum_balance',
             'textfield_id': 'minimum_balance_value'},
            {'label_text': 'Оригинальный номер', 'label_text_color': 'black', 'dropdown_item_id': 'original_number',
             'textfield_id': 'original_number_value'},
            {'label_text': 'Штрихкод', 'label_text_color': 'black',
             'dropdown_item_id': 'detail_barcode', 'textfield_id': 'detail_barcode_value'},
            {'label_text': 'Номер производителя', 'label_text_color': 'black', 'dropdown_item_id': 'manufacturer_number',
             'textfield_id': 'manufacturer_number_value'},
            {'label_text': 'Код номенклатуры', 'label_text_color': 'black', 'dropdown_item_id': 'nomenclature_code',
             'textfield_id': 'nomenclature_code_value'},
            {'label_text': 'Цена прихода', 'label_text_color': 'black', 'dropdown_item_id': 'incoming_price',
             'textfield_id': 'incoming_price_value'},
            {'label_text': 'Максимальная скидка %', 'label_text_color': 'black', 'dropdown_item_id': 'max_discount_detail',
             'textfield_id': 'max_discount_detail_value'},
            {'label_text': 'Количество', 'label_text_color': 'black', 'dropdown_item_id': 'amount',
             'textfield_id': 'amount_value'},
            {'label_text': 'Склад', 'label_text_color': 'black', 'dropdown_item_id': 'stock',
             'textfield_id': 'stock_value'}
        ]

        # for i in range(2):
        app = MDApp.get_running_app()

        try:
            check_attr = app.NomenclatureAttributesItemD
            app.NomenclatureAttributesItemD = check_attr
        except:
            app.NomenclatureAttributesItemD = []
        try:
            check_prices = app.PricesItemD
            app.PricesItemD = check_prices
        except:
            app.PricesItemD = []
        for i in range(len(ItemListD + app.NomenclatureAttributesItemD + app.PricesItemD)):
            item_list = ItemListD + app.NomenclatureAttributesItemD + app.PricesItemD
            item = item_list[i]
            my_vid = NomenclatureItem()
            my_vid.label_text = item['label_text']
            my_vid.label_text_color = item['label_text_color']
            my_vid.dropdown_item_id = item['dropdown_item_id']
            my_vid.textfield_id = item['textfield_id']
            my_nomeclature_grid.add_widget(my_vid)



    def menu_callback(self, text_item, name):
        self.menu.dismiss()
        self.ids[name].text = text_item


    def set_current_item_label(self, i):
        app = MDApp.get_running_app()
        amount_items = app.amount_items
        progress_proc = ((i + 1) / amount_items) * 100
        self.progress = 'Обрабатывается ' + str(i + 1) + ' из ' + str(amount_items) + ' (' + str(round(progress_proc)) + \
                        '%)'
        self.progress_value = progress_proc

    def check_choices(self):
        flag = 0
        for child in self.ids.my_nomeclature_grid.children:
            if (child.ids.label_id.text == 'Наименование' and (child.ids.dropdown_item_id.text == '' and child.ids.textfield_id.text == '')) or \
                    (child.ids.label_id.text == 'Наименование в чеке' and (child.ids.dropdown_item_id.text == '' and child.ids.textfield_id.text == '')) or \
                    (child.ids.label_id.text == 'Единица измерения' and (child.ids.dropdown_item_id.text == '' and child.ids.textfield_id.text == '')):
                flag = 1
        if flag == 1:
            self.show_nocheck_dialog()
        else:
            self.import_file_thread()

    @mainthread
    def show_nocheck_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="[color=ff0000]Укажите обязательные данные (выделены красным)[/color]",
            )
        self.dialog.open()


    def import_file(self):
        current_path = self.manager.get_screen("home").ids.nomenclature_file.text
        nomenclature_file = pd.read_excel(current_path)
        kol = len(nomenclature_file.index)
        df3 = pd.DataFrame()

        pol = self.ids.my_nomeclature_grid.children

        plo_out = []
        for p in pol:
            plo_out.append({'label': p.ids.label_id.text, 'dropdown_item': p.ids.dropdown_item_id.text,
                            'textfield': p.ids.textfield_id.text})

        for pl in plo_out:
            try:
                if pl['dropdown_item'] != '' and pl['textfield'] == '':
                    df3[pl['label']] = nomenclature_file[pl['dropdown_item']]
            except Exception as e:
                print(e)

        for pl in plo_out:
            try:
                if pl['textfield'] != '':
                    df4 = pd.DataFrame({pl['label']: pl['textfield']}, index=range(0, kol))
                    df3[pl['label']] = df4
            except Exception as e:
                print(e)


        app = MDApp.get_running_app()
        path = app.path
        os.chdir(path)
        writer = pd.ExcelWriter(r'nomenclature.xlsx')
        df3.to_excel(writer, index=False)
        writer.save()
        self.spinner_toggle()
        self.show_alert_dialog()
        self.add_next_button()

    def import_file_thread(self):
        self.spinner_toggle()
        threading.Thread(target=(self.import_file)).start()

    @mainthread
    def show_alert_dialog(self):
        app = MDApp.get_running_app()
        self.dialog = MDDialog(
            text="Открыть файл?",
            buttons=[
                MDFlatButton(
                    text="Открыть",
                    theme_text_color="Custom",
                    text_color=app.theme_cls.primary_color,
                    on_release=self.open_file
                ),
                MDFlatButton(
                    text="Отмена",
                    theme_text_color="Custom",
                    text_color=app.theme_cls.primary_color,
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
            call('nomenclature.xlsx', shell=True)
        if platform.system() == 'Linux':
            call(['xdg-open', 'nomenclature.xlsx'])
            self.dialog_close()

    @mainthread
    def add_next_button(self):
        btn = MDRaisedButton(
            text="Далее",
            size_hint=(.1, .7),
            pos_hint={'center_x': .9, 'center_y': .5},
        )
        btn.bind(on_release=self.goto_import_screen)
        layout = self.ids.float
        layout.add_widget(btn)

    def goto_import_screen(self, arg):
        app = MDApp.get_running_app()
        screen_list = app.screen_list
        app.current_screen = app.current_screen + 1
        if ((app.current_screen) < len(screen_list)):
            self.manager.set_current(screen_list[app.current_screen])
        else:
            self.manager.set_current('online_import')


    @mainthread
    def spinner_toggle(self):
        if self.ids.nomenclature_adapt_spin.active == False:
            self.ids.nomenclature_adapt_spin.active = True
        else:
            self.ids.nomenclature_adapt_spin.active = False

class NomenclatureItem(MDCard):
    label_text = StringProperty()
    label_text_color = ColorProperty()
    dropdown_item_id = StringProperty()
    textfield_id = StringProperty()

    def drop(self, name):
        app = MDApp.get_running_app()
        nomenclature_file = app.nomenclature_file
        out = nomenclature_file.columns.values.tolist()
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
            caller=caller,
            items=items,
            position="center",
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, text_item, name):
        self.menu.dismiss()
        self.ids.dropdown_item_id.text = text_item




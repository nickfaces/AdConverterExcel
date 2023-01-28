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
import os

class WorkScreen(MDScreen):
    dialog = None
    progress = StringProperty('')
    progress_value = NumericProperty(0)
    app = MDApp.get_running_app()
    app.import_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(WorkScreen, self).__init__(**kwargs)
        my_grid = self.ids.my_grid
        ItemListD = [
            {'label_text': 'Наименование', 'label_text_color': 'red', 'dropdown_item_id': 'name',
             'textfield_id': 'name_value'},
            {'label_text': 'Код работы', 'label_text_color': 'black', 'dropdown_item_id': 'code',
             'textfield_id': 'code_value'},
            {'label_text': 'Категория', 'label_text_color': 'black', 'dropdown_item_id': 'category',
             'textfield_id': 'category_value'},
            {'label_text': 'Штрихкод', 'label_text_color': 'black', 'dropdown_item_id': 'barcode', 'textfield_id': 'barcode_value'},
            {'label_text': 'Группа', 'label_text_color': 'black', 'dropdown_item_id': 'group', 'textfield_id': 'group_value'},
            {'label_text': 'Исполнитель', 'label_text_color': 'black', 'dropdown_item_id': 'worker',
             'textfield_id': 'worker_value'},
            {'label_text': 'Фиксированная стоимость', 'label_text_color': 'black', 'dropdown_item_id': 'fix_price',
             'textfield_id': 'fix_price_value'},
            {'label_text': 'Стоимость нормочаса', 'label_text_color': 'black', 'dropdown_item_id': 'rt_price',
             'textfield_id': 'rt_price_value'},
            {'label_text': 'Норма времени', 'label_text_color': 'black', 'dropdown_item_id': 'rt_time',
             'textfield_id': 'rt_time_value'},
            {'label_text': 'Коэффициент', 'label_text_color': 'black', 'dropdown_item_id': 'coefficient',
             'textfield_id': 'coefficient_value'},
            {'label_text': 'Кратность', 'label_text_color': 'black', 'dropdown_item_id': 'multiplicity',
             'textfield_id': 'multiplicity_value'},
            {'label_text': 'Максимальная скидка', 'label_text_color': 'black', 'dropdown_item_id': 'max_discount',
             'textfield_id': 'max_discount_value'},
            {'label_text': 'Метка', 'label_text_color': 'black', 'dropdown_item_id': 'label',
             'textfield_id': 'label_value'},
            {'label_text': 'Примечание', 'label_text_color': 'black',
             'dropdown_item_id': 'comment', 'textfield_id': 'comment_value'}
        ]
        app = MDApp.get_running_app()
        app.ItemListD = ItemListD

        # for i in range(2):
        for i in range(len(ItemListD)):
            item_list = ItemListD
            item = item_list[i]
            my_vid = WorkItem()
            my_vid.label_text = item['label_text']
            my_vid.label_text_color = item['label_text_color']
            my_vid.dropdown_item_id = item['dropdown_item_id']
            my_vid.textfield_id = item['textfield_id']
            my_grid.add_widget(my_vid)



    def menu_callback(self, text_item, name):
        self.menu.dismiss()
        self.ids[name].text = text_item


    def set_current_item_label(self, i):
        app = MDApp.get_running_app()
        amount_items = app.amount_items
        progress_proc = ((i + 1) / amount_items) * 100
        self.progress_value = progress_proc

    def check_choices(self):
        flag = 0
        for child in self.ids.my_grid.children:
            if (child.ids.label_id.text == 'Наименование' and (child.ids.dropdown_item_id.text == '' and child.ids.textfield_id.text == '')):
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
        current_path = self.manager.get_screen("home").ids.work_file.text
        work_file = pd.read_excel(current_path)
        kol = len(work_file.index)
        df3 = pd.DataFrame()

        pol = self.ids.my_grid.children

        plo_out = []
        for p in pol:
            plo_out.append({'label': p.ids.label_id.text, 'dropdown_item': p.ids.dropdown_item_id.text,
                            'textfield': p.ids.textfield_id.text})

        for pl in plo_out:
            try:
                if pl['dropdown_item'] != '' and pl['textfield'] == '':
                    df3[pl['label']] = work_file[pl['dropdown_item']]
            except Exception as e:
                print(e)

        for pl in plo_out:
            try:
                if pl['textfield'] != '':
                    df4 = pd.DataFrame({pl['label']: pl['textfield']}, index=range(0, kol))
                    df3[pl['label']] = df4
            except Exception as e:
                print(e)

        # for i, row in work_file.iterrows():
        #     Clock.schedule_interval(lambda dt: self.set_current_item_label(i), 1)

        app = MDApp.get_running_app()
        path = app.path
        os.chdir(path)
        writer = pd.ExcelWriter(r'work.xlsx')
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
            call('work.xlsx', shell=True)
        if platform.system() == 'Linux':
            call(['xdg-open', 'work.xlsx'])
            self.dialog_close()

    @mainthread
    def add_next_button(self):
        btn1 = MDRaisedButton(
            text="Далее",
            size_hint=(.1, .7),
            pos_hint={'center_x': .9, 'center_y': .5},
        )
        btn1.bind(on_release=self.goto_import_screen)
        layout = self.ids.float
        layout.add_widget(btn1)

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
        if self.ids.work_adapt_spin.active == False:
            self.ids.work_adapt_spin.active = True
        else:
            self.ids.work_adapt_spin.active = False


class WorkItem(MDCard):
    label_text = StringProperty()
    label_text_color = ColorProperty()
    dropdown_item_id = StringProperty()
    textfield_id = StringProperty()

    def drop(self, name):
        app = MDApp.get_running_app()
        work_file = app.work_file
        out = work_file.columns.values.tolist()
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




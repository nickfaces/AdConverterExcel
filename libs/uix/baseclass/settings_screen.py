from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
import pandas as pd

class SettingsScreen(Screen):

    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.goback()
    pass

    def drop(self, name):
        print('111', name)
        current_path = self.manager.get_screen("home").ids.input_file.text
        input_file = pd.read_excel(current_path)
        out = input_file.columns.values.tolist()
        kol = len(input_file.index)
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
        print('222', caller)
        self.menu = MDDropdownMenu(
            caller= caller,
            items=items,
            position="center",
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, text_item, name):
        self.menu.dismiss()
        print(text_item)
        self.ids[name].text = text_item

    def import_file(self):
        print('start')
        current_path = self.manager.get_screen("home").ids.input_file.text
        input_file = pd.read_excel(current_path)
        print(input_file)
        kol = len(input_file.index)
        for k in input_file:
            print(k)

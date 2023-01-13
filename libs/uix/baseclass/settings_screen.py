from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem

class SettingsScreen(Screen):

    # changing screens also can be done in python
    # def goto_home_screen(self):
    #     self.manager.goback()
    pass

    def drop(self):


        items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "text": f"Item {i}",
            }
            for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=items,
            position="auto",
            width_mult=4,
        )
        self.menu.open()


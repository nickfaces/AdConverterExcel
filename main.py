from kivymd.app import MDApp
from kivy.core.window import Window
from libs.uix.root import Root
from kivy.config import Config
Config.set('kivy','window_icon','icon.ico')


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "AdConverterExcel"
        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

    def build(self):
        self.title = 'АвтоДилер'
        self.icon = 'icon.ico'
        self.root = Root()
        self.root.set_current("home")


if __name__ == "__main__":
    MainApp().run()
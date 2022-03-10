from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from layout1 import MyLayout1
from kivymd_extensions.akivymd import *
from kivy.config import Config
import json as jso


Config.set("kivy", "window_icon", "")
with open("media/file json/file.json") as f:
    data = jso.load(f)

# gestion de la taille de l'ecran
Window.size = (750, 650)


class MyApp(MDApp):
    def build(self):

        self.load_all_file_kv()
        self.icon = data["icon"]["avatar6"]
        self.title = ""
        self.theme_cls.theme_style = "Light"
        return MyLayout1()

    def load_all_file_kv(self):
        Builder.load_file("layout.kv")


if __name__ == '__main__':
    obj = MyApp()
    obj.run()

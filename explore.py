import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from kivy.base import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
import japanize_kivy
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.spinner import Spinner
import subprocess
import threading



Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 200)
Config.set('graphics', 'resizable', 0)
Config.write()

Builder.load_file("12345.kv")


class MyLayout(Widget):
    item_list = ObjectProperty(None)
    label_text = ObjectProperty(None)
    input_text = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.run_button() #始めの二度押し解消

    def convert(cmd):
        print(cmd)
        subprocess.run(cmd)

    def run_button(self):
        print('pushed')
        path = self.ids.input_path.text
        path = path[2:]
        path = path[:-3]
        out_extension = '.'
        if self.ids.item_list.text == 'PNG':
            out_extension = '.png'
        print(path)
        cmd = f'ffmpeg.exe -i \"{path}\" output{out_extension} -progress prog.txt'
        th1 = threading.Thread(target=MyLayout.convert, args=(cmd,))
        th1.start()

    def test_but(self):
        self.ids.aaa.text = self.ids.item_list.text
        print(self.ids.aaa.text)


class SpinnerButton(Button):
    pass


class MySpinner(Spinner):
    option_cls = ObjectProperty(SpinnerButton)

class PathButton(Button):
    @staticmethod        
    def get_path():
        root = tk.Tk()
        root.withdraw()
        return(str(filedialog.askopenfilenames()))


class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()
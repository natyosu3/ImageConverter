import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from kivy.base import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
import japanize_kivy
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.spinner import Spinner
import subprocess
import threading
import img2pdf
import fitz
import os



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
        out_extension = self.ids.item_list.text
        if out_extension == '選択...' :
            self.popup_open()
            return print('e')
        
        path = self.ids.input_path.text
        path = path[2:]
        path = path[:-3]
        fullpath=path
        path = os.path.splitext(os.path.basename(path))
        filename = path[0]
        input_ext = path[1]

        out_name = str(self.ids.out_name.text)
        if out_name == '':
            out_name = filename

        if out_extension == '.pdf': #出力がPDFの場合
            with open(f"{out_name}.pdf","wb") as f:
                f.write(img2pdf.convert([fullpath]))

        if input_ext == '.pdf': #入力がPDFの場合
            print(fullpath)
            pages = fitz.open(fullpath)
            for page in pages:
                pix = page.get_pixmap()
                pix.save(f"{out_name}_%i.png" % (page.number+1))
            return

        cmd = f'ffmpeg.exe -i \"{path}\" {out_name}{out_extension}'
        th1 = threading.Thread(target=MyLayout.convert, args=(cmd,))
        th1.start()

    def on_touch_d(self, touch):
        print(touch.pos)
        if self.ids.init_ms.collide_point(*touch.pos):
            self.ids.init_ms.text = ''

    def popup_open(self):
        content = PopupMenu(popup_close=self.popup_close)
        self.popup = Popup(title='RUN ERROR', content=content, size_hint=(0.6, 0.6), auto_dismiss=False)
        self.popup.open()

    def popup_close(self):
        self.popup.dismiss()

class SpinnerButton(Button):
    pass


class PopupMenu(BoxLayout):
    popup_close = ObjectProperty(None)


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
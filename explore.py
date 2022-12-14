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


os.environ ['KIVY_GL_BACKEND'] = 'angle_sdl2'
Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 200)
Config.set('graphics', 'resizable', 0)
#Config.write()

Builder.load_file("12345.kv")

# ファイルパスリスト(global)
input_paths=[]


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
        global input_paths
        out_extension = self.ids.item_list.text
        if out_extension == '選択...' :
            self.popup_open()
            return print('e')
        
        fullpath = input_paths[0]
        path = os.path.splitext(os.path.basename(input_paths[0]))
        filename = path[0]
        input_ext = path[1]

        out_name = str(self.ids.out_name.text)

        # (error)入出力拡張子が同じ場合
        if input_ext == out_extension:
            print('e')
            self.popup_open2()
            return

        # 出力ファイル名が未入力の場合-空文字
        if out_name == '':
            out_name = filename

        # 複数ファイルの場合
        if len(input_paths) != 1:
            for i in range(len(input_paths)):
                fullpath = input_paths[i]
                path = os.path.splitext(os.path.basename(input_paths[i]))
                filename = path[0]
                input_ext = path[1]

                # 出力がPDFの場合
                if out_extension == '.pdf':
                    with open(f"{filename}.pdf","wb") as f:
                        f.write(img2pdf.convert([fullpath]))
                
                # 入力がPDFの場合
                elif input_ext == '.pdf':
                    print(fullpath)
                    pages = fitz.open(fullpath)
                    for page in pages:
                        pix = page.get_pixmap()
                        pix.save(f"{filename}_%i{out_extension}" % (page.number+1))
                    
                # その他
                else:
                    cmd = f'ffmpeg.exe -i \"{fullpath}\" {filename}{out_extension}'
                    th1 = threading.Thread(target=MyLayout.convert, args=(cmd,))
                    th1.start()

        # 単一ファイルの場合
        else:
            if out_extension == '.pdf': #出力がPDFの場合
                with open(f"{out_name}.pdf","wb") as f:
                    f.write(img2pdf.convert([fullpath]))
                return

            elif input_ext == '.pdf': #入力がPDFの場合
                print(fullpath)
                pages = fitz.open(fullpath)
                for page in pages:
                    pix = page.get_pixmap()
                    pix.save(f"{out_name}_%i.png" % (page.number+1))
                return
            else:
                cmd = f'ffmpeg.exe -i \"{fullpath}\" {out_name}{out_extension}'
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

    def popup_open2(self):
        content = PopupMenu2(popup_close=self.popup_close)
        self.popup = Popup(title='EXT ERROR', content=content, size_hint=(0.6, 0.6), auto_dismiss=False)
        self.popup.open()

    def popup_close(self):
        self.popup.dismiss()

class SpinnerButton(Button):
    pass


class PopupMenu(BoxLayout):
    popup_close = ObjectProperty(None)

class PopupMenu2(BoxLayout):
    popup_close = ObjectProperty(None)


class MySpinner(Spinner):
    option_cls = ObjectProperty(SpinnerButton)

class PathButton(Button):
    @staticmethod        
    def get_path():
        global input_paths

        root = tk.Tk()
        root.withdraw()
        pts = filedialog.askopenfilenames()
        for pt in pts:
            input_paths.append(pt)
        return str(pts)


class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()
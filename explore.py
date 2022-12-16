import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from kivy.base import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
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
Config.set('graphics', 'height', 225)
Config.set('graphics', 'resizable', 0)
Config.write()

# kvファイル読み込み
Builder.load_file("12345.kv")

# ファイルパスリスト(global)
input_paths=[]


class MyLayout(Widget):
    item_list = ObjectProperty(None)
    label_text = ObjectProperty(None)
    input_text = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        Clock.schedule_interval(self.my_callback, 0.7)
        self.add_widget(Decoration())
        
    # I/O 拡張子をループで取得
    def my_callback(self, dt):
        try:
            self.ids.output_ext.text = self.ids.item_list.text
            out = eval(self.ids.input_path.text)
            self.ids.input_ext.text = os.path.splitext(out[0])[1]
        except SyntaxError:
            self.ids.input_ext.text = '未入力'

    def change_condition(self, dt):
        self.ids.condition.text = 'Ready'

    def clock_run(self):
        Clock.schedule_once(self.change_condition, 3)

    def convert(self, cmd):
        print(cmd)
        subprocess.run(cmd)
        self.ids.condition.text = 'Finished'
        self.clock_run()

    def run_button(self):
        global input_paths
        out_extension = self.ids.item_list.text
        out_dir = self.ids.output_path.text + '/'

        if out_extension == '選択...' :
            self.popup_open()
            return print('e')
        
        try:
            fullpath = input_paths[0]
            path = os.path.splitext(os.path.basename(input_paths[0]))
            filename = path[0]
            input_ext = path[1]
        except:
            self.InputErrorPopupMenu()
            return print('e')

        if input_ext != ('.png' or '.PNG' or '.jpeg' or '.JPEG' or '.jpg' or '.JPG' or '.webp' or '.Webp' or '.WEBP' or '.pdf' or '.PDF' or '.gif' or '.GIF'):
            self.Input_EXT_ErrorPopupMenu()
            return None

        out_name = str(self.ids.out_name.text)

        # (error)入出力拡張子が同じ場合
        if input_ext == out_extension:
            print('e')
            self.popup_open2()
            return

        # 出力ファイル名が未入力の場合-空文字
        if out_name == '':
            out_name = filename

        if out_dir == '/':
            out_dir = ''
        
        self.ids.condition.text = 'Running'

        # 複数ファイルの場合
        if len(input_paths) != 1:
            for i in range(len(input_paths)):
                fullpath = input_paths[i]
                path = os.path.splitext(os.path.basename(input_paths[i]))
                filename = path[0]
                input_ext = path[1]

                # 出力がPDFの場合
                if out_extension == '.pdf' or input_ext == '.gif' or '.GIF':
                    with open(f"{out_dir}{filename}.pdf","wb") as f:
                        f.write(img2pdf.convert([fullpath]))
                    self.ids.condition.text = 'Finished'
                    self.clock_run()
                
                # 入力がPDFの場合
                elif input_ext == '.pdf' or '.PDF':
                    print(fullpath)
                    pages = fitz.open(fullpath)
                    for page in pages:
                        pix = page.get_pixmap()
                        pix.save(f"{out_dir}{filename}_%i{out_extension}" % (page.number+1))
                    self.ids.condition.text = 'Finished'
                    self.clock_run()
                    
                # その他
                else:
                    cmd = f'ffmpeg.exe -i \"{fullpath}\" \"{out_dir}{filename}{out_extension}\"'
                    th1 = threading.Thread(target=MyLayout.convert, args=(self, cmd,))
                    th1.start()

        # 単一ファイルの場合
        else:
            # 出力がPDFの場合
            if out_extension == '.pdf' or (input_ext == ('.gif' or '.GIF')):
                with open(f"{out_dir}{out_name}.pdf","wb") as f:
                    f.write(img2pdf.convert([fullpath]))
                self.ids.condition.text = 'Finished'
                self.clock_run()

            # 入力がPDFの場合
            elif input_ext == '.pdf':
                print(fullpath)
                pages = fitz.open(fullpath)
                for page in pages:
                    pix = page.get_pixmap()
                    pix.save(f"{out_dir}{out_name}_%i.png" % (page.number+1))
                self.ids.condition.text = 'Finished'
                self.clock_run()
                
            else:
                cmd = f'ffmpeg.exe -i \"{fullpath}\" \"{out_dir}{out_name}{out_extension}\"'
                th1 = threading.Thread(target=MyLayout.convert, args=(self, cmd,))
                th1.start()

    def popup_open(self):
        content = PopupMenu(popup_close=self.popup_close)
        self.popup = Popup(title='RUN ERROR', content=content, size_hint=(0.6, 0.6), auto_dismiss=False)
        self.popup.open()

    def popup_open2(self):
        content = PopupMenu2(popup_close=self.popup_close)
        self.popup = Popup(title='EXT ERROR', content=content, size_hint=(0.6, 0.6), auto_dismiss=False)
        self.popup.open()

    def InputErrorPopupMenu(self):
        content = InputErrorPopupMenu(popup_close=self.popup_close)
        self.popup = Popup(title='INPUT ERROR', content=content, size_hint=(0.6, 0.6), auto_dismiss=False)
        self.popup.open()

    def Input_EXT_ErrorPopupMenu(self):
        content = Input_EXT_ErrorPopupMenu(popup_close=self.popup_close)
        self.popup = Popup(title='INPUT_EXT ERROR', content=content, size_hint=(0.6, 0.6), auto_dismiss=False)
        self.popup.open()
        self.ids.condition.text = 'Error'
        self.clock_run()

    def popup_close(self):
        self.popup.dismiss()

class SpinnerButton(Button):
    pass


class PopupMenu(BoxLayout):
    popup_close = ObjectProperty(None)

class PopupMenu2(BoxLayout):
    popup_close = ObjectProperty(None)

class InputErrorPopupMenu(BoxLayout):
    popup_close = ObjectProperty(None)

class Input_EXT_ErrorPopupMenu(BoxLayout):
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


class OutPathButton(Button):
    @staticmethod        
    def get_path():
        root = tk.Tk()
        root.withdraw()
        out_dir = filedialog.askdirectory()
        return out_dir

class Decoration(Widget):
    pass


class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()
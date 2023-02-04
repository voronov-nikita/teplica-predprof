# ТЗ:
# https://docs.google.com/document/d/1yNu_mfNUTXRuimC1jlhbPLuVora4HbI8/edit

from webbrowser import open_new_tab
import requests

# Основное приложение
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.lang import Builder


# Класс для Выпадающего меню
class LeftMenu(Screen):
    def __init__(self):
        super().__init__()
        self.add_widget(Builder.load_file("KV.kv"))


class MainScreen(Screen):
    def __init__(self):
        super().__init__()
        # имя экрана
        self.name = "Main"
        self.k = 1
        # отправляем get запрос на сайт и получаем ответ
        res = requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{self.k}")
        # Стандартный Лэйбел
        self.lbl = MDLabel(text=res.text,
                           halign="center",
                           pos_hint={"center_x": .5,
                                     "center_y": 0.85},
                           )
        self.fl = FloatLayout()
        self.btn_next = Button(on_release=self.next)
        self.dp = LeftMenu()
        # запускаем функцию Init()
        self.Init()

    def Init(self):
        #
        btn1 = MDRectangleFlatButton(text="update",
                                     size_hint=(1, .25),
                                     # pos=(.5, .5),
                                     pos_hint={'x': 0, 'y': 0.5},
                                     # md_bg_color=MainApp().theme_cls.primary_dark,
                                     on_press=self.update
                                     )
        #
        btn2 = MDRectangleFlatButton(text="next",
                                     size_hint=(1, .25),
                                     # pos=(.5, .5),
                                     pos_hint={'x': 0, 'y': 0.25},
                                     # md_bg_color=MainApp().theme_cls.primary_dark,
                                     on_press=self.count
                                     )
        #
        btn3 = MDRectangleFlatButton(text="humidity",
                                     size_hint=(1, .25),
                                     # pos=(.5, .5),
                                     pos_hint={'x': 0, 'y': 0},
                                     on_press=self.next
                                     )

        self.fl.add_widget(self.lbl)
        self.fl.add_widget(btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)
        self.fl.add_widget(self.dp)

        # обьединяем self и наш layout
        self.add_widget(self.fl)

    # функция для перехода на следующий экран
    def next(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "Second"
        return 0

    # основляем текст
    def update(self, instance):
        res = requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{self.k}")
        self.lbl.text = res.text

    # изменяем id в ссылке
    def count(self, instance):
        if self.k == 4:
            self.k = 1
        else:
            self.k += 1
        res = requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{self.k}")
        self.lbl.text = res.text


class SecondScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Second"
        self.k = 1
        res = requests.get(f'https://dt.miet.ru/ppo_it/api/hum/{self.k}')
        self.lbl = MDLabel(text=res.text,
                           halign="center",
                           pos_hint={"center_x": .5,
                                     "center_y": 0.85},
                           # color_text = self.theme_cls.theme_style,
                           )
        self.fl = FloatLayout()
        self.dp = LeftMenu()
        self.Init()

    def Init(self):
        btn1 = MDRectangleFlatButton(text="update",
                                     size_hint=(1, .25),
                                     pos_hint={'x': 0, 'y': 0.5},
                                     on_press=self.update
                                     )
        btn2 = MDRectangleFlatButton(text="next",
                                     size_hint=(1, .25),
                                     pos_hint={'x': 0, 'y': 0.25},
                                     on_press=self.count
                                     )
        btn3 = MDRectangleFlatButton(text="temperature",
                                     size_hint=(1, .25),
                                     pos_hint={'x': 0, 'y': 0},
                                     on_press=self.next
                                     )

        self.fl.add_widget(self.lbl)
        self.fl.add_widget(btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "Main"
        return 0

    def update(self, instance):
        res = requests.get(f'https://dt.miet.ru/ppo_it/api/hum/{self.k}')
        self.lbl.text = res.text

    def count(self, instance):
        if self.k == 6:
            self.k = 1
        else:
            self.k += 1
        res = requests.get(f'https://dt.miet.ru/ppo_it/api/hum/{self.k}')
        self.lbl.text = res.text


class ExtraScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = "ExtraMode"

        self.bx = BoxLayout(orientation="vertical")
        self.Init()

    def Init(self):
        btn1 = MDRectangleFlatButton(text="1")
        btn2 = MDRectangleFlatButton(text="2")
        btn3 = MDRectangleFlatButton(text="3")
        btn4 = MDRectangleFlatButton(text="4")
        self.bx.add_widget(btn1)
        self.bx.add_widget(btn2)
        self.bx.add_widget(btn3)
        self.bx.add_widget(btn4)

        self.add_widget(self.bx)


class TabelScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Table"

        self.dp = LeftMenu()
        self.fl = FloatLayout()

        self.Init()

    def Init(self):
        btn = MDRaisedButton(text="back",
                             pos_hint={"x": .79, "y": .885},
                             size_hint=(.2, .1),
                             on_press=self.back)
        table = MDDataTable(pos_hint={"center_x": .5,
                                      "center_y": .55},
                            size_hint=(0.9, .6),
                            column_data=[
                                ("№ id", dp(10)),
                                ("temperature", dp(20)),
                                ("humidity", dp(15)),
                                ("other", dp(15)),

                            ],
                            row_data=[
                                ("1", "10", "55", "64"),
                                ("2", "11", "44", "32"),
                                ("3", "66", "33", "5")
                            ]
                            )
        self.fl.add_widget(table)
        self.fl.add_widget(btn)
        self.fl.add_widget(self.dp)
        self.add_widget(self.fl)

    def back(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "Main"
        return 0


class EditScreen(Screen):
    def __init__(self, **kwargs):
        super(EditScreen, self).__init__(**kwargs)
        self.name = "Edit"

        self.max_temp = 0
        self.min_temp = 0
        self.max_hum = 0
        self.min_hum = 0

        self.fl = FloatLayout()
        self.bx = BoxLayout(orientation="vertical")
        self.fl = FloatLayout()
        self.lbl = MDLabel(text="EDIT",
                           halign="center",
                           size_hint=(1, 0.1),
                           pos_hint={"x": 0, "y": 0.8},
                           )

        self.Init()

    def Init(self):
        btn = MDRaisedButton(text="Last",
                             size_hint=(0.2, 0.1),
                             pos_hint={"x": 0.8, "y": 0.9},
                             on_press=self.next
                             )
        self.txt1 = MDTextField(hint_text=f"Temperature",
                                mode="fill",
                                size_hint=(1, 0.5),
                                pos_hint={"x": 0, "y": .8}
                                )
        self.txt2 = MDTextField(hint_text=f"Temperature-Humidity",
                                helper_text="Hum",
                                mode="fill",
                                size_hint=(1, 0.5),
                                pos_hint={"x": 0, "y": 0.3}
                                )
        self.txt3 = MDTextField(hint_text=f"Humidity-Earth",
                                helper_text="Hum",
                                mode="fill",
                                size_hint=(1, 0.5),
                                pos_hint={"x": 0, "y": 0}
                                )

        btn_save_data = MDRaisedButton(
            text="Save",
            size_hint=(1, .1),
            pos_hint={"x": 0, "y": 0},
            on_press=self.save_data
        )

        self.bx.add_widget(self.lbl)
        self.fl.add_widget(btn)
        self.bx.add_widget(self.txt1)
        self.bx.add_widget(self.txt2)
        self.bx.add_widget(self.txt3)
        self.bx.add_widget(btn_save_data)

        self.fl.add_widget(self.bx)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'down'
        self.manager.current = "Main"
        return 0

    def save_data(self, instance):
        if self.txt1.text is not None and self.txt1.text != "":
            self.min_hum = float(self.txt1.text)
            print("save")

        if self.txt2.text is not None and self.txt2.text != "":
            self.min_hum = float(self.txt2.text)
            print("save")

        if self.txt3.text is not None and self.txt3.text != "":
            self.min_hum = float(self.txt2.text)
            print("save")


class MainApp(MDApp, Screen):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = "Yellow"
        self.theme_cls.theme_style = "Dark"

        self.sm.add_widget(MainScreen())
        self.sm.add_widget(TabelScreen())
        self.sm.add_widget(ExtraScreen())
        self.sm.add_widget(EditScreen())
        self.sm.add_widget(SecondScreen())

        return self.sm

    def edit_call(self):
        self.sm.transition.direction = "up"
        self.sm.current = "Edit"
        return 0

    def extra_mode(self):
        self.sm.transition.direction = "right"
        self.sm.current = "ExtraMode"
        return 0

    def table_info(self):
        self.sm.transition.direction = "right"
        self.sm.current = "Table"
        return 0

    def change_color_sys(self):
        self.theme_cls.primary_palette = ("Yellow" if self.theme_cls.primary_palette == "Orange" else "Orange")
        self.theme_cls.theme_style = ("Light" if self.theme_cls.theme_style == "Dark" else "Dark")
        return 0

    def git_info(self):
        open_new_tab("https://github.com/voronov-nikita/teplica_predprof")
        return 0


if __name__ == "__main__":
    MainApp().run()

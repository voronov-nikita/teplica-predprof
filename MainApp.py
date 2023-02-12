# ТЗ:
# https://docs.google.com/document/d/1yNu_mfNUTXRuimC1jlhbPLuVora4HbI8/edit


from kivy.config import Config

Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 400)
Config.set("graphics", "height", 500)

from webbrowser import open_new_tab
import requests
from json import loads
from translate import Translator
import matplotlib.pyplot as plt

# Основное приложение
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.fitimage import FitImage
# from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.metrics import dp
from kivy.lang import Builder


# преобразование json в словарь
def splitting_for(s):
    return loads(s)


def translate_app(s):
    translator = Translator(from_lang="en", to_lang="ru")
    return translator.translate(s)


# Класс для Выпадающего меню
class LeftMenu(Screen):
    def __init__(self):
        super().__init__()
        self.add_widget(Builder.load_file("FeftMenu.kv"))


class MainScreen(Screen):
    def __init__(self):
        super().__init__()
        # имя экрана
        self.name = "Main"

        self.button_value = []
        for i in range(1, 4 + 1):
            res = requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{i}")
            self.button_value.append(
                f"""Sensor {i}:\nTemperature: {splitting_for(res.text)["temperature"]}\nHumidity: {splitting_for(res.text)["humidity"]}""")

        # # Стандартный Лэйбел
        # self.lbl = MDLabel(
        #     text=f"""Sensor {self.k}:\nTemperature: {splitting_for(res.text)["temperature"]}\nHumidity: {splitting_for(res.text)["humidity"]}""",
        #     halign="center",
        #     pos_hint={"center_x": .5,
        #               "center_y": 0.85},
        # )
        self.fl = FloatLayout()
        self.dp = LeftMenu()
        # запускаем функцию Init()
        self.Init()

    def Init(self):
        #
        self.btn1 = MDRectangleFlatButton(text=self.button_value[0],
                                          size_hint=(0.25, .25),
                                          # pos=(.5, .5),
                                          pos_hint={'center_x': 0.3, 'center_y': 0.7},
                                          # md_bg_color=(0, 1, 0, 0.1),
                                          on_press=self.update
                                          )
        #
        btn2 = MDRectangleFlatButton(text=self.button_value[1],
                                     size_hint=(0.25, .25),
                                     # pos=(.5, .5),
                                     pos_hint={'center_x': 0.7, 'center_y': 0.7},
                                     # md_bg_color=(0, 1, 0, 0.05),
                                     on_release=self.update
                                     )
        #
        btn3 = MDRectangleFlatButton(text=self.button_value[2],
                                     size_hint=(0.25, .25),
                                     # pos=(.5, .5),
                                     pos_hint={'center_x': 0.3, 'center_y': 0.4},
                                     # md_bg_color=(0, 1, 0, 0.1),
                                     on_release=self.update
                                     )
        btn4 = MDRectangleFlatButton(text=self.button_value[3],
                                     size_hint=(0.25, .25),
                                     # pos=(.5, .5),
                                     pos_hint={'center_x': 0.7, 'center_y': 0.4},
                                     # md_bg_color=(0, 1, 0, 0.05),
                                     on_release=self.update
                                     )
        self.btn_doing = MDRectangleFlatButton(
            text="DO",
            size_hint=(.4, .2),
            pos_hint={'center_x': 0.71, 'center_y': 0.1},
            md_bg_color=(0, 1, 0, 0.1),
            on_press=self.doing
        )

        self.btn_next = MDRectangleFlatButton(text="more",
                                              size_hint=(.4, .2),
                                              pos_hint={"center_x": 0.29, "center_y": 0.1},
                                              md_bg_color=(0, 1, 0, 0.1),
                                              on_release=self.next
                                              )

        # self.fl.add_widget(self.lbl)
        self.fl.add_widget(self.btn_doing)
        self.fl.add_widget(self.btn_next)
        self.fl.add_widget(self.btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)
        self.fl.add_widget(btn4)
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
        id_btn = instance.text[7:8]
        res = requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{id_btn}")
        txt = f"""Sensor {id_btn}:\nTemperature: {splitting_for(res.text)["temperature"]}\nHumidity: {splitting_for(res.text)["humidity"]}"""
        instance.text = txt
        return 0

    def doing(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "Doing"
        return 0


class DoingScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Doing"

        self.temp = EditScreen().min_temp
        self.hum_air = EditScreen().min_hum_air
        self.hum_eath = EditScreen().min_hum_eath

        self.dp = LeftMenu()
        self.fl = FloatLayout()
        self.bx = BoxLayout(orientation="vertical")

        self.Init()

    def average_value(self, x):
        return sum(x) // len(x)

    def temp_hum(self):
        res_temp = []
        res_air = []
        res_eath = []
        for i in range(1, 4 + 1):
            res_temp.append(
                splitting_for(requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{i}").text)["temperature"])
            res_air.append(splitting_for(requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{i}").text)["humidity"])
        for i in range(1, 6 + 1):
            res_eath.append(splitting_for(requests.get(f'https://dt.miet.ru/ppo_it/api/hum/{i}').text)["humidity"])
        return [res_temp, res_air, res_eath]

    def Init(self):
        self.btn_open = MDRectangleFlatButton(
            text="Open",
            size_hint=(.9, .2),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            disabled=(False if self.average_value(self.temp_hum()[0]) >= self.temp else True)
        )
        self.btn_start_water = MDRectangleFlatButton(
            text="Start Watering",
            size_hint=(.9, .2),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            disabled=(False if self.average_value(self.temp_hum()[0]) >= self.temp else True)
        )

        self.btn_stop_water = MDRectangleFlatButton(
            text="Stop Watering",
            size_hint=(.9, .2),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            disabled=(False if self.average_value(self.temp_hum()[0]) >= self.temp else True)
        )

        self.fl.add_widget(self.btn_open)
        self.fl.add_widget(self.btn_start_water)
        self.fl.add_widget(self.btn_stop_water)
        self.fl.add_widget(self.bx)
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)


class SecondScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Second"
        self.k = 1
        res = requests.get(f'https://dt.miet.ru/ppo_it/api/hum/{self.k}')
        self.button_value = []
        for i in range(1, 6 + 1):
            res = requests.get(f"https://dt.miet.ru/ppo_it/api/hum/{i}")
            self.button_value.append(
                f"""Sensor {i}:\nHumidity: {splitting_for(res.text)["humidity"]}""")
        self.fl = FloatLayout()
        self.dp = LeftMenu()
        self.Init()

    def Init(self):
        btn1 = MDRectangleFlatButton(text=self.button_value[0],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.3, 'center_y': 0.8},
                                     on_press=self.update
                                     )
        btn2 = MDRectangleFlatButton(text=self.button_value[1],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.7, 'center_y': 0.8},
                                     on_press=self.update
                                     )
        btn3 = MDRectangleFlatButton(text=self.button_value[2],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.3, 'center_y': 0.55},
                                     on_press=self.update
                                     )
        btn4 = MDRectangleFlatButton(text=self.button_value[3],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.7, 'center_y': 0.55},
                                     on_press=self.update
                                     )
        btn5 = MDRectangleFlatButton(text=self.button_value[4],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.3, 'center_y': 0.35},
                                     on_press=self.update
                                     )
        btn6 = MDRectangleFlatButton(text=self.button_value[5],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.7, 'center_y': 0.35},
                                     on_press=self.update
                                     )
        self.btn_next = MDRectangleFlatButton(
            text="back",
            size_hint=(.4, .2),
            pos_hint={'x': 0.52, 'y': 0},
            md_bg_color=(0, 1, 0, 0.1),
            on_press=self.next
        )
        self.btn_doing = MDRectangleFlatButton(
            text="DO",
            size_hint=(.4, .2),
            pos_hint={'x': 0.08, 'y': 0},
            md_bg_color=(0, 1, 0, 0.1),
            on_press=self.doing
        )

        # self.fl.add_widget(self.lbl)
        self.fl.add_widget(self.btn_doing)
        self.fl.add_widget(self.btn_next)
        self.fl.add_widget(btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)
        self.fl.add_widget(btn4)
        self.fl.add_widget(btn5)
        self.fl.add_widget(btn6)
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "Main"
        return 0

    def update(self, instance):
        id_btn = instance.text[7:8]
        res = requests.get(f"https://dt.miet.ru/ppo_it/api/hum/{id_btn}")
        txt = f"""Sensor {id_btn}:\nHumidity: {splitting_for(res.text)["humidity"]}"""
        instance.text = txt
        return 0

    def doing(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "Doing"
        return 0


class ExtraScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = "ExtraMode"

        self.extra_status = True
        self.count_open = 0

        self.switch = MDSwitch(
            pos_hint={'center_x': .5, 'center_y': .75},
            thumb_color_active=(255, 0, 0, 1),
            track_color_active=(255, 0, 0, 0.3),
            width=dp(64)
        )
        self.switch.bind(active=self.warning)

        self.dp = LeftMenu()
        self.bx = BoxLayout(orientation="vertical",
                            pos_hint={"x": 0, "y": 0},
                            size_hint=(1, 0.7))
        self.fl = FloatLayout()
        self.lbl = MDLabel(text="WARNING\nBy turning on the extra mode, you take full responsibility for what happened",
                           halign="center",
                           size_hint=(0.8, .2),
                           pos_hint={"center_x": 0.5, "center_y": 0.9},
                           theme_text_color="Custom",
                           text_color=(1, 0, 0, 1),
                           line_color=(1, 0, 0, 1),
                           font_size=dp(30),
                           )
        self.Init()

    def Init(self):
        self.btn1 = MDRectangleFlatButton(text="Open Leaf",
                                          disabled=self.extra_status,
                                          size_hint=(1, 0.1),
                                          font_size=dp(15),
                                          theme_text_color="Custom",
                                          line_color=(1, 0, 0, 0.8),
                                          text_color=(1, 0, 0, 1),
                                          on_press=self.leaf_move
                                          )
        self.btn2 = MDRectangleFlatButton(text="Watering",
                                          disabled=self.extra_status,
                                          size_hint=(1, 0.1),
                                          font_size=dp(15),
                                          theme_text_color="Custom",
                                          line_color=(1, 0, 0, 0.8),
                                          text_color=(1, 0, 0, 1),
                                          on_press=self.water_run
                                          )
        self.btn3 = MDRectangleFlatButton(text="3",
                                          disabled=self.extra_status,
                                          size_hint=(1, 0.1),
                                          font_size=dp(15),
                                          theme_text_color="Custom",
                                          line_color=(1, 0, 0, 0.8),
                                          text_color=(1, 0, 0, 1),

                                          )
        self.btn4 = MDRectangleFlatButton(text="4",
                                          disabled=self.extra_status,
                                          size_hint=(1, 0.1),
                                          font_size=dp(15),
                                          theme_text_color="Custom",
                                          line_color=(1, 0, 0, 0.8),
                                          text_color=(1, 0, 0, 1),
                                          )

        self.fl.add_widget(self.lbl)
        self.fl.add_widget(self.switch)
        self.bx.add_widget(self.btn1)
        self.bx.add_widget(self.btn2)
        self.bx.add_widget(self.btn3)
        self.bx.add_widget(self.btn4)
        self.fl.add_widget(self.bx)
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    def leaf_move(self, instance):
        if self.count_open == 0:
            self.count_open = 1
        else:
            self.count_open = 0
        res = requests.patch("https://dt.miet.ru/ppo_it/api/fork_drive", params={"state": self.count_open})
        print(res.status_code)

    def water_run(self, instance):
        print("Watering")

    def water_all_run(self, instance):
        if self.water_all == 0:
            self.water_all = 1
        else:
            self.water_all = 0
        res = requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", params={"state": self.water_all})
        print(res.status_code)

    def warning(self, instance, value):
        if value:
            self.lbl.text_color = (1, 1, 1, 0.4)
            self.lbl.line_color = (1, 1, 1, 0.4)
            self.btn1.disabled = False
            self.btn2.disabled = False
            self.btn3.disabled = False
            self.btn4.disabled = False
        else:
            self.lbl.text_color = (1, 0, 0, 1)
            self.lbl.line_color = (1, 0, 0, 1)
            self.btn1.disabled = True
            self.btn2.disabled = True
            self.btn3.disabled = True
            self.btn4.disabled = True


class AutomodeScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "AutoMode"

        self.lbl = MDLabel(
            text="This is an automatic mode\nHere you can configure the automation of your greenhouse",
            halign="center",
            pos_hint={"x": 0.1, "y": 0.8},
            size_hint=(0.8, 0.2),
            theme_text_color="Custom",
            text_color=(1, 1, 0, 1),
            font_size=dp(40),
            line_color=(1, 1, 0, 0.8),
        )

        self.fl = FloatLayout()
        self.dp = LeftMenu()

        self.watering_time = None
        self.temp_time = None

        self.Init()

    def Init(self):
        # BLOCK №1
        self.text1 = Label(text="Auto_Watering",
                           pos_hint={"center_x": 0.3,
                                     "center_y": 0.5},
                           color=(1, 1, 0, 1),
                           )
        self.time1 = MDRaisedButton(
            text="Set Time",
            pos_hint={"center_x": 0.8, "center_y": 0.5},
            disabled=True,
            md_bg_color=(1, 1, 0, 1),
            on_press=self.show_timer_watering
        )
        self.switch1 = MDSwitch(
            pos_hint={'center_x': .5, 'center_y': .5},
            thumb_color_active=(255, 255, 0, 1),
            track_color_active=(255, 255, 0, 0.3),
            width=dp(64)
        )
        self.switch1.bind(active=self.sw_press1)

        # BLOKC №2
        self.text2 = Label(text="Auto_temperature",
                           pos_hint={"center_x": 0.3,
                                     "center_y": 0.3},
                           color=(1, 1, 0, 1)
                           )
        self.time2 = MDRaisedButton(
            text="Set Time",
            pos_hint={"center_x": 0.8, "center_y": 0.3},
            disabled=True,
            md_bg_color=(1, 1, 0, 1),
            on_press=self.show_timer_temp
        )
        self.switch2 = MDSwitch(
            pos_hint={'center_x': .5, 'center_y': .3},
            thumb_color_active=(255, 255, 0, 1),
            track_color_active=(255, 255, 0, 0.3),
            width=dp(64),
        )
        self.switch2.bind(active=self.sw_press2)

        self.fl.add_widget(self.text1)
        self.fl.add_widget(self.time1)
        self.fl.add_widget(self.switch1)

        self.fl.add_widget(self.text2)
        self.fl.add_widget(self.time2)
        self.fl.add_widget(self.switch2)

        self.fl.add_widget(self.lbl)
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    # <-----------------Watering----------------->
    def show_timer_watering(self, instance):
        timer = MDTimePicker()
        timer.bind(time=self.get_time_watering)
        timer.open()

    def get_time_watering(self, instance, time):
        self.watering_time = str(time)
        print(self.watering_time)

    # <-----------------Temperature----------------->
    def show_timer_temp(self, instance):
        timer = MDTimePicker()
        timer.bind(time=self.get_time_watering)
        timer.open()

    def get_time_temp(self, instance, time):
        self.temp_time = str(time)
        print(self.temp_time)

    # <-----------------Pressed----------------->
    def sw_press1(self, switch, value):
        if value:
            self.time1.disabled = False
        else:
            self.time1.disabled = True

    def sw_press2(self, switch, value):
        if value:
            self.time2.disabled = False
        else:
            self.time2.disabled = True


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
        self.min_hum_eath = 0
        self.min_hum_air = 0

        self.fl = FloatLayout()
        self.dp = LeftMenu()
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
                             pos_hint={"x": 0.8, "y": 0.88},
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
                                pos_hint={"x": 0, "y": 0.3},
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
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "Main"
        return 0

    def save_data(self, instance):
        if self.txt1.text is not None and self.txt1.text != "":
            self.min_temp = float(self.txt1.text)
            print("save", self.min_temp)

        if self.txt2.text is not None and self.txt2.text != "":
            self.min_hum_air = float(self.txt2.text)
            print("save", self.min_hum_air)

        if self.txt3.text is not None and self.txt3.text != "":
            self.min_hum_eath = float(self.txt3.text)
            print("save", self.min_hum_eath)


class MainApp(MDApp, Screen):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        # self.theme_cls.material_style = "M3"
        self.green = (97, 158, 17, 1)
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"

        self.sm.add_widget(MainScreen())
        self.sm.add_widget(TabelScreen())
        self.sm.add_widget(DoingScreen())
        self.sm.add_widget(AutomodeScreen())
        self.sm.add_widget(ExtraScreen())
        self.sm.add_widget(EditScreen())
        self.sm.add_widget(SecondScreen())

        return self.sm

    def edit_call(self):
        self.sm.transition.direction = "left"
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

    def auto_mode(self):
        self.sm.transition.direction = "right"
        self.sm.current = "AutoMode"
        return 0

    def change_color_sys(self):
        screen_now = self.sm.current

        self.theme_cls.primary_palette = (
            "Green" if self.theme_cls.primary_palette != "Green" else "Pink"
        )
        self.theme_cls.theme_style = (
            "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        )
        return 0

    def git_info(self):
        open_new_tab("https://github.com/voronov-nikita/teplica_predprof")
        return 0


if __name__ == "__main__":
    MainApp().run()

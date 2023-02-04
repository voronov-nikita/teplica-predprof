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
from kivy.lang import Builder

# Класс для Выпадающего меню
class DropDownMenuOpen(Screen):
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
        self.dp = DropDownMenuOpen()
        # запускаем функцию Init()
        self.Init()

    def Init(self):
        #
        btn1 = MDRectangleFlatButton(text="update",
                                     size_hint=(1, .25),
                                     # pos=(.5, .5),
                                     pos_hint={'x': 0, 'y': 0.5},
                                     on_press=self.update
                                     )
        #
        btn2 = MDRectangleFlatButton(text="next",
                                     size_hint=(1, .25),
                                     # pos=(.5, .5),
                                     pos_hint={'x': 0, 'y': 0.25},
                                     on_press=self.count
                                     )
        #
        btn3 = MDRectangleFlatButton(text="humidity",
                                     size_hint=(1, .25),
                                     # pos=(.5, .5),
                                     pos_hint={'x': 0, 'y': 0},
                                     on_press=self.next_is_edit
                                     )

        self.fl.add_widget(self.lbl)
        self.fl.add_widget(btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)
        self.fl.add_widget(self.dp)

        # обьединяем self и наш layout
        self.add_widget(self.fl)

    # функция для перехода на следующий экран
    def next(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "Second"
        return 0

    def next_is_edit(self, instance):
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
        self.dp = DropDownMenuOpen()
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


class EditScreen(Screen):
    def __init__(self, **kwargs):
        super(EditScreen, self).__init__(**kwargs)
        self.name = "Edit"

        self.fl = FloatLayout()
        self.bx = BoxLayout(orientation="vertical")
        self.lbl = MDLabel(text="EDIT", halign="center")

        self.Init()

    def Init(self):
        btn = MDRaisedButton(text="Last",
                             on_press=self.next
                             )
        txt1 = MDTextField(hint_text="Temperature",
                           mode="fill",
                           size_hint=(1, 0.3),
                           pos_hint={"x": 0, "y": .4}
                           )
        txt2 = MDTextField(hint_text="Humidity",
                           mode="fill",
                           size_hint=(1, 0.3),
                           pos_hint={"x": 0, "y": .1}
                           )

        self.bx.add_widget(self.lbl)
        self.bx.add_widget(btn)
        self.bx.add_widget(txt1)
        self.bx.add_widget(txt2)

        self.fl.add_widget(self.bx)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'down'
        self.manager.current = "Main"
        return 0


class MainApp(MDApp, Screen):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = "Yellow"
        self.theme_cls.theme_style = "Dark"

        self.sm.add_widget(MainScreen())
        # self.sm.add_widget(DropDownMenuOpen())
        self.sm.add_widget(EditScreen())
        self.sm.add_widget(SecondScreen())

        return self.sm

    def edit_call(self):
        self.sm.transition.direction = "up"
        self.sm.current = "Edit"

    def change_color_sys(self):
        self.theme_cls.primary_palette = ("Yellow" if self.theme_cls.primary_palette == "Orange" else "Orange")
        self.theme_cls.theme_style = ("Light" if self.theme_cls.theme_style == "Dark" else "Dark")
        return 0


if __name__ == "__main__":
    MainApp().run()

import requests

# Основное приложение
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder

from kivymd.uix.textfield import MDTextField


# Класс для Выпадающего меню
class DropDownMenuOpen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "DropDownMenu"

    def drpdown_(self):
        # Все элементы Выпадающего меню
        self.menu_elem = [
            {
                "viewclass": "MDRectangleFlatIconButton",
                "text": "Edit",
                "icon": "pencil",
                "on_press": lambda x="Example 1": self.edit()
            },
            {
                "viewclass": "MDRectangleFlatIconButton",
                "text": "Themes",
                "icon": "view-headline",
                "on_release": lambda x="Example 2": self.themes()
            },
            {
                "viewclass": "MDRectangleFlatIconButton",
                "text": "button 3",
                "icon": "android",
                "on_release": lambda x="Example 3": self.test()
            },
        ]
        # Задаем параметры: что делать при вызове, биндим элементы,
        # задаем размер ширины меню
        self.dpmenu = MDDropdownMenu(
            caller=self.ids.menu_,
            items=self.menu_elem,
            width_mult=2,
        )
        # запускаем меню
        self.dpmenu.open()

    def edit(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "Main"
        return 0

    def themes(self):
        pass

    def test(self):
        print("click")

    # биндим данные из файла
    Builder.load_file("KV.kv")


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
                                     on_press=self.next
                                     )

        self.fl.add_widget(self.dp)

        self.fl.add_widget(self.lbl)
        self.fl.add_widget(btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)

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

        self.fl.add_widget(self.dp)
        self.fl.add_widget(self.lbl)
        self.fl.add_widget(btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)

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
    def __init__(self):
        super().__init__()
        self.name = "Edit"

        self.fl = FloatLayout()
        self.bx = BoxLayout(orientation="vertical")
        self.lbl = MDLabel(text="EDIT", halign="center")

        self.Init()

    def Init(self):
        txt1 = MDTextField(hint_text="Temperature",
                           mode="fill",
                           size_hint=(1, 0.3),
                           pos_hint={"x": 0, "y": .4})
        txt2 = MDTextField(hint_text="Humidity",
                           mode="fill",
                           size_hint=(1, 0.3),
                           pos_hint={"x": 0, "y": .1}
                           )

        self.bx.add_widget(self.lbl)
        self.bx.add_widget(txt1)
        self.bx.add_widget(txt2)

        self.fl.add_widget(self.bx)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "Main"
        return 0


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        sm.add_widget(EditScreen())
        sm.add_widget(SecondScreen())

        return sm


if __name__ == "__main__":
    MainApp().run()

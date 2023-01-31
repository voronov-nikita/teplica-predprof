import requests

# Основное приложение
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image


class MainScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Main"
        self.k = 1
        res = requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{self.k}")
        self.lbl = Label(text=res.text)
        self.fl = BoxLayout(orientation="vertical")
        self.Init()

    def Init(self):
        btn1 = Button(text="update",
                      # size_hint=(.1, .1),
                      # pos=(.5, .5),
                      # pos_hint={'x': 0, 'y': 0.9},
                      on_press=self.update
                      )
        btn2 = Button(text="next",
                      # size_hint=(.1, .1),
                      # pos=(.5, .5),
                      # pos_hint={'x': 0.4, 'y': 0.9},
                      on_press=self.count
                      )
        btn3 = Button(text="humidity",
                      # size_hint=(.1, .1),
                      # pos=(.5, .5),
                      # pos_hint={'x': 0.8, 'y': 0.9},
                      on_press=self.next
                      )
        self.fl.add_widget(self.lbl)
        self.fl.add_widget(btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "Second"
        return 0

    def update(self, instance):
        res = requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{self.k}")
        self.lbl.text = res.text

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
        self.lbl = Label(text = res.text)
        self.fl = BoxLayout(orientation = 'vertical')
        self.Init()

    def Init(self):
        btn1 = Button(text="update",
                      # size_hint=(.1, .1),
                      # pos=(.5, .5),
                      # pos_hint={'x': 0, 'y': 0.9},
                      on_press=self.update
                      )
        btn2 = Button(text="next",
                      # size_hint=(.1, .1),
                      # pos=(.5, .5),
                      # pos_hint={'x': 0.4, 'y': 0.9},
                      on_press=self.count
                      )
        btn3 = Button(text="temperature",
                      # size_hint=(.1, .1),
                      # pos=(.5, .5),
                      # pos_hint={'x': 0.8, 'y': 0.9},
                      on_press=self.next
                      )
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


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        sm.add_widget(SecondScreen())

        return sm


if __name__ == "__main__":
    MainApp().run()

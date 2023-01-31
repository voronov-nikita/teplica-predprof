# Основное приложение
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image


class MainScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Main"
        self.fl = FloatLayout()
        self.Init()

    def Init(self):
        btn1 = Button(text="1",
                      # size_hint=(.1, .1),
                      pos=(.5, .5),
                      pos_hint={'x': 0, 'y': 0.9},
                      on_press=self.next
                      )
        btn2 = Button(text="2",
                      # size_hint=(.1, .1),
                      # pos=(.5, .5),
                      # pos_hint={'x': 0.4, 'y': 0.9},
                      on_press=self.next
                      )
        btn3 = Button(text="3",
                      # size_hint=(.1, .1),
                      # pos=(.5, .5),
                      # pos_hint={'x': 0.8, 'y': 0.9},
                      on_press=self.next
                      )
        self.fl.add_widget(btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "Second"
        return 0


class SecondScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Second"
        self.fl = FloatLayout()
        self.Init()

    def Init(self):
        pass

    def next(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "Main"
        return 0


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        sm.add_widget(SecondScreen())

        return sm


if __name__ == "__main__":
    MainApp().run()

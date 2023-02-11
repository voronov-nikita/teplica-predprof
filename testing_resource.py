from kivy.config import Config

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '200')
Config.write()

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import sys
import datetime

######
# How to use?
# ===========
#
# start script like: python timer.py 5m
# This will set the timer to 5minutes.
#
# Syntax: timer.py <minutes>m
######


for arg in sys.argv:
    if arg.endswith("m"):
        sys.argv.remove(arg)  # remove this arg - so kivy will not get it
        countdown = int(arg.split("m")[0])

Builder.load_string("""
<MainLayout>:
    button: button
    Button:
        id: button
        on_press: root.toggle()
    AnchorLayout:
        Label:
            text: "%s:%s" % (root.minutes, root.seconds)
            font_size: 120
""")


class MainLayout(FloatLayout):
    minutes = StringProperty()
    seconds = StringProperty()
    running = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.sound = SoundLoader.load('bell.wav')
        self.delta = datetime.datetime.now() + datetime.timedelta(0, 60 * countdown)
        self.update()

    def start(self):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update, 0.05)

    def stop(self):
        if self.running:
            self.running = False
            Clock.unschedule(self.update)

    def update(self, *kwargs):
        delta = self.delta - datetime.datetime.now()
        self.minutes, seconds = str(delta).split(":")[1:]
        self.seconds = seconds[:5]

        if int(self.minutes) == 0:
            if int(self.seconds.split(".")[0]) == 0:
                if int(self.seconds.split(".")[1]) < 20:
                    self.seconds = "00.00"
                    self.button.background_color = (1, 0, 0, 1)
                    self.sound.play()
                    self.stop()

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()


if __name__ == '__main__':
    class TimerApp(App):
        def build(self):
            return MainLayout()


    TimerApp().run()
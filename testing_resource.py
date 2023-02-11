from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

from datetime import datetime, date, time, combine


class IncrediblyCrudeClock(Label):
    a = time(0, 1, 1)

    def update(self, *args):
        self.text = str(self.a)
        print(str(self.a))

        self.a = datetime.combine(date.today(), self.a) - datetime.combine(date.today(), time(0,0,1))

class TimeApp(App):
    def build(self):
        crudeclock = IncrediblyCrudeClock()
        Clock.schedule_interval(crudeclock.update, 1)
        return crudeclock

if __name__ == "__main__":
    TimeApp().run()
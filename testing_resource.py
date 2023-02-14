from kivy.config import Config

Config.set('graphics', 'resizable', False)
from kivy.app import App
import pytz
from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from time import strftime
import re

Window.size = (500, 500)


class HourglassApp(App):
    sw_started = False
    sw_seconds = 0

    alarm_time = " "

    running = False

    def on_start(self):
        Clock.schedule_interval(self.update, 0)

    def update(self, nap):
        self.root.ids.time.text = strftime('[size=80][font=GOTHICB.ttf]%I[/font]:%M %p[/size]\n %a, %B %d')

        if self.sw_started:
            self.sw_seconds += nap

        m, s = divmod(self.sw_seconds, 60)

        self.root.ids.stopwatch.text = ('%02d:%02d.[size=40]%02d[/size]' %
                                        (int(m), int(s), int(s * 100 % 100)))

        if self.alarm_time == strftime('%I:%M %p'):

            if strftime('%S') == '00' and strftime('%S') < '09':
                self.root.ids.check_time.text = '[size=60]Wake Up![/size]'
                self.sound = SoundLoader.load('C:/Users/Able Valued Client/Downloads/Alarm Clock_alarm.wav')
                self.sound.play()

        current_time = strftime("[size=30]%H:%M:%S[/size]")
        self.root.ids.okay.text = "[size=30]Local Time[/size]"
        self.root.ids.okay1.text = current_time

        home = pytz.timezone("Asia/Tokyo")
        local_time = datetime.now(home)
        current_time = local_time.strftime("%H:%M:%S")
        self.root.ids.okay2.text = "Tokyo    " + current_time

        home = pytz.timezone("Australia/Sydney", )
        local_time = datetime.now(home)
        current_time = local_time.strftime("%H:%M:%S")
        self.root.ids.okay4.text = "Sydney   " + current_time

        home = pytz.timezone("America/New_York")
        local_time = datetime.now(home)
        current_time3 = local_time.strftime("%H:%M:%S")
        self.root.ids.okay6.text = "New York    " + current_time

        home = pytz.timezone("Europe/Madrid")
        local_time = datetime.now(home)
        current_time = strftime("%H:%M:%S")
        self.root.ids.okay8.text = "Madrid   " + current_time

        home = pytz.timezone("Africa/Cairo")
        local_time = datetime.now(home)
        current_time = strftime("%H:%M:%S")
        self.root.ids.okay10.text = "Cairo   " + current_time

        home = pytz.timezone('Israel')
        local_time = datetime.now(home)
        current_time = strftime("%H:%M:%S")
        self.root.ids.okay12.text = "Israel   " + current_time

        home = pytz.timezone("America/Mexico_City")
        local_time = datetime.now(home)
        current_time = strftime("%H:%M:%S")
        self.root.ids.okay12.text = "Mexico  " + current_time

    def start_stop(self):
        self.root.ids.start_stop.text = 'Start' if self.sw_started else 'Stop'
        self.sw_started = not self.sw_started

    def reset(self):
        if self.sw_started:
            self.root.ids.start_stop.text = 'Start'
            self.sw_started = False

        self.sw_seconds = 0

    def press(self, alarm_time):
        if len(alarm_time) != 8:
            self.root.ids.check_time.text = "Invalid time format!\nTry add a zero before the hour \nif it's less than 10 and or add PM/AM"
        else:
            if int(alarm_time[0:2]) > 12:
                self.root.ids.check_time.text = "Invalid HOUR format! Please try again..."
            elif int(alarm_time[3:5]) > 59:
                self.root.ids.check_time.text = "Invalid MINUTE format! Please try again..."
            else:
                self.alarm_time = alarm_time
                self.root.ids.check_time.text = "Setting the alarm now..."

    def start(self):
        cd_time = self.root.ids.text_input.text
        check = re.findall("[a-zA-Z]", cd_time)
        if cd_time == '' or len(cd_time) != 8 or check:
            self.root.ids.show.text = 'Please enter the time like this "00:00:05"'
        elif cd_time == '00:00:00':
            Clock.unschedule(self.begin)
        elif self.root.ids.button.text == 'Reset':
            self.reset()

        else:
            self.root.ids.button.text = 'Reset'
            h = cd_time[0:2]
            m = cd_time[3:5]
            s = cd_time[6:8]
            h = int(h)
            m = int(m)
            s = int(s)

            self.delta = datetime.now() + timedelta(hours=h, minutes=m, seconds=s)
            if not self.running:
                self.running = True
                Clock.schedule_interval(self.begin, 0.05)

    def reset(self):

        self.root.ids.button.text = 'Start'
        self.root.ids.show.text = 'Enter the time to countdown in this format "HH:MM:SS"\n For example, [font=GOTHICB]00:00:30[/font]'
        self.root.ids.text_input.text = '00:00:00'

        if self.running:
            self.running = False
            Clock.unschedule(self.begin)

    def pause(self):
        if self.running:
            self.running = False
            Clock.unschedule(self.begin)

    def begin(self, cd_start):
        delta = self.delta - datetime.now()
        delta = str(delta)
        self.root.ids.show.text = '[size=50] 0' + delta[0:7] + '[/size]'

        if delta[0:7] == "0:00:00":
            '0' + delta[0:7]
            self.sound = SoundLoader.load(
                'C:/Users/Able Valued Client/Downloads/mixkit-rooster-crowing-in-the-morning-2462.wav')
            self.sound.play()
            self.reset()

    def toggle(self):
        if self.running:
            self.reset()
        else:
            self.start()


if __name__ == '__main__':
    HourglassApp().run()

from kivy.config import Config

Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 400)
Config.set("graphics", "height", 500)

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class TestApp(App):
    def add_number(self, instance):
        self.text_input.text = self.text_input.text + str(instance.text)

    def clear(self, instance):
        self.text_input.text = ""

    def equals(self, instance):
        try:
            self.text_input.text = str(eval(self.text_input.text))
        except:
            self.text_input.text = "Error"

    def build(self):

        bl = BoxLayout(orientation="vertical", padding=25, spacing=20)
        self.text_input = TextInput(text='', multiline=False, font_size=50, halign="right", size_hint=(1, .2), background_color="black", foreground_color="white")
        bl.add_widget(self.text_input)

        gl = GridLayout(cols=4, spacing=10)
        gl2 = GridLayout(cols=1, spacing=10, size_hint = (1, .5))

        gl.add_widget(Button(text="7", on_press=self.add_number))
        gl.add_widget(Button(text="8", on_press=self.add_number))
        gl.add_widget(Button(text="9", on_press=self.add_number))
        gl.add_widget(Button(text="*", on_press=self.add_number))

        gl.add_widget(Button(text="4", on_press=self.add_number))
        gl.add_widget(Button(text="5", on_press=self.add_number))
        gl.add_widget(Button(text="6", on_press=self.add_number))
        gl.add_widget(Button(text="-", on_press=self.add_number))

        gl.add_widget(Button(text="1", on_press=self.add_number))
        gl.add_widget(Button(text="2", on_press=self.add_number))
        gl.add_widget(Button(text="3", on_press=self.add_number))
        gl.add_widget(Button(text="+", on_press=self.add_number))

        gl.add_widget(Widget())
        gl.add_widget(Button(text="0", on_press=self.add_number))
        gl.add_widget(Widget())
        gl.add_widget(Button(text="/", on_press=self.add_number))

        gl2.add_widget(Button(text="=", on_press=self.equals))
        gl2.add_widget(Button(text="C", on_press=self.clear))



        bl.add_widget(gl)
        bl.add_widget(gl2)

        return bl


if __name__ == '__main__':
    TestApp().run()
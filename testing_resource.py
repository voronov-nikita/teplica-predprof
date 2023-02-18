from kivymd.app import MDApp
from kivymd.uix.label import MDLabel


class MAinApp(MDApp):
    def build(self):
        return MDLabel(text="lox",
                       halign = "center")

MAinApp().run()

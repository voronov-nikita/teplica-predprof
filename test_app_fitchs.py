from kivy.config import Config

Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 400)
Config.set("graphics", "height", 500)

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu


KV = '''
MDScreen:

    MDTopAppBar:
        id:tool1
        title:'My Demo App'
        pos_hint:{'top':1}
        right_action_items : [["home", lambda x: app.menu.open()]]

'''


class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        items_d = ['Snapshot','Settings','History','Logout','Exit']
        menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in items_d
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.tool1,
            items=menu_items,
            width_mult=2,
        )

    def menu_callback(self, text_item):
        print(text_item)
        self.menu.dismiss()

    def build(self):
        return self.screen


Test().run()
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.screen import MDScreen


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return (
            MDScreen(
                MDCard(
                    FitImage(
                        source="icon/settings_for_edit.jpg",
                        # size_hint_y=0.35,
                        # pos_hint={"top": 1},
                        # radius=(36, 36, 0, 0),
                    ),
                    radius=36,
                    md_bg_color="grey",
                    pos_hint={"center_x": .5, "center_y": .5},
                    size_hint=(0.4, 0.8),
                ),
            )
        )


Example().run()
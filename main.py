import matplotlib as mt
import requests

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix


res = requests.get('https://dt.miet.ru/ppo_it/api/temp_hum/2')

ls = res.text.split(",")

for i in ls:
    print(i)

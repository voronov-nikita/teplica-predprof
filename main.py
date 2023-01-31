# Просьба коментировать весь написанный код, если же комент требуется!


# Для отображения информации
import matplotlib as mt
import requests

# Основное приложение
# from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.uix.floatlayout import FloatLayout

# сайт на который отправляем GET запрос
# Пример!
# типо опрашиваем сервер
list_data_info=[]
for i in range(1, 5):
    res = requests.get(f'https://dt.miet.ru/ppo_it/api/temp_hum/{i}')
    list_data_info.append(res.text)





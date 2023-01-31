# https://docs.google.com/document/d/1yNu_mfNUTXRuimC1jlhbPLuVora4HbI8/edit
# Выше ссылка на требования к работе.
# Просьба коментировать весь написанный код, если же комент требуется!


# Для отображения информации -> Вообще не точная информация
import matplotlib as mt
# для отправки запросов на сервер
import requests



# сайт на который отправляем GET запрос
# Пример!
# типо опрашиваем сервер
list_temperatrure_info = [requests.get(f'https://dt.miet.ru/ppo_it/api/temp_hum/{i}').text for i in range(1, 5)]
list_humidity_info = [requests.get(f'https://dt.miet.ru/ppo_it/api/hum/{i}') for i in range(1, 7)]

print(list_temperatrure_info)
print(list_humidity_info)

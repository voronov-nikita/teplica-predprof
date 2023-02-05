import requests
import json

ls = json.loads(str(
    requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/1").text
))
print(ls)
print(ls["id"])
print(ls["temperature"])
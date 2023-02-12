import requests
import json

dicti = {
    "state": 0
}

# патч запросы!!!
res1 = requests.patch("https://dt.miet.ru/ppo_it/api/fork_drive", params={"state": 0})
res2 = requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", params={"state":0})
res3 = requests.patch("https://dt.miet.ru/ppo_it/api/watering", params={"id":6, "state":0})

print(res1.status_code)
print(res2.status_code)
print(res3.status_code)
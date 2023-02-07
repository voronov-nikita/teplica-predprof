import requests

params={
    "state": 1
}


res = requests.get(f"https://dt.miet.ru/ppo_it/api/total_hum")
print(res)

from datetime import datetime as dt
from threading import Thread
from time import sleep


def send_get_request(list_open, list_soil):
    while True:
        time = str(dt.now().hour)+str(dt.now().minute)
        if time in list_open:
            print("Air")
        if time in list_soil:
            print("Soil")
        sleep(60)
        print("Stop")
        print("Stop")


send_get_request(["1914", "1915"], ["1915", "1916"])



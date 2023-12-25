# coding=utf-8

# import requests

# def valid(key):
#
#     url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={key}"
#
#     data = requests.get(url).json()
#     # print(data)
#     return data
#
# print(valid("032f175c8aad045f7655c1130fe7bbdf"))

import datetime
import requests
import json

# dt = [1647345600, 1647356400, 1647367200, 1647766800]
# for i in dt:
#     date = datetime.datetime.fromtimestamp(i).strftime("%m/%d/%Y, %H:%M:%S")

#     print(date)
#

# url = "https://api.openweathermap.org/data/2.5/forecast?q=Batu%20Pahat&lang=zh_tw&units=metric&&appid=032f175c8aad045f7655c1130fe7bbdf"
# response = requests.get(url).json()
# data = json.dumps(response, indent=2, ensure_ascii=False)
#
# with open("data.txt", "w") as f:
#     f.write(data)
# l = []
# with open("data.txt", "r") as f:
#     data = json.loads(f.read())
#     for daily_data in data['list']:
#         dt = daily_data['dt']
#         # print(dt)
#         l.append(dt)
#         date = datetime.datetime.fromtimestamp(dt).strftime("%m/%d/%Y, %I:%M %p")
#         print(date)
#
# print(len(l))
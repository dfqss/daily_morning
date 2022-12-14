from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import json

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  # 读取文本内容
  read_file = open("phrase.txt", encoding="utf-8")
  phrases = []
  # 将文本中的字符串存入短语集合中
  for line in read_file:
    phrases.append(line)
  # 将删去首行的文本重新写入
  count = 0
  new_phrases = []
  for phrase in phrases:
    if count == 0:
      # print('首行：' + phrase)
      count += 1
      continue
    new_phrases.append(phrase)
  read_file.close()
  # 写入新的文本内容
  write_file = open("phrase.txt", encoding="utf-8", mode='w')
  write_file.write(''.join(new_phrases))
  write_file.close()
  return phrases[0]
  #words = requests.get("https://api.shadiao.pro/chp")
  #if words.status_code != 200:
    #return get_words()
  #return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, min_temperature, max_temperature = get_weather()
data = {
  "city":{"value":"有你的地方", "color":get_random_color()},
  "weather":{"value":wea, "color":get_random_color()},
  "temperature":{"value":temperature, "color":get_random_color()},
  "min_temperature":{"value":min_temperature, "color":get_random_color()},
  "max_temperature":{"value":max_temperature, "color":get_random_color()},
  "love_days":{"value":get_count(), "color":get_random_color()},
  "birthday_left":{"value":get_birthday(), "color":get_random_color()},
  "words":{"value":get_words(), "color":get_random_color()}
}
# data = {
#   "weather":{"value":wea, "color":},
#   "temperature":{"value":temperature, "color":get_random_color()},
#   "min_temperature":{"value":min_temperature, "color":get_random_color()},
#   "max_temperature":{"value":max_temperature, "color":get_random_color()},
#   "love_days":{"value":get_count(), "color":get_random_color()},
#   "birthday_left":{"value":get_birthday(), "color":get_random_color()},
#   "words":{"value":words1, "color":get_random_color()}
# }
res = wm.send_template(user_id, template_id, data)
print(res)

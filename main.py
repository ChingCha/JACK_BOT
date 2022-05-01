import discord
import requests
import json
import random
import os

from discord.ext import commands, tasks
from dotenv import load_dotenv
from weather.alarm import *

#import keep_alive
with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default() #all none default
intents.members = True
# 事件定義 特定事件

load_dotenv()
bot = commands.Bot(command_prefix='-j', intents=intents)
data = sets(jdata['TOKEN'], APIToken=jdata['APIToken'], channels=jdata['warning_channels'], Tags=jdata['warning'])
###線上json###
JsonUrl = "https://api.jsonstorage.net/v1/json/" + jdata["JsonUrl"]
JsonUrlToken = jdata["JsonUrlToken"]
JsonUrl_cloudburst = "https://api.jsonstorage.net/v1/json/" + jdata["JsonUrl_cloudburst"]
JsonUrlToken_cloudburst = jdata["JsonUrlToken_cloudburst"]
##############
def setup():
    try:
        open(data.checkFile)
    except:
        with open(data.checkFile, "w") as outfile:
            json.dump({}, outfile, ensure_ascii=False, indent=4)
            print("建立 check.json 完成")
#
@bot.event
async def on_ready():
    print(">> Bot is online <<")
    Jstatus = discord.Status.dnd
    #discord.Status.<狀態>，可以是online（上線）,offline（下線）,idle（閒置）,dnd（請勿打擾）,invisible（隱身）
    Jactivity = discord.Game(name="NEKOPARA Vol. JACK",type = 3)
    #type可以是playing（遊玩中）、streaming（直撥中）、listening（聆聽中）、watching（觀看中）、custom（自定義）
    await bot.change_presence(status = Jstatus, activity = Jactivity)
    #
    if requests.get(f"{JsonUrl}").status_code >= 300:
        print("請申請一個API https://app.jsonstorage.net/")
        return bot.close()
    print("-"*15)
    print(bot.user.name)
    print(bot.user.id)
    print(bot.user)
    print("-"*15)
    if data.APIToken:
        earthquake.start()
        print("地震報告啟動")
        print("天氣警報啟動")
    else:
        print("請至 https://opendata.cwb.gov.tw/userLogin 獲取中央氣象局TOKEN並放置於 .env 檔案中")
    print(">> Bot is Ready <<")
    #

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'已載入 {extension} 指令庫。')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'關閉 {extension} 指令庫。')
    
@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'重新載入 {extension} 指令庫。')  


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(F"cmds.{filename[:-3]}")


###計時偵測###
@tasks.loop(seconds=10)
async def earthquake():
    # 大型地震
    API = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={data.APIToken}&format=JSON&areaName="
    # 小型地震
    API2 = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={data.APIToken}&format=JSON"
    #天氣警特報
    API3 = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/W-C0033-002?Authorization={data.APIToken}&format=JSON"

    b = requests.get(API).json()
    s = requests.get(API2).json()
    r = requests.get(API3).json()

    _API = b["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]
    _API2 = s["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]
    _API3 = r["records"]["record"]
    async def goTo(how, now):
        for ch in data.channels:
            if how != API3:
                await sosIn(bot.get_channel(ch), ({API: b, API2: s}[how]), data)
                requests.put(f"{JsonUrl}?apiKey={JsonUrlToken}", json=now)
            else:
                await Rain(bot.get_channel(ch), ({API3: r}[how]), data)
                requests.put(f"{JsonUrl_cloudburst}?apiKey={JsonUrlToken_cloudburst}", json=now)

    file = requests.get(f"{JsonUrl}").json() or {}
    for i in [API, API2]:
        if not file.get(i):
            print(f"file[i]:{file[i]}")
            file[i] = ""
    if file[API] != _API:
        print(f"file[API]:{file[API]}")
        file[API] = _API
        await goTo(API, file)
    if file[API2] != _API2:
        print(f"file[API]:{file[API]}")
        file[API2] = _API2
        await goTo(API2, file)

    cloudburst = requests.get(f"{JsonUrl_cloudburst}").json() or {}
    if cloudburst["records"]["record"] != _API3:
        await goTo(API3, cloudburst)
#########
#keep_alive.keep_alive() #repl.it架設解除註解
bot.run(jdata['TOKEN'])
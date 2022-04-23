import discord
from discord.ext import commands, tasks
import json
import random
import os
import requests
from dotenv import load_dotenv
with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)
from function import *

intents = discord.Intents.default() #all none default
intents.members = True
# 事件定義 特定事件

bot = commands.Bot(command_prefix='-j', intents=intents)
data = sets(
    os.getenv("TOKEN"), APIToken=os.getenv("APIToken")
    #channels = bot.get_channel(int(jdata['lobby'])),
    #Tags = 967070589632282635
)

@bot.event
async def on_ready():
    print(">> Bot is online <<")

def setup():
    try:
        open(data.checkFile)
    except:
        with open(data.checkFile, "w") as outfile:
            json.dump({}, outfile, ensure_ascii=False, indent=4)
            print("建立 check.json 完成")

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
        bot.load_extension(F'cmds.{filename[:-3]}')


@bot.event
async def on_ready():
    print("-"*15)
    print(bot.user.name)
    print(bot.user.id)
    print(bot.user)
    print("-"*15)
    setup()
    if data.APIToken:
        earthquake.start()
        print("地震報告啟動")
    else:
        print("請至 https://opendata.cwb.gov.tw/userLogin 獲取中央氣象局TOKEN並放置於 .env 檔案中")


@tasks.loop(seconds=10)
async def earthquake():
    # 大型地震
    API = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={data.APIToken}&format=JSON&areaName="
    # 小型地震
    API2 = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={data.APIToken}&format=JSON"

    b = requests.get(API).json()
    s = requests.get(API2).json()
    _API = b["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]
    _API2 = s["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]

    async def goTo(how, now):
        for ch in data.channels:
            await sosIn(bot.get_channel(ch), ({API: b, API2: s}[how]), data)
        with open(data.checkFile, 'w') as outfile:
            json.dump(now, outfile, ensure_ascii=False, indent=4)

    with open(data.checkFile, "r") as file:
        file = json.load(file)
    for i in [API, API2]:
        if not file.get(i):
            file[i] = ""
    if file[API] != _API:
        file[API] = _API
        await goTo(API, file)
    if file[API2] != _API2:
        file[API2] = _API2
        await goTo(API2, file)

bot.run(jdata['TOKEN'])
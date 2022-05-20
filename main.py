from encodings import utf_8
import discord
import requests
import json
import random
import os

from discord.ext import commands, tasks
from dotenv import load_dotenv
from weather.alarm import *
from imgsauce.config import config
#from imgsauce.saucebot import bot
#import keep_alive
with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


from imgsauce.bot import bot
from imgsauce.cogs.admin import Admin
from imgsauce.cogs.misc import Misc
from imgsauce.cogs.sauce import Sauce
from imgsauce.config import config
from imgsauce.log import log

intents = discord.Intents.default() #all none default
intents.members = True
# 事件定義 特定事件

load_dotenv()
#bot = commands.Bot(command_prefix='-j', intents=intents)
bot = commands.AutoShardedBot(
    command_prefix=[p.strip() for p in str(config.get('Bot', 'command_prefixes', fallback='-j')).split(',')],
    case_insensitive=True,
)
data = sets(jdata['TOKEN'], APIToken=jdata['APIToken'], channels=jdata['warning_channels'], Tags=jdata['warning'])
###線上json###
JsonUrl = "https://api.jsonstorage.net/v1/json/" + jdata["JsonUrl"]
JsonUrlToken = jdata["JsonUrlToken"]
JsonUrl_cloudburst = "https://api.jsonstorage.net/v1/json/" + jdata["JsonUrl_cloudburst"]
JsonUrlToken_cloudburst = jdata["JsonUrlToken_cloudburst"]
JsonUrlS = "https://api.jsonstorage.net/v1/json/" + jdata["JsonUrlS"]
JsonUrlSToken = jdata["JsonUrlSToken"]

bot.add_cog(Sauce())
bot.add_cog(Misc())
bot.add_cog(Admin())

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
    log.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    print(f'{bot.user.display_name} is in {len(bot.guilds)} guild(s) and ready for work!')
    print('------')
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

@bot.command()
async def tag(ctx):
    await ctx.send(f"⚠️ @everyone 注意，感謝大家的注意⚠️") 

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(F"cmds.{filename[:-3]}")


###計時偵測###
@tasks.loop(seconds=3)
async def earthquake():
    # 大型地震
    API = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={data.APIToken}&limit=1&offset=0&format=JSON"
    # 小型地震
    API2 = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={data.APIToken}&limit=1&offset=0&format=JSON"
    #天氣警特報
    API3 = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/W-C0033-002?Authorization={data.APIToken}&limit=1&offset=0&format=JSON"

    b = requests.get(API).json()
    s = requests.get(API2).json()
    r = requests.get(API3).json()

    _API = b["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]
    _API2 = s["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]
    _API3 = r["records"]["record"]
    async def goToBIG():
        for ch in data.channels:
            await sosIn(bot.get_channel(ch), data, b)
            requests.put(f"{JsonUrl}?apiKey={JsonUrlToken}", json=b)
            print(f"成功發布地震警報")   
    async def goToS():
        for ch in data.channels:
            await sosIn(bot.get_channel(ch), data, s)
            requests.put(f"{JsonUrlS}?apiKey={JsonUrlSToken}", json=s)
            print(f"成功發布小型地震警報")  
    async def toRain():
        for ch in data.channels:
            await Rain(bot.get_channel(ch) , data, r)
            web = jdata["JsonUrlToken_cloudburst"]
            requests.put(web, json=r)
            print(f"成功發布天氣警報")
    file = requests.get(f"{JsonUrl}").json() or {}
    if file["records"]["earthquake"][0]["earthquakeInfo"]["originTime"] != _API:
        await goToBIG()
    file2 = requests.get(f"{JsonUrlS}").json() or {}
    if file2["records"]["earthquake"][0]["earthquakeInfo"]["originTime"] != _API2:
        await goToS()
    cloudburst = requests.get(f"{JsonUrl_cloudburst}").json() or {}    
    if cloudburst["records"]["record"] != _API3:       
        await toRain()

##########
#keep_alive.keep_alive() #repl.it架設解除註解
bot.run(jdata['TOKEN'])
import discord
from discord.ext import commands, tasks
import json
import random
import os

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default() #all none default
intents.members = True
# 事件定義 特定事件

bot = commands.Bot(command_prefix='-j', intents=intents)


@bot.event
async def on_ready():
    print(">> Bot is online <<")
    Jstatus = discord.Status.dnd
    #discord.Status.<狀態>，可以是online（上線）,offline（下線）,idle（閒置）,dnd（請勿打擾）,invisible（隱身）
    Jactivity = discord.Game(name="NEKOPARA Vol. JACK",type = 3)
    #type可以是playing（遊玩中）、streaming（直撥中）、listening（聆聽中）、watching（觀看中）、custom（自定義）
    await bot.change_presence(status = Jstatus, activity = Jactivity)

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

bot.run(jdata['TOKEN'])
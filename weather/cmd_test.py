import discord
import datetime
import json
import requests

from discord.ext import commands 
from core.classes import Cog_Extension

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open('cloudburst_api_test.json','r',encoding='utf8') as jtest:
    jrain = json.load(jtest)
with open('earthquake_api_test.json','r',encoding='utf8') as jtest2:
    jeew = json.load(jtest2)
with open('weather_api_test.json','r',encoding='utf8') as jtest3:
    jpop = json.load(jtest3)

def checkSos(ac):
    return {
        "0": "⚪",
        "1": "⚪",
        "2": "🟡",
        "3": "🟢",
        "4": "🟢",
        "5": "🔴",
        "6": "🟤",
        "7": "🟤",
        "8": "🟣",
        "9": "⚫"
    }[str(int(ac))] + " "

def earthquake_depth(i):
    if int(i) < 70:
        return "🔴"
    elif int(i) >= 70 and int(i) <= 300 :
        return "🟡"
    elif int(i) > 300:
        return "🟢"

class cmd_test(Cog_Extension):
    @commands.command() #-jrctx 測試發布大雨特報
    async def rctx(self, ctx):
        rt = jrain["records"]["record"][0]["datasetInfo"]["validTime"]["startTime"]
        inp = jrain["records"]["record"][0]
        inpInfo = inp["datasetInfo"]
        contentText = inp["contents"]["content"]["contentText"]
        Description = inpInfo["datasetDescription"] #氣象類型
        await ctx.send(f'🌧 {Description} 訊息發送測試')
        embed=discord.Embed(title=f"🌧{Description}", description=f"{contentText}", color=0x00ffd5, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Taiwan OpenData System", icon_url="https://imgur.com/qtSQyzd.png")
        embed.add_field(name="警特報連結", value=f"[中央氣象局](https://www.cwb.gov.tw/V8/C/P/Warning/W26.html?T=202204291915)", inline=True)
        embed.set_footer(text="警特報提供：臺灣交通部中央氣象局", icon_url='https://i.imgur.com/NwLYUXr.png')
        await ctx.send(embed=embed)

    @commands.command() #-jectx 測試發布地震特報
    async def ectx(self, ctx):

        inp = jeew["records"]["earthquake"][0]
        inpInfo = inp["earthquakeInfo"]
        reportType = inp["reportType"]  #報告種類
        reportContent = inp["reportContent"]    #報告敘述
        reportweb = inp["web"]  #報告網頁
        earthquakeNo = inp["earthquakeNo"]
        location = inpInfo["epiCenter"]["location"]
        originTime = inpInfo["originTime"]
        magnitudeValue = inpInfo["magnitude"]["magnitudeValue"]
        magnitudeType = inpInfo["magnitude"]["magnitudeType"]
        cha = checkSos(magnitudeValue)
        value = inpInfo["depth"]["value"]  # 地震深度
        unit = inpInfo["depth"]["unit"]  # 深度單位
        dep = earthquake_depth(value)
        areaDesc = inp["intensity"]["shakingArea"][1]["areaDesc"]
        areaName = inp["intensity"]["shakingArea"][1]["areaName"]
        reportImageURI = inp["reportImageURI"]
        await ctx.send(f'🏚️ {reportType} 訊息發送測試')
        embed=discord.Embed(title=f"🏚️{reportType}", description=f"{reportContent}", color=0x00ffd5, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Taiwan EEW System", icon_url="https://i.imgur.com/zirawV0.png")
        embed.set_image(url=f"{reportImageURI}")
        embed.add_field(name="警特報連結", value=f"[中央氣象局]({reportweb})", inline=True)
        embed.add_field(name="編號", value=f"{earthquakeNo}", inline=True)
        embed.add_field(name="震央位置", value=f"{location}", inline=True)
        embed.add_field(name="發生時間", value=f"{originTime}", inline=True)
        embed.add_field(name="規模", value=f"{str(cha)}{magnitudeType}{magnitudeValue}", inline=True)
        embed.add_field(name="深度", value=f"{str(dep)}{value}{unit}", inline=True)
        embed.add_field(name=f"{areaDesc}", value=f"{areaName}", inline=False)
        embed.set_footer(text="警特報提供：臺灣交通部中央氣象局", icon_url='https://i.imgur.com/NwLYUXr.png')
        if int(magnitudeValue) >= 5:            
            ccr = jdata["warning"]
            await ctx.send(f"⚠️ <@&{ccr}> 芮氏5.0以上地震報告⚠️")
        
        await ctx.send(embed=embed)

def setup(bot): #註冊
    bot.add_cog(cmd_test(bot))
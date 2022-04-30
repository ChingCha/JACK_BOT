import discord
import datetime
import json
import requests

from discord.ext import commands 
from core.classes import Cog_Extension
from report.Rain import *
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

def risk_factor(dc):
    if int(dc) < 35:
        return "🔵"
    elif int(dc) >= 35 and int(dc) < 40 :
        return "🟡"
    elif int(dc) >= 40:
        return "🔴"

def WXRT(dc):
    if dc == "01":
        return "☀"
    elif dc == "02" or "03":
        return "⛅"
    elif dc == "04" or "05" or "06" or "07":
        return "☁"
    elif int(dc) >= 8 and  int(dc) <= 20 :
        return "🌧"
    elif dc == "21" or "22":
        return "⛈"
    elif dc == "23":
        return "❄"
    elif int(dc) >= 24 and  int(dc) <= 28 :
        return "🌫"
    else: return "0"

class develop(Cog_Extension):
    @commands.command() #-jping
    async def ping(self, ctx):    #ctx = context 問與答 上下文
        await ctx.send(f'機器人延遲時間：{round(self.bot.latency*1000)} ms')

    @commands.command() #-jabout
    async def about(self, ctx):
        embed=discord.Embed(title="Jack的替身使者", url="https://zh.wikipedia.org/wiki/%E6%A1%90%E4%BA%BA", description="能力介紹", color=0x00ffcc, timestamp = datetime.datetime.utcnow())
        embed.set_author(name="至尊乂JACK老大卍霸主Ω四等㊣", icon_url="https://i.imgur.com/IoKgVwa.png")
        embed.set_thumbnail(url="https://i.imgur.com/IoKgVwa.png")
        embed.set_image(url="https://memes.tw/gif/download?name=f8c2c3e8af3782606fd163b8ff6eb4e6.gif")
        embed.add_field(name="技能1：星爆氣流斬", value="強大的雙刀流技能", inline=True)
        embed.add_field(name="技能2：幫我稱十秒", value="需要隊友幫忙支援10秒", inline=True)
        embed.add_field(name="技能3：這就是MMORPG不合理的地方", value="就真的很不合理", inline=False)
        embed.add_field(name="奧義：無限課金", value="打不贏就課金", inline=False)
        embed.set_footer(text="上述技能如有跟他人雷同，純屬巧合。")
        await ctx.send(embed=embed)
    
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
        


    @commands.command()
    async def wf(self, ctx):
        APIToken = jdata['APIToken']
        APIT = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-065?Authorization={APIToken}&limit=1&offset=0&format=JSON&locationName=%E9%B3%B3%E5%B1%B1%E5%8D%80&elementName=Wx,PoP12h,T,RH&sort=time"
        t = requests.get(APIT).json()
        
        inp = t["records"]["locations"][0]["location"][0]
        descriptionPOP = inp["weatherElement"][0]["time"][0]["elementValue"][0]["value"]
        descriptionWX = inp["weatherElement"][1]["time"][0]["elementValue"][0]["value"]
        #descriptionWXI = inp["weatherElement"][1]["time"][0]["elementValue"][1]["value"]
        descriptionT = inp["weatherElement"][2]["time"][0]["elementValue"][0]["value"]
        descriptionRH = inp["weatherElement"][3]["time"][0]["elementValue"][0]["value"]
        
        cc = WXRT(descriptionT)
        DC = int(descriptionT) + int(descriptionRH)*0.1
        DCC = risk_factor(DC)
        await ctx.send(f'{str(cc)} 高雄市鳳山區天氣預報')
        embed=discord.Embed(title=f"高雄市鳳山區天氣預報", description=f"[中央氣象局](https://www.cwb.gov.tw/V8/C/W/Town/Town.html?TID=6401200)", color=0x00ffff, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Taiwan OpenData System", icon_url="https://i.imgur.com/qtSQyzd.png")
        embed.add_field(name=f"降雨機率", value=f"{descriptionPOP}%", inline=True)
        embed.add_field(name=f"天氣現象", value=f"{str(cc)}{descriptionWX}", inline=True)
        embed.add_field(name=f"溫度", value=f"{descriptionT}℃", inline=True)
        embed.add_field(name=f"相對溼度", value=f"{descriptionRH}%", inline=True)
        embed.add_field(name=f"危險係數", value=f"{str(DCC)} {str(DC)} {str(DCC)}", inline=True)
        embed.set_footer(text=f"鄉鎮預報提供：臺灣交通部中央氣象局", icon_url='https://i.imgur.com/NwLYUXr.png')

        await ctx.send(embed=embed)

def setup(bot): #註冊
    bot.add_cog(develop(bot))
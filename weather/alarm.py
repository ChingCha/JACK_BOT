import discord
import datetime
import json

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


class sets:
    __slots__ = ["checkFile", "channels", "Tags", "APIToken", "token"]

    def __init__(self, token, APIToken=None, **kwargs):
        self.checkFile = kwargs.get("checkFile", "check.json")
        self.channels = list(map(int, kwargs.get("channels", "").split()))
        self.Tags = list(map(str, kwargs.get("Tags", "").split()))
        self.APIToken = APIToken
        self.token = token

 
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

def depthSos(dc):
    if int(dc) < 70:
        return "🔴"
    elif int(dc) >= 70 and int(dc) <= 300 :
        return "🟡"
    elif int(dc) > 300:
        return "🟢"

def Description_icon(type):
    if type == "濃霧特報":
        return "🌫"
    elif type == "陸上強風特報":
        return " 🌪"
    else:
        return "🌧"

async def sosIn(channel, data, b):
    try:
        inp = b["records"]["earthquake"][0]
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
        dep = depthSos(value)
        areaDesc = inp["intensity"]["shakingArea"][1]["areaDesc"]
        areaName = inp["intensity"]["shakingArea"][1]["areaName"]
        reportImageURI = inp["reportImageURI"]
        await channel.send(f'🏚️ {reportType}')
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
        channels=jdata['warning_channels']
        if int(magnitudeValue) >= 5:            
            await channels.send(f"⚠️ @everyone 芮氏5.0以上地震報告⚠️")
        await channel.send(embed=embed)
    except Exception as err:
        print(err)

async def Rain(channel, data, r):
    try:
        inp = r["records"]["record"][0]
        inpInfo = inp["datasetInfo"]
        contentText = inp["contents"]["content"]["contentText"]
        Description = inpInfo["datasetDescription"] #氣象類型
        icon_emoji = Description_icon(Description)
        await channel.send(f'{icon_emoji} {Description} ')
        embed=discord.Embed(title=f"{icon_emoji} {Description}", description=f"{contentText}", color=0x00ffd5, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Taiwan OpenData System", icon_url="https://imgur.com/qtSQyzd.png")
        embed.add_field(name="警特報連結", value=f"[中央氣象局](https://www.cwb.gov.tw/V8/C/P/Warning/W26.html?T=202204291915)", inline=True)
        embed.set_footer(text="警特報提供：臺灣交通部中央氣象局", icon_url='https://i.imgur.com/NwLYUXr.png')       
        print("su")
        await channel.send(embed=embed)
    except Exception as err:
        print(err)
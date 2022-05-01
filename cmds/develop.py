import discord
import datetime
import json
import requests

from discord.ext import commands 
from core.classes import Cog_Extension
with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

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
        embed=discord.Embed(title="Jack的替身使者", url="https://zh.wikipedia.org/wiki/%E6%A1%90%E4%BA%BA", description="職業：⚔️雙刀流封閉者⚔️", color=0x00ffcc, timestamp = datetime.datetime.utcnow())
        embed.set_author(name="至尊乂JACK老大卍霸主Ω四等㊣", icon_url="https://i.imgur.com/y9yFNWD.png")
        embed.set_thumbnail(url="https://i.imgur.com/IoKgVwa.png")
        embed.add_field(name="🈲 星爆氣流斬 🈲", value="強大的雙刀流技能", inline=True)
        embed.add_field(name="⏱️ 幫我稱十秒 ⏱️", value="需要隊友幫忙支援10秒", inline=True)
        embed.add_field(name="⛔ 這就是MMORPG不合理的地方 ⛔", value="就真的很不合理", inline=True)
        embed.add_field(name="💸 奧義：無限課金 💸", value="打不贏就課金", inline=True)
        embed.set_footer(text="⚔️上述技能如有跟他人雷同，純屬巧合。")
        await ctx.send(embed=embed)
        await ctx.send('https://i.imgur.com/gAgdONA.gif')
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
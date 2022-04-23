import imp
import discord
from discord.ext import commands 
from core.classes import Cog_Extension
import datetime

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

def setup(bot): #註冊
    bot.add_cog(develop(bot))
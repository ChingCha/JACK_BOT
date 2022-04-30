import discord
import datetime
class sets:
    __slots__ = ["checkFile", "channels", "Tags", "APIToken", "token"]

    def __init__(self, token, APIToken=None, **kwargs):
        self.checkFile = kwargs.get("checkFile", "check.json")
        self.channels = list(map(int, kwargs.get("channels", "").split()))
        self.Tags = list(map(str, kwargs.get("Tags", "").split()))
        self.APIToken = APIToken
        self.token = token

async def Rain(channel, data, sets: sets):
    try:
        inp = data["records"]["record"][0]
        inpInfo = inp["datasetInfo"]
        contentText = inp["contents"]["content"]["contentText"]
        Description = inpInfo["datasetDescription"] #氣象類型
        await channel.send(f'🌧 {Description} 訊息發送測試')
        embed=discord.Embed(title=f"🌧{Description}", description=f"{contentText}", color=0x00ffd5, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Taiwan OpenData System", icon_url="https://imgur.com/qtSQyzd.png")
        embed.add_field(name="警特報連結", value=f"[中央氣象局](https://www.cwb.gov.tw/V8/C/P/Warning/W26.html?T=202204291915)", inline=True)
        embed.set_footer(text="警特報提供：臺灣交通部中央氣象局", icon_url='https://i.imgur.com/NwLYUXr.png')
        await channel.send(embed=embed)
    except Exception as err:
        print(err)

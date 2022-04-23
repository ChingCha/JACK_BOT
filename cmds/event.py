import discord
from discord.ext import commands 
from core.classes import Cog_Extension
import json

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class event(Cog_Extension):
    @commands.Cog.listener() #成員加入
    async def on_member_join(self, member):
        #print(f'{member} join')
        channel = self.bot.get_channel(int(jdata['lobby']))
        await channel.send(jdata['welcome_pic'])
        await channel.send(f'歡迎 {member.mention} 加入JACK堂!')
        await channel.send(f'請先看 公告區頁面\n接著在公告最下方點選表情符號自動加入身分組')

    @commands.Cog.listener()  #成員離開
    async def on_member_remove(self, member):
        #print(f'{member} leave!')
        channel = self.bot.get_channel(int(jdata['lobby']))
        await channel.send(f'{member} 離開JACK堂!')
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        keyword = ['jack','JACK','jack老大','JACK老大']
        if msg.content in keyword and msg.author != self.bot.user:
            await msg.channel.send('吵三小')

    @commands.Cog.listener() #新增身分組
    async def on_raw_reaction_add(self, data):
        print(str(data.emoji))
        if data.message_id == 967470412164390973: #指定訊息ID
            if str(data.emoji) == '⚔️':
                #print("work")
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(967460666518679572) #指定身分組ID
                await data.member.add_roles(role)
                await data.member.send(f"你取得了 {role} 身分組")
    @commands.Cog.listener() #移除身分組
    async def on_raw_reaction_remove(self, data):
        print(str(data.emoji))
        if data.message_id == 967470412164390973: #指定訊息ID
            if str(data.emoji) == '⚔️':
                #print("work")
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(967460666518679572) #指定身分組ID
                await user.remove_roles(role)
                await user.send(f"你移除了 {role} 身分組")

def setup(bot): #註冊
    bot.add_cog(event(bot))
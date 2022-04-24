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
        channel2 = self.bot.get_channel(int(jdata['post']))
        await channel.send(jdata['welcome_pic'])
        await channel.send(f'***歡迎*** {member.mention} ***加入JACK堂!*** :thumbsup: \n\n :white_check_mark: 請先看 {channel2.mention} 的內容\n\n:white_check_mark: 接著在公告最下方點選表情符號自動加入身分組')

    @commands.Cog.listener()  #成員離開
    async def on_member_remove(self, member):
        #print(f'{member} leave!')
        channel = self.bot.get_channel(int(jdata['lobby']))
        await channel.send(f':cry: {member} ***離開JACK堂!*** :cry:')
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        keyword = ['jack','JACK','jack老大','JACK老大']
        if msg.content in keyword and msg.author != self.bot.user:
            await msg.channel.send('請先儲值在與我說話')
        elif msg.content.startswith('jack') and msg.author != self.bot.user:
            await msg.channel.send(f'請先儲值在與我說話')

    @commands.Cog.listener() #新增身分組
    async def on_raw_reaction_add(self, data):
        #print(str(data.message_id))
        #print(str(data.emoji))
        if data.message_id == int(jdata['role_msg']): #指定訊息ID
            if str(data.emoji) == '⚔️':
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(int(jdata["role_brother"])) #指定身分組ID
                await data.member.add_roles(role)
                await data.member.send(f"歡迎來到JACK堂 ⚔️ {data.member.mention} \n 您已經取得了⚔️ {role} ⚔️身分組\n ⭐請保持尊重、包容、友善⭐")
            elif str(data.emoji) == '🚗':
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(int(jdata["role_car"])) #指定身分組ID
                await data.member.add_roles(role)
                await data.member.send(f"你取得了 {role} 身分組")
            elif str(data.emoji) == '<:jack_GBF_FFG:640901912866324481>':
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(int(jdata["role_GBF"])) #指定身分組ID
                await data.member.add_roles(role)
                await data.member.send(f"你取得了 {role} 身分組")
            elif str(data.emoji) == '<:jack_poe:848102597263884299>':
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(int(jdata["role_POE"])) #指定身分組ID
                await data.member.add_roles(role)
                await data.member.send(f"你取得了 {role} 身分組")
            elif str(data.emoji) == '<:jack_minecraft:848106005225406485>':
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(int(jdata["role_MC"])) #指定身分組ID
                await data.member.add_roles(role)
                await data.member.send(f"你取得了 {role} 身分組")
            elif str(data.emoji) == '<:jack_maplestory:848103098009649214>':
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(int(jdata["role_MS"])) #指定身分組ID
                await data.member.add_roles(role)
                await data.member.send(f"你取得了 {role} 身分組")
            elif str(data.emoji) == '<:jack_work2:585786773112881172>':
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(int(jdata["role_8+9"])) #指定身分組ID
                await data.member.add_roles(role)
                await data.member.send(f"你取得了 {role} 身分組")


    @commands.Cog.listener() #移除身分組
    async def on_raw_reaction_remove(self, data):
        #print(str(data.emoji))
        if data.message_id == int(jdata['role_msg']): #指定訊息ID
            if str(data.emoji) == '⚔️':
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(int(jdata["role_brother"])) #指定身分組ID               
                await user.remove_roles(role)
                await user.send(f"你移除了 {role} 身分組")
            elif str(data.emoji) == '🚗':
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(int(jdata["role_car"])) #指定身分組ID               
                await user.remove_roles(role)
                await user.send(f"你移除了 {role} 身分組")
            elif str(data.emoji) == '<:jack_GBF_FFG:640901912866324481>':
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(int(jdata["role_GBF"])) #指定身分組ID               
                await user.remove_roles(role)
                await user.send(f"你移除了 {role} 身分組")
            elif str(data.emoji) == '<:jack_poe:848102597263884299>':
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(int(jdata["role_POE"])) #指定身分組ID               
                await user.remove_roles(role)
                await user.send(f"你移除了 {role} 身分組")
            elif str(data.emoji) == '<:jack_minecraft:848106005225406485>':
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(int(jdata["role_MC"])) #指定身分組ID               
                await user.remove_roles(role)
                await user.send(f"你移除了 {role} 身分組")
            elif str(data.emoji) == '<:jack_maplestory:848103098009649214>':
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(int(jdata["role_MS"])) #指定身分組ID               
                await user.remove_roles(role)
                await user.send(f"你移除了 {role} 身分組")
            elif str(data.emoji) == '<:jack_work2:585786773112881172>':
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(int(jdata["role_8+9"])) #指定身分組ID               
                await user.remove_roles(role)
                await user.send(f"你移除了 {role} 身分組")

def setup(bot): #註冊
    bot.add_cog(event(bot))
import discord
from discord.ext import commands 
from core.classes import Cog_Extension

class error(Cog_Extension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error,commands.errors.MissingRequiredArgument):
            await ctx.send("你的指令缺少了一些參數")
        elif isinstance(error,commands.errors.CommandNotFound):
            await ctx.send("找不到你輸入的指令")
        else:
            await ctx.send("指令錯誤")

def setup(bot): #註冊
    bot.add_cog(error(bot))
from discord.ext import commands

from imgsauce.config import config

bot = commands.AutoShardedBot(
    command_prefix=[p.strip() for p in str(config.get('Bot', 'command_prefixes', fallback='-j')).split(',')],
    case_insensitive=True,
)
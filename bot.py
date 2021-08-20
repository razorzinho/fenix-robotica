import discord
from discord.ext import commands
from data import settings
client = commands.Bot(command_prefix=settings.bot_prefix, intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=settings.activity_name))

# Carregar códigos essenciais do bot antes de carregar os móudlos
client.load_extension('terminal')
client.load_extension('error_handler')
client.load_extension('extensions')
client.load_extension('nickname')
client.load_extension('help')
client.load_extension('disconnect')

client.run(settings.bot_token)
import discord
import help
from discord.ext import commands
from data import settings
intents = discord.Intents.all()

client = commands.Bot(command_prefix = settings.bot_prefix, help_command=CustomHelpCommand, intents=intents, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=settings.activity_name))
client.load_extension('error_handler')
client.load_extension('terminal')
client.load_extension('disconnect')
client.load_extension('extensions')
client.load_extension('help')

@client.event
async def on_ready():
    if client.user.name is not f'[{settings.bot_prefix}] {settings.bot_name}':
        await client.user.edit(username=f'[{settings.bot_prefix}] {settings.bot_name}')
        print('Nome do bot atualizado.')
    else:
        print('Nome do bot já está correto.')

client.run(settings.bot_token)
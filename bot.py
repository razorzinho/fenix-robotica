import discord
import os
import logging
from discord.ext import commands

<<<<<<< HEAD
file = open("./data/settings.json")
data = json.loads(file.read())
token = data["data"][0]["bot_token"]
autor = data["data"][0]["author_name"]
id_autor = data["data"][0]["author_id"]

=======
# Carregar dados principais do bot

from data import settings
modules_dir = settings.modules_dir

>>>>>>> 18138c2ff833f935cdfae193d5f7e62a68022340
intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.invites = True

<<<<<<< HEAD
client = commands.Bot(command_prefix = '?', intents = intents, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Fênix Empire Network em www.fenbrasil.net"))
=======
client = commands.Bot(command_prefix = '?', intents=intents, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Fênix Empire Network em www.fenbrasil.net"))
>>>>>>> 18138c2ff833f935cdfae193d5f7e62a68022340
client.remove_command('help')

# Comandos de carregamento, desativação e recarga dos módulos

@client.command(aliases=['carregar', 'ativar'])
async def load(ctx, extension):
    client.load_extension(f'{modules_dir}.{extension}')
    await ctx.send('Extensão carregada.')

@client.command(aliases=['descarregar', 'desativar'])
async def unload(ctx, extension):
    client.unload_extension(f'{modules_dir}.{extension}')
    await ctx.send('Extensão desativada.')

@client.command(aliases=['recarregar'])
async def reload(ctx, extension):
    client.unload_extension(f'{modules_dir}.{extension}')
    client.load_extension(f'{modules_dir}.{extension}')
    await ctx.send('Extensão recarregada.')

# Ao inicializar o bot, carregar todos os módulos presentes no diretório /modules

for filename in os.listdir('./'+modules_dir):
    if filename.endswith('.py') and filename not in settings.disabled:
        client.load_extension(f'{modules_dir}.{filename[:-3]}')

# Quando o bot estiver pronto, iniciar o loop de mudança de status: 

@client.event
async def on_ready():
    print(f'Bot {client.user} on-line. \nCriado por {settings.author_name} -> {settings.author_id}')

# Logs do terminal do bot:

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='terminal.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client.run(settings.bot_token)
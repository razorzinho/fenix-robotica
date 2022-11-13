import discord
from discord import app_commands
from data import settings
from dotenv import dotenv_values

config = dotenv_values(".env")

# Definição do bot e seus parâmetros principais:
client = commands.Bot(command_prefix=settings.bot_prefix, intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=settings.activity_name))

try:
    synced = await bot.tree.sync()
    print(f"{len(synced)} comandos sincronizados.")
except  Exception as e:
    print(e)

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    interaction.response.send_message(f"Pong! Tempo de resposta atual: `{interaction.client.latency}`")

# Carregar códigos essenciais do bot antes de carregar os móudlos
#client.load_extension('terminal')
#client.load_extension('error_handler')
#client.load_extension('extensions')
#client.load_extension('nickname')
#client.load_extension('help')
#client.load_extension('disconnect')

# Inicializar o bot. Token no arquivo /data/settings.py
client.run(config.CLIENT_TOKEN)
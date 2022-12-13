import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values
import json

file = open("./config.json")
config = json.load(file,)

env = dotenv_values(".env")

# Definição do bot e seus parâmetros principais:
client = commands.Bot(command_prefix=config["client"]["prefix"], intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=config["client"]["status"]))

client.load_extension('error_handler')
client.load_extension('extensions')
client.load_extension('disconnect')
client.load_extension('terminal')

client.run(env["CLIENT_TOKEN"])
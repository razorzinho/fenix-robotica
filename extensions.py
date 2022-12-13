import os
import discord
from discord.ext import commands
from discord import app_commands
import json

file = open("./config.json")
config = json.load(file,)

def setup(client):

# Ao inicializar o bot, carregar todos os módulos presentes no diretório /modules, exceto os marcados como desabilitados
    for filename in os.listdir('./'+config["client"]["extensions_module"]["modules_dir"]):
        if filename.endswith('.py') and filename not in settings.disabled_modules:
            await client.load_extension(f'{config["client"]["extensions_module"]["modules_dir"]}.{filename[:-3]}')
            await client.tree.sync(guild=discord.Object(id=config["client"]["guild_id"]))

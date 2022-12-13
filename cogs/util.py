import discord
from discord.ext import commands
from discord import app_commands
import json

file = open("./config.json")
config = json.load(file,)

class CLASS(commands.Cog, name='', description=''''''):

    def __init__(self, client):
        self.client = client




@client.tree.command(name="ping", description="Requisita o tempo de resposta médio da conexão.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! 🏓 Tempo de resposta atual: `{interaction.client.latency}ms`" , delete_after=5)
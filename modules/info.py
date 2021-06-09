import discord
from discord.ext import commands
from modules.storage import info
from modules.storage import cargos

class Info(commands.Cog):
    
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Info(client))

import discord
from discord.ext import commands
from discord import app_commands
import json

file = open("./config.json")
config = json.load(file,)

class CLASS(commands.Cog, name='', description=''''''):

    def __init__(self, client):
        self.client = client
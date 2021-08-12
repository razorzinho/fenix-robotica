import discord
from discord.ext import commands
from data import settings

class Help(commands.HelpCommand):

    def __init__(self, client):
        self.client = client

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'')

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)

    async def send_command_help(self, command):
        return await super().send_command_help(command)

def setup(client):
    client.add_cog(Help(client))
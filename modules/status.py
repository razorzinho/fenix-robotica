import discord
from discord.ext import commands, tasks
from modules.storage import status
delay = status.status_delay
activities = status.activity
statuses = status.statuses

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.change_status.start()

    @tasks.loop(seconds=delay)
    async def change_status(self):
        await self.client.change_presence(status=next(statuses), activity=discord.Activity(type=discord.ActivityType.playing, name=next(activities)))

def setup(client):
    client.add_cog(Status(client))
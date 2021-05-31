import discord
import json
from discord.ext import commands, tasks
from itertools import cycle
from pathlib import Path

script_location = Path(__file__).absolute().parent
file_location = script_location / 'settings' / 'config.json'
file = file_location.open()
data = json.loads(file.read())
delay = int(data["settings"][0]["tasks"][0]["status_delay"])

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=delay)
    async def change_status(self):
        activity = cycle([data["settings"][0]["activities"][0]])
        status = cycle([data["settings"][0]["status"][0]])
        type = cycle([data["settings"][0]["type"][0]])
        print(activity + status)
        await self.client.change_presence(status=next(status), activity=next(type)+"("+next(activity)+")")
        self.client.change_status.start

def setup(client):
    client.add_cog(Status(client))
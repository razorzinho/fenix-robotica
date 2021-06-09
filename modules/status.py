import discord
from discord.ext import commands, tasks
<<<<<<< HEAD
from itertools import cycle
from pathlib import Path

script_location = Path(__file__).absolute().parent
file_location = script_location / 'settings' / 'config.json'
file = file_location.open()
data = json.loads(file.read())
delay = int(data["settings"][0]["tasks"][0]["status_delay"])
=======
from modules.storage import status
delay = status.status_delay
activities = status.activity
statuses = status.statuses
>>>>>>> 18138c2ff833f935cdfae193d5f7e62a68022340

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.change_status.start()

    @tasks.loop(seconds=delay)
    async def change_status(self):
<<<<<<< HEAD
        activity = cycle([data["settings"][0]["activities"][0]])
        status = cycle([data["settings"][0]["status"][0]])
        type = cycle([data["settings"][0]["type"][0]])
        print(activity + status)
        await self.client.change_presence(status=next(status), activity=next(type)+"("+next(activity)+")")
        self.client.change_status.start
=======
        await self.client.change_presence(status=next(statuses), activity=discord.Activity(type=discord.ActivityType.playing, name=next(activities)))
>>>>>>> 18138c2ff833f935cdfae193d5f7e62a68022340

def setup(client):
    client.add_cog(Status(client))
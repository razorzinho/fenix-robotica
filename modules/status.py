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

    # Lista de status do Bot - dependem do estado dos servidores:
status = cycle([
    # Mensagem do site
    #discord.Status.online,
    # Jailbreak on-line + IP:
    discord.Status.online,
    # Jailbreak offline:
    discord.Status.do_not_disturb,
    # Jailbreak em manutenção:
    discord.Status.do_not_disturb,
    # Jailbreak reiniciando:
    discord.Status.idle,
    # Zombie Plague on-line + IP:
    discord.Status.online,
    # Zombie Plague offline:
    discord.Status.do_not_disturb,
    # Zombie Plague em manutenção:
    discord.Status.do_not_disturb,
    # Zombie Plague reiniciando:
    discord.Status.idle,
    # TTT on-line + IP:
    discord.Status.online,
    # TTT offline:
    discord.Status.do_not_disturb,
    # TTT em manutenção:
    discord.Status.do_not_disturb,
    # TTT reiniciando:
    discord.Status.idle
    ])
    
    # A seguinte lista contém as atividades respectivas de cada status:
activity = cycle([
    #discord.Streaming('Fênix Empire Network', 'fenbrasil.net', 'Acesse aqui o nosso site!'),
    discord.Game('Jailbreak on-line em ip.fenbrasil:27050'),
    discord.Game('Jailbreak offline.'),
    discord.Game('Jailbreak em manutenção.'),
    discord.Game('Jailbreak reiniciando.'),
    discord.Game('Zombie Plague on-line em ip.fenbrasil:27016'),
    discord.Game('Zombie Plague offline.'),
    discord.Game('Zombie Plague em manutenção.'),
    discord.Game('Zombie Plague reiniciando.'),
    discord.Game('TTT on-line em ip.fenbrasil:27015'),
    discord.Game('TTT offline.'),
    discord.Game('TTT em manutenção.'),
    discord.Game('TTT reiniciando.')
])

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=delay)
    async def change_status(self):
        await self.client.change_presence(status=next(status), activity=next(activity)) 
        self.client.change_status.start()

def setup(client):
    client.add_cog(Status(client))
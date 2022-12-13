import discord
from discord.ext import commands
from discord import app_commands
import json

file = open("./config.json")
config = json.load(file,)

class CLASS(commands.Cog, name='', description=''''''):

    def __init__(self, client):
        self.client = client







@client.tree.command(name="clear", description="Apaga a quantidade de mensagens requisitada no canal em que é utilizado.")
@app_commands.describe(quantidade="Quantas mensagens devo apagar neste canal?")
@app_commands.checks.has_any_role(1041422699039297570, 1041445230571958292, 1041417371417596006, 1047497834263494667, 976493314113175645, 721503210405363733, 954879451190145106, 1021082331215319112)
async def clear(interaction: discord.Interaction, quantidade: int):
    if quantidade <= 0:
        await interaction.response.send_message(f"{interaction.user.mention}, você deve definir uma quantidade válida de mensagens (1 ou mais).", delete_after=5)
    await interaction.channel.purge(limit=quantidade)
    await interaction.channel.send(f"{interaction.user.mention}, apaguei {quantidade} mensagens neste canal.", delete_after=5)
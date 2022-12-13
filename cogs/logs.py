import discord
from discord.ext import commands
from discord import app_commands
import json

file = open("./config.json")
config = json.load(file,)

class CLASS(commands.Cog, name='', description=''''''):

    def __init__(self, client):
        self.client = client


@client.event
async def on_ready():
    print(f"{client.user.name} está on-line!")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} comandos sincronizados.")
    except Exception as e:
        print(e)



@client.event
async def on_member_remove(member):
    channel = await member.guild.fetch_channel(config[f"{member.guild.id}"]["join_module"]["log_channel_id"])
    await channel.send(content=f"O usuário {member.mention} deixou o servidor.")

@client.tree.command(name="clear_reactions", description="Remove todas as reações de uma mensagem.")
@app_commands.describe(id_canal="Qual o ID do canal?", id_mensagem="Qual é o ID da mensagem?")
@app_commands.checks.has_any_role(1041422699039297570, 1041445230571958292, 1041417371417596006, 1047497834263494667, 976493314113175645, 721503210405363733, 954879451190145106, 1021082331215319112)
async def clear_reactions(interaction: discord.Interaction, id_canal: str, id_mensagem: str):
    channel = await interaction.guild.fetch_channel(id_canal)
    message = await channel.fetch_message(id_mensagem)
    if not channel:
        await interaction.response.send_message("Você deve inserir um ID de canal válido.", delete_after=5)
    if not message:
        await interaction.response.send_message("Você deve inserir um ID de mensagem válido.", delete_after=5)
    await message.clear_reactions()
    await interaction.response.send_message("Removi todas as reações da mensagem requisitada.", delete_after=5)

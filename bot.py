import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values
import json

file = open("./config.json")
config = json.load(file,)

env = dotenv_values(".env")

# Definição do bot e seus parâmetros principais:
client = commands.Bot(command_prefix=config["client"]["prefix"], intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=config["client"]["status"]))

@client.event
async def on_ready():
    print(f"{client.user.name} está on-line!")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} comandos sincronizados.")
    except Exception as e:
        print(e)

@client.event
async def on_member_join(member):
    join_roles = []
    channel = await client.fetch_channel(config["join_module"]["log_channel_id"])
    guild_roles = await member.guild.fetch_roles()
    for role in guild_roles:
        if role.id in config["join_module"]["roles_id"]:
            join_roles.append(role)
    for role in join_roles:
        await member.add_roles(role, "Cargos básicos ao entrar no servidor.", True)
    await channel.send(f"Dei os cargos iniciais para {member.mention}.")
    print(f"Cargos adicionados a {member.name}#{memeber.discriminator} com sucesso.")

#@client.event
#async def on_reaction_add(reaction, user):
    # if reaction.message.id not (in config.messages.languages.message and in config.messages.tech.message):
    #     return
    # else:
    #     if not user.get_role()

#@client.event
#async def on_reaction_remove(reaction, user):
    # if reaction.message.id not (in config.messages.languages.message and in config.messages.tech.message):
    #     return
    # else:
        
@client.tree.command(name="clear", description="Apaga a quantidade de mensagens requisitada no canal em que é utilizado.")
@app_commands.describe(quantidade="Quantas mensagens devo apagar neste canal?")
async def clear(interaction: discord.Interaction, quantidade: int):
    await interaction.channel.purge(quantidade)
    await interaction.response.send_message(f"{interaction.user.mention} , apaguei {quantidade} mensagens neste canal.")


@client.tree.command(name="ping", description="Requisita o tempo de resposta médio da conexão.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Tempo de resposta atual: `{interaction.client.latency}`", 
    ephemeral=True)

@client.tree.command(name="react", description="Cria as reações na mensagem configurada de acordo com os cargos registrados.")
async def react(interaction: discord.Interaction):
    for i in config["messages"]:
        channel = await client.fetch_channel(config["messages"][i]["channel"])
        message = await channel.fetch_message(config["messages"][i]["message"])
        for n in config["reaction_roles"][i]:
            await message.add_reaction(config["reaction_roles"][i][n]["role_id"])

client.run(env["CLIENT_TOKEN"])
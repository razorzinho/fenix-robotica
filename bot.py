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
    channel = await member.guild.fetch_channel(config["join_module"]["log_channel_id"])
    guild_roles = await member.guild.fetch_roles()
    for role in guild_roles:
        if role.id in config["join_module"]["roles_id"]:
            join_roles.append(role)
    await member.edit(roles=join_roles, reason="Atribuir cargos iniciais do servidor.")
    await channel.send(content=f"Dei os cargos iniciais para {member.mention}.")

@client.event
async def on_member_remove(member):
    channel = await member.guild.fetch_channel(config["join_module"]["log_channel_id"])
    await channel.send(content=f"O usuário {member.mention} deixou o servidor.")

@client.event
async def on_raw_reaction_add(payload):
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    if member.bot:
        return
    channel_id = payload.channel_id
    message_id = payload.message_id
    if channel_id != config["messages"]["languages"]["channel_id"] and channel_id != config["messages"]["tech"]["channel_id"]:
        return
    if message_id != config["messages"]["languages"]["message_id"] and message_id != config["messages"]["tech"]["message_id"]:
        return
    for cat in config["messages"]:
        if config["messages"][cat]["message_id"] == message_id:
            value = cat
            print(value)
            break
    if not cat:
        return
    role = config["reaction_roles"][value][payload.emoji.name]
    cargo = guild.get_role(role["role_id"])
    print(member.get_role(role["role_id"]))
    if not cargo:
        return
    if not member.get_role(role["role_id"]):
        await member.add_roles(cargo, reason=f"{member.name} requisitou a adição do cargo por meio de reação.")
        
@client.event
async def on_raw_reaction_remove(payload):
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    if member.bot:
        return
    channel_id = payload.channel_id
    message_id = payload.message_id
    if channel_id != config["messages"]["languages"]["channel_id"] and channel_id != config["messages"]["tech"]["channel_id"]:
        return
    if message_id != config["messages"]["languages"]["message_id"] and message_id != config["messages"]["tech"]["message_id"]:
        return
    for cat in config["messages"]:
        if config["messages"][cat]["message_id"] == message_id:
            value = cat
            print(value)
            break
    if not cat:
        return
    role = config["reaction_roles"][value][payload.emoji.name]
    cargo = guild.get_role(role["role_id"])
    print(member.get_role(role["role_id"]))
    if not cargo:
        return
    if member.get_role(role["role_id"]):
        await member.remove_roles(cargo, reason=f"{member.name} requisitou a remoção do cargo por meio de reação.")

@client.tree.command(name="clear", description="Apaga a quantidade de mensagens requisitada no canal em que é utilizado.")
@app_commands.describe(quantidade="Quantas mensagens devo apagar neste canal?")
async def clear(interaction: discord.Interaction, quantidade: int):
    if quantidade <= 0:
        await interaction.response.send_message(f"{interaction.user.mention}, você deve definir uma quantidade válida de mensagens (1 ou mais).", delete_after=5)
    await interaction.channel.purge(limit=quantidade)
    await interaction.channel.send(f"{interaction.user.mention}, apaguei {quantidade} mensagens neste canal.", delete_after=5)

@client.tree.command(name="clear_reactions", description="Remove todas as reações de uma mensagem.")
@app_commands.describe(id_canal="Qual o ID do canal?", id_mensagem="Qual é o ID da mensagem?")
async def clear_reactions(interaction: discord.Interaction, id_canal: str, id_mensagem: str):
    channel = await interaction.guild.fetch_channel(id_canal)
    message = await channel.fetch_message(id_mensagem)
    if not channel:
        await interaction.response.send_message("Você deve inserir um ID de canal válido.", delete_after=5)
    if not message:
        await interaction.response.send_message("Você deve inserir um ID de mensagem válido.", delete_after=5)
    await message.clear_reactions()
    await interaction.response.send_message("Removi todas as reações da mensagem requisitada.", delete_after=5)

@client.tree.command(name="ping", description="Requisita o tempo de resposta médio da conexão.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! 🏓 Tempo de resposta atual: `{round(interaction.client.latency)*1000}`" , delete_after=5)

@client.tree.command(name="react", description="Cria as reações na mensagem configurada de acordo com os cargos registrados.")
async def react(interaction: discord.Interaction):
    for i in config["messages"]:
        channel = await client.fetch_channel(config["messages"][i]["channel_id"])
        message = await channel.fetch_message(config["messages"][i]["message_id"])
        for n in config["reaction_roles"][i]:
            emoji = await interaction.guild.fetch_emoji(config["reaction_roles"][i][n]["emoji_id"])
            await message.add_reaction(emoji)
    await interaction.channel.send("Reações correspondentes aos cargos criadas nas mensagens.", delete_after=5)

client.run(env["CLIENT_TOKEN"])
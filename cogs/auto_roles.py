import discord
from discord.ext import commands
from discord import app_commands
import json

file = open("./config.json")
config = json.load(file,)

class CLASS(commands.Cog, name='', description=''''''):

    def __init__(self, client):
        self.client = client


    # for guild_id in client.guilds:
    #     if not config["messages"][{guild_id}]:
    #         continue
    #     guildid = int(guild_id)
    #     guild = await client.fetch_guild(guildid)
    #     channel = await guild.fetch_channel(config["messages"][guild_id]["channel_id"])
    #     if not channel:
    #         print(f"Canal inválido ou inexistente no servidor {guild.name} ({guild.id})")
    #         continue
    #     if not message:
    #         print(f"Mensagem inválida ou inexistente no servidor {guild.name} ({guild.id})")
    #         print("Tentando criar uma nova...")

@client.event
async def on_member_join(member):
    join_roles = []
    channel = await member.guild.fetch_channel(config[f"{member.guild.id}"]["join_module"]["log_channel_id"])
    guild_roles = await member.guild.fetch_roles()
    if not member.bot:
        for role in guild_roles:
            join_roles.append(role)
        await member.edit(roles=join_roles, reason="Atribuir cargos iniciais do servidor.")
        await channel.send(content=f"Dei os cargos iniciais para {member.mention}.")
    else:
        for role in guild_roles:
            if role.id in config[f"{member.guild.id}"]["join_module"]["bot_roles_id"]:
                join_roles.append(role)
        await member.edit(roles=join_roles, reason="Atribuir cargos iniciais do servidor.")
        await channel.send(content=f"Dei os cargos iniciais para {member.mention}.")    


@client.event
async def on_raw_reaction_add(payload):
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    if member.bot:
        return
    channel_id = payload.channel_id
    message_id = payload.message_id
    if channel_id not in config["messages"][f"{guild.id}"][cat]["channel_id"]:
        return
    if message_id not in config["messages"][f"{guild.id}"][cat]["message_id"]:
        return
    for cat in config["messages"]:
        if config["messages"][f"payload.guild_id"][cat]["message_id"] == message_id:
            value = cat
            break
    if not cat:
        return
    role = config["reaction_roles"][f"{payload.guild_id}"][value][payload.emoji.name]
    cargo = guild.get_role(role["role_id"])
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
    for cat in config["messages"][payload.guild_id]:
        if config["messages"][f"payload.guild_id"][cat]["message_id"] == message_id:
            value = cat
            break
    if not cat:
        return
    role = config["reaction_roles"][f"payload.guild_id"][value][payload.emoji.name]
    cargo = guild.get_role(role["role_id"])
    if channel_id not in config["messages"][f"{guild.id}"][cat]["channel_id"]:
        return
    if message_id not in config["messages"][f"{guild.id}"][cat]["message_id"]:
        return
    if not cargo:
        return
    if member.get_role(role["role_id"]):
        await member.remove_roles(cargo, reason=f"{member.name} requisitou a remoção do cargo por meio de reação.")

@client.tree.command(name="react", description="Cria as reações na mensagem configurada de acordo com os cargos registrados.")
@app_commands.checks.has_any_role(1041422699039297570, 1041445230571958292, 1041417371417596006, 1047497834263494667, 976493314113175645, 721503210405363733, 954879451190145106, 1021082331215319112)
async def react(interaction: discord.Interaction):
    for i in config["messages"][interaction.guild_id]:
        channel = await client.fetch_channel(config[f"{interaction.guild_id}"]["messages"][i]["channel_id"])
        message = await channel.fetch_message(config[f"{interaction.guild_id}"]["messages"][i]["message_id"])
        for n in config["reaction_roles"][f"{interaction.guild_id}"][i]:
            emoji = await interaction.guild.fetch_emoji(config["reaction_roles"][f"{interaction.guild_id}"][i][n]["emoji_id"])
            await message.add_reaction(emoji)
    await interaction.channel.send("Reações correspondentes aos cargos criadas nas mensagens.", delete_after=5)
import discord
from discord import app_commands
from discord.ext import tasks, commands
from dotenv import dotenv_values
from sourceserver.sourceserver import SourceServer
from datetime import datetime
import pytz
from sourceserver.exceptions import SourceError
import json

file = open("./config.json")
config = json.load(file,)

env = dotenv_values(".env")

os = {
    [76]: "Linux",
    [108]: "Linux",
    [119]: "Windows",
    [109]: "MacOS",
    [111]: "MacOS"
}

games = {
    [4000]: "Garry's Mod",
    [730]: "Counter Strike: Global Offensive"
}

gamemodes = {
    "Trouble in Terrorist Town": "Trouble in Terrorist Town",
    "Counter-Strike: Global Offensive": "Jailbreak"
}

type = {
    [68]: "Servidor dedicado",
    [100]: "Servidor dedicado",
    [108]: "Servidor não dedicado",
    [112]: "SourceTV"
}

visibility = {
    [0]: "Público",
    [1]: "Protegido por senha"
}

# "131.196.196.197:27410": {
#                         "channel_id": 1053508047709937766,
#                         "info_embed_colour": 11337728,
#                         "info_message_id": 1055948500157878342,
#                         "players_embed_colour": 11337728,
#                         "players_message_id": 0
#                     }

# Definição do bot e seus parâmetros principais:
client = commands.Bot(command_prefix=config["client"]["prefix"], intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=config["client"]["status"]))

servers = {}

# Loop de atualização e monitoramento dos servidores
@tasks.loop(seconds=config["query_module"]["delay"]) #config["query_module"]["delay"])
async def status_update():
    print(servers)
    tz = pytz.timezone("America/Sao_Paulo")
    time = datetime.now(tz=tz)
    timestamp = datetime.strftime(time, "%H:%M:%S - %d/%m/%Y")
    for guild in client.guilds:
        print(guild)
        guild_id = str(guild.id)
        if guild_id not in config["query_module"]:
            continue
        for server_ip in config["query_module"][guild_id]["constant_status"]["servers"]:
            print(server_ip)
            if server_ip not in servers:
                try:
                    try:
                        servers[server_ip] = SourceServer(server_ip)
                    except SourceError as e:
                        print("Informações do servidor inválidas, pulando")
                        print(e)
                        servers.pop(server_ip)
                        continue
                    if "channel_id" not in config["query_module"][guild_id]["constant_status"]["servers"][server_ip]:
                        print("Não há um canal configurado para realizar a atividade de atualização de status de servidores. Saindo do loop.")
                        break
                    info_embed = discord.Embed(colour=config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["info_embed_colour"], description=config["query_module"]["server_info_fields"]["info_description"])
                    info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_name"], value=servers[server_ip].info["name"], inline=False)
                    info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_game_name"], value=f'{games[str(servers[server_ip].info["id"])]} ({servers[server_ip].info["id"]})', inline=False)
                    info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_ping"], value=servers[server_ip].ping(), inline=False)
                    info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_gamemode"], value=gamemodes[servers[server_ip].info["game"]], inline=False)
                    info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_map"], value=servers[server_ip].info["map"], inline=False)
                    info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_os"], value=os[str(servers[server_ip].info["environment"])], inline=False)
                    info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_type"], value=type[str(servers[server_ip].info["server_type"])], inline=False)
                    info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_visibility"], value=visibility[str(servers[server_ip].info["visibility"])], inline=False)
                    if games[str(servers[server_ip].info["id"])] == "Garry's Mod":
                        info_embed.set_image(url=f'https://fenixempire.net.br/loading-page/images/maps/{servers[server_ip].info["map"]}.jpg')
                    info_embed.set_footer(text=f"Última atualização: {timestamp}")
                    # if servers[server_ip].info["game"] == "Counter-Strike: Global Offensive":
                    #     info_embed.add_field(name=f'Jogadores on-line: {servers[server_ip].info["players"]}/{servers[server_ip].info["max_players"]}', value="\u200b", inline=False)
                    # else:
                    players_embed = discord.Embed(colour=config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["players_embed_colour"], title=f'Jogadores on-line: {servers[server_ip].info["players"]}/{servers[server_ip].info["max_players"]}', description=config["query_module"]["server_info_fields"]["players_description"])
                    players_list = "Nenhum jogador on-line atualmente."
                    count, players = servers[server_ip].getPlayers()
                    if count > 0:
                        players_list = ""
                        for player in players:
                            if player[1] == "":
                                players_list += f"Jogador se conectando" + "\n"
                                continue
                            players_list += f"{player[1]} | {player[2]} | {float('{:.1f}'.format(player[3]/60/60))}" + "\n"
                    players_embed.add_field(name="\u200b", value=f"```{players_list}```", inline=False)
                    players_embed.set_footer(text=f"Última atualização: {timestamp}")
                    channel = await guild.fetch_channel(config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["channel_id"])
                    async for message in channel.history(limit=200):
                        if message.id == config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["info_message_id"]:
                            continue 
                        if message.id == config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["players_message_id"]:
                            continue
                        await message.delete()
                        print("Apaguei mensagens indevidas no canal de status fixo de servidores.")
                    if "info_message_id" not in config["query_module"][guild_id]["constant_status"]["servers"][server_ip] or config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["info_message_id"] == 0:
                        print("Não há uma mensagem atualmente configurada para informações gerais do servidor")
                        await channel.send(embed=info_embed)
                    else:
                        info_message = await channel.fetch_message(config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["info_message_id"])
                        await info_message.edit(embed=info_embed)
                    if "players_message_id" not in config["query_module"][guild_id]["constant_status"]["servers"][server_ip] or config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["players_message_id"] == 0:
                        # if servers[server_ip].info["game"] == "Counter-Strike: Global Offensive":
                        #     return
                        print("Não há uma mensagem atualmente configurada para informações específicas dos jogadores")
                        await channel.send(embed=players_embed)
                    else:
                        # if servers[server_ip].info["game"] == "Counter-Strike: Global Offensive":
                        #     return
                        players_message = await channel.fetch_message(config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["players_message_id"])
                        await players_message.edit(embed=players_embed)
                    if server_ip == config["query_module"]["client_status_server_ip"]:
                        await client.change_presence(status=discord.Status.online, activity=discord.Game(f'✅ {servers[server_ip].info["map"]} | {count}/{servers[server_ip].info["max_players"]}'))
                        print("Status do bot atualizado.")
                except Exception as e:
                    print("Algo deu errado. Interrompendo. Será retomado no próximo ciclo.")
                    print(e)
                    continue
            else:
                if "channel_id" not in config["query_module"][guild_id]["constant_status"]["servers"][server_ip]:
                    print("Não há um canal configurado para realizar a atividade de atualização de status de servidores. Saindo do loop.")
                    break
                info_embed = discord.Embed(colour=config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["info_embed_colour"], description=config["query_module"]["server_info_fields"]["info_description"])
                info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_name"], value=servers[server_ip].info["name"], inline=False)
                info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_game_name"], value=f'{games[str(servers[server_ip].info["id"])]} ({servers[server_ip].info["id"]})', inline=False)
                info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_ping"], value=servers[server_ip].ping(), inline=False)
                info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_gamemode"], value=gamemodes[servers[server_ip].info["game"]], inline=False)
                info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_map"], value=servers[server_ip].info["map"], inline=False)
                info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_os"], value=os[str(servers[server_ip].info["environment"])], inline=False)
                info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_type"], value=type[str(servers[server_ip].info["server_type"])], inline=False)
                info_embed.add_field(name=config["query_module"]["server_info_fields"]["server_visibility"], value=visibility[str(servers[server_ip].info["visibility"])], inline=False)
                if games[str(servers[server_ip].info["id"])] == "Garry's Mod":
                    info_embed.set_image(url=f'https://fenixempire.net.br/loading-page/images/maps/{servers[server_ip].info["map"]}.jpg')
                info_embed.set_footer(text=f"Última atualização: {timestamp}")
                # if servers[server_ip].info["game"] == "Counter-Strike: Global Offensive":
                #     info_embed.add_field(name=f'Jogadores on-line: {servers[server_ip].info["players"]}/{servers[server_ip].info["max_players"]}', value="\u200b", inline=False)
                # else:
                players_embed = discord.Embed(colour=config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["players_embed_colour"], title=f'Jogadores on-line: {servers[server_ip].info["players"]}/{servers[server_ip].info["max_players"]}', description=config["query_module"]["server_info_fields"]["players_description"])
                players_list = "Nenhum jogador on-line atualmente."
                count, players = servers[server_ip].getPlayers()
                if count > 0:
                    players_list = ""
                    for player in players:
                        if player[1] == "":
                            players_list += f"Jogador se conectando" + "\n"
                            continue
                        players_list += f"{player[1]} | {player[2]} | {float('{:.1f}'.format(player[3]/60/60))}" + "\n"
                players_embed.add_field(name="\u200b", value=f"```{players_list}```", inline=False)
                players_embed.set_footer(text=f"Última atualização: {timestamp}")
                channel = await guild.fetch_channel(config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["channel_id"])
                async for message in channel.history(limit=200):
                    if message.id == config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["info_message_id"]:
                        continue 
                    if message.id == config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["players_message_id"]:
                        continue
                    await message.delete()
                    print("Apaguei mensagens indevidas no canal de status fixo de servidores.")
                if "info_message_id" not in config["query_module"][guild_id]["constant_status"]["servers"][server_ip] or config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["info_message_id"] == 0:
                    print("Não há uma mensagem atualmente configurada para informações gerais do servidor")
                    await channel.send(embed=info_embed)
                else:
                    info_message = await channel.fetch_message(config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["info_message_id"])
                    await info_message.edit(embed=info_embed)
                if "players_message_id" not in config["query_module"][guild_id]["constant_status"]["servers"][server_ip] or config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["players_message_id"] == 0:
                    # if servers[server_ip].info["game"] == "Counter-Strike: Global Offensive":
                    #     return
                    print("Não há uma mensagem atualmente configurada para informações específicas dos jogadores")
                    await channel.send(embed=players_embed)
                else:
                    # if servers[server_ip].info["game"] == "Counter-Strike: Global Offensive":
                    #     return
                    players_message = await channel.fetch_message(config["query_module"][guild_id]["constant_status"]["servers"][server_ip]["players_message_id"])
                    await players_message.edit(embed=players_embed)
                if server_ip == config["query_module"]["client_status_server_ip"]:
                    await client.change_presence(status=discord.Status.online, activity=discord.Game(f'✅ {servers[server_ip].info["map"]} | {count}/{servers[server_ip].info["max_players"]}'))
                    print("Status do bot atualizado.")

@client.event
async def on_ready():
    print(f"{client.user.name} está on-line!")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} comandos sincronizados.")
        status_update.start()
    except Exception as e:
        print(e)
    # for guild in client.guilds:
    #     guild_id = str(guild.id)
    #     if guild_id not in config["messages"]:
    #         continue
    #     for cat in config["messages"][guild_id]:
    #         channel = await guild.fetch_channel(config["messages"][guild_id][cat]["channel_id"])
    #         message = await channel.fetch_message(config["messages"][guild_id][cat]["message_id"])
    #         if not channel:
    #             print(f"Canal inválido ou inexistente no servidor {guild.name} ({guild.id})")
    #             continue
    #         print("Editando mensagem válida atual")
    #         embed = discord.Embed(colour=config["messages"][guild_id][cat]["colour"], title=config["messages"][guild_id][cat]["title"], type='rich', url=None, description=config["messages"][guild_id][cat]["description"])
    #         embed.add_field(name="NOTA:", value=config["messages"][guild_id][cat]["items_title"], inline=True)
    #         # if "fields" in config["messages"][guild_id][cat]:
    #         #     for field in config["messages"][guild_id][cat]["fields"]:
    #         #         embed.add_field(name=config["messages"][guild_id][cat]["fields"][field]["name"], value=config["messages"][guild_id][cat]["fields"][field]["value"], inline=config["messages"][guild_id][cat]["fields"][field]["inline"])
    #         #     return
    #         for item in config["reaction_roles"][guild_id][cat]:
    #             emoji_id = config["reaction_roles"][guild_id][cat][item]["emoji_id"]
    #             msg_emoji = await guild.fetch_emoji(emoji_id)
    #             embed.add_field(name=msg_emoji, value=f'**{config["reaction_roles"][guild_id][cat][item]["description"]}**', inline=False)
    #         #embed.add_field(name=config["messages"][guild_id][cat]["items_title"], value=description_field, inline=True)
    #         await message.edit(content=None, embed=embed)
    #         if "message_id" in config["messages"][guild_id][cat] and config["messages"][guild_id][cat]["message_id"] != 0:
    #             valid_message = await channel.fetch_message(config["messages"][guild_id][cat]["message_id"])
    #         else:
    #             print(f"Mensagem inválida para a categoria {cat} ou inexistente no servidor {guild.name} ({guild.id})")
    #             print("Tentando criar uma nova...")
    #             async for message in channel.history(limit=100):
    #                 if message.id != config["messages"][guild_id][cat]["message_id"]:
    #                     await message.delete()
    #             embed = discord.Embed(colour=config["messages"][guild_id][cat]["colour"], title=config["messages"][guild_id][cat]["title"], type='rich', url=None, description=config["messages"][guild_id][cat]["description"])
    #             if "fields" in config["messages"][guild_id][cat]:
    #                 for field in config["messages"][guild_id][cat]["fields"]:
    #                     embed.add_field(name=config["messages"][guild_id][cat]["fields"][field]["name"], value=config["messages"][guild_id][cat]["fields"][field]["value"], inline=config["messages"][guild_id][cat]["fields"][field]["inline"])
    #                 return
    #             # description_field = ""
    #             # for item in config["reaction_roles"][guild_id][cat]:
    #             #     emoji_id = config["reaction_roles"][guild_id][cat][item]["emoji_id"]
    #             #     msg_emoji = await guild.fetch_emoji(emoji_id)
    #             #     description_field += f'{msg_emoji} = **{config["reaction_roles"][guild_id][cat][item]["description"]}**\n'
    #             # message_content = config["messages"][guild_id][cat]["items_title"] + "\n"
    #             # message_content += description_field
    #             # await channel.send(embed=embed) #valid_embed = await channel.send(embed=embed)
    #             # message = await channel.send(content=message_content) #valid_message = await channel.send(content=message_content)
    #         for item in config["reaction_roles"][guild_id][cat]:
    #             emoji_id = config["reaction_roles"][guild_id][cat][item]["emoji_id"]
    #             emoji = await guild.fetch_emoji(emoji_id)
    #             await message.add_reaction(emoji)
                
@client.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    join_roles = []
    channel = await member.guild.fetch_channel(config["join_module"][guild_id]["log_channel_id"])
    if not member.bot:
        for role_id in config["join_module"][guild_id]["roles_id"]:
            role = member.guild.get_role(role_id)
            join_roles.append(role)
        await member.edit(roles=join_roles, reason="Atribuir cargos iniciais do servidor.")
        await channel.send(content=f"Dei os cargos iniciais para {member.mention}.")
    else:
        for role in config["join_module"][guild_id]["bot_roles_id"]:
            role = member.guild.get_role(role_id)
            join_roles.append(role)
        await member.edit(roles=join_roles, reason="Atribuir cargos iniciais do servidor.")
        await channel.send(content=f"Dei os cargos iniciais para {member.mention}.")

@client.event
async def on_member_remove(member):
    channel = await member.guild.fetch_channel(config["join_module"][f"{member.guild.id}"]["log_channel_id"])
    await channel.send(content=f"O usuário {member.mention} deixou o servidor.")

@client.event
async def on_raw_reaction_add(payload):
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    if member.bot:
        return
    message_id = payload.message_id
    value = False
    for cat in config["messages"][f"{payload.guild_id}"]:
        if config["messages"][f"{payload.guild_id}"][cat]["message_id"] == message_id:
            value = cat
            break
    if not cat:
        return
    if not value:
        print("Mensagem ou canal inválido(s). Ignorando reação.")
        return
    role = config["reaction_roles"][f"{payload.guild_id}"][value][payload.emoji.name]
    cargo = guild.get_role(role["role_id"])
    if not cargo:
        print("Cargo inválido para adicionar. Verificar configuração.")
        return
    if not member.get_role(role["role_id"]):
        await member.add_roles(cargo, reason=f"{member.name} requisitou a adição do cargo {cargo.name} por meio de reação.")
        
@client.event
async def on_raw_reaction_remove(payload):
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    if member.bot:
        return
    message_id = payload.message_id
    value = False
    for cat in config["messages"][f"{payload.guild_id}"]:
        if config["messages"][f"{payload.guild_id}"][cat]["message_id"] == message_id:
            value = cat
            break
    if not cat:
        return
    if not value:
        print("Mensagem ou canal inválido(s). Ignorando reação.")
        return
    role = config["reaction_roles"][f"{payload.guild_id}"][value][payload.emoji.name]
    cargo = guild.get_role(role["role_id"])
    if not cargo:
        return
    if member.get_role(role["role_id"]):
        await member.remove_roles(cargo, reason=f"{member.name} requisitou a remoção do cargo {cargo.name} por meio de reação.")

@client.tree.command(name="role", description="Dá ou remove o cargo especificado ao membro especificado ou si mesmo.")
@app_commands.describe(cargo="Qual cargo deverá ser alterado?", membro="Qual usuário deverá receber/perder o cargo?")
@app_commands.checks.has_any_role(1041422699039297570, 1041445230571958292, 1041417371417596006, 1047497834263494667, 976493314113175645, 721503210405363733, 954879451190145106, 1021082331215319112)
async def role(interaction: discord.Interaction, cargo: discord.Role, membro: discord.Member):
    if not membro:
        membro = interaction.user
    for role in membro.roles:
        if cargo == role:
            remove = True
            break
        remove = False
    if remove:
        await interaction.response.send_message(f"Removi o cargo {cargo.name} de {membro.mention}.", delete_after=5)
        await membro.remove_roles(cargo, reason=f"{interaction.user} removeu o cargo {cargo.name} de {membro.name}#{membro.discriminator}.")
    else:
        await interaction.response.send_message(f"Dei o cargo {cargo.name} para {membro.mention}.", delete_after=5)
        await membro.add_roles(cargo, reason=f"{interaction.user} deu o cargo {cargo.name} para {membro.name}#{membro.discriminator}.")

@client.tree.command(name="clear", description="Apaga a quantidade de mensagens requisitada no canal em que é utilizado.")
@app_commands.describe(quantidade="Quantas mensagens devo apagar neste canal?")
@app_commands.checks.has_any_role(1041422699039297570, 1041445230571958292, 1041417371417596006, 1047497834263494667, 976493314113175645, 721503210405363733, 954879451190145106, 1021082331215319112)
async def clear(interaction: discord.Interaction, quantidade: int):
    if quantidade <= 0:
        await interaction.response.send_message(f"{interaction.user.mention}, você deve definir uma quantidade válida de mensagens (1 ou mais).", delete_after=5)
    await interaction.channel.purge(limit=quantidade)
    await interaction.channel.send(f"{interaction.user.mention}, apaguei {quantidade} mensagens neste canal.", delete_after=5)

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

@client.tree.command(name="ping", description="Requisita o tempo de resposta médio da conexão.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! 🏓 Tempo de resposta atual: `{interaction.client.latency}ms`" , delete_after=5)

@client.tree.command(name="clear_roles", description="Limpa TODOS os cargos específicos de interações deste servidor. UTILIZAR SOMENTE SE TIVER CERTEZA.")
@app_commands.checks.has_any_role(1041422699039297570, 1041445230571958292, 1041417371417596006, 1047497834263494667, 976493314113175645, 721503210405363733, 954879451190145106, 1021082331215319112)#config["moderation"]["allowed_roles_id"])
async def clear_roles(interaction: discord.Interaction):
    await interaction.response.send_message("Reconfigurando cargos do servidor. Atualizando membros. Isto poderá levar **bastante** tempo.", delete_after=8)
    should_remove = []
    should_add = []
    for usr in interaction.guild.members:
        print(f"{usr.name}#{usr.discriminator}")
        for role_id in config["join_module"][f"{interaction.guild_id}"]["roles_id"]:
            if not usr.get_role(role_id):
                print(f"ID do cargo a ser adicionado: {role_id}")
                role = interaction.guild.get_role(role_id)
                #should_add.append(role)
                print(role)
                await usr.add_roles(role, reason=f"{usr.name} não tem cargos iniciais do servidor.", atomic=True)
                continue
        for cat in config["reaction_roles"][f"{interaction.guild_id}"]:
            print(cat)
            for obj in config["reaction_roles"][f"{interaction.guild_id}"][cat]:
                print(obj)
                for aux in config["reaction_roles"][f"{interaction.guild_id}"][cat][obj]:
                    if aux == "role_id":
                        role_id = config["reaction_roles"][f"{interaction.guild_id}"][cat][obj][aux]
                        print(f"ID do cargo a ser removido: {role_id}")
                        if usr.get_role(role_id):
                            role = interaction.guild.get_role(role_id)
                            #should_remove.append(role)
                            await usr.remove_roles(role, reason=f"{usr.name} tem cargos de interação, e foi requisitada a remoção de todos.", atomic=True)
                            print(role)
                            continue
        print(f"lista de cargos a serem adicionados: {should_add}")
        print(f"lista de cargos a serem removidos: {should_remove}")
        
        

@client.tree.command(name="react", description="Cria as reações na mensagem configurada de acordo com os cargos registrados.")
@app_commands.checks.has_any_role(1041422699039297570, 1041445230571958292, 1041417371417596006, 1047497834263494667, 976493314113175645, 721503210405363733, 954879451190145106, 1021082331215319112)
async def react(interaction: discord.Interaction):
    await interaction.channel.send("Reações correspondentes aos cargos criadas nas mensagens.", delete_after=5)

# @client.tree.command(name="status", description="Envia as informações do servidor requisitado.")
# @app_commands.describe(servidor="Qual servidor requisitar?")
# @app_commands.choices(servidor=[
#     app_commands.Choice(name="Gmod TTT", value=config["query_module"]["status"]["server_ip"]["ttt"]),
#     app_commands.Choice(name="CSGO Jailbreak", value=config["query_module"]["status"]["server_ip"]["jailbreak"]),
# ])
# async def status(interaction: discord.Interaction, servidor: app_commands.Choice[str]):
#     pass

@client.tree.command(name="shutdown", description="Desfaz a conexão do bot com a API do Discord de forma segura e rápida.")
@app_commands.checks.has_any_role(1041422699039297570, 1041445230571958292, 1041417371417596006, 1047497834263494667, 976493314113175645, 721503210405363733, 954879451190145106, 1021082331215319112)
async def shutdown(interaction: discord.Interaction):
    await interaction.response.send_message("Desligando...", ephemeral=True)
    await client.close()

client.run(env["CLIENT_TOKEN"])
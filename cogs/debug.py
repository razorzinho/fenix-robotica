import discord
from discord.ext import commands
from discord import app_commands
import json

file = open("./config.json")
config = json.load(file,)

class Debug(commands.Cog, name='Desenvolvimento e testes', description='''Módulo de testes e desenvolvimento. Restrito e, geralmente, desabilitado.'''):

    def __init__(self, client):
        self.client = client


@app_commands.command(name='carregar', description='Carrega extensões do BOT. Somente acessível por Programadores')
@app_commands.checks.has_any_role(config["client"]["extensions_module"]["allowed_roles_id"])
@app_commands.describe(extension="Extensão a ser carregada.")
async def load(self, interaction: discord.Interaction, extension):
    client.load_extension(f'{config["client"]["extensions_module"]["modules_dir"]}.{extension}')
    await interaction.response.send_message(f'Extensão **{str(extension)}** carregada.', delete_after=5)

@app_commands.command(name='descarregar', description='Desabilita extensões ativas do BOT. Somente acessível por Programadores')
@app_commands.checks.has_any_role(config["client"]["extensions_module"]["allowed_roles_id"])
@app_commands.describe(extension="Extensão a ser descarregada.")
async def unload(self, interaction: discord.Interaction, extension):
        client.unload_extension(f'{config["client"]["extensions_module"]["modules_dir"]}.{extension}')
        await interaction.response.send_message(f'Extensão **{str(extension)}** desativada.', delete_after=5)

@app_commands.command(name='recarregar', description='Recarrega extensões ativas do BOT. Somente acessível por Programadores')
@app_commands.checks.has_any_role(config["client"]["extensions_module"]["allowed_roles_id"])
@app_commands.describe(extension="Extensão a ser recarregada. (desativa e ativa a extensão)")
async def reload(self, interaction: discord.Interaction, extension):
        client.unload_extension(f'{config["client"]["extensions_module"]["modules_dir"]}.{extension}')
        client.load_extension(f'{config["client"]["extensions_module"]["modules_dir"]}.{extension}')
        await interaction.response.send_message(f'Extensão **{str(extension)}** recarregada.', delete_after=5)

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
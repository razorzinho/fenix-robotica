import discord
import os
import logging
from discord.ext import commands

# Carregar dados principais do bot

from modules.storage import cargos
from data import settings
bot_token = settings.bot_token
author = settings.author_name
author_id = settings.author_id
modules_dir = settings.modules_dir

intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.invites = True
intents.reactions = True

client = commands.Bot(command_prefix = settings.bot_prefix, intents=intents, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=settings.activity_name))
client.remove_command('help')

# Comandos de carregamento, desativação e recarga dos módulos

@client.command(aliases=['carregar', 'ativar'])
@commands.has_any_role(*cargos.admin_roles_id)
async def load(ctx, extension):
    client.load_extension(f'{modules_dir}.{extension}')
    await ctx.send(f'Extensão {str(extension)} carregada.')

@client.command(aliases=['descarregar', 'desativar'])
@commands.has_any_role(*cargos.admin_roles_id)
async def unload(ctx, extension):
    client.unload_extension(f'{modules_dir}.{extension}')
    await ctx.send(f'Extensão {str(extension)} desativada.')

@client.command(aliases=['recarregar'])
@commands.has_any_role(*cargos.admin_roles_id)
async def reload(ctx, extension):
    client.unload_extension(f'{modules_dir}.{extension}')
    client.load_extension(f'{modules_dir}.{extension}')
    await ctx.send(f'Extensão {str(extension)} recarregada.')

# Ao inicializar o bot, carregar todos os módulos presentes no diretório /modules, exceto os marcados como desabilitados

for filename in os.listdir('./'+modules_dir):
    if filename.endswith('.py') and filename not in settings.disabled_modules:
        client.load_extension(f'{modules_dir}.{filename[:-3]}')

# Quando o bot estiver pronto, enviar mensagem no terminal.

@client.event
async def on_ready():
    print(f'Bot {client.user} on-line. \nCriado por {settings.author_name} -> {settings.author_id}')

# Cuidar de erros relacionados a comandos
#@client.event
#async def on_command_error(ctx, error):
    # Todas as funções abaixo estão gerando erro de tipo. 
#    if isinstance(error, commands.MissingRole(missing_role=None)):
#        await ctx.message.reply(f"Ops, parece que você não tem o cargo necessário para utilizar este comando, {ctx.message.author.name}.")
#    elif isinstance(error, commands.MissingAnyRole(missing_roles=None)):
#        await ctx.message.reply(f"Ops, parece que você não tem o cargo necessário para utilizar este comando, {ctx.message.author.name}.")
#    elif isinstance(error, commands.MissingRequiredArgument()):
#        await ctx.message.reply(f"Ops, parece que você errou o formato deste comando, {ctx.message.author.name}. Utilize o comando ?help comando para saber como se utiliza.")
#    elif isinstance(error, commands.MissingPermissions()):
#        await ctx.message.reply(f"Ops, parece que você não tem a permissão necessária para este comando, {ctx.message.author.name}.")
#    elif isinstance(error, commands.MemberNotFound()):
#        await ctx.message.reply(f"O membro requisitado não foi encontrado. Talvez você tenha errado o formato do comando? \nUse ?help <comando> para ver como utilizá-lo ou garanta que está usando o nome ou mencionando o membro.")
#    elif isinstance(error, commands.CommandNotFound()):
#        await ctx.message.reply(f"Parece que o comando que você está tentando utilizar não existe. Use o comando ?help para ver a lista completa de comandos.")
#    elif isinstance(error, commands.ExtensionAlreadyLoaded()):
#        await ctx.message.reply(f"A extensão que você tentou carregar já está habilitada.")
#    elif isinstance(error, commands.ExtensionNotFound()):
#        await ctx.message.reply(f"Esta extensão não existe.")
#    elif isinstance(error, commands.ExtensionNotLoaded()):
#        await ctx.message.reply(f"A extensão que você tentou desabilitar não está habilitada.")
#    elif isinstance(error, commands.ExtensionFailed()):
#        await ctx.message.reply(f"A extensão requisitada está gerando um erro:\n```{Exception}```")
#    return


# Logs do terminal do bot:

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='terminal.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client.run(settings.bot_token)
import discord
import os
import logging
from datetime import datetime
from discord.ext import commands
from modules.storage import logs

# Carregar dados principais do bot

from modules.storage import cargos
from data import settings
bot_token = settings.bot_token
author = settings.author_name
author_id = settings.author_id
modules_dir = settings.modules_dir

intents = discord.Intents.all()

client = commands.Bot(command_prefix = settings.bot_prefix, intents=intents, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=settings.activity_name))
client.remove_command('help')

# Comandos de carregamento, desativação e recarga dos módulos

@client.command(aliases=['ajuda', 'comandos'], help='Comando de ajuda do BOT. Lista e explica todos os comandos e coisas importantes sobre o funcionamento do mesmo.')
@commands.guild_only()
async def help(ctx):
    pfp = ctx.author.avatar_url
    embed = discord.Embed(colour=settings.help_embed_colour)
    embed.set_author(name=settings.embed_title, icon_url=pfp)
    embed.set_footer(text='Quaisquer outras dúvidas, fale com um membro Staff.', icon_url=ctx.guild.icon_url)
    await ctx.reply(embed=embed)

@client.command(aliases=['carregar', 'ativar'], help='Carrega módulos do BOT. Somente acessível por Administradores Chefe')
@commands.has_any_role(cargos.admin_roles_id[0])
async def load(ctx, extension):
    client.load_extension(f'{modules_dir}.{extension}')
    await ctx.send(f'Extensão **{str(extension)}** carregada.')

@client.command(aliases=['descarregar', 'desativar'], help='Desabilita módulos ativos do BOT. Somente acessível por Administradores Chefe')
@commands.has_any_role(cargos.admin_roles_id[0])
async def unload(ctx, extension):
    client.unload_extension(f'{modules_dir}.{extension}')
    await ctx.send(f'Extensão **{str(extension)}** desativada.')

@client.command(aliases=['recarregar'], help='Recarrega módulos ativos do BOT. Somente acessível por Administradores Chefe')
@commands.has_any_role(cargos.admin_roles_id[0])
async def reload(ctx, extension):
    client.unload_extension(f'{modules_dir}.{extension}')
    client.load_extension(f'{modules_dir}.{extension}')
    await ctx.send(f'Extensão **{str(extension)}** recarregada.')

# Comando de desativar o bot de forma segura; NÃO FECHAR O TERMINAL, SOMENTE DESLIGÁ-LO POR ESTE COMANDO.

@client.command()
@commands.has_role(cargos.admin_roles_id[0])
async def kill(ctx, *, reason='Sem motivo.'):
    cor = logs.bot_logout_colour
    logs_channel = client.get_channel(logs.bot_logs_channel_id)
    now = datetime.now()
    horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
    embed = discord.Embed(colour=cor)
    embed.set_author(name=client.user.name, url='https://fenbrasil.net/panel/discord', icon_url=client.user.avatar_url)
    embed.add_field(name='Desativação do BOT', value=f'BOT desligado por {ctx.author.mention}\n**Motivo:** {reason}', inline=False)
    embed.set_footer(text=f'{horario}', icon_url=client.user.avatar_url)
    logs_channel.send(embed=embed)
    await logs_channel.send(embed=embed)
    await ctx.send('Desligando...')
    await client.close()

# Ao inicializar o bot, carregar todos os módulos presentes no diretório /modules, exceto os marcados como desabilitados

for filename in os.listdir('./'+modules_dir):
    if filename.endswith('.py') and filename not in settings.disabled_modules:
        client.load_extension(f'{modules_dir}.{filename[:-3]}')

# Cuidar de erros relacionados a comandos
@client.event
async def on_command_error(ctx, error):
    logs_channel = client.get_channel(logs.bot_logs_channel_id)
    error = error.original
    if isinstance(error, commands.MissingRole):
        await ctx.reply(f"Ops, parece que você não tem o cargo necessário para utilizar este comando, {ctx.author.name}.")
    elif isinstance(error, commands.MissingAnyRole):
        await ctx.reply(f"Ops, parece que você não tem o cargo necessário para utilizar este comando, {ctx.author.name}.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Ops, parece que você errou o formato deste comando, {ctx.author.name}. Utilize o comando ?help comando para saber como se utiliza.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply(f"Ops, parece que você não tem a permissão necessária para este comando, {ctx.author.name}.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.reply(f"O membro requisitado não foi encontrado. Talvez você tenha errado o formato do comando? \nUse ?help <comando> para ver como utilizá-lo ou garanta que está usando o nome ou mencionando o membro.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"Parece que o comando que você está tentando utilizar não existe. Use o comando ?help para ver a lista completa de comandos.")
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.reply(f"O módulo que você tentou carregar já está habilitado.")
    elif isinstance(error, commands.ExtensionNotFound):
        await ctx.reply(f"Este módulo não existe.")
    elif isinstance(error, commands.ExtensionNotLoaded):
        await ctx.reply(f"O módulo que você tentou desabilitar não está habilitado.")
    elif isinstance(error, commands.ExtensionFailed):
        await ctx.reply(f"O módulo **{ctx.message.content[-4:]}** está gerando erros e não pôde ser habilitado. Vide logs. Marquei você no canal.")
        await logs_channel.send(f"{ctx.author.mention} O módulo **{ctx.message.content[-4:]}** está gerando um erro:\n```{error}```")

# Logs do terminal do bot:

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='terminal.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client.run(settings.bot_token)
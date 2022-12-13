import discord
from discord.ext import commands
from datetime import datetime
from modules.storage import cargos, logs
from data.settings import bot_prefix

def setup(client):

    # Comando de desativar o bot de forma segura; NÃO FECHAR O TERMINAL, SOMENTE DESLIGÁ-LO POR ESTE COMANDO.
    @app_commands.command(aliases=['desligar', 'desconectar'], hiddden=True, help=f'\"{bot_prefix}kill *motivo*\" Me desliga pelo motivo especificado. Somente Programadores Sênior podem utilizá-lo.')
    @app_commands.checks.has_role(cargos.admin_roles_id[0])
    async def kill(ctx, *, reason='Sem motivo.'):
        cor = logs.bot_logout_colour
        logs_channel = client.get_channel(logs.bot_logs_channel_id)
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        embed = discord.Embed(colour=cor)
        embed.set_author(name=client.user.name, url='https://fenbrasil.net/panel/discord', icon_url=client.user.avatar_url)
        embed.add_field(name='Desativação do BOT', value=f'BOT desligado por {ctx.author.mention}\n**Motivo:** {reason}', inline=False)
        embed.set_footer(text=f'{horario}', icon_url=client.user.avatar)
        logs_channel.send(embed=embed)
        await logs_channel.send(embed=embed)
        await ctx.send('Desligando...')
        await client.close()
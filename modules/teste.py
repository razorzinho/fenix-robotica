import discord
from discord.ext import commands
from data import settings
title = settings.embed_title

class Teste(commands.Cog, name='Teste', description='''Categoria de comandos para testes do bot. Não possui quaisquer comandos de real utilidade aos membros do Discord.'''):

    def __init__(self, client):
        self.client = client

    # Comandos
    @commands.command(aliases=['ping_pong', 'teste'], help='Informa o ping atual de resposta do bot.', usage=f'{settings.bot_prefix}ping', hidden=True)
    @commands.guild_only()
    async def ping(self, ctx):
        await ctx.reply(f'Pong! :ping_pong: \n**Ping médio:** `{round(self.client.latency*1000)} ms`')

    @commands.command(aliases=['repetir', 'repita', 'diga'], help='Faz a Nyx enviar uma mensagem copiando a frase utilizada no comando.', usage=f'{settings.bot_prefix}echo *frase*')
    @commands.guild_only()
    async def echo(self, ctx, arg):
        await ctx.send(arg)

def setup(client):
    client.add_cog(Teste(client))
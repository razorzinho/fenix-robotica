import discord
from discord.ext import commands
from data import settings
title = settings.embed_title
from modules.storage import teste
avatar_roles = teste.avatar_roles

class Teste(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Comandos
    @commands.command(aliases=['ping', 'teste'])
    async def ping_pong(self, ctx):
        await ctx.message.reply(f'Pong! :ping_pong: \n**Ping médio:** `{round(self.client.latency*1000)} ms`')

    @commands.command(name="avatar", help="Envia a foto de perfil de um usuário.")
    @commands.has_any_role(teste.avatar_roles)
    async def avatar(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        pfp = member.avatar_url
        icon = ctx.guild.icon_url
        embed=discord.Embed(color=0xff0000)
        embed.set_author(name=f"Avatar de {member}", url=pfp)
        embed.set_image(url=pfp)
        embed.set_footer(text=f"Pedido por {ctx.author.icon_url}", icon_url=icon)
        await ctx.send(embed=embed)

    @commands.command(aliases=['repita', 'diga'])
    async def repetir(self, ctx, arg):
        await ctx.send(arg)

def setup(client):
    client.add_cog(Teste(client))
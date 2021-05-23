import discord
from discord.ext import commands


class Teste(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Comandos
    @commands.command(aliases=['ping', 'teste'])
    async def ping_pong(self, ctx):
        await ctx.send(f'Pong! :ping_pong: \n**Ping médio:** `{round(self.client.latency*1000)} ms`')

    @commands.command(name="avatar", help="Envia a foto de perfil de um usuário.")
    async def avatar(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.message.author
        url = member.avatar_url
        embed=discord.Embed(color=0xff0000)
        embed.set_author(name="Fênix Empire Network Brasil", url="https://fenbrasil.net")
        embed.set_thumbnail(url=url)
        embed.add_field(name=f"{ctx.message.author},",value=f"este é o avatar de {member.mention} ", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['repita', 'diga'])
    async def repetir(self, ctx, arg):
        await ctx.send(arg)

def setup(client):
    client.add_cog(Teste(client))
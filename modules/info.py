import discord
from data import settings
from discord.ext import commands
from datetime import datetime
from modules.storage import info, cargos

class Info(commands.Cog, name='Informativo', description='''Comandos de informações gerais sobre o nosso servidor.'''):
    
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['servidor'], help='Exibe informações sobre o servidor do Discord.', usage=f'{settings.bot_prefix}server')
    @commands.guild_only()
    async def server(self, ctx):
        embed=discord.Embed(color=info.welcome_colour, description='Informações sobre este servidor:')
        embed.set_author(name=ctx.guild.name, url=settings.url, icon_url=ctx.guild.icon.url)
        embed.set_footer(text=f'Informações requisitadas por {ctx.author}. | Data: {datetime.now().strftime("às %H:%M:%S em %d/%m/%Y")}', icon_url=ctx.author.avatar.url)
        if ctx.guild.banner:
            embed.set_thumbnail(ctx.guild.banner.url)
        embed.add_field(name='Dono do servidor:', value=ctx.guild.owner, inline=False)
        embed.add_field(name='Data de criação do servidor:', value=ctx.guild.created_at.__format__("às %H:%M:%S em %d/%m/%Y"), inline=False)
        embed.add_field(name='Contagem de membros:', value=ctx.guild.member_count, inline=False)
        embed.add_field(name='Região do servidor:', value=ctx.guild.region, inline=False)
        embed.add_field(name='Canal de regras:', value=ctx.guild.rules_channel.mention, inline=False)
        embed.add_field(name='Canal de avisos públicos:', value=ctx.guild.public_updates_channel.mention, inline=False)
        embed.add_field(name='Contagem de boosts:', value=len(ctx.guild.premium_subscribers), inline=False)
        embed.add_field(name='Cargo intrínseco ao bot:', value=ctx.guild.self_role.mention, inline=False)
        #embed.add_field(name=':', value=ctx.guild., inline=False)
        #embed.add_field(name=':', value=ctx.guild., inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pfp', 'foto'], help='Envia a foto de perfil de um usuário.', usage=f'{settings.bot_prefix}avatar *@membro*')
    @commands.guild_only()
    @commands.has_any_role(cargos.member_role_id)
    async def avatar(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author
        user = await self.client.fetch_user(member.id)
        if user.accent_color:
            embed=discord.Embed(color=user.accent_color.value, description=f'Comando de avatar requisitado por {ctx.author.mention}')
        else:
            embed=discord.Embed(color=info.welcome_colour, description=f'Comando de avatar requisitado por {ctx.author.mention}')
        embed.set_author(name=f'Avatar de {user}', url=ctx.author.avatar.url)
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['perfil', 'conta', 'sobre'], help='Exibe informações gerais sobre o membro mencionado.', usage=f'{settings.bot_prefix}')
    @commands.guild_only()
    @commands.has_any_role(cargos.member_role_id)
    async def profile(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author
        user = await self.client.fetch_user(member.id)
        if user.accent_color:
            embed=discord.Embed(color=user.accent_color.value, description=f'Comando requisitado por {ctx.author.mention}:')
        else:
            embed=discord.Embed(color=info.rules_colour, description='Comando de informação de usuários:')
        embed.set_author(name=f'Dados da conta do Discord de {user}', url=settings.url, icon_url=member.avatar.url)
        embed.set_thumbnail(url=user.avatar.url)
        if user.banner:
            embed.set_image(url=user.banner.url) 
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.author.avatar.url)
        embed.add_field(name='Nome e discriminador:', value=user, inline=False)
        embed.add_field(name='ID da conta:', value=user.id, inline=False)
        embed.add_field(name='Data de criação da conta:', value=user.created_at.strftime("às %H:%M:%S em %d/%m/%Y"), inline=False)
        embed.add_field(name='Data de entrada neste servidor:', value=member.joined_at.strftime("às %H:%M:%S em %d/%m/%Y"), inline=False)
        isbot = 'Não'
        if user.bot: 
            isbot = 'Sim' 
        embed.add_field(name='É um bot?', value=isbot)
        embed.add_field(name='Cargos:', value=', '.join(map(str,member.roles)), inline=False)
        embed.add_field(name='Cargo mais alto na hierarquia:', value=member.top_role.mention)
        if member.premium_since:
            embed.add_field(name='Dá boost no servidor desde:', value=member.premium_since.strftime("às %H:%M:%S em %d/%m/%Y"))
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Info(client))
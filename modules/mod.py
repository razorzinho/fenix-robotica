import discord
from discord.ext import commands
from modules.storage import cargos
from data import settings
title = settings.embed_title
url = settings.url
admin = cargos.admin_roles_id[0]

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role(admin)
    async def clear(self, ctx, amount=0):
        if amount==0:
            await ctx.send('**Você deve especificar a quantidade de mensagens a serem apagadas, ' + ctx.author.mention +'.**', delete_after=5.0)
        else:
            await ctx.channel.purge(limit=amount+1)
            if amount==1:
                await ctx.send(f'**Uma mensagem foi apagada.**', delete_after=3)
            else:
                await ctx.send(f'**{amount} mensagens foram apagadas.**', delete_after=3) 

    @clear.error 
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.channel.purge(limit=1)
            await ctx.send(f'**Você não tem permissão para usar este comando, {ctx.author.mention}.**\nVocê precisa do cargo Admin.', delete_after=4.0)

    @commands.command()
    @commands.has_role(admin)
    async def kick(self, ctx, member : discord.Member, *, reason):
        # Mensagem de aviso ao membro que foi punido:
        autor = ctx.message.author
        autor_pfp = autor.avatar_url
        footer = ctx.guild.icon_url
        cor = 0xff0000
        embed=discord.Embed(color=cor)
        embed.set_author(name=title, url=url, icon_url=autor_pfp)
        embed.add_field(name="Você foi expulso do servidor pelo motivo:", value=reason ,inline=False)
        embed.add_field(name="Quem te expulsou: ", value=autor.mention, inline=True)
        embed.set_footer(text="Você tem direito a recorrer esta punição em nosso site.", icon_url=footer)
        await member.send(embed=embed)
        await member.kick(reason=reason)
        await ctx.send(f'O usuário {member.mention} foi expulso do servidor.')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.channel.purge(limit=1)
            await ctx.send(f'**Você não tem permissão para usar este comando, {ctx.author.mention}.**', delete_after=4.0)
        elif isinstance(error, commands.MissingRequiredArgument()):
            await ctx.send(f'**{ctx.message.author.mention}, você deve especificar quem será expulso e o motivo.**', delete_after=5.0)

    @commands.command()
    @commands.has_role(admin)
    async def ban(self, ctx, member:discord.Member, *, reason):
        autor = ctx.message.author
        pfp_autor = autor.avatar_url
        footer = ctx.guild.icon_url
        cor = 0xff0000
        embed=discord.Embed(color=cor)
        embed.set_author(name=title, icon_url=pfp_autor)
        embed.add_field(name="Você foi banido do servidor pelo motivo:", value=reason ,inline=False)
        embed.add_field(name="Quem te baniu: ", value=autor.mention, inline=True)
        embed.set_footer(text="Você tem direito a recorrer esta punição em nosso site.", icon_url=footer)
        await member.send(embed=embed)
        await member.ban(reason=reason)
        await ctx.send(f'O usuário {member.mention} foi banido do servidor.')
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.channel.purge(limit=1)
            await ctx.send('**Você não tem permissão para usar este comando.**', delete_after=5.0)

    @commands.command()
    @commands.has_role(admin)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
<<<<<<< HEAD
            autor = ctx.message.author
=======
>>>>>>> 18138c2ff833f935cdfae193d5f7e62a68022340
            await ctx.send(f'O usuário {user.mention} foi desbanido do servidor.')
            return

    @unban.error
    async def unban_error(self, ctx, error):
<<<<<<< HEAD
        if isinstance(error, commands.MissingPermissions):
=======
        if isinstance(error, commands.MissingRole):
>>>>>>> 18138c2ff833f935cdfae193d5f7e62a68022340
            await ctx.channel.purge(limit=1)
            await ctx.send(f'**Você não tem permissão para usar este comando, {ctx.author.mention}.**', delete_after=5.0)
        elif  isinstance(error, commands.MissingRequiredArgument()):
            await ctx.send(f'**{ctx.message.author.mention}, você deve especificar o nome do usuário que será desbanido.**', delete_after=5.0)

def setup(client):
    client.add_cog(Mod(client))
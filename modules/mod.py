import discord
from discord.ext import commands

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True, manage_channels=True, kick_members=True)
    async def clear(self, ctx, amount=0):
        if amount==0:
            await ctx.send('**Você deve especificar a quantidade de mensagens a serem apagadas, ' + ctx.message.author.mention +'.**', delete_after=5.0)
        else:
            await ctx.channel.purge(limit=amount+1)
            if amount==1:
                await ctx.send(f'**Uma mensagem foi apagada.**', delete_after=2.5)
            else:
                await ctx.send(f'**{amount} mensagens foram apagadas.**', delete_after=2.5)  

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason):
        # Mensagem de aviso ao membro que foi punido:
        autor = ctx.message.author
        icon = ctx.guild.icon_url
        cor = 0xff0000
        url = "https://fenbrasil.net"
        embed=discord.Embed(color=cor)
        embed.set_author(name="Fênix Empire Network Brasil", url=url)
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Você foi expulso do servidor pelo motivo:", value=reason ,inline=False)
        embed.add_field(name="Quem te expulsou: ", value=autor, inline=True)
        embed.set_footer(text="Você tem direito a recorrer esta punição em nosso site.")
        await member.send(embed=embed)
        await member.kick(reason=reason)
        await ctx.send(f'O usuário {member.mention} foi expulso do servidor.')
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.purge(limit=1)
            await ctx.send(f'**Você não tem permissão para usar este comando, {ctx.author.mention}.**', delete_after=4.0)
        elif isinstance(error, commands.MissingRequiredArgument()):
            await ctx.send(f'**{ctx.message.author.mention}, você deve especificar quem será expulso e o motivo.**', delete_after=5.0)

    @commands.command()
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason):
        autor = ctx.message.author
        icon = ctx.guild.icon_url
        cor = 0xff0000
        embed=discord.Embed(color=cor)
        embed.set_author(name="Fênix Empire Network Brasil")
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Você foi banido do servidor pelo motivo:", value=reason ,inline=False)
        embed.add_field(name="Quem te baniu: ", value=autor, inline=True)
        embed.set_footer(text="Você tem direito a recorrer esta punição em nosso site.")
        await member.send(embed=embed)
        await member.ban(reason=reason)
        await ctx.send(f'O usuário {member.mention} foi banido do servidor.')
    
    @ban.error
    async def ban_error(self, ctx, error, reason):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.purge(limit=1)
            await ctx.send('**Você não tem permissão para usar este comando.**', delete_after=5.0)
        elif isinstance(error, commands.MissingRequiredArgument(reason)):
            await ctx.send('**Você deve especificar quem será banido e o motivo.**', delete_after=5.0)

    @commands.command()
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            autor = ctx.message.author
            user_id = self.client.get_user(user.id)
            user_dm = self.client.fetch_user(user_id)
            icon = ctx.guild.icon_url
            cor = 0xff0000
            url = "https://fenbrasil.net"
            embed=discord.Embed(color=cor)
            embed.set_author(name="Fênix Empire Network Brasil", url=url)
            embed.set_thumbnail(url=icon)
            embed.add_field(name="Você foi desbanido do servidor.", value="Você pode usar o comando ativo do servidor para retornar.",inline=False)
            embed.add_field(name="Você foi desbanido por ", value=autor, inline=True)
            embed.set_footer(text="Quaisquer dúvidas, entre em nosso site.")
            await user_dm.send(embed=embed)
            await ctx.send(f'O usuário {user.mention} foi desbanido do servidor.')
            return

    #@unban.error
    #async def unban_error(self, ctx, error):
    #    if isinstance(error, commands.MissingPermissions):
    #        await ctx.channel.purge(limit=1)
    #        await ctx.send(f'**Você não tem permissão para usar este comando, {ctx.author.mention}.**', delete_after=5.0)
    #    elif  isinstance(error, commands.MissingRequiredArgument()):
    #        await ctx.send(f'**{ctx.message.author.mention}, você deve especificar o nome do usuário que será desbanido.**', delete_after=5.0)

def setup(client):
    client.add_cog(Mod(client))
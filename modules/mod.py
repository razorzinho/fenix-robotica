import discord
import os
from discord.ext import commands
from modules.storage import cargos
from modules.storage import logs
from datetime import datetime
from data import settings
title = settings.embed_title
url = settings.url
admin = cargos.admin_roles_id

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(*admin)
    async def clear(self, ctx, amount=0):
        logs_channel = self.client.get_channel(logs.message_logs_channel_id)
        if amount==0:
            await ctx.message.reply(f'**Você deve especificar a quantidade de mensagens a serem apagadas, {ctx.author.name}.**', delete_after=5.0)
        elif amount < 0:
            emoji = ':thinking:'
            await ctx.message.reply(f'**Você não pode apagar um número negativo de mensagens, {ctx.author.name} {emoji}**', delete_after=5.0)
        if amount==1:   
                await ctx.channel.purge(limit=1) 
                await ctx.message.reply('Por que você está usando clear para uma única mensagem?', delete_after=5.0)
        else:
            cor = logs.message_deleted_colour
            pfp = ctx.author.avatar_url
            icon = ctx.guild.icon_url
            now = datetime.now()
            horario = now.strftime("%H:%M:%S-%d:%m:%Y")
            autor = ctx.author.name
            arquivo = f'mensagens_{ctx.channel.name}_{horario}_por_{autor}.log'
            with open(arquivo, 'w', encoding='utf-8') as log:
                #print(f'Arquivo {arquivo} gerado.') // Usado para testes
                async for message in ctx.channel.history(limit=amount, oldest_first=False):
                    data_mensagem = message.created_at
                    log.writelines(f'[{data_mensagem}] - ({message.author.id}) - {message.author.name}: {message.content} ({message.attachments})\n')
            await ctx.channel.purge(limit=amount+1)
            embed = discord.Embed(colour=cor)
            embed.set_author(name='Comando clear utilizado', icon_url=pfp)
            embed.add_field(name='Utilizado por:', value=ctx.author.mention, inline=False)
            embed.add_field(name='Quantidade de mensagens apagadas:', value=amount, inline=False)
            embed.add_field(name='Mensagens apagadas:', value='Log salvo no arquivo enviado abaixo:', inline=False)
            embed.set_footer(text=settings.embed_title, icon_url=icon)
            await logs_channel.send(embed=embed)
            file = discord.File('./'+arquivo)
            await logs_channel.send(file=file)
            os.remove('./'+arquivo)

    @clear.error 
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.channel.purge(limit=1)
            await ctx.send(f'**Você não tem permissão para usar este comando, {ctx.author.mention}.**\nVocê precisa do cargo Admin.', delete_after=4.0)

    @commands.command()
    @commands.has_any_role(*admin)
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
    @commands.has_any_role(*admin)
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
    @commands.has_any_role(*admin)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'O usuário {user.mention} foi desbanido do servidor.')
            return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.channel.purge(limit=1)
            await ctx.send(f'**Você não tem permissão para usar este comando, {ctx.author.mention}.**', delete_after=5.0)
        elif  isinstance(error, commands.MissingRequiredArgument()):
            await ctx.send(f'**{ctx.message.author.mention}, você deve especificar o nome do usuário que será desbanido.**', delete_after=5.0)

def setup(client):
    client.add_cog(Mod(client))
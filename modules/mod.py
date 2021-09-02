import discord
import os
from discord.ext import commands
from modules.storage import cargos
from modules.storage import logs
from datetime import datetime
from data import settings
prefix = settings.bot_prefix
title = settings.embed_title
url = settings.url
admin = cargos.admin_roles_id

class Mod(commands.Cog, name='Moderação', description='''Comandos especiais de uso administrativo. Servem com intuito de moderar e organizar o servidor, bem como punir membros. Somente acessíveis por Administradores+'''):

    def __init__(self, client):
        self.client = client

    # Apagar mensagens enviadas em canais restritos por usuários que não sejam bots ou não venham de webhooks:
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if not message.author.bot and message.channel.id in logs.not_messegeable and message.webhook_id is None:
            logs_channel = self.client.get_channel(logs.moderation_logs_channel_id)
            embed = discord.Embed(colour=logs.message_deleted_colour)
            embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar.url)
            embed.add_field(name='Mensagem enviada em canal restrito', value='Já foi removida, informações abaixo:', inline=False)
            embed.add_field(name='Autor da mensagem:', value=message.author.mention, inline=False)
            embed.add_field(name='Conteúdo da mensagem:', value=f'```{message.content}```', inline=False)
            embed.add_field(name='Anexos da mensagem:', value=message.attachments, inline=False)
            embed.add_field(name='Canal da mensagem:', value=message.channel.mention, inline=False)
            embed.set_footer(text=f'{message.guild.name} | {message.created_at}', icon_url=message.guild.icon.url)
            await logs_channel.send(embed=embed)
            await message.delete()

    # Comando de limpeza; apaga a quantidade especificada de mensagens. Só pode ser usado com mais de uma mensagem.
    @commands.command(aliases=['limpar', 'apagar', 'remover'], help='''Apaga a quantidade dada de mensagens no canal em que foi utilizado. Somente membros Staff podem usá-lo.''', usage=f'{prefix}clear *quantidade*')
    @commands.guild_only()
    @commands.has_any_role(*admin)
    async def clear(self, ctx, amount=0):
        logs_channel = self.client.get_channel(logs.message_logs_channel_id)
        if amount==0:
            await ctx.reply(f'**Você deve especificar a quantidade de mensagens a serem apagadas, {ctx.author.name}.**', delete_after=5.0)
        elif amount < 0:
            emoji = ':thinking:'
            await ctx.reply(f'**Você não pode apagar um número negativo de mensagens, {ctx.author.name} {emoji}**', delete_after=5.0)
        if amount==1:   
                await ctx.channel.purge(limit=1) 
                await ctx.reply('Por que você está usando clear para uma única mensagem?', delete_after=5.0)
        else:
            cor = logs.message_deleted_colour
            pfp = ctx.author.avatar.url
            icon = ctx.guild.icon.url
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
            embed.add_field(name='Mensagens apagadas:', value='Log salvo no arquivo abaixo:', inline=False)
            embed.set_footer(text=settings.embed_title, icon_url=icon)
            file = discord.File('./'+arquivo)
            await logs_channel.send(embed=embed, file=file)
            os.remove('./'+arquivo)

    @commands.command(aliases=['expulsar'], help='''Expulsa o membro mencionado pelo motivo especificado. Somente Administradores podem utilizá-lo.''', usage=f'{prefix}kick *@membro* **motivo**')
    @commands.guild_only()
    @commands.has_any_role(*admin)
    async def kick(self, ctx, member : discord.Member, *, reason):
        # Mensagem de aviso ao membro que foi punido:
        autor = ctx.message.author
        autor_pfp = autor.avatar.url
        footer = ctx.guild.icon.url
        cor = 0xff0000
        embed=discord.Embed(color=cor)
        embed.set_author(name=title, url=url, icon_url=autor_pfp)
        embed.add_field(name="Você foi expulso do servidor pelo motivo:", value=reason ,inline=False)
        embed.add_field(name="Quem te expulsou: ", value=autor.mention, inline=True)
        embed.set_footer(text="Você tem direito a recorrer esta punição em nosso site.", icon_url=footer)
        await member.send(embed=embed)
        await member.kick(reason=reason)
        await ctx.send(f'O usuário {member.mention} foi expulso do servidor.')

    @commands.command(aliases=['banir'], help='''Bane o membro mencionado pelo motivo especificado. Somente Administradores podem utilizá-lo.''', usage=f'{prefix}ban *@membro* **motivo**')
    @commands.guild_only()
    @commands.has_any_role(*admin)
    async def ban(self, ctx, member:discord.Member, *, reason):
        autor = ctx.message.author
        pfp_autor = autor.avatar.url
        footer = ctx.guild.icon.url
        cor = 0xff0000
        embed=discord.Embed(color=cor)
        embed.set_author(name=title, icon_url=pfp_autor)
        embed.add_field(name="Você foi banido do servidor pelo motivo:", value=reason ,inline=False)
        embed.add_field(name="Quem te baniu: ", value=autor.mention, inline=True)
        embed.set_footer(text="Você tem direito a recorrer esta punição em nosso site.", icon_url=footer)
        await member.send(embed=embed)
        await member.ban(reason=reason)
        await ctx.send(f'O usuário {member.mention} foi banido do servidor.')
    
    @commands.command(aliases=['desbanir'], help='''Desbane o usuário portador do *ID/nome#tag* especificado. Somente Administradores podem utilizá-lo.''', usage=f'{prefix}unban *ID/Nome#tag*')
    @commands.guild_only()
    @commands.has_any_role(*admin)
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

<<<<<<< HEAD
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

=======
>>>>>>> dev
def setup(client):
    client.add_cog(Mod(client))
import discord
from discord import role
from discord.ext import commands
from datetime import datetime
from modules.storage import logs, cargos
from data import settings
url = settings.url

class Logs(commands.Cog, name='Logs', description='''Módulo de registro de eventos do bot e do servidor. Não possui comandos.'''):

    def __init__(self, client):
        self.client = client  

    # Logs do bot
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            guild = guild
            admins_ids = []
            for member in guild.members:
                for role in member.roles:
                    if role.id in cargos.admin_roles_id:
                        admins_ids.append(member.id)
        print(f'{self.client.user} on-line. \nCriado por {settings.author_name} -> {settings.author_id}')
        logs_channel = self.client.get_channel(logs.bot_logs_channel_id)
        cor = logs.bot_online_colour
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        embed = discord.Embed(colour=cor)
        embed.set_author(name=self.client.user.name, url=settings.url_panel, icon_url=self.client.user.avatar.url)
        embed.add_field(name='Prefixo utilizado: ', value=f'[{settings.bot_prefix}]')
        embed.add_field(name='Data de criação: ', value=f'{guild.created_at.__format__("às %H:%M:%S em %d/%m/%Y")}', inline=False)
        embed.add_field(name='Quantidade atual de membros: ', value=f'{guild.member_count}', inline=False)
        embed.add_field(name='Dono do servidor: ', value=f'{guild.owner}', inline=False)
        admins = []
        for member_id in admins_ids:
            member = guild.get_member(member_id)
            admins.append(member)
        embed.add_field(name='Administradores:', value='\n'.join(map(str,admins)), inline=False)
        embed.add_field(name='Região do servidor: ', value=f'{guild.region}', inline=False)
        embed.add_field(name='Outras informações do servidor: ', value=f'```{guild.features}```', inline=False)
        #print(guild.banner)
        if guild.banner is not None:
            embed.set_image(url=guild.banner)
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text=f'Ativado no servidor {guild.name}, ID: ({guild.id}) | {horario}', icon_url=guild.icon.url)
        await logs_channel.send(embed=embed)

    # Logs de mensagens
    @commands.Cog.listener()
    async def on_message(self, message):
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        logs_channel = self.client.get_channel(logs.message_logs_channel_id)
        # Se não for uma mensagem do canal de logs, do bot ou do sistema (automática do Discord), registrar no log
        if message.channel.id not in logs.unlogged_channels_id and message.channel.id not in logs.not_messegeable and not message.is_system() and not message.author == self.client.user and not message.author.bot:
            cor = logs.message_log_colour
            url = message.jump_url
            mensagem = message.content
            autor = message.author
            icon = autor.avatar.url
            footer = message.guild.icon.url
            embed=discord.Embed(color=cor)
            embed.set_author(name="Mensagem enviada", url=url, icon_url=icon)
            embed.add_field(name="Autor da mensagem:", value=autor.mention, inline=True)
            embed.add_field(name="Mensagem:", value=f"```{mensagem}```", inline=False)
            embed.add_field(name="Enviada no canal: ", value=f"<#{message.channel.id}>", inline=True)
            embed.add_field(name="Arquivos enviados: ", value=message.attachments, inline=False)
            embed.set_footer(text=f"ID da mensagem: {message.id} | {horario}", icon_url=footer)
            await logs_channel.send(embed=embed)

    # Logs de mensagens editadas
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        logs_channel = self.client.get_channel(logs.message_logs_channel_id)
        if not before.channel == logs_channel and not before.is_system() and not before.author == self.client.user:
            autor = before.author
            url = before.jump_url
            icon = before.author.avatar.url
            footer = before.guild.icon.url
            cor = logs.message_edited_colour
            embed = discord.Embed(color=cor)
            embed.set_author(name="Mensagem editada", url=url, icon_url=icon)
            embed.add_field(name="Autor da mensagem: " , value=autor.mention , inline=True)
            embed.add_field(name="Mensagem original: ", value=f"```{before.content}```", inline=False)
            embed.add_field(name="Arquivos enviados: ", value=before.attachments, inline=False)
            embed.add_field(name="Mensagem nova: ", value=f"```{after.content}```")
            embed.add_field(name="Arquivos enviados: ", value=after.attachments, inline=False)
            embed.add_field(name="Canal da mensagem: ", value=f"<#{before.channel.id}>", inline=True)
            embed.set_footer(text=f"ID da mensagem: {before.id} | Data: {horario}", icon_url=footer)
            await logs_channel.send(embed=embed)


    # Logs de mensagens apagadas
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        logs_channel = self.client.get_channel(logs.message_logs_channel_id)
        if not message.channel == logs_channel and not message.is_system() and not message.author == self.client.user:
            autor = message.author
            icon = message.author.avatar.url
            footer = message.guild.icon.url
            cor = logs.message_deleted_colour
            embed = discord.Embed(color=cor)
            embed.set_author(name="Mensagem apagada", url=message.jump_url, icon_url=icon)
            embed.add_field(name="Autor da mensagem:" , value=autor.mention , inline=True)
            embed.add_field(name="Conteúdo da mensagem:", value=f"```{message.content}```", inline=False)
            embed.add_field(name="Arquivos enviados:", value=message.attachments, inline=False)
            embed.add_field(name="Enviada no canal: ", value=f"<#{message.channel.id}>", inline=True)
            embed.set_footer(text=f"ID da mensagem: {message.id} | Data: {horario}", icon_url=footer)
            await logs_channel.send(embed=embed)

    # Logs de entrada de membros + aviso ao novo membro para ler às regras do servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):
        logs_channel = self.client.get_channel(logs.member_logs_channel_id)
        members_channel = self.client.get_channel(logs.public_member_channel_id)
        user_date = member.created_at.__format__("%d/%m/%Y")
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        pfp = member.avatar.url
        cor = logs.member_join_colour
        user = member.mention
        embed=discord.Embed(color=cor)
        embed.set_author(name="Novo membro", url=url)
        embed.set_thumbnail(url=pfp)
        embed.add_field(name='O usuário', value=f" {user} entrou no servidor", inline=True)
        embed.add_field(name="Data de criação da conta: ", value=user_date, inline=False)
        embed.set_footer(text=f"ID: {member.id} | Data: {horario}", icon_url=member.guild.icon.url)
        await logs_channel.send(embed=embed)
        await members_channel.send(embed=embed)

    # Logs de saída de membros
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logs_channel = self.client.get_channel(logs.member_logs_channel_id)
        members_channel = self.client.get_channel(logs.public_member_channel_id)
        user_joined = member.joined_at.__format__("às %H:%M:%S em %d/%m/%Y")
        user_date = member.created_at.__format__("às %H:%M:%S em %d/%m/%Y")
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        icon = member.avatar.url
        cor = logs.member_leave_colour
        user = member.mention
        embed=discord.Embed(color=cor)
        embed.set_author(name="Um membro saiu", url=url)
        embed.set_thumbnail(url=icon)
        embed.add_field(name='O usuário', value=f" {user} deixou o servidor.\nEntrou no servidor {user_joined}", inline=True)
        embed.add_field(name="Data de criação da conta: ", value=user_date, inline=False)
        embed.set_footer(text=f"ID: {member.id} | Data: {horario}", icon_url=member.guild.icon.url)
        await logs_channel.send(embed=embed)
        await members_channel.send(embed=embed)


    # Logs de banimento
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        logs_channel = self.client.get_channel(logs.moderation_logs_channel_id)
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        banned = member.avatar.url
        author = guild.icon.url
        footer = author
        cor = logs.member_ban_colour
        user = member.mention
        embed=discord.Embed(color=cor)
        embed.set_author(name="Membro banido", url=url, icon_url=banned)
        embed.set_thumbnail(url=author)
        embed.add_field(name="O usuário ", value=f"{user} foi banido do servidor", inline=True)
        embed.add_field(name="Motivo do banimento: ", value="algum motivo...", inline=True)
        embed.set_footer(text=f"ID do usuário banido: {member.id} | Data: {horario}", icon_url=footer)
        await logs_channel.send(embed=embed)

    # Logs de desbanimento
    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        logs_channel = self.client.get_channel(logs.moderation_logs_channel_id)
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        banned = member.avatar.url
        author = guild.icon.url
        footer = author
        cor = logs.member_unban_colour
        user = member.mention
        embed=discord.Embed(color=cor)
        embed.set_author(name="Membro desbanido", url=url, icon_url=banned)
        embed.set_thumbnail(url=author)
        embed.add_field(name='O usuário', value=f" {user} foi desbanido do servidor", inline=True)
        embed.set_footer(text=f"ID do usuário: {member.id} | Data: {horario}", icon_url=footer)
        await logs_channel.send(embed=embed)

    # Logs de criação de convites
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        logs_channel = self.client.get_channel(logs.invites_logs_channel_id)
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        icon = invite.guild.icon.url
        footer = icon
        cor = logs.invite_created_colour
        url = invite.url
        autor = invite.inviter
        embed=discord.Embed(color=cor)
        embed.set_author(name="Convite criado", url=url)
        embed.set_thumbnail(url=icon)
        embed.add_field(name=f"O convite {invite}", value=" foi criado.", inline=True)        
        embed.add_field(name="Criado por ", value=autor.mention, inline=True)
        embed.add_field(name='Canal do convite: ', value=f'<#{invite.channel.id}>', inline=True)
        embed.add_field(name="Limite de usos:", value=invite.max_uses, inline=True)
        # Verifica se o convite é permanente (duração automática)
        if invite.max_age == 0:
            validade = 'Permanente'
        else:
            validade = f'{invite.max_age/60} minutos'
        embed.add_field(name="Duração limite:", value=f'{validade}', inline=True)
        # Verifica se o convite removerá o membro do servidor depois de certo tempo
        if invite.temporary:
            temporario = 'Sim.'
        else: 
            temporario = 'Não.'
        embed.add_field(name="Convite de estadia temporária? ", value=temporario, inline=True)
        # Verifica se o convite ainda está ativo
        if invite.revoked:
            ativo = 'Não.'
        else:
            ativo = 'Sim.'
        embed.add_field(name="Ativo? ", value=ativo, inline=True)
        embed.set_footer(text=f"Data: {horario}", icon_url=footer)
        await logs_channel.send(embed=embed)

    # Logs de remoção de convites
    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        logs_channel = self.client.get_channel(logs.invites_logs_channel_id)
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        icon = invite.guild.icon.url
        footer = invite.guild.icon.url
        cor = logs.invite_deleted_colour
        url = invite.url
        embed=discord.Embed(color=cor)
        embed.set_author(name="Convite apagado", url=url)
        embed.set_thumbnail(url=icon)
        embed.add_field(name=f"O convite ", value=invite.id, inline=True)
        embed.add_field(name="Para o canal", value=f'<#{invite.channel.id}> foi apagado.', inline=True)
        embed.set_footer(text=f"Data: {horario}", icon_url=footer)
        await logs_channel.send(embed=embed)

def setup(client):
    client.add_cog(Logs(client))
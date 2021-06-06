import discord
import json
from pathlib import Path
from discord.ext import commands
from datetime import datetime

dir = Path(__file__).absolute().parent
file_location = dir / 'settings' / 'config.json'
file = file_location.open()
data = json.loads(file.read())
logs_channel_id = int(data["settings"][0]["logs"][0]["logs_channel_id"])
member_logs_channel_id = int(data["settings"][0]["logs"][0]["member_logs_channel_id"])

class Logs(commands.Cog):

    def __init__(self, client):
        self.client = client   

    # Logs de mensagens
    @commands.Cog.listener()
    async def on_message(self, message):
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        logs_channel = self.client.get_channel(logs_channel_id)
        # Se não for uma mensagem do canal de logs, do bot ou do sistema (automática do Discord), registrar no logS
        if not message.channel == logs_channel and not message.is_system() and not message.author == self.client.user:
            #msg_date = message.created_at.strftime("às %H:%M:%S em %d/%m/%Y")
            cor = int(data["settings"][0]["logs"][0]["message_log_colour"])
            url = message.jump_url
            mensagem = message.content
            autor = message.author
            embed=discord.Embed(color=cor)
            embed.set_author(name="Mensagem enviada", url=url)
            embed.add_field(name="Autor da mensagem:", value=autor.mention, inline=True)
            embed.add_field(name="Mensagem:", value=mensagem, inline=False)
            #embed.add_field(name="Enviada em: ", value=msg_date, inline=True)
            # Anexar qualquer imagem ou arquivo à mensagem de log
            if message.attachments:
                atch = message.attachments.to_file
                embed.set_thumbnail(url=atch)
            # Se não, usar o ícone do servidor na mensagem de log
            else:
                icon = message.guild.icon_url
                embed.set_thumbnail(url=icon)
            embed.add_field(name="Enviada no canal: ", value=f"<#{message.channel.id}>", inline=True)
            embed.set_footer(text=f"ID da mensagem: {message.id} | {horario}")
            await logs_channel.send(embed=embed)

    # Logs de entrada de membros
    @commands.Cog.listener()
    async def on_member_join(self, member):
        logs_channel = self.client.get_channel(member_logs_channel_id)
        user_date = member.joined_at.strftime("%d/%m/%Y")
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        pfp = member.avatar_url
        cor = int(data["settings"][0]["logs"][0]["member_join_colour"])
        url = "https://fenbrasil.net"
        user = member.mention
        embed=discord.Embed(color=cor)
        embed.set_author(name="Novo membro", url=url)
        embed.set_thumbnail(url=pfp)
        embed.add_field(name='O usuário', value=f" {user} entrou no servidor", inline=True)
        embed.add_field(name="Data de criação da conta: ", value=user_date, inline=False)
        embed.set_footer(text=f"ID: {member.id} | Data: {horario}")
        await logs_channel.send(embed=embed)

    # Logs de saída de membros
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logs_channel = self.client.get_channel(member_logs_channel_id)
        user_date = member.joined_at.strftime("às %H:%M:%S em %d/%m/%Y")
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        icon = member.avatar_url
        cor = int(data["settings"][0]["logs"][0]["member_leave_colour"])
        url = "https://fenbrasil.net"
        user = member.mention
        embed=discord.Embed(color=cor)
        embed.set_author(name="Um membro saiu", url=url)
        embed.set_thumbnail(url=icon)
        embed.add_field(name='O usuário', value=f" {user} deixou o servidor", inline=True)
        embed.add_field(name="Data de criação da conta: ", value=user_date, inline=False)
        embed.set_footer(text=f"ID: {member.id} | Data: {horario}")
        await logs_channel.send(embed=embed)


    # Logs de banimento
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        logs_channel = self.client.get_channel(logs_channel_id)
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        banned = member.avatar_url
        author = guild.icon_url
        cor = int(data["settings"][0]["logs"][0]["member_ban_colour"])
        url = "https://fenbrasil.net"
        user = member.mention
        embed=discord.Embed(color=cor)
        embed.set_author(name="Membro banido", url=url, icon_url=banned)
        embed.set_thumbnail(url=author)
        embed.add_field(name="O usuário ", value=f"{user} foi banido do servidor", inline=True)
        embed.add_field(name="Motivo do banimento: ", value="algum motivo...", inline=True)
        embed.set_footer(text=f"ID do usuário banido: {member.id} | Data: {horario}")
        await logs_channel.send(embed=embed)

    # Logs de desbanimento
    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        logs_channel = self.client.get_channel(logs_channel_id)
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        banned = member.avatar_url
        author = guild.icon_url
        cor = int(data["settings"][0]["logs"][0]["member_unban_colour"])
        url = "https://fenbrasil.net"
        user = member.mention
        embed=discord.Embed(color=cor)
        embed.set_author(name="Membro desbanido", url=url, icon_url=banned)
        embed.set_thumbnail(url=author)
        embed.add_field(name='O usuário', value=f" {user} foi desbanido do servidor", inline=True)
        embed.set_footer(text=f"ID do usuário: {member.id} | Data: {horario}")
        await logs_channel.send(embed=embed)

    # Logs de criação de convites
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        logs_channel = self.client.get_channel(logs_channel_id)
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        icon = invite.guild.icon_url
        cor = int(data["settings"][0]["logs"][0]["invite_created_colour"])
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
        embed.set_footer(text=f"Data: {horario}")
        await logs_channel.send(embed=embed)

    # Logs de remoção de convites
    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        logs_channel = self.client.get_channel(logs_channel_id)
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        created = invite.created_at
        icon = invite.guild.icon_url
        cor = int(data["settings"][0]["logs"][0]["invite_deleted_colour"])
        url = invite.url
        embed=discord.Embed(color=cor)
        embed.set_author(name="Convite apagado", url=url)
        embed.set_thumbnail(url=icon)
        embed.add_field(name=f"O convite ", value=invite.id, inline=True)
        embed.add_field(name="Para o canal", value=f'<#{invite.channel.id}> foi apagado.', inline=True)
        embed.set_footer(text=f"Data: {horario}")
        await logs_channel.send(embed=embed)

def setup(client):
    client.add_cog(Logs(client))
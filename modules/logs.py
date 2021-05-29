import discord
import json
from pathlib import Path
from discord.ext import commands
from datetime import datetime

dir = Path(__file__).absolute().parent
file_location = dir / 'settings' / 'config.json'
file = file_location.open()
data = json.loads(file.read())
channel_id = int(data["settings"][0]["logs"][0]["logs_channel_id"])

class Logs(commands.Cog):

    def __init__(self, client):
        self.client = client    

    @commands.Cog.listener()
    async def on_message(self, message):
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        logs_channel = self.client.get_channel(channel_id)
        # Se não for uma mensagem do canal de logs ou do sistema (automática do Discord), registrar no logS
        if not message.channel == logs_channel and not message.is_system() and not message.author == self.client:
            msg_date = message.created_at.strftime("às %H:%M:%S em %d/%m/%Y")
            cor = 0xff0000
            url = message.jump_url
            mensagem = message.content
            autor = message.author
            embed=discord.Embed(color=cor)
            embed.set_author(name="Mensagem enviada", url=url)
            embed.add_field(name="Autor da mensagem:", value=autor, inline=False)
            embed.add_field(name="Mensagem:", value=mensagem, inline=False)
            embed.add_field(name="Enviada em: ", value=msg_date, inline=True)
            # Anexar qualquer imagem ou arquivo à mensagem de log
            if message.attachments:
                atch = message.attachments.to_file
                embed.set_thumbnail(url=atch)
            # Se não, usar o ícone do servidor na mensagem de log
            else:
                icon = message.guild.icon_url
                embed.set_thumbnail(url=icon)
            embed.add_field(name="Enviada no canal ", value=f"{message.channel}", inline=True)
            embed.set_footer(text=f"ID da mensagem: {message.id} | {horario}")
            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logs_channel = self.client.get_channel(channel_id)
        user_date = member.joined_at.strftime("%d/%m/%Y")
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        pfp = member.avatar_url
        cor = 0x0000ff
        url = "https://fenbrasil.net"
        embed=discord.Embed(color=cor)
        embed.set_author(name="LOGS FEN", url=url)
        embed.set_thumbnail(url=pfp)
        embed.add_field(name=f"O usuário {member.mention} entrou no servidor.", value=f"Criado em {user_date}", inline=False)
        embed.set_footer(text=f"ID: {member.id} | Data: {horario}")
        await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logs_channel = self.client.get_channel(channel_id)
        user_date = member.joined_at.strftime("às %H:%M:%S em %d/%m/%Y")
        now = datetime.now()
        horario = now.strftime("às %H:%M:%S em %d/%m/%Y")
        icon = member.avatar_url
        cor = 0x0000ff
        url = "https://fenbrasil.net"
        embed=discord.Embed(color=cor)
        embed.set_author(name="LOGS FEN", url=url)
        embed.set_thumbnail(url=icon)
        embed.add_field(name=f"O usuário {member.mention} deixou o servidor.", value=f"Criado em {user_date}", inline=False)
        embed.set_footer(text=f"ID: {member.id} | Data: {horario}")
        await logs_channel.send(embed=embed)

def setup(client):
    client.add_cog(Logs(client))
import discord
from datetime import datetime
from discord.ext import commands, tasks
from modules.storage import widgets

class Widgets(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        count = member.guild.member_count
        channel = discord.utils.get(member.guild.voice_channels, id=widgets.counting_channel_id)
        await channel.edit(name=f'{count} membros', reason='Atualizar contagem de membros.')
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        count = member.guild.member_count
        channel = discord.utils.get(member.guild.voice_channels, id=widgets.counting_channel_id)
        await channel.edit(name=f'{count} membros', reason='Atualizar contagem de membros.')

def setup(client):
    client.add_cog(Widgets(client))
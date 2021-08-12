import discord
from discord.ext import commands
from data import settings
from modules.storage import tickets, cargos

class Reactions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        rules_channel = self.client.get_channel(tickets.rules_channel_id)
        await rules_channel.send(f'<@{member.id}>', delete_after=1.0)

    @commands.command()
    async def rules(self, ctx):
        channel = ctx.channel
        embed = discord.Embed(colour=tickets.report_ticket_colour)
        embed.set_author(name=settings.embed_title, icon_url=ctx.guild.icon.url)
        embed.add_field(name='Além disso, você deve ler e concordar com os termos e serviços do Discord, listados abaixo:', 
        value=''''https://discord.com/terms
https://discordapp.com/guidelines''', inline=False)
        embed.set_footer(text=f'Clique no botão abaixo para obter o cargo <@&{cargos.member_role_id}> para ter acesso completo aos canais principais do Discord.', icon_url=self.client.avatar.url)
        await channel.purge(limit=1)


def setup(client):
    client.add_cog(Reactions(client))
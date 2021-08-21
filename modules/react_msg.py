import discord
from discord import channel
from discord.ext import commands
from data import settings
from modules.storage import tickets, cargos, info

class Reactions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        rules_channel = self.client.get_channel(tickets.rules_channel_id)
        await rules_channel.send(f'<@{member.id}>', delete_after=1.0)

    @commands.command(hidden=True)
    async def rules(self, ctx):
        channel = ctx.channel
        embed = discord.Embed(colour=tickets.report_ticket_colour)
        embed.set_author(name=settings.embed_title, icon_url=ctx.guild.icon.url)
        embed.add_field(name='Além disso, você deve ler e concordar com os termos e serviços do Discord, listados abaixo:', 
        value='''https://discord.com/terms
https://discordapp.com/guidelines''', inline=False)
        embed.add_field(name='Dos nossos termos:', value=f'''**É total responsabilidade de cada usuário ler, de forma integral, todas as regras do nosso servidor do Discord e, ao estar utilizando deste, é obrigado a seguir e respeitar todas elas sob pena de punição de acordo com nossas diretrizes.**
        Além disso, ainda que algum membro remova sua reação desta mensagem, é prova de que este concordou com os termos a posse do cargo <@&{cargos.member_role_id}>''')
        embed.set_footer(text=f'Reaja abaixo para atestar que você leu e concordou com nossos termos e obter acesso completo aos canais principais do nosso servidor do Discord.', icon_url=self.client.user.avatar.url)
        await channel.purge(limit=1)
        message = await channel.send(embed=embed)
        await message.add_reaction('✅')
        print(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = payload.member
        role = member.guild.get_role(cargos.member_role_id)
        if payload.emoji.name == '✅' and not member.get_role(cargos.member_role_id) and message.author == self.client.user and payload.channel_id == info.rules_channel_id:
            await member.add_roles(role, reason='Concordou com as regras do servidor.')

def setup(client):
    client.add_cog(Reactions(client))
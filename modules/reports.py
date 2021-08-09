import discord
from discord.enums import ButtonStyle
from discord_buttons_plugin import *
from discord.ext import commands
from modules.storage import cargos
from modules.storage import tickets
from data import settings
import bot

buttons = bot.buttons

warning_title = 'Note que:'
warning_message = f'abrir tickets repetidamente sem necessidade poderá levar a punição no servidor do Discord. Nossos membros da equipe sempre levarão a sério qualquer ticket aqui criado, então, pedimos que faça o mesmo e não disperdice nosso tempo com brincadeiras.\nUm <@&{cargos.admin_roles_id[0]}> poderá fechar ou reabrir um ticket criado de acordo com a necessidade para com cada caso.'

class Reports(commands.Cog):

    def __init__(self, client):
        self.client = client 
    
    @commands.command()
    @commands.has_any_role(cargos.admin_roles_id[0])
    async def reports(self, ctx):
        channel_id = tickets.ticket_system_channels[0]
        channel = self.client.get_channel(channel_id)
        cor = tickets.report_ticket_colour
        footer = settings.embed_title
        url = settings.url
        icon = ctx.guild.icon_url
        embed = discord.Embed(color=cor)
        embed.set_author(name='Sistema de tickets', url=url)
        embed.add_field(name='Denúncia privada', value=f'Clieque no botão abaixo para criar um ticket e fazer uma reclamação/denúncia. Somente usuários <@&{cargos.admin_roles_id[0]}> terão acesso ao canal criado para que você faça sua denúncia.', inline=False)
        embed.add_field(name=tickets.warning_title, value=tickets.warning_message, inline=False)
        embed.set_footer(text=footer, icon_url=icon)
        await channel.purge(limit=1)
        await buttons.send(
            embed=embed,
            channel = ctx.channel.id,
            components= [
                ActionRow([
                    Button (
                        label="Denunciar",
                        style=ButtonStyle.red,
                        custom_id="button_report"
                    )
                ])
            ]
        )

    @buttons.click
    async def button_report(ctx):
        message = ctx.message
        channel = ctx.channel
        thread = await channel.start_thread(name=f'Denúncia {ctx.author.name}', auto_archive_duration=60, type=discord.private_thread, reason=f'{ctx.author.name} iniciou uma denúncia.')

def setup(client):
    client.add_cog(Reports(client))
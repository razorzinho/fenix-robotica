import discord
from datetime import datetime

from discord.enums import TeamMembershipState
from data import settings
from modules.storage import tickets
from modules.storage import cargos
from discord.ext import commands

#help_channel_id = tickets.ticket_system_channels[1]
#bugs_channel_id = tickets.ticket_system_channels[2]
#feedback_channel_id = tickets.ticket_system_channels[3]
#bans_channel_id = tickets.ticket_system_channels[4]
#staff_channel_id = tickets.ticket_system_channels[5]

warning_title = 'Note que:'
warning_message = f'abrir tickets repetidamente sem necessidade poderá levar a punição no servidor do Discord. Nossos membros da equipe sempre levarão a sério qualquer ticket aqui criado, então, pedimos que faça o mesmo e não disperdice nosso tempo com brincadeiras.\nUm <@&{cargos.admin_roles_id[0]}> poderá fechar ou reabrir um ticket criado de acordo com a necessidade para com cada caso.'
activation_emoji = '⚠️'
lock_emoji = '🔒'
unlock_emoji = '🔓'

class Tickets(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(*cargos.admin_roles_id)
    async def reports(self, ctx):
        channel_id = tickets.ticket_system_channels[0]
        channel = self.client.get_channel(channel_id)
        cor = tickets.report_ticket_colour
        footer = settings.embed_title
        url = settings.url
        icon = ctx.guild.icon_url
        pfp = ctx.author.avatar_url
        embed = discord.Embed(color=cor)
        embed.set_author(name='Sistema de tickets', url=url, icon_url=pfp)
        embed.add_field(name='Denúncia privada', value=f'Reaja abaixo em {activation_emoji} para criar um ticket e fazer uma reclamação/denúncia. Somente usuários <@&{cargos.admin_roles_id[0]}> terão acesso ao canal criado para que você faça sua denúncia.', inline=False)
        embed.add_field(name=warning_title, value=warning_message, inline=False)
        embed.set_footer(text=footer, icon_url=icon)
        message = await channel.send(embed=embed)
        await message.add_reaction(activation_emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        category_id = tickets.ticket_system_categories[0]
        now = datetime.now()
        data = now.strftime("%d-%m-%Y")
        perms = {
            user:discord.PermissionOverwrite(
                read_message_history=True,
                read_messages=True,
                send_messages=True
            ),
            tickets.ticket_system_roles[0]:discord.PermissionOverwrite(
                read_message_history=True,
                read_messages=True,
                send_messages=True
            )
        }
        if reaction.message.channel == self.client.get_channel(tickets.ticket_system_channels[0]) and reaction.emoji == activation_emoji:
            new_channel = await user.guild.create_text_channel(name=f'denúncia_{user.name}_{data}', overwrites=perms, category=category_id, reason=f'Canal de denúncia requisitado por {user.name}')
            embed = discord.Embed(cor=tickets.report_ticket_colour)
            embed.set_author(name='Sistema de tickets', url=settings.url, icon_url=user.avatar_url)
            embed.add_field(name='Denúncia:', value=f'Sentimos muito pelo inconveniente. Um <@&{cargos.admin_roles_id[0]}> atenderá você em breve.', inline=False)
            embed.add_field(name='Modo de uso:', value='envie neste canal quaisquer informações pertinentes à sua denúncia. Inicie informando quem você deseja denunciar e, em seguida, explique-nos o que aconteceu.\nPara fechar este ticket, reaja em {lock_emoji}.', inline=False)
            embed.add_field(name=warning_title, value='ao reagir em confirmar fechamento do ticket, você não terá mais acesso ao mesmo.')
            embed.set_footer(text=settings.embed_title, icon_url=reaction.guild.icon_url)
            await new_channel.send(f'Olá, {user.mention}')
            message = await new_channel.send(embed=embed)
            await message.add_reaction(lock_emoji)
        #if reaction.message.channel in discord.utils.get.category_id.category.text_channels and reaction.emoji == lock_emoji:
        #    new_perms = {
        #        user:discord.PermissionOverwrite(
        #            read_message_history = False,
        #            read_messages = False
        #        )
        #    }
        #    new_channel.edit(overwrites=new_perms)
        #    embed = discord.Embed(color=tickets.report_ticket_colour)
        #    embed.add_field(name='Ticket fechado por', value=user.mention, inline=False)
        #    await new_channel.send(embed=embed)
        #elif reaction.message.channel in category_id.text_channels and reaction.emoji == unlock_emoji:
        #    new_perms = {
        #        user:discord.PermissionOverwrite(
        #            read_message_history = True,
        #            read_messages = True
        #        ),
        #        tickets.ticket_system_roles[0]:discord.PermissionOverwrite(
        #            read_message_history = True,
        #            read_message = True
        #        )
        #    }
        #    embed = discord.Embed(color=tickets.report_ticket_colour)
        #    embed.add_field(name='Ticket reaberto por', value=user.mention, inline=False)
        #    embed.add_field(name=settings.empty_value, value=f'Para fechar este ticket, reaja em {lock_emoji}.')
        #    embed.add_field(name=warning_title, value='preferível não fechar e reabrir um ticket mais de uma vez.')
        #    embed.set_footer(name=settings.embed_title, icon_url=user.guild.icon_url)
        #    await new_channel.edit(overwrites=new_perms)
        #    message = await new_channel.send(emebed=embed)
        #    await message.add_reaction(lock_emoji)

def setup(client):
    client.add_cog(Tickets(client))
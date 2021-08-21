from discord.ext import commands
from modules.storage import help
from data import settings
import discord

attributes = {
    'aliases': ['ajuda', 'lista', 'comandos'],
    'help': 'Lista todos os comandos em suas respectivas categorias e suas descrições. Este comando :)',
    'usage': f'{settings.bot_prefix}help (*comando|categoria*)'
}

class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__(command_attrs=attributes, show_hidden=False)

    @commands.guild_only()
    async def send_bot_help(self, mapping):
        ctx = self.context
        embed = discord.Embed(colour=help.help_colour)
        embed.set_author(name=f'Ajuda Fênix Robótica: comandos', url=settings.url, icon_url=ctx.guild.icon.url)
        embed.set_footer(text=f'Use ?help *comando|categoria* para ver um guia mais detalhado.', icon_url=ctx.author.avatar.url)
        for cog in mapping:
            if cog is None: 
                continue
            comandos = []
            for command in mapping[cog]:
                aliases = []
                if not command.hidden:
                    comandos.append(command.name)
                if command.aliases is not None:
                    aliases.append(command.aliases)
                else:
                    aliases = ''
            if not comandos:
                continue
            embed.add_field(name=f'{cog.qualified_name}:', value="\n".join(map(str,comandos)) +' ou: '+ " , ".join(map(str,aliases)), inline=False)
        await ctx.send(embed=embed)

    @commands.guild_only()
    async def send_cog_help(self, cog):
        ctx = self.context
        embed = discord.Embed(colour=help.cog_help_colour, description=f'**{cog.description}**')
        embed.set_author(name=f'Ajuda Fênix Robótica: categoria {cog.qualified_name}', url=settings.url, icon_url=ctx.guild.icon.url)
        embed.set_footer(text=f'Requisitado por {ctx.author}. | Use ?help *comando|categoria* para exibir este guia.', icon_url=ctx.author.avatar.url)
        aliases = []
        for command in cog.walk_commands():
            if command.aliases:
                aliases.append(command.aliases)
                embed.add_field(name=f'{command.qualified_name} |' ', '.join(map(str,command.aliases)), value=f'''{command.description}
            **Uso:** {command.usage}''', inline=False)
            else:
                embed.add_field(name=f'{command.qualified_name}', value=f'''{command.description}
            **Uso:** {command.usage}''', inline=False)
        await ctx.send(embed=embed)

    @commands.guild_only()
    async def send_group_help(self, group):
        ctx = self.context
        embed = discord.Embed(colour=help.group_help_colour)
        await ctx.send(f'Texto genérico')

    @commands.guild_only()
    async def send_command_help(self, command):
        ctx = self.context
        embed = discord.Embed(colour=help.command_help_colour, description=f'**{command.help}**')
        embed.set_author(name=f'Ajuda Fênix Robótica: comando {command.qualified_name} | {command.cog_name}', url=settings.url, icon_url=ctx.guild.icon.url)
        embed.set_footer(text=f'Requisitado por {ctx.author} | Use ?help para ver a lista completa de comandos e categorias.', icon_url=ctx.author.avatar.url)
        if command.aliases:
            embed.add_field(name='Outros formas do comando:', value=', '.join(map(str,command.aliases)), inline=False)
        embed.add_field(name='Uso:', value=command.usage, inline=False)
        await ctx.send(embed=embed)

    @commands.guild_only()
    async def command_not_found(self, string):
        ctx = self.context
        await ctx.reply(f'O comando {string} não existe. Use ?help para ver a lista completa de comandos.')

    @commands.guild_only()
    async def subcommand_not_found(self, command, string):
        ctx = self.context
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return await ctx.reply(f'O comando `{command.qualified_name}` não possui subcomandos.')
        return await ctx.reply(f'O comando `{command.qualified_name}` não possui um subcomando chamado `{string}`.')
            

def setup(client):
    client.help_command = CustomHelpCommand()
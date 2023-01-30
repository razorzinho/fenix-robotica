import discord
from modules.storage import logs
from discord.ext import commands

def setup(client):
    # Cuidar de erros relacionados a comandos
    @client.event
    async def on_command_error(ctx, error):
        logs_channel = client.get_channel(logs.bot_logs_channel_id)
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f"Ops, parece que você não tem o cargo necessário para utilizar este comando, {ctx.author.name}.")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.reply(f"Ops, parece que você não tem um cargo necessário para utilizar este comando, {ctx.author.name}.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Ops, parece que você errou o formato deste comando, {ctx.author.name}. Utilize o comando ?help comando para saber como se utiliza.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"Ops, parece que você não tem a permissão necessária para este comando, {ctx.author.name}.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(f"O membro requisitado não foi encontrado. Talvez você tenha errado o formato do comando? \nUse ?help <comando> para ver como utilizá-lo ou garanta que está usando o nome ou mencionando o membro.")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.reply(f"Parece que o comando que você está tentando utilizar não existe. Use o comando **?help** para ver a lista completa de comandos.")
        elif isinstance(error.original, commands.ExtensionAlreadyLoaded):
            await ctx.reply(f"O módulo que você tentou carregar já está habilitado.")
        elif isinstance(error.original, commands.ExtensionNotFound):
            await ctx.reply(f"Este módulo não existe.")
        elif isinstance(error.original, commands.ExtensionNotLoaded):
            await ctx.reply(f"O módulo que você tentou desabilitar não está habilitado.")
        elif isinstance(error.original, commands.ExtensionFailed):
            await ctx.reply(f"O módulo **{ctx.message.content[-4:]}** está gerando erros e não pôde ser habilitado. Vide logs. Marquei você no canal.")
            await logs_channel.send(f"{ctx.author.mention} O módulo **{ctx.message.content[-4:]}** está gerando um erro:\n```{error}```")
        raise error
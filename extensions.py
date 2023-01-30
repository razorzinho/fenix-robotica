import os
from data import settings
from modules.storage import cargos
from discord.ext import commands

def setup(client):

    # Ao inicializar o bot, carregar todos os módulos presentes no diretório /modules, exceto os marcados como desabilitados
    for filename in os.listdir('./'+settings.modules_dir):
        if filename.endswith('.py') and filename not in settings.disabled_modules:
            client.load_extension(f'{settings.modules_dir}.{filename[:-3]}')

    # Comandos de carregamento, desativação e recarga dos módulos
    @client.command(aliases=['carregar', 'ativar'], hiddden=True, help='Carrega módulos do BOT. Somente acessível por Administradores Chefe')
    @commands.has_any_role(cargos.admin_roles_id[0])
    async def load(ctx, extension):
        client.load_extension(f'{settings.modules_dir}.{extension}')
        await ctx.send(f'Extensão **{str(extension)}** carregada.')

    @client.command(aliases=['descarregar', 'desativar'], hiddden=True, help='Desabilita módulos ativos do BOT. Somente acessível por Administradores Chefe')
    @commands.has_any_role(cargos.admin_roles_id[0])
    async def unload(ctx, extension):
            client.unload_extension(f'{settings.modules_dir}.{extension}')
            await ctx.send(f'Extensão **{str(extension)}** desativada.')

    @client.command(aliases=['recarregar'], hiddden=True, help='Recarrega módulos ativos do BOT. Somente acessível por Administradores Chefe')
    @commands.has_any_role(cargos.admin_roles_id[0])
    async def reload(ctx, extension):
            client.unload_extension(f'{settings.modules_dir}.{extension}')
            client.load_extension(f'{settings.modules_dir}.{extension}')
            await ctx.send(f'Extensão **{str(extension)}** recarregada.')
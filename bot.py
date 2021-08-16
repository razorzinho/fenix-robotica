import discord
import database
from discord.ext import commands
from data import settings
from modules.storage import logs
client = commands.Bot(command_prefix = settings.bot_prefix, intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=settings.activity_name))

# Carregar códigos essenciais do bot antes de carregar os móudlos
client.load_extension('terminal')
client.load_extension('error_handler')
client.load_extension('extensions')
client.load_extension('nickname')
# Desabilitado por estar com desenvolvimento parado
#client.load_extension('help')
client.load_extension('disconnect')

# Inicialização do Banco de dados ocorre depois que o bot está on-line
@client.event
async def on_ready():
    print('Inicializando banco de dados...')
    # Tentar inicializar o banco de dados sem interromper o funcionamento do bot:
    try:
        client.load_extension('database')
        print('Banco de dados carregado...')
    # Se não for possível iniciar o banco de dados, registrar no canal de logs do servidor.
    except Exception as err:
        print('Houve algum erro com o módulo do banco de dados. Registrando no canal de logs...')
        logs_channel = client.get_channel(logs.bot_logs_channel_id)
        embed = discord.Embed(colour=logs.bot_logout_colour)
        embed.set_author(name=client.user.name, url=settings.url_panel, icon_url=client.user.avatar.url)
        embed.add_field(name='O módulo do banco de dados gerou o seguinte erro:', value=f'```{err}```', inline=False)
        await logs_channel.send(embed=embed)
        print('Erro do banco de dados registrado no canal de logs.')
    database.get_database(settings.db)

client.run(settings.bot_token)
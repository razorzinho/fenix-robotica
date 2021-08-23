import discord
import random
from data import settings
from modules.storage import fun
from discord.ext import commands

class Diversão(commands.Cog, name='Diversão', description='''Categoria de comandos focados em diversão e descontração.'''):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['8ball', 'dado', 'pergunta'], help='Dá uma resposta a uma pergunta enviada no comando. Tente a sorte...', usage=f'{settings.bot_prefix}dadinho *pergunta*')
    async def dadinho(self, ctx, *, question):
        await ctx.reply(f'**Pergunta:** {question} \n**Resposta:** {random.choice(fun.responses)}')

    @commands.command(aliases=['bater'], help='Dá um tapa no usuário mencionado, pelo motivo especificado.', usage=f'{settings.bot_prefix}slap *@alvo*')
    async def tapa(self, ctx, members:commands.Greedy[discord.Member], *, reason='nenhum motivo.'):
        slapped = ", ".join(x.name for x in members)
        await ctx.reply(f'{slapped} levou um tapa por {reason}')

def setup(client):
    client.add_cog(Diversão(client))
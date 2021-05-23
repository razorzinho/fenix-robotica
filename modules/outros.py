import discord
import random
from discord.ext import commands

class Outros(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['8ball', 'dado', 'pergunta'], mention_author=True)
    async def dadinho(self, ctx, *, question):
        responses = [
        'Sim.',
        'Certamente.',
        'Com toda certeza.',
        'Sim - com certeza.',
        'Muito provavelmente.',
        'Acredito que sim.',
        'Talvez...',
        'Quem sabe?',
        'Não tenho certeza.',
        'Pode ser que sim, pode ser que não.',
        'Ligo não filho da puta :rage:',
        'Se mata desgraça :skull_crossbones:',
        'Não.',
        'Impossível.',
        'Nem a pau.',
        'Nunca, jamais.',
        'Nem em sonhos.'
        ]
        await ctx.send(f'**Pergunta:** {question} \n**Resposta:** {random.choice(responses)}')
    @dadinho.error
    async def dadinho_error(ctx, error, question):
        if isinstance(error, commands.MissingRequiredArgument(question)):
            await ctx.send(f'Você deve enviar uma pergunta.', delete_after=4.0)

    @commands.command(aliases=['bater'])
    async def tapa(self, ctx, members:commands.Greedy[discord.Member], *, reason='nenhum motivo.'):
        slapped = ", ".join(x.name for x in members)
        await ctx.send('{} levou um tapa por {}'.format(slapped, reason))



def setup(client):
    client.add_cog(Outros(client))
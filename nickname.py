from data import settings

def setup(client):

    @client.event
    async def on_ready():
        if client.user.name is not f'[{settings.bot_prefix}] {settings.bot_name}':
            await client.user.edit(username=f'[{settings.bot_prefix}] {settings.bot_name}')
            print('Nome do bot atualizado.')
        else:
            print('Nome do bot já está correto.')
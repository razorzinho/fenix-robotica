from discord.ext import commands
import pymongo
from data import database

class Database(commands.Cog):

    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Database(client))

client = pymongo.MongoClient(f'{database.host}:{database.password}@cluster0.0n6lq.mongodb.net/{database.database}?retryWrites=true&w=majority')
db = client.test
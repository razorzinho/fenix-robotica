import discord
from discord.ext import commands
import mysql.connector
from data import database
database = database.mydb

frdb = mysql.connector.connect(
    host = database.host,
    user = database.user,
    password = database.password,
    database = database.database
)

cursor = frdb.cursor()
cursor.execute('SHOW DATABASES')

for dbs in cursor:
    if not database.database in dbs:
        frdb.execute(f'CREATE DATABASE {database.database}')

class Database(commands.Cog):

    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Database(client))
import discord
from discord.ext import commands
import mysql.connector
from data import database
database = database.mydb

class Database(commands.Cog):

    def __init__(self, client):
        self.client = client

frdb = mysql.connector.connect(
    host = database.host,
    user = database.user,
    password = database.password,
    database = database.database
)

cursor = frdb.cursor()
cursor.execute("SHOW DATABASES")

for dbs in cursor:
    if not database.database in dbs:
        frdb.execute(f"CREATE DATABASE {database.database}")

frdb.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")


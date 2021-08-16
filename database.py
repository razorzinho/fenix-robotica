import pymongo
from data import settings
from modules.storage import *

# Função de conexão ao banco de dados:
def get_database(db):
    if not db:
        raise TypeError('O banco de dados que será utilizado deve ser especificado.')
    # Linha que define a conexão ao banco usando os dados:
    CONNECTION_STRING = f'{settings.host}:{settings.password}@{settings.cluster}.{settings.port}/{db}?retryWrites=true&w=majority'
    # Iniciar conexão
    try:
        cursor = pymongo.MongoClient(CONNECTION_STRING)
        # Criar o banco de dados:
        print('Banco de dados acessado com êxito.')
        return cursor[db]
    except:
        raise TypeError('Não foi possível conectar-se ao banco de dados, ou algum dado de conexão está incorreto.')

# Função de registro de dados na coleção desejada:
def to_collection(db:str, collection:str, data):
    if not db:
        raise TypeError('O banco de dados deve ser especificado.')
    if not collection:
        raise TypeError('A coleção do banco deve ser especificada.')
    if not data:
        raise TypeError('Algum dado deve ser passado para ser inserido ao banco.')
    get_db = get_database(db)
    collection = get_db[collection]
    collection.insert_once(data)

# Função de obtenção de dados do banco de dados:
def from_database(db, collection, data=None, one: bool=False):
    data = data if data else {}
    if one and not data: 
        raise TypeError('Para buscar um dado específico, o filtro deve ser especificado.')
    db = get_database(db)
    collection = db[collection]
    if one:
        return collection.find_one(data)
    return collection.find({}, data)

def test_db():
        try:
            dbname = get_database(settings.db)
            test = {
                'data':
                {
                    'Foo': 'Success'
                }
            }
            col = 'testing'
            to_collection(db=settings.db, collection=col, data=test)
            print(test)
            print('OK! Dados acima enviados ao banco de dados.')
            print('Agora, testando extração de dados...')
        except:
            raise TypeError('O teste de registro falhou por algum motivo.')
        try:
            dbname = from_database(settings.db, collection='test', one=False)
            print(dbname)
            print('Teste de extração de dados realizado com êxito.')
        except:
            raise TypeError('Algo deu errado com o teste de extração de dados.')


# Isto faz com que seja possível que outros arquivos do prorama utilizem esta conexão ao banco:
if __name__ == "__main__":
    test_db()

def setup(client):
    @client.event
    async def on_ready():
        print('Banco de dados executado...')
        get_database(settings.db)
        test_db()

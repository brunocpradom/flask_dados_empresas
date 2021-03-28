from pymongo import MongoClient

host = '172.17.0.1'

def connexion():
    client = MongoClient(host = host)
    db = client.dados_empresas
    return db
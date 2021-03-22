import os
import glob
import csv
import pandas as pd
import time
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import pandas as pd
from tqdm import tqdm
from sul_de_minas import sul_de_minas

Base = declarative_base()

class Config(Base):
    """Classe que defini a tabela que conterá informações como data da
    última atualização da tabela, data_de_criação do banco de dados,
    quantas vezes ele já foi atualizado.
    """
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    data_atualizacao = Column(String(40))
    data_de_criacao_banco_de_dados = Column(String(40))
    num_atualizacoes = Column(String(30))

    def __init__(self,data_atualizacao, data_de_criacao_banco_de_dados, num_atualizacoes):
        self.data_atualizacao = data_atualizacao
        self. data_de_criacao_banco_de_dados = data_de_criacao_banco_de_dados
        self.num_atualizacoes = num_atualizacoes

    def __repr__(self):
        return "<Config(data_atualizacao = '%s')>" % self.data_atualizacao

class Empresas(Base):
    """Classe que defini a tabela que conterá informações das empresas
    Fonte de dados:Receita federal
    """
    __tablename__ = 'empresas'

    cnpj = Column(String(50),primary_key=True)
    id = Column(String(50))
    nome_empresarial =Column(String(300))
    nome_Fantasia = Column( String(200))
    situacao_cadastral =Column(String(40))
    data_da_situacao_cadastral = Column(String(50))
    motivo_cadastral = Column(String(100))
    cod_natureza_juridica = Column(String(100))
    data_inicio_ativ = Column(String(50))
    cnae_fiscal = Column(String(50), index = True )
    tipo_de_logradouro = Column(String(200))
    logradouro = Column(String(300))
    numero = Column(String(100))
    complemento = Column(String(200))
    bairro = Column(String(100))
    cep = Column(String(100))
    uf = Column(String(90),index = True)
    cod_municipio = Column(String(90))
    municipio = Column(String(200),index = True)
    ddd = Column(String(50))
    telefone = Column(String(50))
    ddd2 =Column(String(50))
    telefone2 = Column(String(50))
    ddd3 = Column(String(50))
    fax = Column(String(50))
    e_mail = Column(String(200))
    qualif_do_responsavel = Column(String(50))
    capital_social = Column(String(50))
    porte = Column(String(50))
    opcao_pelo_simples = Column(String(40))
    data_opcao_pelo_simples = Column(String(50))
    data_exclusao_do_simples = Column(String(50))
    opcao_pelo_MEI = Column(String(50))
    situacao_especial = Column(String(100))
    data_situacao_especial = Column(String(50))

def empresas_to_mysql(engine):
    os.chdir('/mnt/DeV/projects/1_pessoal/busca_cnpj/dados/dados_12_2020/dados/UFs/MG')
    client = MongoClient("mongodb+srv://bcpm:bcpm1921@empresasmg.rqldh.mongodb.net/empresas?retryWrites=true&w=majority")
    db = client.empresas_sul_de_minas
    document = db.empresas

    print('upper()')
    sul_de_minas_upper = [cidade.upper() for cidade in sul_de_minas]

    for file in glob.glob('*.*'):

        if file.replace('1.csv','') in sul_de_minas_upper:
            print(file)
            open_file = csv.DictReader(open(str(file),encoding = 'utf-8'))

            df =pd.read_csv(str(file), index_col = 'CNPJ')
            df.to_sql('empresas', con = engine , if_exists = 'append', method = 'multi', chunksize = 100000)

def main_tables():
    print('starting engine')
    engine = create_engine("mysql://{user}:{pw}@{host}/{db}".format(user = 'brunocpradom',
                                                    pw =   'bcpm1921',
                                                    host ='brunocpradom.mysql.pythonanywhere-services.com',
                                                    db ='brunocpradom$empresas_sul_de_minas'))
    print('Creating tables')
    Base.metadata.create_all(engine, checkfirst =True)
    print('ok')
    print('iniciando inserção de dados')
    empresas_to_mysql(engine)

main_tables()
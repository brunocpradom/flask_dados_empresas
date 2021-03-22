import os
import glob
import csv
from pymongo import MongoClient
from sul_de_minas import sul_de_minas

os.chdir('/mnt/DeV/projects/1_pessoal/busca_cnpj/dados/dados_12_2020/dados/UFs/MG')
#client = MongoClient()
client = MongoClient("mongodb+srv://bcpm:bcpm1921@empresasmg.rqldh.mongodb.net/empresas?retryWrites=true&w=majority")
db = client.empresas_sul_de_minas
document = db.empresas

print('upper()')
sul_de_minas_upper = [cidade.upper() for cidade in sul_de_minas]


for file in glob.glob('*.*'):

    if file.replace('1.csv','') in sul_de_minas_upper:
        print(file)
        open_file = csv.DictReader(open(str(file),encoding = 'utf-8'))
        list_of_dict = []
        for row in open_file:
            list_of_dict.append(row)

        result = document.insert_many(list_of_dict)
        result.inserted_ids
import os

from flask import Flask, render_template, request, jsonify
from helpers import (
    situacao_cadastral, find_emp, find_soc,find_cnpj_attached_to_socios,
    cnae_setor, find_cnae, render_pie_chart
                    )

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY")
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    return app

app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cnpj',methods= [ 'POST'])
def cnpj():
    texto ={}
    cnpj = request.json.get('cnpj','')
    
    texto['CNPJ'] = request.json.get('cnpj')

    datas = find_emp(texto)
    
    return jsonify(datas)

@app.route('/cnae',methods = ['POST'])
def cnae():
    texto = {}
    texto['CNAE_fiscal'] = request.json['cnae']
    texto['Município'] = request.json['municipio'].upper()
    texto = situacao_cadastral(texto,request.json['situacao_cadastral'])
        
    datas = find_emp(texto)
    return jsonify(datas)


@app.route('/cnaeporsetor',methods = [ 'POST'])
def cnae_por_setor():
    cod_setor = request.json['codigo_setor']
    municipio = request.json['municipio']
    sit_cad = request.json['situacao_cadastral']

    texto = cnae_setor(cod_setor,municipio,sit_cad)
    datas = find_emp(texto)
    return jsonify(datas)
        
    
@app.route('/cnaeporuf', methods = ['POST'])
def cnae_por_uf():
    texto = {}
    texto['CNAE_fiscal'] = request.json['cnae'] 
    texto['UF'] = request.json['uf'].upper()
    texto = situacao_cadastral(texto,sit = request.json['situacao_cadastral'])
    datas = find_emp(texto)
    return jsonify(datas)


@app.route('/cnaebusca', methods = ['POST'])
def search_cnae_meaning():

    texto = {}
    cnae_regex ={}
    cnae_regex['$regex'] = request.json['atividade_economica']
    texto['CNAE_sig'] = cnae_regex
    
    datas = find_cnae(texto)
    
    return jsonify(datas)

@app.route('/municipio',methods =['POST'])
def municipio():
    texto = {}
    texto['Município'] = request.json['municipio'].upper()
    texto = situacao_cadastral(texto,request.json['situacao_cadastral'])
    
    datas = find_emp(texto)
    
    return jsonify(datas)


@app.route('/socios', methods = ['POST'])
def socios_attach_to_cnpj():
    
    cnpj = request.json['cnpj']
    texto = {}
    texto['cnpj'] = cnpj.strip()
    
    datas = find_soc(texto)
    
    return jsonify(datas)
    

@app.route('/socios/nome',methods =['POST'])
def socios_nome():
    nome_socio = request.json['nome']
    texto = {}
    texto['nome_socio'] = nome_socio.upper()
    datas = find_cnpj_attached_to_socios(texto)

    return jsonify(datas)



        

@app.route('/graficos',methods=['GET', 'POST'])
def graficos():
    if request.method == 'POST':
        
        cidade = request.json['municipio']
        texto = {}
        texto['Município'] = cidade.upper()
        
        data = render_pie_chart(texto)
        
                
        return jsonify({'lista':data})
        

# @app.route('/graficos/empresasativas',methods = ['GET', 'POST'])
# def empresas_ativas():
#     if request.method == 'POST':
#         client = MongoClient()
#         db = client.dados_empresas
#         emp_ativa = db.empresas_ativas2
        
#         cidade =request.form['municipio']
#         setor = request.form['setor']
        
        
#         todas_datas = emp_ativa.distinct('data')
#         lista = list(todas_datas)
#         valores_para_grafico =[]
#         for i in lista:
#             parametros = []
#             texto = {}
#             texto['data'] = i
#             texto["Município"] = cidade.upper()
#             result = emp_ativa.find(texto,{'_id' : 0, setor.upper() : 1})
#             parametros.append(list(result)[0][setor.upper()])
#             parametros.append(i)
#             valores_para_grafico.append(parametros)
#             
            
#         datas =[]
#         qtd_empresas = []
        
#         for n in valores_para_grafico:
#             qtd_empresas.append(n[0])
#             datas.append(n[1])
        
#         doc2 = db.empresas_ativas
#         texto2 = {}
#         texto2['Município'] = cidade.upper()
#         result2 = doc2.find(texto2,{'_id':0, setor.upper():1,'data':1})
#         lista2 = list(result2)
#         
        
#         qtd_empresas.append(lista2[0][setor.upper()])
#         datas.append(lista2[0]['data'])
        
        
#         lista ={'A': 'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA',
#                 'B': 'INDÚSTRIAS EXTRATIVAS',
#                 'C': 'INDÚSTRIAS DE TRANSFORMAÇÃO',
#                 'D': 'ELETRICIDADE E GÁS',
#                 'E': 'ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO',
#                 'F': 'CONSTRUÇÃO',
#                 'G': 'COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS',
#                 'H': 'TRANSPORTE, ARMAZENAGEM E CORREIO',
#                 'I': 'ALOJAMENTO E ALIMENTAÇÃO',
#                 'J': 'INFORMAÇÃO E COMUNICAÇÃO',
#                 'K': 'ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS',
#                 'L': 'ATIVIDADES IMOBILIÁRIAS',
#                 'M': 'ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS',
#                 'N': 'ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES',
#                 'O': 'ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL',
#                 'P': 'EDUCAÇÃO',
#                 'Q': 'SAÚDE HUMANA E SERVIÇOS SOCIAIS',
#                 'R': 'ARTES, CULTURA, ESPORTE E RECREAÇÃO',
#                 'S': 'OUTRAS ATIVIDADES DE SERVIÇOS',
#                 'T': 'SERVIÇOS DOMÉSTICOS',
#                 'U': 'ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS'}
#         titulo = lista[setor.upper()] + ' - ' + cidade.upper()
#         plt.title(titulo)
#         plt.plot(datas, qtd_empresas)
#         plt.ylabel('números de empresas')
        
#         nome = './static/' +  cidade + setor + '_emp_at' + '.jpg'
#         plt.savefig(nome)
        
#         return render_template('resultadograficos.html', img = nome)
#     if request.method == 'GET':
#         return render_template('empresasativas.html')

if __name__ == '__main__':
    app.run(debug=True)
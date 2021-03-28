import os

from flask import Flask, render_template,flash, request,redirect , url_for

from database import connexion
from helpers import (situacao_cadastral, find_emp, find_soc,find_cnpj_attached_to_socios,
                    cnae_setor, find_cnae)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cnpj',methods= ['GET', 'POST'])
def cnpj():
    if request.method =='POST':
        texto ={}
        texto['CNPJ'] = str(request.form['cnpj'])

        datas = find_emp(texto)
        return render_template('datatable.html', datas = datas)
    
    if request.method =='GET':
        return render_template('cnpj.html')

@app.route('/cnae',methods = ['GET', 'POST'])
def cnae():
    if request.method =='POST':
        texto = {}
        texto['CNAE_fiscal'] = request.form['cnae']
        texto['Município'] = request.form['municipio'].upper()
        texto = situacao_cadastral(texto,request.form['sit_cad'])
        
        datas = find_emp(texto)
            
        return render_template('datatable.html', datas = datas)
    if request.method == 'GET':
        return render_template('cnae.html')

@app.route('/municipio',methods =['GET','POST'])
def municipio():
    if request.method =='POST':
        texto = {}
        texto['Município'] = request.form['municipio'].upper()
        texto = situacao_cadastral(texto,request.form['sit_cad'])
        
        datas = find_emp(texto)
    
        return render_template('datatable.html', datas = datas)

    if request.method == 'GET':
        return render_template('municipio.html')

@app.route('/socios', methods = ['GET', 'POST'])
def socios_attach_to_cnpj():
    if request.method =='POST':
        cnpj = request.form['cnpj']
        texto = {}
        texto['cnpj'] = cnpj.strip()
        
        datas = find_soc(texto)
        
        return render_template('datatablesocios.html', datas = datas)

    if request.method == 'GET':
        return render_template('socios.html')

@app.route('/socios/nome',methods =['GET', 'POST'])
def socios_nome():
    if request.method == 'POST':
        nome_socio = request.form['nome']
        texto = {}
        texto['nome_socio'] = nome_socio.upper()
        datas = find_cnpj_attached_to_socios(texto)

        return render_template('datatable.html', datas = datas)
    
    if request.method == 'GET':
        return render_template('sociosnome.html')

@app.route('/cnaeporsetor',methods = ['GET', 'POST'])
def cnae_por_setor():
    if request.method == 'POST':
        cod_setor = request.form['cod_setor']
        municipio = request.form['municipio']
        sit_cad = request.form['sit_cad']

        texto = cnae_setor(cod_setor,municipio,sit_cad)
        datas = find_emp(texto)
        return render_template('datatable.html', datas = datas)
        
    if request.method == 'GET':
        return render_template('cnaeporsetor.html')

@app.route('/cnaeporuf', methods = ['GET', 'POST'])
def cnae_por_uf():
    if request.method == 'POST':
        texto = {}
        texto['CNAE_fiscal'] = request.form['cnae'] 
        texto['UF'] = request.form['estado'].upper()
        texto = situacao_cadastral(texto,sit = request.form['sit_cad'])
        datas = find_emp(texto)

        return render_template('datatable.html', datas = datas)

    if request.method == 'GET':
        return render_template('cnaeporuf.html')

@app.route('/cnaebusca', methods = ['GET', 'POST'])
def search_cnae_meaning():
    if request.method == 'POST':
        
        texto = {}
        cnae_regex ={}
        cnae_regex['$regex'] = request.form['ativ_econom']
        texto['CNAE_sig'] = cnae_regex
        
        datas = find_cnae(texto)

        return render_template('datatable_ativ_econ.html', datas = datas)
        
    if request.method == 'GET':

        return render_template('cnaebusca.html')

#!Daqui pra baixo preciso reescrever usando o highchart ao invés do matplotlib
# @app.route('/graficos',methods=['GET', 'POST'])
# def graficos():
#     if request.method == 'POST':
#         client = MongoClient()
#         db = client.dados_empresas
#         graficos = db.empresas_ativas
        
#         cidade = request.form['municipio']
#         texto = {}
#         texto['Município'] = cidade.upper()
        
#         
#         results = graficos.find(texto,{'_id': 0, 'data':0})
        
#         alfabeto = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']
        
#         lista = []
        
#         for i in results:
#             for n in alfabeto:
#                 lista.append(i[n])
        
#         
        
#         labels = ['Agricultura,pecuária,prod.florestal,pesca','Indústrias extrativas','Indústrias de transformação',
#         'Eletricidade e gás','Água,esgoto,ativ.gest.resíduos','Construçãp','Comércio,reparação de veículos',
#         'Transporte, armazenagem e correio','Alojamento e alimentação','Informação e comunicação',
#         'Ativ.financeiras de seguros e serv.rel.','Atividades imobiliárias','At. profissionais tec. e científicas',
#         'Ativ.administrativas e serv. complementares','Admin.pública,defesa e seguridade social','Educação',
#         'Saúde humana e serviços sociais','Artes,cultura,esporte e recreação','Outras ativ. de serviços',
#         'Serviços domésticos','Org.internacionais e outras inst.extraterritoriais']
        
#         data = lista
#         explode = (0,0.1,0,0)
        
#         ax =plt.gca()
        
#         wedges, texts = ax.pie(data, colors =['lightgray','lightcoral','firebrick','red','peru','orange','gold','yellow',
#                                     'olive','yellowgreen','lawngreen','green','aquamarine','lightseagreen',
#                                     'deepskyblue','blueviolet','violet','magenta','crimson','black','pink',
#                                     'darkolivegreen','dodgerblue'])
#         plt.rcParams['figure.figsize'] = (15,8)
#         ax.legend(wedges,labels,
#                 title="Setores",
#                 loc="center left",
#                 bbox_to_anchor=(1, 0, 0.5, 1))
        
#         #plt.setp(autotexts, size=8, weight="bold")
        
#         titulo = 'Empresas por setor - ' + cidade.upper()
#         ax.set_title(titulo)
        
#         nome = './static/' +  cidade +'.jpg'
        
#         plt.savefig(nome)
        
#         return render_template('resultadograficos.html', img = nome)
#         #return send_file(nome,as_attachment=True)
#     if request.method =='GET':
#         return render_template('graficos.html')

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
#             print('primeira pesquisa')
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
#         print('segunda pesquisa')
#         
#         qtd_empresas.append(lista2[0][setor.upper()])
#         datas.append(lista2[0]['data'])
#         
#         
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
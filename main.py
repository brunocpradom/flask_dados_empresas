import sys
from flask import Flask, render_template,flash, request,redirect , url_for, session, send_file
from pymongo import MongoClient
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template('cnpj.html')

@app.route('/cnpj',methods= ['GET', 'POST'])
def cnpj():
    if request.method =='POST':
        client = MongoClient()
        db = client.dados_empresas
        documents = db.empresas
        
        cnpj = request.form['cnpj']
        texto ={}
        texto['CNPJ'] = str(cnpj)
        
        print(texto,file=sys.stderr)
        
        result = documents.find(texto,{'_id':0})
        print(result,file=sys.stderr)
        datas=[]
        for i in result:
            datas.append(i)
        
        data_table = []
        for n in range(len(datas)):
            for i in datas[n]:
                data_table.append(datas[n][i])  
        
            
            
        return render_template('datatable.html', datas = datas)
    
    if request.method =='GET':
        return render_template('cnpj.html')

@app.route('/cnae',methods = ['GET', 'POST'])
def cnae():
    if request.method =='POST':
        client = MongoClient()
        db = client.dados_empresas
        documents = db.empresas
        
        cnae = request.form['cnae']
        municipio = request.form['municipio']
        sit_cad = request.form['sit_cad']
        
        texto = {}
        texto['CNAE_fiscal'] = cnae
        texto['Município'] = municipio
        texto['Situação_cadastral'] = sit_cad
        print(texto,file=sys.stderr)
        
        result = documents.find(texto,{'_id':0})
        
        datas=[]
        for i in result:
            datas.append(i)
        for i in datas:
            print(i,file=sys.stderr)
            print('',file=sys.stderr)
            
        data_table = []
        for n in range(len(datas)):
            for i in datas[n]:
                data_table.append(datas[n][i])  
        #for i in data_table:
        #    print(i,file=sys.stderr)
        #print(data_table,file=sys.stderr)
        
            
            
        return render_template('datatable.html', datas = datas)
    if request.method == 'GET':
        return render_template('cnae.html')

@app.route('/municipio',methods =['GET','POST'])
def municipio():
    if request.method =='POST':
        client = MongoClient()
        db = client.dados_empresas
        documents = db.empresas
        
        municipio = request.form['municipio']
        sit_cad = request.form['sit_cad']
        
        texto = {}
        texto['Município'] = municipio.upper()
        texto['Situação_cadastral'] = sit_cad.lower()
        print(texto,file=sys.stderr)
        
        result = documents.find(texto,{'_id':0})
        
        datas=[]
        for i in result:
            datas.append(i)
        for i in datas:
            print(i,file=sys.stderr)
            print('',file=sys.stderr)
            
        data_table = []
        for n in range(len(datas)):
            for i in datas[n]:
                data_table.append(datas[n][i])  
        #for i in data_table:
        #    print(i,file=sys.stderr)
        #print(data_table,file=sys.stderr)
        
            
            
        return render_template('datatable.html', datas = datas)
    if request.method == 'GET':
        return render_template('municipio.html')

@app.route('/socios', methods = ['GET', 'POST'])
def socios():
    if request.method =='POST':
        client = MongoClient()
        db = client.dados_empresas
        socios = db.socios
        
        cnpj = request.form['cnpj']
                
        texto = {}
        texto['cnpj'] = cnpj.strip()
        
        socios_dict = []
       
        result = socios.find(texto,{'_id':0})
        
        for i in result:
            socios_dict.append(i)
        
       
        return render_template('datatablesocios.html', datas = socios_dict)
    if request.method == 'GET':
        return render_template('socios.html')

@app.route('/socios/nome',methods =['GET', 'POST'])
def socios_nome():
    if request.method == 'POST':
        client = MongoClient()
        db = client.dados_empresas
        socios = db.socios
        
        nome_socio = request.form['nome']
                
        texto = {}
        texto['nome_socio'] = nome_socio.upper()
        
        socios_dict = []
       
        result = socios.find(texto,{'_id':0})
        
        for i in result:
            socios_dict.append(i)
        
        dict_cnpjs={}
        lista=[]
        for n in range(len(socios_dict)):
                dict_cnpjs['CNPJ'] = socios_dict[n]['cnpj']
                lista.append(dict_cnpjs)
                dict_cnpjs = {}
        
        texto2 = {}
        texto2['$or'] = lista
        documents = db.empresas
        
        result = documents.find(texto2,{'_id':0 })
        datas = []
        data_table =[]
        for i in result :
            datas.append(i)
       
        return render_template('datatable.html', datas = datas)
    
    if request.method == 'GET':
        return render_template('sociosnome.html')

# @app.route('/graficos',methods=['GET', 'POST'])
# def graficos():
#     if request.method == 'POST':
#         client = MongoClient()
#         db = client.dados_empresas
#         graficos = db.empresas_ativas
        
#         cidade = request.form['municipio']
#         texto = {}
#         texto['Município'] = cidade.upper()
        
#         print(texto,file=sys.stderr)
#         results = graficos.find(texto,{'_id': 0, 'data':0})
        
#         alfabeto = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']
        
#         lista = []
        
#         for i in results:
#             for n in alfabeto:
#                 lista.append(i[n])
        
#         print(lista,file=sys.stderr)
        
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
#             print(valores_para_grafico,file=sys.stderr)
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
#         print(lista2,file=sys.stderr)
#         qtd_empresas.append(lista2[0][setor.upper()])
#         datas.append(lista2[0]['data'])
#         print('quantidade de empresas :', qtd_empresas,file=sys.stderr )
#         print(datas,file=sys.stderr)
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

@app.route('/cnaeporsetor',methods = ['GET', 'POST'])
def cnae_por_setor():
    if request.method == 'POST':
        cod_setor = request.form['cod_set']
        municipio = request.form['municipio']
        sit_cad = request.form['sit_cad']
        
        cnae_setor ={'A': "(^01\w*|^02\w*|^03\w*)" ,
            'B': "(^05\w*|^06\w*|^07\w*|^08\w*|^09\w*)" , 
            'C': "(^10\w*|^11\w*|^12\w*|^13\w*|^14\w*|^15\w*|^16\w*|^17\w*|^18\w*|^19\w*|^20\w*|^21\w*|^22\w*|^23\w*|^24\w*|^25\w*|^26\w*|^27\w*|^28\w*|^29\w*|^30\w*|^31\w*|^32\w*|^33\w*)" , 
            'D': "(^35\w*)" , 
            'E': "(^36\w*|^37\w*|^38\w*|^39\w*)",
            'F': "(^41\w*|^42\w*|^43\w*)" , 
            'G': "(^45\w*|^46\w*|^47\w*)",
            'H': "(^49\w*|^50\w*|^51\w*|^52\w*|^53\w*)" , 
            'I': "(^55\w*|^56\w*)" , 
            'J': "(^58\w*|^59\w*|^60\w*|^61\w*|^62\w*|^63\w*)" , 
            'K': "(^64\w*|^65\w*|^66\w*)" , 
            'L': "(^68\w*)" , 
            'M': "(^69\w*|^70\w*|^71\w*|^72\w*|^73\w*|^74\w*|^75\w*)" , 
            'N': "(^77\w*|^78\w*|^79\w*|^80\w*|^81\w*|^82\w*)" , 
            'O': "(^84\w*)" , 
            'P': "(^85\w*)" , 
            'Q': "(^86\w*|^87\w*|^88\w*)",
            'R': "(^90\w*|^91\w*|^92\w*|^93\w*)" , 
            'S': "(^94\w*|^95\w*|^96\w*)" , 
            'T': "(^97\w*)" , 
            'U': "(^99\w*)" } 

        list_alf =['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']
        
        for alf in list_alf:
            if cnaeregex.upper() == alf:
                situação_cadastral = self.root.ids.sitcadsetor.text                
                
                texto = {}
                texto['$regex'] = cnae_setor[alf]
                
                dict1 = {}
                dict2 = {}
                dict1['CNAE_fiscal']= texto
                dict2['Município'] = texto2.upper()
                lista = []
                
                lista.append(dict1)
                lista.append(dict2)
                
                texto = {}
                texto['$and'] = lista
                self.situacao_cadastral(texto = texto,sit = situação_cadastral)
                
                return texto
        
    if request.method == 'GET':
        return render_template('cnaeporsetor.html')

@app.route('/cnaeporuf')
def cnae_por_uf():
    return render_template('cnaeporuf.html')

@app.route('/cnaebusca')
def cnaebusca():
    return render_template('cnaebusca.html')


if __name__ == '__main__':
    app.run(debug=True)
from database import connexion

def situacao_cadastral(texto,sit):
        if sit.lower() == '':
            return texto
        if sit.lower() == 'todas':
            return texto
        if sit.lower() == 'ativa':
            texto['Situação_cadastral'] = sit.lower()
            return texto
        if sit.lower() == 'outros':
            outros = {}
            lista_parametros = []
            outros['Situação_cadastral']= 'baixada'
            lista_parametros.append(outros)
            outros = {}
            outros['Situação_cadastral']= 'suspensa'
            lista_parametros.append(outros)
            outros = {}
            outros['Situação_cadastral']= 'inapta'
            lista_parametros.append(outros)
            outros = {}
            outros['Situação_cadastral'] = 'nula'

            texto['$or'] = lista_parametros
            return texto

def find_emp(texto):
    db = connexion()
    documents = db.empresas
    result = documents.find(texto,{'_id':0})
    datas=[]
    for i in result:
        datas.append(i)

    return datas

def find_cnae(texto):
    
    db = connexion()
    documents = db.cnae_legenda
    result = documents.find(texto,{'_id':0})
    datas = []
    for i in result :
        datas.append(i)
    return datas

def find_soc(texto):
    db = connexion()
    socios = db.socios
    result = socios.find(texto,{'_id':0})
    datas = []
    for i in result:
        datas.append(i)
    return datas

def find_cnpj_attached_to_socios(texto):
    db = connexion()
    socios = db.socios
    result = socios.find(texto,{'_id':0})
    socios_dict = []
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
    for i in result :
        datas.append(i)
    return datas

def cnae_setor(cod_setor, municipio, sit_cad):
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
        if cod_setor.upper() == alf:                
            
            texto = {}
            texto['$regex'] = cnae_setor[alf]
            
            dict1 = {}
            dict2 = {}
            dict1['CNAE_fiscal']= texto
            dict2['Município'] = municipio.upper()
            lista = []
            
            lista.append(dict1)
            lista.append(dict2)
            
            texto = {}
            texto['$and'] = lista
            texto = situacao_cadastral(texto = texto,sit = sit_cad)
            
            return texto

def render_pie_chart(texto):
    db = connexion()
    graficos = db.empresas_ativas
    results = graficos.find(texto,{'_id': 0, 'data':0})
        
    alfabeto = [
        'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q',
        'R','S','T','U'
        ]
    
    lista = []
    
    for i in results:
        for n in alfabeto:
            lista.append(i[n])
            
    return lista
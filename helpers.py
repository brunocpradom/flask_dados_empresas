

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
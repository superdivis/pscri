# +-------------------------------------------------------------+
# | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
# | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
# | Data inicio: 01/07/2024                                     |
# | Data finalização: xx/xx/xx                                  |
# | Autor: Alexandre Silva dos Santos                           |
# | Email: alexandresantoscompunb@gmail.com                     |
# +-------------------------------------------------------------+----------------------------------------------------------

#Serviços da calculadora

import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from datetime import date
from calculadora_ipea_dao import * 
from processamento import *
from operator import itemgetter

#+------------------------
#| Constantes iniciais 
#+------------------------
ip = 'localhost'
#ip = '10.4.201.187'
#ip = '192.168.0.8' 

max_col = 340
max_lin = 340
min_lin = 1
min_col = 1

app = Flask(__name__)
CORS(app, support_credentials=True)

#+------------------------
#| Inicia as variáveis
#+------------------------
atividades_contas_nacionais = retorna_atividades()
matriz_insumo = prepara_ajuste_matriz(max_lin, max_col)
regioes_br = retorna_regioes()
vetor_y = prepara_vetor_y(max_lin, min_col)
pib_atual = ler_vetor_pib(max_lin, min_col)
vetor_x = prepara_vetor_x(matriz_insumo,vetor_y)
vetor_v = calcular_vetor_v(pib_atual,vetor_x)
delta_y = np.zeros((max_lin,1), dtype=np.float64)

#+---------------------------+
#| Inicialização dos choques |
#+---------------------------+----------------------
#Vetores
delta_y_n = np.zeros((max_lin,1), dtype=np.float64)
delta_y_ne = np.zeros((max_lin,1), dtype=np.float64)
delta_y_se = np.zeros((max_lin,1), dtype=np.float64)
delta_y_s = np.zeros((max_lin,1), dtype=np.float64)
delta_y_co = np.zeros((max_lin,1), dtype=np.float64)

#Choque default na atividade 1 - Agricultura, inclusive o apoio à agricultura e a pós-colheita
delta_y_n[0]    = 1000
delta_y_ne[68]  = 1000
delta_y_se[136] = 1000
delta_y_s[204]  = 1000
delta_y_co[272] = 1000

#+-----------------------------+
#|Quadro Resumo - Multiplicador|
#+-----------------------------+----------------------
delta_x_n = preparar_delta_x(matriz_insumo,delta_y_n)
delta_x_ne = preparar_delta_x(matriz_insumo,delta_y_ne)
delta_x_se = preparar_delta_x(matriz_insumo,delta_y_se)
delta_x_s = preparar_delta_x(matriz_insumo,delta_y_s)
delta_x_co = preparar_delta_x(matriz_insumo,delta_y_co)
delta_x = monta_delta_x(delta_x_n[0:68],delta_x_ne[68:136],delta_x_se[136:204],delta_x_s[204:272],delta_x_co[272:])

delta_pib_n = calcular_delta_pib(pib_atual, vetor_v, delta_x_n)
delta_pib_ne = calcular_delta_pib(pib_atual, vetor_v, delta_x_ne)
delta_pib_se = calcular_delta_pib(pib_atual, vetor_v, delta_x_se)
delta_pib_s = calcular_delta_pib(pib_atual, vetor_v, delta_x_s)
delta_pib_co = calcular_delta_pib(pib_atual, vetor_v, delta_x_co)

#Cálculo dos vetores com os PIBs novos
pib_novo_n  =  calcular_novo_pib(pib_atual,delta_pib_n)
pib_novo_ne  =  calcular_novo_pib(pib_atual,delta_pib_ne)
pib_novo_se  =  calcular_novo_pib(pib_atual,delta_pib_se)
pib_novo_s  =  calcular_novo_pib(pib_atual,delta_pib_s)
pib_novo_co  =  calcular_novo_pib(pib_atual,delta_pib_co)

#Totals dos vetores com os PIBs novos por região
pib_novo_soma_n = np.sum(pib_novo_n[0:68])
pib_novo_soma_ne = np.sum(pib_novo_ne[68:136])
pib_novo_soma_se = np.sum(pib_novo_se[136:204])
pib_novo_soma_s =  np.sum(pib_novo_s[204:272])
pib_novo_soma_co = np.sum(pib_novo_co[272:])
pib_novo = pib_novo_n[0:68] + pib_novo_ne[68:136] + pib_novo_se[136:204] + pib_novo_s[204:272] + pib_novo_co[272:]

#Cálculo dos multiplicadores
multiplicador_n = round(np.sum(delta_x_n)/np.sum(delta_y_n),2)
multiplicador_ne = round(np.sum(delta_x_ne)/np.sum(delta_y_ne),2)
multiplicador_se = round(np.sum(delta_x_se)/np.sum(delta_y_se),2)
multiplicador_s = round(np.sum(delta_x_s)/np.sum(delta_y_s),2)
multiplicador_co = round(np.sum(delta_x_co)/np.sum(delta_y_co),2)

#Cálculo dos PIBs
pib_atual_soma_n = np.sum(pib_atual[0:68])
pib_atual_soma_ne = np.sum(pib_atual[68:136])
pib_atual_soma_s =  np.sum(pib_atual[204:272])
pib_atual_soma_se = np.sum(pib_atual[136:204])
pib_atual_soma_co = np.sum(pib_atual[272:])

#Cálculo dos vazamentos
vazamento_n = round(((np.sum(delta_x_n) - np.sum(delta_x_n[0:68])) / np.sum(delta_x_n)) * 100 ) 
vazamento_ne = round(((np.sum(delta_x_ne) - np.sum(delta_x_ne[68:136])) / np.sum(delta_x_ne)) * 100  )
vazamento_s = round(((np.sum(delta_x_s) - np.sum(delta_x_s[204:272])) / np.sum(delta_x_s)) * 100  )
vazamento_se = round(((np.sum(delta_x_se) - np.sum(delta_x_se[136:204])) / np.sum(delta_x_se)) * 100  )
vazamento_co = round(((np.sum(delta_x_co) - np.sum(delta_x_co[272:])) / np.sum(delta_x_co)) * 100  )

#Cálculo dos percentuais de crescimento
per_pib_n = round(((pib_novo_soma_n / pib_atual_soma_n) - 1) * 100 , 2 )
per_pib_ne = round(((pib_novo_soma_ne / pib_atual_soma_ne) - 1) * 100 , 2 )
per_pib_s = round(((pib_novo_soma_s / pib_atual_soma_s) - 1) * 100 , 2  )
per_pib_se = round(((pib_novo_soma_se / pib_atual_soma_se) - 1) * 100 , 2 )
per_pib_co = round(((pib_novo_soma_co / pib_atual_soma_co) - 1) * 100  , 2 )


@app.route("/")
def index():
    return render_template("index.html")

#+-----------------------------------------------------------
#   ********   ********  **********
#  **//////** /**/////  /////**/// 
# **      //  /**           /**    
#/**          /*******      /**    
#/**    ***** /**////       /**    
#//**  ////** /**           /**    
# //********  /********     /**    
#  ////////   ////////      //     
#
#+-------------------------------------

# Endpoint para listar regioes
@app.route('/regioes', methods=['GET'])
def obter_regioes():
    ret = retorna_regioes()
    regioes = []
    if len(ret) == 0:
        return jsonify({'erro': 'Regiões não encontradas!'}), 404
    #Montagem da lista de jogadores
    for parametro in ret:
        tmp_json={"id":parametro[0] ,"sigla":parametro[1] ,"nome":parametro[2]}
        regioes.append(tmp_json)
    return jsonify(regioes)


# Endpoint para listar nivel territorial
@app.route('/nivelterritorial', methods=['GET'])
def obter_nivel_territorial():
    ret = retorna_nivel_territorial()
    nt = []
    if len(ret) == 0:
        return jsonify({'erro': 'Nivel territorial não encontradas!'}), 404
    #Montagem da lista de jogadores
    for parametro in ret:
        tmp_json={"id":parametro[0] ,"nome":parametro[1] }
        nt.append(tmp_json)
    return jsonify(nt)


# Endpoint para listar atividades
@app.route('/atividades', methods=['GET'])
def obter_atividades():
    ret = retorna_atividades()
    atividades = []
    if len(ret) == 0:
        return jsonify({'erro': 'Atividades não encontradas!'}), 404
    #Montagem da lista de jogadores
    for parametro in ret:
        tmp_json={"id":parametro[0] ,"descricaoatividade":parametro[1] }
        atividades.append(tmp_json)
    return jsonify(atividades)


# Endpoint para listar atividades
@app.route('/matriz', methods=['GET'])
def obter_matriz():
    ret = retorna_matriz() 
    matriz = []
    if len(ret) == 0:
        return jsonify({'erro': 'Matriz não encontradas!'}), 404
    #Montagem do array de valores da matriz
    for parametro in ret:
        tmp_json={"id":parametro[0] ,"linha":parametro[1], "j1":parametro[2] , "j2":parametro[3], "j3":parametro[4], "j4":parametro[5], "j5":parametro[6],"j7":parametro[7]}
        matriz.append(tmp_json)
    return jsonify(matriz)

# Endpoint para obter uma simulação
@app.route('/simulacao/<int:id_simulacao>', methods=['GET'])
def obter_simulacao(id_simulacao):
    ret = obter_simulacao_id(id_simulacao)
    simulacao = []
    if len(ret) == 0:
        return jsonify({'erro': 'Simulação não encontrada!'}), 404
    #Montagem do array de valores de Delta Y
    for parametro in ret:
        tmp_json={"id_simulacao":parametro[0] ,"nome":parametro[1] ,"id_atividade":parametro[2], "descricaoatividade":parametro[3], "id_regiao":parametro[4], "nome_regiao":parametro[5], "valor":parametro[6]}
        simulacao.append(tmp_json)
    return jsonify(simulacao)

# Endpoint para obter simulações gravadas
@app.route('/simulacoes', methods=['GET'])
def obter_simulacoes():
    ret = listar_simulacoes()
    simulacao = []
    if len(ret) == 0:
        return jsonify({'erro': 'Simulações não encontradas!'}), 404
    #Montagem da lista de simulações salvas
    for parametro in ret:
        tmp_json={"id":parametro[0] ,"nome":parametro[1] }
        simulacao.append(tmp_json)
    return jsonify(simulacao)


# Endpoint para obter sistema de dados
@app.route('/sistemas', methods=['GET'])
def obter_sistemas():
    ret = listar_sistemas()
    sistemas = []
    if len(ret) == 0:
        return jsonify({'erro': 'Sistemas não encontrados!'}), 404
    #Montagem da lista de sistemas salvos
    for parametro in ret:
        tmp_json={"id":parametro[0] , "nome":parametro[2] ,  "descricao":parametro[1]}
        sistemas.append(tmp_json)
    return jsonify(sistemas)

# Endpoint para obter sistema de dados
@app.route('/delta_x', methods=['GET'])
def obter_delta_x():
    if len(delta_x_n) == 0:
        return jsonify({'erro': 'Sistemas não encontrados!'}), 404
    #Montagem da lista de sistemas salvos
    i=0
    delta_ret = []
    for item in delta_x_n:
        tmp_json={"index": i , "valor": item }
        delta_ret.append(tmp_json)
    return jsonify(delta_ret)

# Endpoint para obter resumo de informações
@app.route('/resumo', methods=['GET'])
def obter_resumo():
    #Montagem do resumo
    tmp_json={"multiplicador_n": multiplicador_n ,  "multiplicador_ne": multiplicador_ne, 
              "multiplicador_s": multiplicador_s, "multiplicador_se": multiplicador_se, 
              "multiplicador_co": multiplicador_co, "vazamento_n": vazamento_n , "vazamento_ne": vazamento_ne,
              "vazamento_se": vazamento_se , "vazamento_s": vazamento_s ,"vazamento_co": vazamento_co , "per_pib_n": per_pib_n ,
              "per_pib_ne": per_pib_ne , "per_pib_s": per_pib_s , "per_pib_se": per_pib_se , "per_pib_co": per_pib_co }
    return jsonify(tmp_json)

# Endpoint para obter pib bruto
@app.route('/pib_novo_bruto', methods=['GET'])
def obter_pib_novo_bruto():
    if len(pib_novo) == 0:
        return jsonify({'erro': 'PIB Novo não calculado!'}), 404
    #Montagem da lista com o PIB Novo
    i=1
    pib_novo_ret = []
    for item in pib_novo:
        tmp_json={"index": i , "valor": item[0] }
        pib_novo_ret.append(tmp_json)
        i = i + 1
    return jsonify(pib_novo_ret)

# Endpoint para obter pib
@app.route('/pib_novo_completo', methods=['GET'])
def obter_pib_novo_completo():
    atividades = retorna_atividades()
    regioes = retorna_regioes()
    if (len(pib_novo) == 0 & len(atividades) == 0 & len(regioes) == 0):
        return jsonify({'erro': 'PIB Novo completo não calculado!'}), 404
    #Montagem da lista com o PIB Novo
    i = 1
    at = 0
    rg = 0
    pib_novo_ret = []
    for item in pib_novo:
        tmp_json={"index": i , "valor": item[0] , "id_atividade": at + 1 , "desc_atividade": atividades[at][1], "nome_regiao": regioes[rg][2]}
        pib_novo_ret.append(tmp_json)
        i = i + 1
        if (at<=66):
            at = at + 1
        else:
            at=0
            rg = rg + 1
    return jsonify(pib_novo_ret)

# Endpoint para obter pib ordenado pelo valor de crescimento
@app.route('/pib_novo_top', methods=['GET'])
def obter_pib_novo_top():
    atividades = retorna_atividades()
    regioes = retorna_regioes()
    if (len(pib_novo) == 0 & len(atividades) == 0 & len(regioes) == 0):
        return jsonify({'erro': 'PIB Novo completo não calculado!'}), 404
    #Montagem da lista com o PIB Novo
    i = 1
    at = 0
    rg = 0
    pib_top_ret = []
    for item in pib_novo:
        #Processa participação no pib da região
        if (rg == 0):
            pib_participacao = round((pib_novo[i-1][0]/pib_atual_soma_n) * 100, 2)
        elif (rg == 1):
            pib_participacao = round((pib_novo[i-1][0]/pib_atual_soma_ne) * 100, 2)
        elif (rg == 2):
            pib_participacao = round((pib_novo[i-1][0]/pib_atual_soma_se) * 100, 2)
        elif (rg == 3):
            pib_participacao = round((pib_novo[i-1][0]/pib_atual_soma_s) * 100, 2)
        else:
            pib_participacao = round((pib_novo[i-1][0]/pib_atual_soma_co) * 100, 2)

        #Calcula o percentual de crescimento
        perc_crescimento = [0]
        if (pib_novo[i-1][0] > 0 and pib_atual[i-1,0] > 0):
            perc_crescimento = ((pib_novo[i-1] - pib_atual[i-1,0])/pib_atual[i-1,0]) * 100 


        tmp_json={"index": i , "perc_crescimento": round(perc_crescimento[0],2) ,
                  "delta_x": round(delta_x[i-1][0],2), 
                  "pib_novo": pib_novo[i-1][0], 
                  "pib_atual": pib_atual[i-1,0] , 
                  "pib_participacao": pib_participacao , 
                  "id_atividade": at + 1 , 
                  "desc_atividade": atividades[at][1], 
                  "nome_regiao": regioes[rg][2]}
        pib_top_ret.append(tmp_json)
        i = i + 1
        if (at<=66):
            at = at + 1
        else:
            at=0
            rg = rg + 1
    s1 = json.dumps(pib_top_ret)        
    d1 = json.loads(s1)
    #sorted_data = sorted(d1, key = itemgetter('perc_crescimento'), reverse=True)
    sorted_data = sorted(d1, key = itemgetter('delta_x'), reverse=True)
    return jsonify(sorted_data)

# Endpoint para obter resumo de informações
@app.route('/pib_por_regiao', methods=['GET'])
def obter_pib_por_regiao():
    #Somatório dos pibs
    tmp_json={"pib_total_n": round(pib_novo_soma_n) ,  
              "pib_total_ne": round(pib_novo_soma_ne), 
              "pib_total_se": round(pib_novo_soma_se), 
              "pib_total_s": round(pib_novo_soma_s), 
              "pib_total_co": round(pib_novo_soma_co),
              "pib_atual_total_n": round(pib_atual_soma_n) ,  
              "pib_atual_total_ne": round(pib_atual_soma_ne), 
              "pib_atual_total_se": round(pib_atual_soma_se), 
              "pib_atual_total_s": round(pib_atual_soma_s), 
              "pib_atual_total_co": round(pib_atual_soma_co),
              "delta_pib_total_n": round(np.sum(delta_pib_n)) ,
              "delta_pib_total_ne": round(np.sum(delta_pib_ne)) ,
              "delta_pib_total_se": round(np.sum(delta_pib_se)) ,
              "delta_pib_total_s": round(np.sum(delta_pib_s)) ,
              "delta_pib_total_co": round(np.sum(delta_pib_co)) ,
              "delta_x_soma_n": round(np.sum(delta_x_n)),
              "delta_x_soma_ne": round(np.sum(delta_x_ne)),
              "delta_x_soma_se": round(np.sum(delta_x_se)),
              "delta_x_soma_s": round(np.sum(delta_x_s)),
              "delta_x_soma_co": round(np.sum(delta_x_co))
              }
    return jsonify(tmp_json)

# Endpoint para obter pib
@app.route('/pib_novo_completo_atividades', methods=['GET'])
def obter_pib_novo_completo_atividades():
    atividades = retorna_atividades()
    regioes = retorna_regioes()
    if (len(pib_novo) == 0 & len(atividades) == 0 & len(regioes) == 0):
        return jsonify({'erro': 'PIB Novo completo não calculado!'}), 404
    #Montagem da lista com o PIB Novo
    data = { "name": "Root", "children":[]}
    i = 1
    at = 0
    rg = 0
    children_interno = []
    for item in pib_novo:
        #tmp_json={ "value": item[0] , "name": atividades[at][1], "nome_regiao": regioes[rg][2]}
        tmp_json={ "value": round(item[0],2) , "name": atividades[at][1]}
        children_interno.append(tmp_json)
        i = i + 1
        if (at<=66):
            at = at + 1
        else:
            at=0
            data['children'].append({"name": regioes[rg][2],"children":children_interno})
            children_interno = []
            rg = rg + 1
    return jsonify(data)
#--------------------------------------------------------------------
#   *******     *******     ********  **********
#  /**////**   **/////**   **//////  /////**/// 
#  /**   /**  **     //** /**            /**    
#  /*******  /**      /** /*********     /**    
#  /**////   /**      /** ////////**     /**    
#  /**       //**     **         /**     /**    
#  /**        //*******    ********      /**    
#  //          ///////    ////////       //     
#
#+-------------------+
#|Cadastrar Simulação|
#+-------------------+
@app.route('/simulacao/inserir', methods=['POST'])
def cadastro():
    try:
        nome_simulacao = request.json.get('nome_simulacao')
        dados_simulacao = request.json.get('dados')
        inserir_simulacao(nome_simulacao, dados_simulacao)
    except:
        return jsonify({'resultado': False}),400       
    return jsonify({'resultado':True}),201


# Endpoint enviar delta y
@app.route('/enviar_delta_y', methods=['POST'])
def enviarDeltaY():
    try:
        dados = request.json.get('dados')
        delta_y = preparar_delta_y(dados, max_lin)
                
        #Choque default na atividade 1 - Agricultura, inclusive o apoio à agricultura e a pós-colheita
        delta_y_n[0]    = 3000
        delta_y_ne[68]  = 3000
        delta_y_se[136] = 3000
        delta_y_s[204]  = 3000
        delta_y_co[272] = 3000
                
        #+-----------------------------+
        #|Quadro Resumo - Multiplicador|
        #+-----------------------------+----------------------
        delta_x_n = preparar_delta_x(matriz_insumo,delta_y_n)
        delta_x_ne = preparar_delta_x(matriz_insumo,delta_y_ne)
        delta_x_se = preparar_delta_x(matriz_insumo,delta_y_se)
        delta_x_s = preparar_delta_x(matriz_insumo,delta_y_s)
        delta_x_co = preparar_delta_x(matriz_insumo,delta_y_co)
        delta_x = monta_delta_x(delta_x_n[0:68],delta_x_ne[68:136],delta_x_se[136:204],delta_x_s[204:272],delta_x_co[272:])

        

        delta_pib_n = calcular_delta_pib(pib_atual, vetor_v, delta_x_n)
        delta_pib_ne = calcular_delta_pib(pib_atual, vetor_v, delta_x_ne)
        delta_pib_se = calcular_delta_pib(pib_atual, vetor_v, delta_x_se)
        delta_pib_s = calcular_delta_pib(pib_atual, vetor_v, delta_x_s)
        delta_pib_co = calcular_delta_pib(pib_atual, vetor_v, delta_x_co)

        #Cálculo dos vetores com os PIBs novos
        pib_novo_n  =  calcular_novo_pib(pib_atual,delta_pib_n)
        pib_novo_ne  =  calcular_novo_pib(pib_atual,delta_pib_ne)
        pib_novo_se  =  calcular_novo_pib(pib_atual,delta_pib_se)
        pib_novo_s  =  calcular_novo_pib(pib_atual,delta_pib_s)
        pib_novo_co  =  calcular_novo_pib(pib_atual,delta_pib_co)

        #Totals dos vetores com os PIBs novos por região
        pib_novo_soma_n = np.sum(pib_novo_n[0:68])
        pib_novo_soma_ne = np.sum(pib_novo_ne[68:136])
        pib_novo_soma_se = np.sum(pib_novo_se[136:204])
        pib_novo_soma_s =  np.sum(pib_novo_s[204:272])
        pib_novo_soma_co = np.sum(pib_novo_co[272:])
        pib_novo = pib_novo_n[0:68] + pib_novo_ne[68:136] + pib_novo_se[136:204] + pib_novo_s[204:272] + pib_novo_co[272:]

        #Cálculo dos multiplicadores
        multiplicador_n = round(np.sum(delta_x_n)/np.sum(delta_y_n),2)
        multiplicador_ne = round(np.sum(delta_x_ne)/np.sum(delta_y_ne),2)
        multiplicador_se = round(np.sum(delta_x_se)/np.sum(delta_y_se),2)
        multiplicador_s = round(np.sum(delta_x_s)/np.sum(delta_y_s),2)
        multiplicador_co = round(np.sum(delta_x_co)/np.sum(delta_y_co),2)

        #Cálculo dos PIBs
        pib_atual_soma_n = np.sum(pib_atual[0:68])
        pib_atual_soma_ne = np.sum(pib_atual[68:136])
        pib_atual_soma_s =  np.sum(pib_atual[204:272])
        pib_atual_soma_se = np.sum(pib_atual[136:204])
        pib_atual_soma_co = np.sum(pib_atual[272:])

        #Cálculo dos vazamentos
        vazamento_n = round(((np.sum(delta_x_n) - np.sum(delta_x_n[0:68])) / np.sum(delta_x_n)) * 100 ) 
        vazamento_ne = round(((np.sum(delta_x_ne) - np.sum(delta_x_ne[68:136])) / np.sum(delta_x_ne)) * 100  )
        vazamento_s = round(((np.sum(delta_x_s) - np.sum(delta_x_s[204:272])) / np.sum(delta_x_s)) * 100  )
        vazamento_se = round(((np.sum(delta_x_se) - np.sum(delta_x_se[136:204])) / np.sum(delta_x_se)) * 100  )
        vazamento_co = round(((np.sum(delta_x_co) - np.sum(delta_x_co[272:])) / np.sum(delta_x_co)) * 100  )

        #Cálculo dos percentuais de crescimento
        per_pib_n = round(((pib_novo_soma_n / pib_atual_soma_n) - 1) * 100 , 2 )
        per_pib_ne = round(((pib_novo_soma_ne / pib_atual_soma_ne) - 1) * 100 , 2 )
        per_pib_s = round(((pib_novo_soma_s / pib_atual_soma_s) - 1) * 100 , 2  )
        per_pib_se = round(((pib_novo_soma_se / pib_atual_soma_se) - 1) * 100 , 2 )
        per_pib_co = round(((pib_novo_soma_co / pib_atual_soma_co) - 1) * 100  , 2 )
    
    except:
        return jsonify({'resultado': False}),400       
    return jsonify({'resultado':True}),201

#------------------------------------------------------------------------
#   *******   **     **  **********
#  /**////** /**    /** /////**/// 
#  /**   /** /**    /**     /**    
#  /*******  /**    /**     /**    
#  /**////   /**    /**     /**    
#  /**       /**    /**     /**    
#  /**       //*******      /**    
#  //         ///////       //     
#
#+---------------------------------------------------------------+
#| Endpoint para atualizar o Cadastro de uma simulação existente |
#+---------------------------------------------------------------+
@app.route('/simulacao/atualizar', methods=['PUT'])
def att_cadastro():
    try:
        id_simulacao = request.json.get('id_simulacao')
        nome_simulacao = request.json.get('nome_simulacao')
        dados_simulacao = request.json.get('dados')
        atualizar_simulacao(id_simulacao, nome_simulacao, dados_simulacao)
    except:
        return jsonify({'resultado': False}),400
    return jsonify({'resultado': True})



#+---------------------------------------------------------------------------------------------------------------------------------------------
#   *******    ********  **        ********  **********  ********
#  /**////**  /**/////  /**       /**/////  /////**///  /**///// 
#  /**    /** /**       /**       /**           /**     /**      
#  /**    /** /*******  /**       /*******      /**     /******* 
#  /**    /** /**////   /**       /**////       /**     /**////  
#  /**    **  /**       /**       /**           /**     /**      
#  /*******   /******** /******** /********     /**     /********
#  ///////    ////////  ////////  ////////      //      //////// 
#
#+-------------------------------------------------------+
#| Endpoint para deletar as informações de uma simulação |
#+-------------------------------------------------------+
@app.route('/simulacao/excluir/<int:id_simulacao>', methods=['DELETE'])
def deletar_jogador(id_simulacao):
    try:
        excluir_simulacao(id_simulacao)
    except:
        return jsonify({'resultado': False}),400   
    return jsonify({'resultado': True})

if __name__ == '__main__':
    app.run(debug=True, host=ip,port=5000)

#if __name__ == '__main__':
#    app.run(debug=True, host=ip)
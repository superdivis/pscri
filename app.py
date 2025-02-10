# +-------------------------------------------------------------+
# | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
# | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
# | Data inicio: 01/07/2024                                     |
# | Data finalização: xx/xx/xx                                  |
# | Autor: Alexandre Silva dos Santos                           |
# | Email: alexandresantoscompunb@gmail.com                     |
# +-------------------------------------------------------------+----------------------------------------------------------

#Serviços da calculadora

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from datetime import date
from calculadora_ipea_dao import * 
from processamento import *

#+------------------------
#| Constantes iniciais 
#+------------------------
ip = 'localhost'
#ip ='192.168.0.128'

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
delta_y = np.zeros((max_lin,0), dtype=np.float64)


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


'''#listar_simulacoes= ["1","Ubatubauba"],["2","Xique-Xique"],["3","Tatuapé"]; #apagar essa linha
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
    return jsonify(simulacao)'''
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
    app.run(debug=True, host=ip)
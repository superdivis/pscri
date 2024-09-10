# +-------------------------------------------------------------+
# | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
# | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
# | Data inicio: 01/07/2024                                     |
# | Data finalização: xx/xx/xx                                  |
# | Autor: Alexandre Silva dos Santos                           |
# | Email: alexandresantoscompunb@gmail.com                     |
# +-------------------------------------------------------------+----------------------------------------------------------

#Serviços da calculadora

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from datetime import date
from calculadora_ipea_dao import * 

ip='192.168.0.128'
file_path = 'E:\Alex\Livano\IPEA\calculadora_estrela\data\Analise de impacto.xlsx'

app = Flask(__name__)
CORS(app, support_credentials=True)

# Dados de exemplo para a API
livros = [
    {'id': 1, 'titulo': 'O Hobbit', 'autor': 'J.R.R. Tolkien'},
    {'id': 2, 'titulo': 'A Guerra dos Tronos', 'autor': 'George R. R. Martin'},
    {'id': 3, 'titulo': 'O Senhor dos Anéis', 'autor': 'J.R.R. Tolkien'}
]


init_calculadora(file_path)


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
# Endpoint para listar todos os livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    return jsonify(livros)


if __name__ == '__main__':
    app.run(debug=True, host=ip,port=5000)

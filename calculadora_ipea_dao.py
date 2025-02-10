# +-------------------------------------------------------------+
# | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
# | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
# | Data inicio: 01/07/2024                                     |
# | Data finalização: xx/xx/xx                                  |
# | Autor: Alexandre Silva dos Santos                           |
# | Email: alexandresantoscompunb@gmail.com                     |
# +-------------------------------------------------------------+----------------------------------------------------------

import os.path
import sqlite3


#+---------------------------+
#| Retorna conexão de banco  |
#+---------------------------+
def retorna_conexao():
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  db_path = os.path.join(BASE_DIR, "pscr.db")
  conn = sqlite3.connect(db_path)  
  return conn

#+---------------------------------------------------------------------------------------------------------------
#
#    ********  ********  **        ********   ******   **********
#   **//////  /**/////  /**       /**/////   **////** /////**/// 
#  /**        /**       /**       /**       **    //      /**    
#  /********* /*******  /**       /******* /**            /**    
#  ////////** /**////   /**       /**////  /**            /**    
#         /** /**       /**       /**      //**    **     /**    
#   ********  /******** /******** /******** //******      /**    
#  ////////   ////////  ////////  ////////   //////       //   
#
#+--------------------------------+
#| Script de leitura das Regioes  |
#+--------------------------------+
def retorna_regioes():
  conn = retorna_conexao()
  cur = conn.cursor()
  str_select = 'select * from regioes'
  cur.execute(str_select)
  rows=cur.fetchall()
  return rows

#+----------------------------------+
#| Script de leitura das Atividades |
#+----------------------------------+
def retorna_atividades():
  conn = retorna_conexao()
  cur = conn.cursor()
  str_select = 'select * from atividades'
  cur.execute(str_select)
  rows=cur.fetchall()
  return rows

#+----------------------------------+
#| Script da Matriz Insumo Produto  |
#+----------------------------------+
def retorna_matriz():
  conn = retorna_conexao()
  cur = conn.cursor()
  str_select = 'select * from matriz'
  cur.execute(str_select)
  rows=cur.fetchall()
  return rows

#+-------------------------------------+
#| Script para obter informação de PIB |
#+-------------------------------------+
def retorna_pib():
  conn = retorna_conexao()
  cur = conn.cursor()
  str_select = 'select * from pib'
  cur.execute(str_select)
  rows=cur.fetchall()
  return rows

#+-----------------------------+
#| Script para obter o vetor y |
#+-----------------------------+
def retorna_vetor_y():
  conn = retorna_conexao()
  cur = conn.cursor()
  str_select = 'select * from vetor_y'
  cur.execute(str_select)
  rows=cur.fetchall()
  return rows

#+-----------------------------+
#| Script para obter siumulacao|
#+-----------------------------+
def obter_simulacao_id(id):
  conn = retorna_conexao()
  cur = conn.cursor()
  str_select = 'select s.id_simulacao, s.nome , a.id , a.descricaoatividade, r.id, r.nome, sdy.valor from simulacao_delta_y sdy inner join simulacao s on s.id_simulacao = sdy.id_simulacao inner join atividades a on a.id = sdy.id_atividade inner join regioes r on r.id = sdy.id_regiao where sdy.id_simulacao = ' + str(id)
  cur.execute(str_select)
  rows=cur.fetchall()
  return rows

#+--------------------------------+
#| Script de nível territorial    |
#+--------------------------------+
def retorna_nivel_territorial():
  conn = retorna_conexao()
  cur = conn.cursor()
  str_select = 'select * from nivel_territorial'
  cur.execute(str_select)
  rows=cur.fetchall()
  return rows

#+------------------------------+
#| Script para obter siumulacoes|
#+------------------------------+
def listar_simulacoes():
  conn = retorna_conexao()
  cur = conn.cursor()
  str_select = 'select * from simulacao' 
  cur.execute(str_select)
  rows=cur.fetchall()
  return rows


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
#+------------------------------+
#| Script para excluir siumulacao|
#+-------------------------------+
def excluir_simulacao(id):
  conn = retorna_conexao()
  cur = conn.cursor()
  str_select = 'DELETE FROM simulacao_delta_y WHERE id_simulacao = ' + str(id)  + '; commit;'
  str_select = str_select + 'DELETE FROM simulacao WHERE id_simulacao = ' + str(id)  + '; commit;' 
  cur.execute(str_select)
  return 200


#+--------------------------------------------------------------------------------------------------------------
#   **  ****     **   ********  ********  *******    **********
#  /** /**/**   /**  **//////  /**/////  /**////**  /////**/// 
#  /** /**//**  /** /**        /**       /**   /**      /**    
#  /** /** //** /** /********* /*******  /*******       /**    
#  /** /**  //**/** ////////** /**////   /**///**       /**    
#  /** /**   //****        /** /**       /**  //**      /**    
#  /** /**    //***  ********  /******** /**   //**     /**    
#  //  //      ///  ////////   ////////  //     //      //     
#+------------------------------------------------------+
#| Script de Inserção de uma simulação                  |
#+------------------------------------------------------+
def inserir_simulacao(nome_simulacao, dados_simulacao):
  conn = retorna_conexao()
  cur = conn.cursor()
  str_insert = "INSERT INTO simulacao (id_simulacao, nome) VALUES(nextval("+ "'" +'simulacao_id_simulacao_seq' +"'" + "::regclass), " + "'" + nome_simulacao + "'" + "); commit;"
  cur.execute(str_insert)
  cur.execute('SELECT LASTVAL()')
  lastid = cur.fetchone()[0]
  for dt in dados_simulacao:
    str_insert = "INSERT INTO simulacao_delta_y (id, id_simulacao, id_atividade, id_regiao, valor) VALUES(nextval(" + "'" + "simulacao_delta_y_id_seq" + "'" + "::regclass) , " + str(lastid) + "," + str(dt['id_atividade']) + "," + str(dt['id_regiao']) + "," + str(dt['valor']) +"); commit;"
    cur.execute(str_insert)
  conn.commit()
  conn.close()
  return lastid

#+-------------------------------------------------------------------------------------------------------------
#
#   **     **  *******   *******        **     **********  ********
#  /**    /** /**////** /**////**      ****   /////**///  /**///// 
#  /**    /** /**   /** /**    /**    **//**      /**     /**      
#  /**    /** /*******  /**    /**   **  //**     /**     /******* 
#  /**    /** /**////   /**    /**  **********    /**     /**////  
#  /**    /** /**       /**    **  /**//////**    /**     /**      
#  //*******  /**       /*******   /**     /**    /**     /********
#   ///////   //        ///////    //      //     //      //////// 
#+------------------------------------+
#|+ Script de Update de uma simulação |
#+------------------------------------+
def atualizar_simulacao(id_simulacao, nome_simulacao, dados_simulacao):
  conn = retorna_conexao()
  cur = conn.cursor()
  str_insert = "UPDATE simulacao SET nome = " + "'" + nome_simulacao + "'" + " WHERE id_simulacao = " + str(id_simulacao) + ";"
  cur.execute(str_insert)
  for dt in dados_simulacao:
    str_insert = "UPDATE simulacao_delta_y SET valor =" + str(dt['valor']) + " WHERE id_simulacao = " + str(id_simulacao) + " and id_atividade =" + str(dt['id_atividade']) + " and id_regiao = " + str(dt['id_regiao']) + ";"
    cur.execute(str_insert)
  conn.commit()
  conn.close()

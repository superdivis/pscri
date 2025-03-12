# +-------------------------------------------------------------+
# | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
# | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
# | Data inicio: 01/07/2024                                     |
# | Data finalização: xx/xx/xx                                  |
# | Autor: Alexandre Silva dos Santos                           |
# | Email: alexandresantoscompunb@gmail.com                     |
# +-------------------------------------------------------------+----------------------------------------------------------

from calculadora_ipea_dao import * 
import pandas as pd
import numpy as np

####################
#Preparação da Matriz de insumo produto por Região (68 x 68 x 5)
def prepara_ajuste_matriz( n_lin , n_col):
  matriz_tmp = retorna_matriz()
  ret_matriz = np.zeros((n_lin, n_col), dtype=np.float64)
  lin = 0
  for linha in matriz_tmp:
    for col in range (n_col):
      ret_matriz[lin, col] = linha[col+2]
    lin = lin + 1
  #print (ret_matriz[0,0])
  #print (ret_matriz[0,339])
  #print (ret_matriz[339,0])
  #print (ret_matriz[339,339])
  return ret_matriz

####################
#Preparação do vetor vy
def prepara_vetor_y(n_lin, n_col):
  ret_vy = np.zeros((n_lin, n_col), dtype=np.float64)
  vy_tmp = retorna_vetor_y()
  lin = 0
  for linha in vy_tmp:
    ret_vy[lin,0] = linha [n_col]
    lin = lin + 1
  #print (ret_vy[0,0])
  #print (ret_vy[339,0])
  return ret_vy

####################
#Lendo o vetor pib
def ler_vetor_pib( n_lin, n_col):
  ret_pib = np.zeros((n_lin, n_col), dtype=np.float64)
  pib_tmp = retorna_pib()
  lin = 0
  for linha in pib_tmp:
    ret_pib[lin,0] =  linha [n_col]
    lin = lin + 1
  #print (ret_pib[0,0])
  #print (ret_pib[339,0])
  return ret_pib

####################
#Preparação do vetor vx
def prepara_vetor_x(matriz, vy):
  print("Criando o vetor vx - Matriz X vy")
  vx = np.dot(matriz, vy)
  return vx

####################
#Cálculo do vetor v
def calcular_vetor_v(pib, vx):
  #print("Calculando vetor v...")
  vv = []
  for i in range(len(pib)):
      tmp = pib[i]/vx[i]
      vv.append(tmp)
  return vv

####################
#Preparar delta y
def preparar_delta_y(dados,n_lin):
  deltaY = np.zeros((n_lin, 1), dtype=np.float64)
  for dt in dados:
    deltaY[dt['id'] - 1,0] = dt['valor']
  return deltaY

#TODO nessa etapa
####################
#Preparar delta x
def preparar_delta_x(matriz, delta_y):
  delta_x = np.dot(matriz, delta_y)
  return delta_x

####################
#Preparar delta pib
def calcular_delta_pib(pib,vv, delta_x):
  delta_pib = []
  for i in range(len(pib)):
    tmp = vv[i]*delta_x[i]
    delta_pib.append(tmp)
  return delta_pib

####################
#Preparar novo pib
def calcular_novo_pib(pib, delta_pib):
  novo_pib = []
  for i in range(len(pib)):
    tmp = pib[i]+delta_pib[i]
    novo_pib.append(tmp)
  return novo_pib

####################
# Calcular total pib regional
# (pib atual / pib novo)
def calcular_total_pib_regional(pib, indice_inicial, indice_final):
  #print(indice_inicial)
  #print(indice_final)
  #print( str(pib[indice_inicial]) , str(pib[indice_final]) )
  pib_regional = pib[indice_inicial:indice_final+1]
  return sum (pib_regional)

####################
# Vincula setores e valores de PIB
# (setor / pib atual / pib novo)
def vincula_setores_pibs(atividades, pib_inicial, pib_atual, deslocamento_territorial):
  i = deslocamento_territorial
  indice_atividade = 0
  v = [atividades[indice_atividade], int(round(pib_inicial[i][0])) , int(round(pib_atual[i][0]))]
  df = pd.DataFrame([v])
  df.columns = ['atividade','pib','pib_atual']
  for ativ in range(len(atividades)-1):
    i = i + 1
    indice_atividade = indice_atividade + 1
    vetor = [ atividades[indice_atividade], int(round(pib_inicial[i][0])) , int(round(pib_atual[i][0])) ]
    df.loc[len(df.index)] = vetor
  return df
  
####################
# Vincula setores e valores de PIB
# (setor / pib atual / pib novo)
def aplicar_simulacao_choque(delta_y):
  for dt in delta_y:
    str_insert = "INSERT INTO pscr.simulacao_delta_y (id, id_simulacao, id_atividade, id_regiao, valor) VALUES(nextval(" + "'" + "pscr.simulacao_delta_y_id_seq" + "'" + "::regclass) , " + str(lastid) + "," + str(dt['id_atividade']) + "," + str(dt['id_regiao']) + "," + str(dt['valor']) +"); commit;"

####################
# Monta novo delta_x com base nas listas de entrada
# (delta_x_n,delta_x_ne,delta_x_se,delta_x_s,delta_x_co)
def monta_delta_x (x1,x2,x3,x4,x5):
  x_tmp = []
  for i in x1:
    x_tmp.append(i)
  for i in x2:
    x_tmp.append(i)
  for i in x3:
    x_tmp.append(i)
  for i in x4:
    x_tmp.append(i)
  for i in x5:
    x_tmp.append(i)
  return x_tmp

  
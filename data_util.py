# +-------------------------------------------------------------+
# | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
# | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
# | Data inicio: 17/08/2024                                     |
# | Data finalização: XX/XX/2024                                |
# | Autor: Alexandre Silva dos Santos                           |
# | Email: alexandresantoscompunb@gmail.com                     |
# +-------------------------------------------------------------+------------------------------------------
import pandas as pd
import numpy as np

############################################################################################################################################################
# Lê execel
# Registro da Análise da Matriz de Insumo Produto
def le_arquivo(file_path, sheet_name):
  ret = pd.read_excel(file_path, sheet_name = sheet_name)
  return ret

####################
#Preparação dos objeto dropdown 
def prepara_dados_dropdown(arquivo_dados, n_col, n_lin):
  dados = []
  for lin in range (n_lin):
    #print ("Lendo registro da linha:" , str(lin)) 
    #print(df.iloc[lin+1][col+2])
    item = {'label': arquivo_dados.iloc[lin][n_col+1] , 'value': int(arquivo_dados.iloc[lin][n_col])}  
    dados.append(item)
  return dados

####################
#Preparação da Matriz de insumo produto por Região (68 x 68 x 5)
def prepara_matriz(arquivo_dados, n_col, n_lin):
  matriz = np.zeros((n_col, n_lin), dtype=np.float64)
  #print("Lendo arquivo...")
  #print(float(df.iloc[1][343]))
  for col in range(n_col):
      #print ("Lendo registro da coluna:" , str(col)) 
      for lin in range (n_lin):
          #print ("Lendo registro da linha:" , str(lin)) 
          #print(df.iloc[lin+1][col+2])
          matriz[lin, col] = float(arquivo_dados.iloc[lin+1][col+2])
    #print (matriz_insumo_produto_regioes[0:4,0:4])
  return matriz

####################
#Preparação do vetor vy
def prepara_vetor_y(arquivo_dados, n_col):
  vy = np.zeros((n_col,1), dtype=np.float64)
  for lin in range (n_col):
    #print(float(df.iloc[lin+1][max_col+2]))
    vy[lin,0] =  float(arquivo_dados.iloc[lin+1][n_col+3])
  return vy

####################
#Preparação do vetor vx
def prepara_vetor_x(matriz, vy):
  print("Criando o vetor vx - Matriz X vy")
  vx = np.dot(matriz, vy)
  return vx
  
####################
#Lendo o vetor pib
def ler_vetor_pib(arquivo, n_col, n_lin):
  print("Lendo arquivo  para o vetor pib...")
  pib = np.zeros((340,1), dtype=np.float64)
  for lin in range (n_lin):
    #print(float(df.iloc[lin+1][max_col+2]))
    pib[lin,0] =  float(arquivo.iloc[lin+1][n_col+7])
  return pib

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
def preparar_delta_y(n_col, valor_choque, setor):
  delta_y = np.zeros((n_col,1), dtype=np.float64)
  delta_y[setor,0] = valor_choque
  return delta_y

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
def calcular_total_pib_reional(pib, indice_inicial, indice_final):
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
# +-------------------------------------------------------------+
# | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
# | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
# | Data inicio: 17/08/2024                                     |
# | Data finalização: 17/08/2024                                |
# | Autor: Alexandre Silva dos Santos                           |
# | Email: alexandresantoscompunb@gmail.com                     |
# +-------------------------------------------------------------+------------------------------------------

#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np
import leafmap.foliumap as leafmap
import squarify
import matplotlib.pyplot as plt

#######################
# Plots

# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)

def init_painel(valores_resumo,df_tabela_pibs):
    #######################
    # Dashboard Main Panel
    col = st.columns((4.5, 6 ), gap='medium')
    
    with col[0]:
        st.markdown('#### PIB por região')
        
        m = leafmap.Map(center=[40, -100], zoom=4)
        cities = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        #regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"
        regions = "regioes_br.geojson"

        m.add_geojson(regions, layer_name="US Regions")
        m.add_points_from_xy(
            cities,
            x="longitude",
            y="latitude",
            color_column="region",
            icon_names=["gear", "map", "leaf", "globe"],
            spin=True,
            add_legend=False,
        )

        m.to_streamlit(height=550)
       
    with col[1]:
                
        st.markdown('#### Resumo Valores')
        col1, col2, col3, col4 = st.columns(4)
        col5, col6, col7, col8 = st.columns(4)
        valor_mult = f'{valores_resumo[0][0]:.2f}'
        valor_vazamento = f'{valores_resumo[1][0]*100:.0f}'
        valor_pib_percentual = f'{valores_resumo[2][0]*100:.2f}'
        col1.metric(label="Região", value= "Norte" )
        col2.metric(label="Multiplicador", value= valor_mult )
        col3.metric(label="Vazamento (%)", value = valor_vazamento )
        col4.metric(label="PIB (%)", value= valor_pib_percentual )

        col5.metric( label="" , value= "Sul" )
        col6.metric( label="" ,value = valor_mult )
        col7.metric( label="" ,value = valor_vazamento )
        col8.metric( label="" ,value= valor_pib_percentual )
        

        st.markdown('#### Top Setores')
        
        st.dataframe(df_tabela_pibs,
                    column_order=("atividade","pib","pib_atual"),
                    hide_index=True,
                    width=None,
                    column_config={
                        "atividade": st.column_config.TextColumn(
                            "Setores",
                        ),
                        "pib": st.column_config.ProgressColumn(
                            "PIB Atual",
                            format="%f",
                            min_value=0,
                            max_value=max(df_tabela_pibs.pib),
                        ),
                        "pib_atual": st.column_config.ProgressColumn(
                            "PIB Novo",
                            format="%f",
                            min_value=0,
                            max_value=max(df_tabela_pibs.pib_atual),
                        )}
                    )
    

#############################################################################################################################################################
# Lê execel
# Registro da Análise da Matriz de Insumo Produto
def le_arquivo(file_path):
  ret = pd.read_excel(file_path, sheet_name='N')
  return ret

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



######################################################################################################################################################
# Page configuration
st.set_page_config(
    page_title="Cálculo de Matriz Insumo Produto IPEA",
    page_icon=":1234:",
    layout="wide",
    initial_sidebar_state="expanded")

st.header("Painel de Simulação de Cenários Regionais - PSCR", divider="blue")

alt.themes.enable("dark")

with st.spinner('Carregando dados...'):
    
    #+-----------------+
    #| Prepara arquivo |
    #+-----------------+-----------------------------------------------------
    # Initialize session state variables
    if 'file_path_matriz' not in st.session_state:
        st.session_state.file_path_matriz = 'Analise de impacto.xlsx'
        st.session_state.df = le_arquivo(st.session_state.file_path_matriz)  

    #+-----------------------------+
    #| Carga de constantes arquivo |
    #+-----------------------------+------------------------------------------
    if 'regioes' not in st.session_state:
        st.session_state.regioes = ["Norte","Nordeste","Sul","Sudeste","Centro-Oeste"]

    if 'estados' not in st.session_state:
        st.session_state.estados = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]

    if 'atividades_contas_nacionais' not in st.session_state:
        st.session_state.atividades_contas_nacionais = [
            "Agricultura, inclusive o apoio à agricultura e a pós-colheita",
            "Pecuária, inclusive o apoio à pecuária",
            "Produção florestal; pesca e aquicultura",
            "Extração de carvão mineral e de minerais não-metálicos",
            "Extração de petróleo e gás, inclusive as atividades de apoio",
            "Extração de minério de ferro, inclusive beneficiamentos e a aglomeração",
            "Extração de minerais metálicos não-ferrosos, inclusive beneficiamentos",
            "Abate e produtos de carne, inclusive os produtos do laticínio e da pesca",
            "Fabricação e refino de açúcar",
            "Outros produtos alimentares",
            "Fabricação de bebidas",
            "Fabricação de produtos do fumo",
            "Fabricação de produtos têxteis",
            "Confecção de artefatos do vestuário e acessórios",
            "Fabricação de calçados e de artefatos de couro",
            "Fabricação de produtos da madeira",
            "Fabricação de celulose, papel e produtos de papel",
            "Impressão e reprodução de gravações",
            "Refino de petróleo e coquerias",
            "Fabricação de biocombustíveis",
            "Fabricação de químicos orgânicos e inorgânicos, resinas e elastômeros",
            "Fabricação de defensivos, desinfestantes, tintas e químicos diversos",
            "Fabricação de produtos de limpeza, cosméticos/perfumaria e higiene pessoal",
            "Fabricação de produtos farmoquímicos e farmacêuticos",
            "Fabricação de produtos de borracha e de material plástico",
            "Fabricação de produtos de minerais não-metálicos",
            "Produção de ferro-gusa/ferroligas, siderurgia e tubos de aço sem costura",
            "Metalurgia de metais não-ferosos e a fundição de metais",
            "Fabricação de produtos de metal, exceto máquinas e equipamentos",
            "Fabricação de equipamentos de informática, produtos eletrônicos e ópticos",
            "Fabricação de máquinas e equipamentos elétricos",
            "Fabricação de máquinas e equipamentos mecânicos",
            "Fabricação de automóveis, caminhões e ônibus, exceto peças",
            "Fabricação de peças e acessórios para veículos automotores",
            "Fabricação de outros equipamentos de transporte, exceto veículos automotores",
            "Fabricação de móveis e de produtos de indústrias diversas",
            "Manutenção, reparação e instalação de máquinas e equipamentos",
            "Energia elétrica, gás natural e outras utilidades",
            "Água, esgoto e gestão de resíduos",
            "Construção",
            "Comércio e reparação de veículos automotores e motocicletas",
            "Comércio por atacado e a varejo, exceto veículos automotores",
            "Transporte terrestre",
            "Transporte aquaviário",
            "Transporte aéreo",
            "Armazenamento, atividades auxiliares dos transportes e correio",
            "Alojamento",
            "Alimentação",
            "Edição e edição integrada à impressão",
            "Atividades de televisão, rádio, cinema e  gravação/edição de som e imagem",
            "Telecomunicações",
            "Desenvolvimento de sistemas e outros serviços de informação",
            "Intermediação financeira, seguros e previdência complementar",
            "Atividades imobiliárias",
            "Atividades jurídicas, contábeis, consultoria e sedes de empresas",
            "Serviços de arquitetura, engenharia, testes/análises técnicas e P & D",
            "Outras atividades profissionais, científicas e técnicas",
            "Aluguéis não-imobiliários e gestão de ativos de propriedade intelectual",
            "Outras atividades administrativas e serviços complementares",
            "Atividades de vigilância, segurança e investigação",
            "Administração pública, defesa e seguridade social",
            "Educação pública",
            "Educação privada",
            "Saúde pública",
            "Saúde privada",
            "Atividades artísticas, criativas e de espetáculos",
            "Organizações associativas e outros serviços pessoais",
            "Serviços domésticos"]    

    #+-------------------------------------------------+
    #| Prepara Cálculos com a Matriz de Insumo Produto |
    #+-------------------------------------------------+----------------------
    if 'max_col' not in st.session_state:
        st.session_state.max_col = 340
        st.session_state.max_lin = st.session_state.max_col
        st.session_state.matriz_insumo_produto_regioes = prepara_matriz(st.session_state.df, st.session_state.max_col, st.session_state.max_lin)
        st.session_state.vy = prepara_vetor_y(st.session_state.df, st.session_state.max_col)
        st.session_state.vx = prepara_vetor_x(st.session_state.matriz_insumo_produto_regioes, st.session_state.vy)
        st.session_state.pib = ler_vetor_pib(st.session_state.df, st.session_state.max_col, st.session_state.max_lin)
        st.session_state.vv = calcular_vetor_v(st.session_state.pib, st.session_state.vx)


    #file_path = 'E:\Alex\Livano\IPEA\calculadora_estrela\data\poc_ipea_us_pop_2010_2019.xlsx'
    #df_reshaped = pd.read_excel(file_path)

    #######################
    # Sidebar
    with st.sidebar:
        st.title('Filtros de Seleção')
        
        #Nível territorial
        areas = ['Regiões' , 'Estados']
        select_area = st.selectbox('Selecione nível territorial: ', areas)
        
        #Seleção da região
        if select_area == "Regiões":
            dados_nivel_territorial = st.session_state.regioes
        else:
            dados_nivel_territorial = st.session_state.estados
        #select_nivel_territorial = st.multiselect('Selecione região: ', dados_nivel_territorial , default = "Norte")
        select_nivel_territorial = st.selectbox('Selecione região: ', dados_nivel_territorial )

        #Seleção do Sistemas
        sistemas = ['Contas Nacionais' , 'CNAE 2.0']
        select_sistema = st.selectbox('Selecione o sistema: ', sistemas)
        
        cnae_2_0 = ["Intermediação financeira, seguros e previdência complementar","Atividades imobiliárias"]

        #Seleção do Sistema
        dados_sistema = st.session_state.atividades_contas_nacionais
        if select_sistema == "Contas Nacionais":
            dados_sistema = st.session_state.atividades_contas_nacionais
        else:
            dados_sistema = cnae_2_0
        #select_atividade = st.multiselect('Selecione a atividade: ', dados_sistema, default = "Agricultura, inclusive o apoio à agricultura e a pós-colheita")
        select_atividade = st.selectbox('Selecione a atividade: ', dados_sistema)                
        choque = st.text_input("Valor do choque (R$ milhões):", 1000)

        st.button("Aplicar choque", type="primary")

    #Cálculo do deslocamento regional
    #deslocamento_territorial = 0
    if select_nivel_territorial == "Norte":
        deslocamento_territorial = 0
    elif select_nivel_territorial == "Nordeste":
        deslocamento_territorial = 68
    elif  select_nivel_territorial == "Sudeste":
        deslocamento_territorial = 136
    elif  select_nivel_territorial == "Sul":
        deslocamento_territorial = 204
    else:
        deslocamento_territorial = 272
    
    id_atividade = st.session_state.atividades_contas_nacionais.index(select_atividade)
    #id_atividade = 0
    deltaY = preparar_delta_y(st.session_state.max_col, choque, id_atividade + deslocamento_territorial)
    deltaX = preparar_delta_x(st.session_state.matriz_insumo_produto_regioes,deltaY)
    deltaPIB = calcular_delta_pib(st.session_state.pib,st.session_state.vv, deltaX)
    novoPIB = calcular_novo_pib(st.session_state.pib, deltaPIB)

    #Pibs regionais
    indicie_inicial = deslocamento_territorial
    indice_final = deslocamento_territorial+ len(st.session_state.atividades_contas_nacionais) -1
    soma_pib_regional_original = calcular_total_pib_reional(st.session_state.pib, indicie_inicial ,indice_final) 
    soma_pib_regional_novo = calcular_total_pib_reional(novoPIB, indicie_inicial , indice_final) 
    variacao_pib_regional = (soma_pib_regional_novo/soma_pib_regional_original) -1

    # Totais
    total_deltaX = sum(deltaX)
    total_deltaY = sum(deltaY)

    multiplicador = total_deltaX/total_deltaY
    vazamento = total_deltaX - sum (deltaX[indicie_inicial:indice_final])
    vazamento_percentual =  vazamento / total_deltaX

    df_tabela_pibs = vincula_setores_pibs (st.session_state.atividades_contas_nacionais, st.session_state.pib, novoPIB, deslocamento_territorial)

print(choque)
print("Resumo")
print("Soma pib original = ", soma_pib_regional_original)
print("Soma pib novo = ", soma_pib_regional_novo)
print("Variação pib regional", variacao_pib_regional* 100, "%")

print("Vazamento = ", vazamento)
print("Vazamento percentual = ", vazamento_percentual*100, "%")

valores_resumo = [multiplicador,vazamento_percentual,variacao_pib_regional]

print (st.session_state.max_col, choque, id_atividade + deslocamento_territorial)

init_painel(valores_resumo,df_tabela_pibs)


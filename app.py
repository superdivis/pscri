# +-------------------------------------------------------------+
# | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
# | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
# | Data inicio: 17/08/2024                                     |
# | Data finalização: XX/XX/2024                                |
# | Autor: Alexandre Silva dos Santos                           |
# | Email: alexandresantoscompunb@gmail.com                     |
# +-------------------------------------------------------------+------------------------------------------

#######################
# Import libraries
import plotly.express as px
from dash import Dash, dcc, html, Input, Output 
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import data_util as du
from dash.exceptions import PreventUpdate


######################################################################################################################################################
# Page configuration

  #+-----------------+
#| Prepara arquivo |
#+-----------------+-----------------------------------------------------
# Initialize session state variables
file_path_matriz = 'Analise de impacto.xlsx'
df = du.le_arquivo(file_path_matriz, 'N')  
df_regioes = du.le_arquivo(file_path_matriz, 'Regioes') 
df_estados = du.le_arquivo(file_path_matriz, 'Estados') 
df_atividades = du.le_arquivo(file_path_matriz, 'Atividades') 
df_sistema = du.le_arquivo(file_path_matriz, 'Sistemas') 

#+------------------------------+
#| Carga de dominíos do arquivo |
#+------------------------------+------------------------------------------
regioes = du.prepara_dados_dropdown(df_regioes, 0, 5) 
estados = du.prepara_dados_dropdown(df_estados, 0, 27)
atividades_contas_nacionais = du.prepara_dados_dropdown(df_atividades, 0, 68)
sistemas = du.prepara_dados_dropdown(df_sistema, 0, 2)


#+-------------------------------------------------+
#| Prepara Cálculos com a Matriz de Insumo Produto |
#+-------------------------------------------------+----------------------
max_col = 340
max_lin = max_col
matriz_insumo_produto_regioes = du.prepara_matriz(df, max_col, max_lin)
vy = du.prepara_vetor_y(df, max_col)
vx = du.prepara_vetor_x(matriz_insumo_produto_regioes, vy)
pib = du.ler_vetor_pib(df, max_col, max_lin)
vv = du.calcular_vetor_v(pib, vx)


#######################
# Sidebar

    
#Nível territorial
areas = ['Regiões' , 'Estados']
#select_area = st.selectbox('Selecione nível territorial: ', areas)

#Seleção da região
dados_nivel_territorial = regioes
#if select_area == "Regiões":
#    dados_nivel_territorial = regioes
#else:
#    dados_nivel_territorial = estados
#select_nivel_territorial = st.multiselect('Selecione região: ', dados_nivel_territorial , default = "Norte")
#select_nivel_territorial = .selectbox('Selecione região: ', dados_nivel_territorial )

#Seleção do Sistemas
sistemas = ['Contas Nacionais' , 'CNAE 2.0']
#select_sistema = st.selectbox('Selecione o sistema: ', sistemas)

cnae_2_0 = ["Intermediação financeira, seguros e previdência complementar","Atividades imobiliárias"]

#Seleção do Sistema
dados_sistema = atividades_contas_nacionais
#if select_sistema == "Contas Nacionais":
#    dados_sistema = atividades_contas_nacionais
#else:
#    dados_sistema = cnae_2_0
select_atividade = 0
choque =  1000

#Cálculo do deslocamento regional
deslocamento_territorial = 0
#if select_nivel_territorial == "Norte":
#    deslocamento_territorial = 0
#elif select_nivel_territorial == "Nordeste":
#    deslocamento_territorial = 68
#elif  select_nivel_territorial == "Sudeste":
#    deslocamento_territorial = 136
#elif  select_nivel_territorial == "Sul":
#   deslocamento_territorial = 204
#else:
#   deslocamento_territorial = 272

#id_atividade = atividades_contas_nacionais.index(select_atividade)
id_atividade = 0
deltaY = du.preparar_delta_y(max_col, choque, id_atividade + deslocamento_territorial)
deltaX = du.preparar_delta_x(matriz_insumo_produto_regioes,deltaY)
deltaPIB = du.calcular_delta_pib(pib,vv, deltaX)
novoPIB = du.calcular_novo_pib(pib, deltaPIB)

#Pibs regionais
indicie_inicial = deslocamento_territorial
indice_final = deslocamento_territorial+ len(atividades_contas_nacionais) -1
soma_pib_regional_original = du.calcular_total_pib_reional(pib, indicie_inicial ,indice_final) 
soma_pib_regional_novo = du.calcular_total_pib_reional(novoPIB, indicie_inicial , indice_final) 
variacao_pib_regional = (soma_pib_regional_novo/soma_pib_regional_original) -1

# Totais
total_deltaX = sum(deltaX)
total_deltaY = sum(deltaY)

multiplicador = total_deltaX/total_deltaY
vazamento = total_deltaX - sum (deltaX[indicie_inicial:indice_final])
vazamento_percentual =  vazamento / total_deltaX

df_tabela_pibs = du.vincula_setores_pibs (atividades_contas_nacionais, pib, novoPIB, deslocamento_territorial)

print(choque)
print("Resumo")
print("Soma pib original = ", soma_pib_regional_original)
print("Soma pib novo = ", soma_pib_regional_novo)
print("Variação pib regional", variacao_pib_regional* 100, "%")

print("Vazamento = ", vazamento)
print("Vazamento percentual = ", vazamento_percentual*100, "%")

valores_resumo = [multiplicador,vazamento_percentual,variacao_pib_regional]

print (max_col, choque, id_atividade + deslocamento_territorial)


# +--------------+
# | App layout   |
# +--------------+------------------------------------------------------------------------------------

dtf = px.data.tips()

def treemap(df, metric='total_bill', path=[px.Constant("all"), 'sex', 'day', 'time']):

    fig = px.treemap(df, path=path, template='none', values=metric, height=650)
    template = '<b>%{label}</b><br><br>Total: %{value:,d}<br>%{percentParent:.1%}'
    fig.data[0]['texttemplate'] = template
    fig.data[0]['hovertemplate'] = template
    return fig


def make_treemap(path, metric):
    if not path or not metric:
        raise PreventUpdate
    if path == 'Yes and No':
        dff = dtf.copy()
        #print(dff)
    else:
        dff = dtf.query('smoker == @path')
    fig = treemap(dff, metric)
    return fig

#make_treemap( 'Yes and No','')

app = Dash(__name__)
app.title = "PSCR-IPEA"
app._favicon = ("transferir.jpeg")
app.layout = html.Div([

    html.H1("Painel de Simulação de Cenários Regionais - PSCR", style={'text-align': 'left', 'margin-left': '15px'}),
    html.Br(), 
    html.Div(children=[
      dbc.Label('Selecione nivel territorial:'),
      dcc.Dropdown(id='nivel_territorial', options=[{'label': 'Regiões', 'value': 1} , {'label': 'Estados', 'value': 2}, ], multi=False, value=1),
    ],style={'padding': 15, 'flex': 1, 'width': '13%'}),
    html.Div(children=[ 
            dbc.Label('Selecione a região:'),
            dcc.Dropdown(id='sel_regioes', options=regioes, multi=True, value=1)           
    ],style={'padding': 15, 'flex': 1, 'width': '13%'}),
    html.Div(children=[ 
            dbc.Label('Selecionar sistema:'),
            dcc.Dropdown(id='sel_sistemas', options=sistemas, multi=False, value=1)           
    ],style={'padding': 15, 'flex': 1, 'width': '13%'}),
    html.Div(children=[ 
            dbc.Label('Selecionar a atividade:'),
            dcc.Dropdown(id='sel_atividades', options=atividades_contas_nacionais, multi=True, value=1)           
    ],style={'padding': 15, 'flex': 1, 'width': '30%'}),
    html.Div(children=[ 
            dbc.Label('Valor do choque (R$ milhões):'),
            html.Br(), 
            dcc.Input(id='input_choque',  value=1000)           
    ],style={'padding': 15, 'flex': 1, 'width': '30%'}),
    html.Div(children=[
      #dbc.Label('Selecione nivel territorial:'),
      #dcc.Graph(id='graph'),
    ],style={'padding': 15 }),

])

# +------------------------------------------------+
# | Connect the Plotly graphs with Dash Components |
# +------------------------------------------------+
#app.callback(
#    [Output(component_id='output_container', component_property='children'),
#     Output(component_id='my_bee_map', component_property='figure')],
#    [Input(component_id='slct_year', component_property='value')]
    
#)



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
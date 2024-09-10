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
from frontend.calculadora_estrela_frontend import *
from backend.calculadora_ipea_dao import * 



#######################
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
        st.session_state.file_path_matriz = 'E:\Alex\Livano\IPEA\calculadora_estrela\data\Analise de impacto.xlsx'
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


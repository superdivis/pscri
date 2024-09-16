# +-------------------------------------------------------------+
# | Projeto da Calculadora da Matriz de Insumo Consumo IPEA     |
# | Cliente: Instituto de Pesquisa Econômica Aplicada - IPEA    |
# | Data inicio: 17/08/2024                                     |
# | Data finalização: 17/08/2024                                |
# | Autor: Alexandre Silva dos Santos                           |
# | Email: alexandresantoscompunb@gmail.com                     |
# | **Prova de conceito (POC) com streamlit                     |
# +-------------------------------------------------------------+----------------------------------------------------------

#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
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
        
        """
        heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', selected_color_theme)
        st.altair_chart(heatmap, use_container_width=True)
        """

    with col[1]:
            """
            st.markdown('#### Gains/Losses')

            df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

            if selected_year > 2010:
                first_state_name = df_population_difference_sorted.states.iloc[0]
                first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
                first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])
            else:
                first_state_name = '-'
                first_state_population = '-'
                first_state_delta = ''
            st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

            if selected_year > 2010:
                last_state_name = df_population_difference_sorted.states.iloc[-1]
                last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])   
                last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])   
            else:
                last_state_name = '-'
                last_state_population = '-'
                last_state_delta = ''
            st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)
            """
            
            st.markdown('#### Resumo Valores')
            col1, col2, col3 = st.columns(3)
            valor_mult = f'{valores_resumo[0][0]:.2f}'
            valor_vazamento = f'{valores_resumo[1][0]*100:.0f}'
            valor_pib_percentual = f'{valores_resumo[2][0]*100:.2f}'
            col1.metric(label="Multiplicador", value= valor_mult )
            col2.metric(label="Vazamento (%)", value = valor_vazamento )
            col3.metric(label="PIB (%)", value= valor_pib_percentual )
                
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
            
    """
    with col[2]:    
        with st.expander('Sobre', expanded=True):
            st.write('''
                - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
                - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
                - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
                ''')
            
    """
     
        
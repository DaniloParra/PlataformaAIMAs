import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt 
################################################################################

#Tabela de estações
estacoes_df = pd.DataFrame([['Taracua','Tiquié','14280000','Fluvio'],
                            ['PariCachoeira','Tiquié','8069003','Pluvio'],
                            ['PariCachoeira','Tiquié','14300000','Fluvio'],
                            ['PirararaPoco','Tiquié','8069004','Pluvio'],
                            ['Cunuri','Tiquié','14310000','Fluvio'],
                            ['Tunui','Içana','8168000','Pluvio'],
                            ['SaoJoaquim','Içana','14215000','Fluvio'],
                            ['Assuncao','Içana','14230000','Fluvio'],
                            ['Assuncao','Içana','8167000','Pluvio'],
                            ['LouroPoco','Içana','14220000','Fluvio'],
                            ['Santana','Içana','8167003','Pluvio']], columns=['Local', 'Região', 'N°Estação', 'Tipo'])


#Título
st.title('Dados hidrológicos do Rio Negro')

#Subtítulo
st.header('Agência Nacional das Águas (ANA)')

#Subtítulo 2
st.subheader('Lista de estações')

#Mostra a tabela das estações
st.table(estacoes_df)

#Define 3 colunas para a seleção dos parâmetros do gráfico
colA1, colA2, colA3 = st.columns(3)

with colA1:
    #Coluna da Região
    regiao_selected = st.selectbox("Selecione a região",
                                ["Tiquie", "Icana"])
    
with colA2:
    #Coluna do tipo de dado (Plúvio ou Flúvio)
    dado_selected = st.selectbox("Selecione o tipo de dado",
                                ["Cotas", "Chuvas"])

with colA3:
    #Coluna do número da estação
    estacao_selected = st.selectbox("Selecione a estação desejada",
                                    estacoes_df['N°Estação'])

#Seleciona o valor do dicionário adequado 
local_selected = estacoes_df.loc[estacoes_df["N°Estação"] == estacao_selected]['Local']
local_selected = local_selected.item()

#Busca o caminho do arquivo com os parâmetros selecionados
df_path = (f"{regiao_selected}_{local_selected}_{estacao_selected}_{dado_selected}.csv")

mask = "NivelConsistencia == 2"

selected_df = pd.read_csv(f"Dados/ANA/{df_path}", header=11, encoding='Latin1', sep=';', dtype={'EstacaoCodigo': 'str', 'Data':'str'}).query(mask)

##### Processa as datas mínimas e máximas do dado selecionado
selected_df['Data'] = pd.to_datetime(selected_df['Data'], format="%d/%m/%Y")

##### Define uma segunda linha de caixas de seleção
colB1, colB2 = st.columns(2)
with colB1:
    data_inicio_selected = st.date_input("Selecione a data inicial",
                                         min_value = selected_df['Data'].min(),
                                         max_value = selected_df['Data'].max(),
                                         value=selected_df['Data'].min())
with colB2:
    data_fim_selected = st.date_input("Selecione a data final",
                                      min_value = selected_df['Data'].min(),
                                      max_value = selected_df['Data'].max(),
                                      value = selected_df['Data'].max())



# #### Data wrangling no dataset selecionado (Talvez melhor colocar em um módulo)
dtype={'EstacaoCodigo': 'str', 'Data':'str'}

cols_cotas_lista = ['Data','Cota01', 'Cota02', 'Cota03','Cota04',
                    'Cota05', 'Cota06','Cota07', 'Cota08', 'Cota09',
                    'Cota10','Cota11', 'Cota12', 'Cota13', 'Cota14',
                    'Cota15', 'Cota16', 'Cota17','Cota18', 'Cota19',
                    'Cota20', 'Cota21', 'Cota22', 'Cota23', 'Cota24',
                    'Cota25', 'Cota26', 'Cota27', 'Cota28', 'Cota29',
                    'Cota30', 'Cota31']

##### CONVERTE O DATAFRAME DE WIDE PARA LONG 
tmp_df = pd.melt(selected_df[cols_cotas_lista],
                 id_vars=['Data'],
                 var_name='Day',
                 value_name='Cotas').sort_values(['Data','Day']).dropna(subset='Day')

tmp_df = tmp_df.dropna(subset =['Cotas']) #remove os nulos

tmp_df['Day'] = tmp_df['Day'].str.replace('Cota','') 
tmp_df['Year'] = tmp_df['Data'].dt.year
tmp_df['Month'] = tmp_df['Data'].dt.month
tmp_df['Data'] = pd.to_datetime(tmp_df[['Year','Month','Day']])


##### GRÁFICO
graph_bt = st.button('Gerar Gráfico')
if graph_bt:
    #Define os parâmetros do gráfico
    #Converte as datas do filtro para datetime
    data_inicio_selected = pd.to_datetime(data_inicio_selected)
    data_fim_selected = pd.to_datetime(data_fim_selected)

    ## Aplica o filtro das datas determinadas na caixa de seleção
    date_stt_mask = tmp_df['Data'] >= data_inicio_selected
    date_end_mask = tmp_df['Data'] <= data_fim_selected
    #st.write(tmp_df[date_stt_mask & date_end_mask])

    fig, ax = plt.subplots()
    ax.plot(tmp_df[date_stt_mask & date_end_mask]['Data'],
            tmp_df[date_stt_mask & date_end_mask]['Cotas'])
    st.pyplot(fig)
    
#st.write(subset)
# st.plotly_chart()


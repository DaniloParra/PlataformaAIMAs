import pandas as pd
import numpy as np
import datetime as dt

file = "Dados/ANA/Tiquie_Taracua_14280000_Cotas.csv"

df = pd.read_csv(file, header=11, encoding='Latin1', sep=';', dtype={'EstacaoCodigo': 'str', 'Data':'str'})

cols_cotas_lista = ['Data','Cota01', 'Cota02', 'Cota03','Cota04',
                    'Cota05', 'Cota06','Cota07', 'Cota08', 'Cota09'
                    'Cota10','Cota11', 'Cota12', 'Cota13', 'Cota14',
                    'Cota15', 'Cota16', 'Cota17','Cota18', 'Cota19',
                    'Cota20', 'Cota21', 'Cota22', 'Cota23', 'Cota24',
                    'Cota25', 'Cota26', 'Cota27', 'Cota28', 'Cota29',
                    'Cota30', 'Cota31']

tmp_df = df.query('NivelConsistencia == 2')
tmp_df['Data'] = pd.to_datetime(tmp_df['Data'], format="%d/%m/%Y")

#tmp_df = pd.melt(tmp_df[cols_cotas_lista],
                 id_vars=['Data'],
                 var_name='Dia',
                value_name='Cotas').sort_values(['Data','Dia']).dropna(subset='Dia')

#tmp_df['Dia'] = tmp_df['Dia'].str.replace('Cota','').astype('int')

#tmp_df['Year'] = tmp_df['Data'].dt.year
#tmp_df['Month'] = tmp_df['Data'].dt.month
#tmp_df['RightData'] = pd.to_datetime(tmp_df[['Year','Month','Dia']])

print(tmp_df.dropna(subset=(['Dia', 'Cotas'])))

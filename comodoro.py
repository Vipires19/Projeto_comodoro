
import streamlit as st
import pandas as pd
import plotly.express as px

if 'data' not in st.session_state:
    df = pd.read_excel(r'C:\Users\user\Downloads\Data science\Python\Projetos do Pirão\projeto_comodoro\Pasta1.xlsx')
    #df = pd.read_excel(r'Pasta1.xlsx')
    df['Status'] = df['Status'].fillna('Não')
    df['Turno'] = df['Turno'].fillna('Não')
    st.session_state['data'] = df

st.set_page_config(
    layout =  'wide',
    page_title = 'Comodoro Delivery',
)

st.title('Comodoro Delivery')

df = st.session_state['data']
df['Mês'] = df['Data'].dt.month
mes = {1: 'Janeiro', 2 :'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6 : 'Junho', 7 : 'Julho', 8 : 'Agosto', 9 : 'Setembro', 10 : 'Outubro', 11 : 'Novembro', 12 : 'Dezembro'}
df['Mês'] = df['Mês'].map(mes)
df['Dia'] = df['Data'].dt.day
df = df[['Mês', 'Dia','Restaurante','Entregador','Status','Turno','Produto','Quantidade','Valor Total','Valor Entregador','Lucro']]
df.set_index('Mês', inplace = True)
df_entregas =  df[df['Produto'] == 'entregas']
df_gaso = df[df['Produto'] == 'combustivel']

mes = df.index
meses = st.selectbox('Mês', mes)
df_mes = df[df.index == meses]
df_mes = df_mes[['Dia','Restaurante','Entregador','Status','Turno','Produto','Quantidade','Valor Total','Valor Entregador','Lucro']]
df_mes_entrega = df_mes[df_mes['Produto'] == 'entregas'][['Dia', 'Restaurante','Entregador','Status','Turno','Produto','Quantidade','Valor Total','Valor Entregador','Lucro']]
df_mes_comb = df_mes[df_mes['Produto'] == 'combustivel'][['Dia', 'Entregador', 'Quantidade', 'Valor Total']]
df_mes = df[df.index == meses] 
col1,col2,col3 = st.columns(3)
col1.metric('Quantidade de entregadores:', df_mes_entrega["Entregador"].value_counts().sum())
col1.metric('Quantidade de entregadores confirmados:',df_mes_entrega[df_mes_entrega['Status']=='confirmado'].value_counts().sum())
col1.metric('Quantidade de entregadores pendentes:',df_mes_entrega[df_mes_entrega['Status']=='pendente'].value_counts().sum())
col1.metric('Quantidade de entregadores rejeitados: ',df_mes_entrega[df_mes_entrega['Status']=='rejeitado'].value_counts().sum())
col2.metric('Quantidade de entregas', f'{df_mes_entrega["Quantidade"].sum()}')
col2.metric('Valor total da entregas', f'R$ {df_mes_entrega["Valor Total"].sum()}')
col2.metric('Valor total de Combustível', f'R$ {df_mes_comb["Valor Total"].sum()}')
col2.metric('Gasto total', f'R$ {(df_mes_entrega["Valor Total"].sum() + df_mes_comb["Valor Total"].sum()):,.2f}')
col3.metric('Lucro mensal', f'R$ {df_mes["Lucro"].sum():,.2f}')

st.dataframe(df_mes_entrega)




df_filtrado = df[['Turno', 'Lucro']]
df_filtrado = df_filtrado[df_filtrado['Turno'].str.strip() != 'Não']
df_filtrado['Lucro'] = df_filtrado['Lucro'].astype(str).replace('[^\d,.-]', '', regex=True).str.replace(',', '.').astype(float)
df_filtrado = df_filtrado.sort_values(by='Turno')
fig_df_filtrado = px.bar(df_filtrado, x='Turno', y='Lucro', title='Lucro por Turno Geral')
st.plotly_chart(fig_df_filtrado)


st.divider()
st.header('Restaurantes')

restaurante = df['Restaurante'].value_counts().index
restaurantes = st.selectbox('Restaurante', restaurante)
df_rest = df[df['Restaurante'] == restaurantes]
df_rest_entrega = df_rest[df_rest['Produto'] == 'entregas']
filtro = ['Mensal', 'Diário']
filtros = st.selectbox('Filtro', filtro)

if filtros == 'Mensal':
    col1,col2,col3,col4 = st.columns(4)
    mes = df_rest.index
    meses = col1.selectbox('Mês', mes)
    df_mes = df_rest[df_rest.index == meses] 
    df_mes = df_mes[['Dia', 'Entregador', 'Status','Turno', 'Produto','Quantidade', 'Valor Total','Lucro', 'Valor Entregador']]
    df_mes_entrega = df_mes[df_mes['Produto'] == 'entregas'][['Dia', 'Entregador', 'Status','Turno', 'Quantidade', 'Valor Total','Lucro', 'Valor Entregador']]
    df_mes_comb = df_mes[df_mes['Produto'] == 'combustivel'][['Dia', 'Entregador', 'Quantidade', 'Valor Total']]
    col1.dataframe(df_mes_entrega)
    col2.metric('Quantidade de entregadores:', df_mes_entrega["Entregador"].value_counts().sum())
    col2.metric('Quantidade de entregadores confirmados:',df_mes_entrega[df_mes_entrega['Status']=='confirmado'].value_counts().sum())
    col2.metric('Quantidade de entregadores pendentes:',df_mes_entrega[df_mes_entrega['Status']=='pendente'].value_counts().sum())
    col2.metric('Quantidade de entregadores rejeitados: ',df_mes_entrega[df_mes_entrega['Status']=='rejeitado'].value_counts().sum())
    col3.metric('Quantidade de entregas', f'{df_mes_entrega["Quantidade"].sum()}')
    col3.metric('Valor total da entregas', f'R$ {df_mes_entrega["Valor Total"].sum()}')
    col3.metric('Custo por entrega', f'R$ {(df_mes_entrega["Valor Total"][0] / df_mes_entrega["Quantidade"][0]):,.2f}')
    col3.metric('Valor total de Combustível', f'R$ {df_mes_comb["Valor Total"].sum()}')
    col4.metric('Gasto total', f'R$ {df_mes_entrega["Valor Total"].sum() + df_mes_comb["Valor Total"].sum()}')
    col4.metric('Lucro mensal', f'R$ {df_mes["Lucro"].sum():,.2f}')
    
    motoca = df_mes_entrega['Entregador'].value_counts().index
    motocas = st.selectbox('Entregadores', motoca)
    df_moto = df_mes_entrega[df_mes_entrega['Entregador'] == motocas]
    df_moto = df_moto[['Dia', 'Status', 'Turno', 'Quantidade', 'Valor Entregador']]
    colunas = {'Dia' : 'Dia', 'Status' : 'Status', 'Turno':'Turno', 'Quantidade' : 'Quantidade de entregas', 'Valor Entregador' : 'Valor pago ao Entregador'}
    df_moto.rename(columns = colunas, inplace = True)
    df_moto.set_index('Dia', inplace = True)
    st.dataframe(df_moto)
    

if filtros == 'Diário':

    col1,col2,col3,col4 = st.columns(4)
    data = df_rest['Dia'].value_counts().index
    datas = col1.selectbox('Dia', data)
    df_data = df_rest[df_rest['Dia'] == datas] 
    df_data = df_data[['Dia', 'Entregador', 'Status','Turno', 'Produto','Quantidade', 'Valor Total','Lucro', 'Valor Entregador']]
    df_data.set_index('Dia', inplace = True)
    df_data_entrega = df_data[df_data['Produto'] == 'entregas'][['Entregador', 'Status','Turno', 'Quantidade', 'Valor Total','Lucro', 'Valor Entregador']]
    df_data_comb = df_data[df_data['Produto'] == 'combustivel'][['Entregador', 'Quantidade', 'Valor Total']]
    col1.dataframe(df_data_entrega)
    col2.metric('Quantidade de entregadores:', df_data_entrega["Entregador"].value_counts().sum())
    col2.metric('Quantidade de entregadores confirmados:',df_data_entrega[df_data_entrega['Status']=='confirmado'].value_counts().sum())
    col2.metric('Quantidade de entregadores pendentes:',df_data_entrega[df_data_entrega['Status']=='pendente'].value_counts().sum())
    col2.metric('Quantidade de entregadores rejeitados: ',df_data_entrega[df_data_entrega['Status']=='rejeitado'].value_counts().sum())
    col3.metric('Quantidade de entregas', f'{df_data_entrega["Quantidade"].sum()}')
    col3.metric('Valor total da entregas', f'R$ {df_data_entrega["Valor Total"].sum()}')
    col3.metric('Custo por entrega', f'R$ {(df_data_entrega["Valor Total"].iloc[0] / df_data_entrega["Quantidade"].iloc[0]):,.2f}')
    col3.metric('Valor total de Combustível', f'R$ {df_data_comb["Valor Total"].sum()}')
    col4.metric('Gasto total', f'R$ {df_data_entrega["Valor Total"].sum() + df_data_comb["Valor Total"].sum()}')
    col4.metric('Lucro diário', f'R$ {df_data["Lucro"].sum():,.2f}')
    
    
    motoca = df_data_entrega['Entregador'].value_counts().index
    motocas = st.selectbox('Entregadores', motoca)
    df_moto = df_data_entrega[df_data_entrega['Entregador'] == motocas]
    df_moto = df_moto[['Status', 'Turno', 'Quantidade', 'Valor Entregador']]
    colunas = {'Status' : 'Status', 'Turno':'Turno', 'Quantidade' : 'Quantidade de entregas', 'Valor Entregador' : 'Valor pago ao Entregador'}
    df_moto.rename(columns = colunas, inplace = True)
    st.dataframe(df_moto)



df_rest_filtrado = df_rest[['Turno', 'Lucro']]

df_rest_filtrado = df_rest_filtrado[df_rest_filtrado['Turno'].str.strip() != 'Não']

df_rest_filtrado['Lucro'] = df_rest_filtrado['Lucro'].astype(str).replace('[^\d,.-]', '', regex=True).str.replace(',', '.').astype(float)

df_filtrado = df_rest_filtrado.sort_values(by='Turno')

fig_df_rest_filtrado = px.bar(df_filtrado, x='Turno', y='Lucro', title='Lucro por Turno')

st.plotly_chart(fig_df_rest_filtrado)
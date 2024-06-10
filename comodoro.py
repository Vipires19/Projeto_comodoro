
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
df_entregas =  df[df['Produto'] == 'entregas']
st.dataframe(df_entregas)
#mes = {1: 'Janeiro', 2 :'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6 : 'Junho', 7 : 'Julho', 8 : 'Agosto', 9 : 'Setembro', 10 : 'Outubro', 11 : 'Novembro', 12 : 'Dezembro'}


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
    col1,col2,col3 = st.columns(3)
    mes = df_rest_entrega['Dia'].value_counts().index.month
    meses = col1.selectbox('Mês', mes)
    df_mes = df_rest_entrega[df_rest_entrega['Dia'].dt.month == meses] 
    df_mes = df_mes[['Dia', 'Entregador', 'Status','Turno', 'Quantidade', 'Valor Total','Lucro', 'Valor Entregador']]
    df_mes['mes'] = df_mes['Dia'].dt.month
    df_mes.set_index('mes', inplace = True)
    df_mes['Dia'] = df_mes['Dia'].dt.day
    col1.dataframe(df_mes)
    col2.metric('Quantidade de entregadores:', df_mes["Entregador"].value_counts().sum())
    col2.metric('Quantidade de entregadores confirmados:',df_mes[df_mes['Status']=='confirmado'].value_counts().sum())
    col2.metric('Quantidade de entregadores pendentes:',df_mes[df_mes['Status']=='pendente'].value_counts().sum())
    col2.metric('Quantidade de entregadores rejeitados: ',df_mes[df_mes['Status']=='rejeitado'].value_counts().sum())
    col3.metric('Quantidade de entregas', f'{df_mes["Quantidade"].sum()}')
    col3.metric('Valor total da entregas', f'R$ {df_mes["Valor Total"].sum()}')
    col3.metric('Lucro mensal', f'R$ {df_mes["Lucro"].sum()}')
    motoca = df_mes['Entregador'].value_counts().index
    motocas = col3.selectbox('Entregadores', motoca)
    df_moto = df_mes[df_mes['Entregador'] == motocas]
    df_moto = df_moto[['Dia', 'Status', 'Turno', 'Quantidade', 'Valor Entregador']]
    colunas = {'Dia' : 'Dia', 'Status' : 'Status', 'Turno':'Turno', 'Quantidade' : 'Quantidade de entregas', 'Valor Entregador' : 'Valor pago ao Entregador'}
    df_moto.rename(columns = colunas, inplace = True)
    df_moto.set_index('Dia', inplace = True)
    col3.dataframe(df_moto)
    

if filtros == 'Diário':
    col1,col2,col3 = st.columns(3)
    data = df_rest_entrega['Dia'].value_counts().index.day
    datas = col1.selectbox('Dia', data)
    df_data = df_rest_entrega[df_rest_entrega['Dia'].dt.day == datas] 
    df_data = df_data[['Dia', 'Entregador', 'Status','Turno', 'Quantidade', 'Valor Total', 'Valor Entregador', 'Lucro']]
    df_data['Dia'] = df_data['Dia'].dt.day
    df_data.set_index('Dia', inplace = True)
    col1.dataframe(df_data)
    col2.metric('Quantidade de entregadores:', df_data["Entregador"].value_counts().sum())
    col2.metric('Quantidade de entregadores confirmados:',df_data[df_data['Status']=='confirmado'].value_counts().sum())
    col2.metric('Quantidade de entregadores pendentes:',df_data[df_data['Status']=='pendente'].value_counts().sum())
    col2.metric('Quantidade de entregadores rejeitados: ',df_data[df_data['Status']=='rejeitado'].value_counts().sum())
    col3.metric('Quantidade de entregas', f'{df_data["Quantidade"].sum()}')
    col3.metric('Valor total da entregas', f'R$ {df_data["Valor Total"].sum()}')
    col3.metric('Lucro mensal', f'R$ {df_data["Lucro"].sum()}')
    motoca = df_data['Entregador'].value_counts().index
    motocas = col3.selectbox('Entregadores', motoca)
    df_moto = df_data[df_data['Entregador'] == motocas]
    col3.dataframe(df_moto)


df_rest_filtrado = df_rest[['Turno', 'Lucro']]

df_rest_filtrado = df_rest_filtrado[df_rest_filtrado['Turno'].str.strip() != 'Não']

df_rest_filtrado['Lucro'] = df_rest_filtrado['Lucro'].astype(str).replace('[^\d,.-]', '', regex=True).str.replace(',', '.').astype(float)

df_filtrado = df_rest_filtrado.sort_values(by='Turno')

fig_df_rest_filtrado = px.bar(df_filtrado, x='Turno', y='Lucro', title='Lucro por Turno')

st.plotly_chart(fig_df_rest_filtrado)
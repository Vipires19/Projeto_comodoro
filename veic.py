import streamlit as st
import pandas as pd

if 'data' not in st.session_state:
    df = pd.read_excel(r'C:\Users\user\Downloads\Data science\Python\projeto_chatbot\projeto_pm\veic_produto.xlsx')
    colunas = {'dia':'Dia', 'semana':'Dia da semana', 'hora':'Hora', 'periodo':'Período','mes':'Mês', 'crime':'Crime','cia':'CIA PM', 'endereco':'Endereço',
       'bairro':'Bairro', 'subsetor':'Subsetor', 'cidade':'Cidade', 'data_recuperado':'Data da Recuperação', 'bairro_recuperado':'Bairro da recuperação',
       'ambiente':'Ambiente', 'tipo':'Tipo do veículo', 'marca':'Marca', 'modelo':'Modelo', 'placa':'Placa', 'ano':'Ano','flagrante':'Flagrante?',
       'vitima':'Vítima', 'num_agressores':'N° de agressores', 'sexo':'Sexo dos agressores', 'cor':'Cor', 'arma':'Arma utilizada', 'transporte':'Transporte utilizado',
       'cor_veic':'Cor do veículo utilizado', 'localizado':'Localizado?'}
    df.rename(columns=colunas,inplace=True)
    cia = {'_1ªCIA': '1ªCia', '_2ªCIA':'2ªCia', '_3ªCIA': '3ªCia'}
    df['CIA PM'] = df['CIA PM'].map(cia)
    crime = {'FV': 'Furto', 'RV':'Roubo'}
    df['Crime'] = df['Crime'].map(crime)
    df.set_index('mês', inplace=True)
    df['Bairro da recuperação']= df['Bairro da recuperação'].fillna('Não Localizado')
    df.fillna({'Localizado?' : 0}, inplace= True)
    loc = {1: 'Sim', 0 : 'Não'}
    df['Localizado?'] = df['Localizado?'].map(loc)
    df.fillna({'Cor do veículo utilizado' : 0}, inplace=True)
    cor_veic = {0: 'N/INF'}
    df['Cor do veículo utilizado'] = df['Cor do veículo utilizado'].map(cor_veic)
    df.fillna({'N° de agressores' : 'N/ INF'}, inplace= True)
    df.fillna({'Sexo dos agressores' : 'N/ INF'}, inplace= True)
    df.fillna({'Cor' : 'N/ INF'}, inplace= True)
    df.fillna({'Arma utilizada' : 'N/ INF'}, inplace= True)
    df.fillna({'Transporte utilizado' : 'N/ INF'}, inplace= True)
    df.fillna({'Cor do veículo utilizado' : 'N/ INF'}, inplace= True)
    st.session_state['data'] = df

df = st.session_state['data']


st.set_page_config(
    layout =  'wide',
    page_title = 'Veículos produto de furto/roubo',
)

st.markdown('# Veículos produto de furto/roubo')
mes = df.index.value_counts().index
meses = st.selectbox('Mês', mes)
df_mes = df[df.index == meses]
furto1 = df_mes[df_mes['Crime'] == 'Furto']
roubo1 = df_mes[df_mes['Crime'] == 'Roubo']
soma_furto = furto1['Crime'].value_counts().max()
soma_roubo = roubo1['Crime'].value_counts().max()
loc_furto = furto1[furto1['Localizado?'] == 'Sim']['Crime'].value_counts().max()
loc_roubo = roubo1[roubo1['Localizado?'] == 'Sim']['Crime'].value_counts().max()
col1,col2,col3,col4 = st.columns(4)
col1.metric(label="Total de Furtos", value= soma_furto)
col2.metric('Furto Localizados', loc_furto)
col3.metric(label="Total de Roubos", value= soma_roubo)
col4.metric('Roubos Localizados', loc_roubo)
cias = df_mes['CIA PM'].value_counts().index
cia = st.selectbox('Cia PM', cias)
df_cia = df_mes[df_mes['CIA PM'] == cia]
furto1 = df_cia[df_cia['Crime'] == 'Furto']
roubo1 = df_cia[df_cia['Crime'] == 'Roubo']
soma_furto = furto1['Crime'].value_counts().max()
soma_roubo = roubo1['Crime'].value_counts().max()
loc_furto = furto1[furto1['Localizado?'] == 'Sim']['Crime'].value_counts().max()
loc_roubo = roubo1[roubo1['Localizado?'] == 'Sim']['Crime'].value_counts().max()
col1,col2,col3,col4 = st.columns(4)
col1.metric(label="Total de Furtos", value= soma_furto)
col2.metric('Furto Localizados', loc_furto)
col3.metric(label="Total de Roubos", value= soma_roubo)
col4.metric('Roubos Localizados', loc_roubo)
dfcol = ['Dia','Hora','Período', 'Crime','Tipo do veículo','Marca','Modelo', 'Placa','Ano','Endereço','Bairro','Subsetor','Localizado?','Data da Recuperação', 'Bairro da recuperação', 'Ambiente']
st.dataframe(df_cia[dfcol],
             column_config= {'Data da Recuperação' : st.column_config.DateColumn()})
st.divider()

crime = df_cia['Crime'].value_counts().index
crimes = st.selectbox('Crime', crime)
df_crime = df_cia[df_cia['Crime'] == crimes]

df_peri = df_crime['Período'].value_counts()
df_loc = df_crime['Localizado?'].value_counts()
df_bairro = df_crime['Bairro'].value_counts()
df_tipo = df_crime['Tipo do veículo'].value_counts()
df_vit = df_crime['Vítima'].value_counts()
df_set = df_crime['Subsetor'].value_counts()



col1,col2,col3 = st.columns(3)
col1.markdown('**Período**')
col1.dataframe(df_peri)
col1.divider()
col1.markdown('**Vítimas**')
col1.dataframe(df_vit)
col2.markdown('**Tipo de veículo**')
col2.dataframe(df_tipo)
col2.divider()
col2.markdown('**Subsetores**')
col2.dataframe(df_set)
col3.markdown('**Bairros**')
col3.dataframe(df_bairro)
col3.divider()
               

st.divider()



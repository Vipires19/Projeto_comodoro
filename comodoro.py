import streamlit as st
import pandas as pd

if 'data' not in st.session_state:
    df = pd.read_excel(r'C:\Users\user\Downloads\Data science\Python\Projetos do Pirão\projeto_comodoro\Pasta1.xlsx')
    df['Status'] = df['Status'].fillna('Não')
    df['Turno'] = df['Turno'].fillna('Não')
    st.session_state['data'] = df

st.set_page_config(
    layout =  'wide',
    page_title = 'Comodoro Delivery',
)

df = st.session_state['data']
df_entregas =  df[df['Produto'] == 'entregas']
st.dataframe(df_entregas)

restaurante = df_entregas['Restaurante'].value_counts().index
restaurantes = st.selectbox('Restaurante', restaurante)
df_rest = df[df['Restaurante'] == restaurantes]
df_rest
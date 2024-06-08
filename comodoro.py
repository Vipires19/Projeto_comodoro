import streamlit as st
import pandas as pd
import plotly.express as px

if 'data' not in st.session_state:
    df = pd.read_excel(r'Pasta1.xlsx')
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

df_filtrado = df[['Turno', 'Lucro']]
df_filtrado = df_filtrado[df_filtrado['Turno'].str.strip() != 'Não']
df_filtrado['Lucro'] = df_filtrado['Lucro'].astype(str).replace('[^\d,.-]', '', regex=True).str.replace(',', '.').astype(float)
df_filtrado = df_filtrado.sort_values(by='Turno')
fig_df_filtrado = px.bar(df_filtrado, x='Turno', y='Lucro', title='Lucro por Turno Geral')
st.plotly_chart(fig_df_filtrado)

restaurante = df_entregas['Restaurante'].value_counts().index
restaurantes = st.selectbox('Restaurante', restaurante)
df_rest = df[df['Restaurante'] == restaurantes]

df_rest

df_rest_filtrado = df_rest[['Turno', 'Lucro']]

df_rest_filtrado = df_rest_filtrado[df_rest_filtrado['Turno'].str.strip() != 'Não']

df_rest_filtrado['Lucro'] = df_rest_filtrado['Lucro'].astype(str).replace('[^\d,.-]', '', regex=True).str.replace(',', '.').astype(float)

df_filtrado = df_rest_filtrado.sort_values(by='Turno')

fig_df_rest_filtrado = px.bar(df_filtrado, x='Turno', y='Lucro', title='Lucro por Turno')

st.plotly_chart(fig_df_rest_filtrado)
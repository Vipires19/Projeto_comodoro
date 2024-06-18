
import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import streamlit_authenticator as stauth
from pathlib import Path


st.set_page_config(
            layout =  'wide',
            page_title = 'Comodoro Delivery',
        )


# --- Authentication ---
# Load hashed passwords
file_path = Path(__file__).parent/"db"/"hashed_pw.pkl"

with file_path.open("rb") as file:
  hashed_passwords = pickle.load(file)
  
credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": hashed_passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(credentials= credentials, cookie_name="st_session", cookie_key="key123", cookie_expiry_days= 1)
authenticator.login()

def pagina_principal():
    st.title('Comodoro Delivery')
    btn = authenticator.logout()
    if btn:
        st.session_state["authentication_status"] == None
    
    df = st.session_state['data']
    df_entregas =  st.session_state['df_entregas']
    df_gaso = st.session_state['df_gaso']
    return(df,df_entregas,df_gaso)

def metricas_gerais():
    df = st.session_state['data']
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

    on1 = st.toggle('Mostrar dados')
    if on1:
        st.dataframe(df_mes_entrega)

    col1,col2,col3 = st.columns(3)
    rest_mais_entregadores = df_mes_entrega.groupby('Restaurante')['Entregador'].count().sort_values(ascending=False).index[0]
    col1.metric('Restaurante com mais entregadores', rest_mais_entregadores)
    rest_mais_entregas = df_mes_entrega.groupby('Restaurante')['Quantidade'].sum().sort_values(ascending=False).index[0]
    col2.metric('Restaurante com mais entregas', rest_mais_entregas)
    ent_mais_entregas = df_mes_entrega.groupby('Entregador')['Quantidade'].sum().sort_values(ascending=False).index[0]
    col3.metric('Entregador com mais entregas', ent_mais_entregas)
    
    df_filtrado = df[['Turno', 'Lucro']]
    df_filtrado = df_filtrado[df_filtrado['Turno'].str.strip() != 'Não']
    df_filtrado['Lucro'] = df_filtrado['Lucro'].astype(str).replace('[^\d,.-]', '', regex=True).str.replace(',', '.').astype(float)
    df_filtrado = df_filtrado.sort_values(by='Turno')
    df_filtrado_agg = df_filtrado.groupby('Turno', as_index=False).sum()
    fig_df_filtrado = px.bar(df_filtrado_agg, x='Turno', y='Lucro', title='Lucro por Turno Geral')

    df_mes_filtrado_situacao = df_mes['Status'].value_counts()
    df_mes_filtrado_situacao.drop('Não', inplace=True)
    fig_df_mes_filtrado_situacao_pizza = px.pie(names=df_mes_filtrado_situacao.index, values=df_mes_filtrado_situacao.values, title='Situação dos Entregadores')

    df_mes_filtrado_entregas = df_mes[['Dia', 'Quantidade']]
    df_mes_filtrado_entregas_agg = df_mes_filtrado_entregas.groupby('Dia', as_index=False).sum()
    fig_df_mes_filtrado_entregas_agg = px.bar(df_mes_filtrado_entregas_agg, x='Dia', y='Quantidade', title='Quantidade de Entregas por Dia')

    df_mes_filtrado_entregas_restaurantes = df_mes[['Restaurante', 'Quantidade']]
    df_mes_filtrado_entregas_restaurantes = df_mes_filtrado_entregas_restaurantes.groupby('Restaurante', as_index=False).sum()
    fig_df_mes_filtrado_entregas_restaurantes = px.bar(df_mes_filtrado_entregas_restaurantes, x='Restaurante', y='Quantidade', title='Quantidade de Entregas por Restaurante')

    df_mes_filtrado_lucro_pizza = df_mes[['Restaurante', 'Lucro']]
    df_mes_filtrado_lucro_pizza_agg = df_mes_filtrado_lucro_pizza.groupby('Restaurante', as_index=False).sum()
    fig_df_mes_filtrado_lucro_pizza = px.pie(df_mes_filtrado_lucro_pizza_agg, names='Restaurante', values='Lucro', title='Lucro Geral por Restaurante')

    col1_graph, col2_graph = st.columns(2)
    col1_2_graph, col2_2_graph = st.columns(2)

    col1_graph.plotly_chart(fig_df_filtrado)
    col2_graph.plotly_chart(fig_df_mes_filtrado_situacao_pizza)
    col1_2_graph.plotly_chart(fig_df_mes_filtrado_entregas_restaurantes)
    col2_2_graph.plotly_chart(fig_df_mes_filtrado_lucro_pizza)
    st.plotly_chart(fig_df_mes_filtrado_entregas_agg)
    
def metricas_restaurantes():
    df = st.session_state['data']
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
        col3.metric('Valor total da entregas', f'R$ {df_mes_entrega["Valor Total"].sum():,.2f}')
        col3.metric('Custo por entrega', f'R$ {(df_mes_entrega["Valor Total"][0] / df_mes_entrega["Quantidade"][0]):,.2f}')
        col3.metric('Valor total de Combustível', f'R$ {df_mes_comb["Valor Total"].sum():,.2f}')
        col4.metric('Gasto total', f'R$ {df_mes_entrega["Valor Total"].sum() + df_mes_comb["Valor Total"].sum():,.2f}')
        col4.metric('Lucro mensal', f'R$ {df_mes["Lucro"].sum():,.2f}')
        
        df_mes_filtrado = df_mes[['Turno', 'Lucro']]
        df_mes_filtrado = df_mes_filtrado[df_mes_filtrado['Turno'].str.strip() != 'Não']
        df_mes_filtrado['Lucro'] = df_mes_filtrado['Lucro'].astype(str).replace('[^\d,.-]', '', regex=True).str.replace(',', '.').astype(float)
        df_filtrado = df_mes_filtrado.sort_values(by='Turno')
        df_filtrado_agg = df_filtrado.groupby('Turno', as_index=False).sum()
        fig_df_mes_filtrado = px.bar(df_filtrado_agg, x='Turno', y='Lucro', title='Lucro por Turno')

        df_mes_filtrado_situacao = df_mes['Status'].value_counts()
        df_mes_filtrado_situacao.drop('Não', inplace=True)
        fig_df_mes_filtrado_situacao_pizza = px.pie(names=df_mes_filtrado_situacao.index, values=df_mes_filtrado_situacao.values, title='Situação dos entregadores')

        df_mes_filtrado_entregas = df_mes[['Dia', 'Quantidade']]
        df_mes_filtrado_entregas_agg = df_mes_filtrado_entregas.groupby('Dia', as_index=False).sum()
        fig_df_mes_filtrado_entregas_agg = px.bar(df_mes_filtrado_entregas_agg, x='Dia', y='Quantidade', title='Quantidade de Entregas por Dia')

        col1_graph, col2_graph = st.columns(2)

        col1_graph.plotly_chart(fig_df_mes_filtrado)
        col2_graph.plotly_chart(fig_df_mes_filtrado_situacao_pizza)
        st.plotly_chart(fig_df_mes_filtrado_entregas_agg)
        
                

                

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
        col3.metric('Valor total da entregas', f'R$ {df_data_entrega["Valor Total"].sum():,.2f}')
        col3.metric('Custo por entrega', f'R$ {(df_data_entrega["Valor Total"].iloc[0] / df_data_entrega["Quantidade"].iloc[0]):,.2f}')
        col3.metric('Valor total de Combustível', f'R$ {df_data_comb["Valor Total"].sum():,.2f}')
        col4.metric('Gasto total', f'R$ {df_data_entrega["Valor Total"].sum() + df_data_comb["Valor Total"].sum():,.2f}')
        col4.metric('Lucro diário', f'R$ {df_data["Lucro"].sum():,.2f}')
        
        df_data_filtrado = df_data[['Turno', 'Lucro']]
        df_data_filtrado = df_data_filtrado[df_data_filtrado['Turno'].str.strip() != 'Não']
        df_data_filtrado['Lucro'] = df_data_filtrado['Lucro'].astype(str).replace('[^\d,.-]', '', regex=True).str.replace(',', '.').astype(float)
        df_filtrado = df_data_filtrado.sort_values(by='Turno')
        df_filtrado_agg = df_filtrado.groupby('Turno', as_index=False).sum()
        fig_df_data_filtrado = px.bar(df_filtrado_agg, x='Turno', y='Lucro', title='Lucro por Turno', barmode="group")

        df_data_filtrado_situacao = df_data['Status'].value_counts()
        df_data_filtrado_situacao.drop('Não', inplace=True)
        fig_df_data_filtrado_situacao_pizza = px.pie(names=df_data_filtrado_situacao.index, values=df_data_filtrado_situacao.values, title='Situação dos entregadores')

        col1_graph, col2_graph = st.columns(2)

        col1_graph.plotly_chart(fig_df_data_filtrado)
        col2_graph.plotly_chart(fig_df_data_filtrado_situacao_pizza)
        

def metricas_entregadores():
    df = st.session_state['data']
    st.divider()
    st.header('Entregadores')

    df_moto_entrega = df[df['Produto'] == 'entregas'][['Dia', 'Entregador', 'Status','Turno', 'Quantidade', 'Valor Total','Lucro', 'Valor Entregador', 'Restaurante']]
    mes = df_moto_entrega.index
    meses = st.selectbox('Referente a:', mes)
    df_mes = df_moto_entrega[df_moto_entrega.index == meses] 
    motoca = df_moto_entrega['Entregador'].value_counts().index
    motocas = st.selectbox('Entregadores', motoca)
    df_moto = df_moto_entrega[df_moto_entrega['Entregador'] == motocas]

    df_moto2 = df_moto[['Dia','Status', 'Turno', 'Quantidade', 'Valor Entregador', 'Restaurante']]
    colunas = {'Dia' : 'Dia', 'Status' : 'Status', 'Turno':'Turno', 'Quantidade' : 'Quantidade de entregas', 'Valor Entregador' : 'Valor pago ao Entregador', 'Restaurante' : 'Restaurante'}
    df_moto2.rename(columns = colunas, inplace = True)

    col1,col2,col3 = st.columns(3)
    col1.dataframe(df_moto2)
    col2.metric('Quantidade de escalas:', df_moto["Dia"].value_counts().sum())
    col2.metric('Quantidade de escalas confirmado:',df_moto[df_moto['Status']=='confirmado'].value_counts().sum())
    col2.metric('Quantidade de escalas pendentes:',df_moto[df_moto['Status']=='pendente'].value_counts().sum())
    col2.metric('Quantidade de entregadores rejeitados: ',df_moto[df_moto['Status']=='rejeitado'].value_counts().sum())
    col3.metric('Quantidade de entregas', f'{df_moto["Quantidade"].sum()}')
    col3.metric('Valor total arrecadado', f'R$ {df_moto["Valor Entregador"].sum():,.2f}')
    col3.metric('Restaurante em que mais trabalhou:', df_moto['Restaurante'].value_counts().index[0])
    col3.metric('Turno em que mais trabalhou:', df_moto['Turno'].value_counts().index[0])

    df_filtrado = df_moto[['Restaurante',  'Quantidade']]
    df_filtrado_agg = df_filtrado.groupby('Restaurante', as_index=False).sum()
    fig_df_filtrado_agg = px.bar(df_filtrado_agg, x='Restaurante', y='Quantidade', title='Quantidade de Entregas de {} por Restaurante'.format(df_moto['Entregador'].iloc[0]))

    df_filtrado_valor_restaurtante = df_moto[['Lucro', 'Restaurante']]
    df_filtrado_valor_restaurtante_agg = df_filtrado_valor_restaurtante.groupby('Restaurante', as_index=False).sum()
    fig_df_mes_filtrado_lucro_pizza = px.pie(df_filtrado_valor_restaurtante_agg, names='Restaurante', values='Lucro', title='Lucro Geral por Restaurante')

    st.plotly_chart(fig_df_filtrado_agg)
    st.plotly_chart(fig_df_mes_filtrado_lucro_pizza)

def main():
    if st.session_state["authentication_status"]:
            
        df = pd.read_excel('files/Pasta1.xlsx')
        df['Status'] = df['Status'].fillna('Não')
        df['Turno'] = df['Turno'].fillna('Não')
        df['Mês'] = df['Data'].dt.month
        mes = {1: 'Janeiro', 2 :'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6 : 'Junho', 7 : 'Julho', 8 : 'Agosto', 9 : 'Setembro', 10 : 'Outubro', 11 : 'Novembro', 12 : 'Dezembro'}
        df['Mês'] = df['Mês'].map(mes)
        df['Dia'] = df['Data'].dt.day
        df = df[['Mês', 'Dia','Restaurante','Entregador','Status','Turno','Produto','Quantidade','Valor Total','Valor Entregador','Lucro']]
        df.set_index('Mês', inplace = True)
        st.session_state['data'] = df
        st.session_state['df_entregas'] = df_entregas =  df[df['Produto'] == 'entregas']
        st.session_state['df_gaso'] = df_gaso = df[df['Produto'] == 'combustivel']
    
        pagina_principal()

        metricas_gerais()

        metricas_restaurantes()

        metricas_entregadores()
        
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect.")

    elif st.session_state["authentication_status"] == None:
        st.warning("Please insert username and password")

if __name__ == '__main__':
    main()
    
import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
import datetime
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import urllib
import urllib.parse

mongo_user = st.secrets['MONGO_USER']
mongo_pass = st.secrets["MONGO_PASS"]

username = urllib.parse.quote_plus(mongo_user)
password = urllib.parse.quote_plus(mongo_pass)
client = MongoClient("mongodb+srv://%s:%s@cluster0.gjkin5a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" % (username, password))
st.cache_resource = client
db = client.estoquecmdr
coll = db.estoque

st.set_page_config(
            layout =  'wide',
            page_title = 'Comodoro Delivery',
        )


# --- Authentication ---
# Load hashed passwords
file_path = Path('comodoro.py').parent/"db"/"hashed_pw.pkl"

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

def inserindo_dados():
    col1,col2,col3,col4,col5 = st.columns(5)
    codigo = col1.number_input('Código do Produto', min_value = 0, max_value = 100000)
    quantidade = col2.number_input('Quant.', min_value = 0, max_value = 100000)
    descricao = col3.text_input('Descrição do produto')
    valor_compra = col4.number_input('Valor de Compra em R$')
    valor_venda = col5.number_input('Valor de venda em R$')
    adiciona_produto = col5.button('Adicionar')
    if adiciona_produto:
        entry = [{'Código' : codigo, 'Quantidade' : quantidade, 'Descrição' : descricao, 'Valor de compra' : valor_compra, 'Valor de venda' : valor_venda}]
        result = coll.insert_many(entry)
    
    estoque = db.estoque.find({})

    estoquedf = []
    for item in estoque:
        estoquedf.append(item)

    df = pd.DataFrame(estoquedf, columns= ['_id', 'Código','Descrição','Quantidade', 'Valor de compra', 'Valor de venda'])
    df.drop(columns='_id', inplace=True)
    st.session_state['estoque'] = df
    estoque = st.session_state['estoque']
    st.dataframe(estoque.set_index('Código')
    



def dados_vendas():
    df2 = st.session_state['data2']
    df3 = st.session_state['data3']
    
    col1,col2,col3,col4,col5,col6 = st.columns(6)
    codigos = df2.index
    cod = col1.selectbox('Código do produto:', codigos)
    produto = df2[df2.index == cod]['produto']
    descricao =  col2.text_input('Descrição', value = produto.iloc[0])
    valor_unit = df2[df2.index == cod]['valor-venda'].iloc[0]
    col3.number_input('Valor unitário', min_value = valor_unit, max_value=valor_unit)
    quantidade = col4.number_input('Quantidade', min_value = 1, max_value = 100000)
    valor_total = valor_unit*quantidade
    valor_compra = col5.metric('Valor', f'R$ {valor_total:.2F}')
    forma_pgto = ['Cartão de crédito', 'Cartão de débito', 'Dinheiro', 'Pix']
    pagamento = col6.selectbox('Forma de pagamento', forma_pgto)
    add = col6.button('Adicionar produto')

    novo_produto = [cod,produto.iloc[0],valor_unit,quantidade,valor_total, pagamento]
    if add:
        df3.loc[len(df3)]=novo_produto

    df3 = df3.set_index('codigo_produto')
    st.session_state['data3'] = df3
    df3 = st.session_state['data3']

def visualiza_vendas():
    lista = os.listdir('files/historico_vendas')
    dia = []
    hora = []
    for i in lista:
        nova_string1 = f'{i.split("venda")[1].split(".csv")[0].split("+")[1]}/{i.split("venda")[1].split(".csv")[0].split("+")[2]}/{i.split("venda")[1].split(".csv")[0].split("+")[3]}'
        nova_string2 = f'{i.split("venda")[1].split(".csv")[0].split("+")[4]}:{i.split("venda")[1].split(".csv")[0].split("+")[5]}:{i.split("venda")[1].split(".csv")[0].split("+")[6]}'
        dia.append(nova_string1)
        hora.append(nova_string2)
    
    data = pd.DataFrame(columns = ['dia','hora'])
    data['dia'] = dia
    data['hora'] = hora

    
    col1,col2 = st.columns(2)
    day = col1.selectbox('Dia', data['dia'].value_counts().index)
    df_dia = data[data['dia'] == day]
    hour = col2.selectbox('Hora', df_dia['hora'].value_counts().index)    
    
    venda_abrir = f'+{day.split("/")[0]}+{day.split("/")[1]}+{day.split("/")[2]}+{hour.split(":")[0]}+{hour.split(":")[1]}+{hour.split(":")[2]}'
    venda_aberta = pd.read_csv(f'files/historico_vendas/venda{venda_abrir}.csv')
    venda_df = pd.DataFrame(venda_aberta)
    venda_df


def pagina_principal():
    st.title('**BOX Comodoro**')

    btn = authenticator.logout()
    if btn:
        st.session_state["authentication_status"] == None
    
    tab1,tab2,tab3 = st.tabs(['Estoque', 'Vendas','Histórico de Vendas'])

    tab1.title('Estoque')
    
    with tab1:
        inserindo_dados()
        estoque = st.session_state['estoque']
        st.dataframe(estoque.set_index('Código'))
        
    tab2.title('Vendas')

    with tab2:
        dados_vendas()
        df3 = st.session_state['data3']
        df3.to_excel('files/venda.xlsx')
        valor_vendas = st.session_state['valor_vendas']
        col1,col2,col3,col4,col5 = st.columns(5)
        soma = df3['valor_venda'].sum()
        col1.metric('Valor Total', f'R$ {soma:.2f}')
        venda = col2.button('Fechar venda')

        data = datetime.datetime.now()
        sell = [data.year,data.month,data.day,soma]
        if venda:
            csv = df3.to_csv(f'files/historico_vendas/venda+{data.day}+{data.month}+{data.year}+{data.hour}+{data.minute}+{data.second}.csv')
            df3 = pd.read_excel('files/nova_venda.xlsx')
            st.session_state['data3'] = df3
            df3 = st.session_state['data3']
            df3 = df3.set_index('codigo_produto')
            df3.to_excel('files/venda.xlsx')
            st.session_state['data3'] = df3
            df3 = st.session_state['data3']
            
            valor_vendas.loc[len(valor_vendas)]= sell

        valor_vendas = valor_vendas.set_index('Ano')
        st.session_state['valor_vendas'] = valor_vendas
        valor_vendas = st.session_state['valor_vendas']
        valor_vendas.to_excel('files/valor_vendas.xlsx')
                       
        st.dataframe(df3)
        
        

    tab3.title('Histórico de vendas')
    with tab3:
        visualiza_vendas()
        

def main():
    if st.session_state["authentication_status"]:
    
        df = pd.read_excel('files/estoque.xlsx')
        st.session_state['data'] = df
        df = st.session_state['data']
        df3 = pd.read_excel('files/venda.xlsx')
        st.session_state['data3'] = df3
        df3 = st.session_state['data3']
        valor_vendas = pd.read_excel('files/valor_vendas.xlsx')
        st.session_state['valor_vendas'] = valor_vendas
        valor_vendas = st.session_state['valor_vendas']
        
        pagina_principal()
  
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect.")

    elif st.session_state["authentication_status"] == None:
        st.warning("Please insert username and password")

vendas = pd.DataFrame(columns = ['Ano','mes','Dia','valor'])
st.session_state['vendas'] = vendas
vendas = st.session_state['vendas']

if __name__ == '__main__':
    main()

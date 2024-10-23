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
import certifi
from db.getUsersInfo import login as db_login
from db.insertSale import register_sale

from datetime import datetime, timedelta, timezone
import pytz

mongo_user = st.secrets['MONGO_USER']
mongo_pass = st.secrets["MONGO_PASS"]

username = urllib.parse.quote_plus(mongo_user)
password = urllib.parse.quote_plus(mongo_pass)

ca = certifi.where()
client = MongoClient("mongodb+srv://%s:%s@cluster0.gjkin5a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" % (username, password), tlsCAFile=ca)
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
    nome = col1.text_input('Nome do Produto')
    codigo = col2.number_input('Código do Produto', min_value = 0, max_value = 100000)
    quantidade = col3.number_input('Quant.', min_value = 0, max_value = 100000)
    #descricao = col3.text_input('Descrição do produto')
    valor_compra = col4.number_input('Valor de Compra em R$')
    valor_venda = col5.number_input('Valor de venda em R$')
    adiciona_produto = col5.button('Adicionar')
    if adiciona_produto:
        entry = [{'Nome': nome,'Código' : codigo, 'Quantidade' : quantidade, 'Valor de compra' : valor_compra, 'Valor de venda' : valor_venda}]
        result = coll.insert_many(entry)
    
    estoque1 = db.estoque.find({})

    estoquedf = []
    for item in estoque1:
        estoquedf.append(item)

    df = pd.DataFrame(estoquedf, columns= ['_id', 'Nome', 'Código','Quantidade', 'Valor de compra', 'Valor de venda'])
    df.drop(columns='_id', inplace=True)
    estoque = df
    st.session_state['estoque'] = estoque

def historico_vendas():

    venda1 = db.Vendas.find({})

    fuso_horario_brasilia = pytz.timezone("America/Sao_Paulo")

    vendadf = []
    for item in venda1:
        # Ajustar o horário armazenado em UTC para o horário de Brasília
        if 'Data da venda' in item:
            data_utc = item['Data da venda']
            if isinstance(data_utc, datetime):
                data_brasilia = data_utc.astimezone(fuso_horario_brasilia)
                item['Data da venda'] = data_brasilia.strftime('%d/%m/%Y %H:%M')

        vendadf.append(item)

    df = pd.DataFrame(vendadf, columns= ['_id', 'Nome', 'Código','Quantidade', 'Valor de venda', 'Data da venda'])
    df.drop(columns='_id', inplace=True)
    historico_venda = df
    st.session_state['historico_venda'] = historico_venda


def efetuando_vendas():

    opcoes_dropdown = ['']
    produto_dict = {}

    st.markdown(
        """
        <style>
        .custom-button {
            margin-top: 28px;
            margin-left: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    todos_produtos = db.estoque.find({})

    for item in todos_produtos:

        nome_dict = item.get('Nome')
        codigo_dict = item.get('Código')

        opcoes_dropdown.append(nome_dict)

        produto_dict[nome_dict] = codigo_dict



    col1,col2,col3,col4, col5,col6,col7 = st.columns(7)
    quantidade = col3.number_input('Quant.', min_value = 0, max_value = 100000, key="input_quantidade_venda")

    valor_venda = col4.number_input('Valor de venda em R$', key="input_valor_venda" )

    with col1:
        nome = st.selectbox('Escolha uma opção:', opcoes_dropdown, key='input_nome_venda')

    codigo_inicial = produto_dict.get(nome, 0)
    
    with col2:
        codigo = st.number_input('Código do Produto', min_value=0, max_value=100000, key="input_codigo_venda", value=codigo_inicial, disabled=True)
                
    with col5:
        cliente = st.text_input('Nome do cliente')
    pagamento = ['Pix', 'Cartão de crédito', 'Cartão de débito', 'Dinheiro', 'Desconto em folha']
    with col6:
        forma_pagamento = st.selectbox('Forma de pagamento', pagamento)

    with col7:
        st.markdown('<div class="custom-button">', unsafe_allow_html=True)
        vende_produto = st.button('Concluir Venda', key="a")
        st.markdown('</div>', unsafe_allow_html=True)

    if vende_produto:
        register_sale(nome, quantidade, valor_venda)
    
    venda1 = db.estoque.find({})

    vendadf = []
    for item in venda1:
        vendadf.append(item)

    df = pd.DataFrame(vendadf, columns= ['_id', 'Nome', 'Código','Quantidade', 'Valor de compra', 'Valor de venda','Cliente', 'Forma de pagamento'])
    df.drop(columns='_id', inplace=True)
    venda = df
    st.session_state['venda'] = venda

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
        efetuando_vendas()
        venda = st.session_state['venda']
        st.dataframe(venda.set_index('Código'))
                     
        
    tab3.title('Histórico de vendas')
    
    with tab3:
        historico_vendas()
        historico_venda = st.session_state['historico_venda']
        st.dataframe(historico_venda.set_index('Código'))

        

def main():
    if st.session_state["authentication_status"]:
    
        pagina_principal()
  
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect.")

    elif st.session_state["authentication_status"] == None:
        st.warning("Please insert username and password")


if __name__ == '__main__':

    main()

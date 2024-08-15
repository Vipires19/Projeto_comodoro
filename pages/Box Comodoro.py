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
    codigo = col1.number_input('Código do Produto', min_value = 0, max_value = 100000)
    quantidade = col2.number_input('Quant.', min_value = 0, max_value = 100000)
    descricao = col3.text_input('Descrição do produto')
    valor_compra = col4.number_input('Valor de Compra em R$')
    valor_venda = col5.number_input('Valor de venda em R$')
    adiciona_produto = col5.button('Adicionar')
    if adiciona_produto:
        entry = [{'Código' : codigo, 'Quantidade' : quantidade, 'Descrição' : descricao, 'Valor de compra' : valor_compra, 'Valor de venda' : valor_venda}]
        result = coll.insert_many(entry)
    
    estoque1 = db.estoque.find({})

    estoquedf = []
    for item in estoque1:
        estoquedf.append(item)

    df = pd.DataFrame(estoquedf, columns= ['_id', 'Código','Descrição','Quantidade', 'Valor de compra', 'Valor de venda'])
    df.drop(columns='_id', inplace=True)
    estoque = df
    st.session_state['estoque'] = estoque

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
        pass                       
        
    tab3.title('Histórico de vendas')
    
    with tab3:
        pass
        

def main():
    if st.session_state["authentication_status"]:
    
        pagina_principal()
  
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect.")

    elif st.session_state["authentication_status"] == None:
        st.warning("Please insert username and password")

if __name__ == '__main__':
    main()

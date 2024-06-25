import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
from openpyxl import load_workbook
import datetime

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
    df = st.session_state['data']
    
    col1,col2,col3,col4,col5 = st.columns(5)

    codigo = col1.number_input('Código do Produto', min_value = 0, max_value = 100000)
    quantidade = col2.number_input('Quant.', min_value = 0, max_value = 100000)
    descricao = col3.text_input('Descrição do produto')
    valor_compra = col4.number_input('Valor de Compra em R$')
    valor_venda = col5.number_input('Valor de venda em R$')
    adiciona_produto = col5.button('Adicionar')

    novo_produto = [codigo,quantidade,descricao,valor_compra,valor_venda]
    if adiciona_produto:
        df.loc[len(df)]= novo_produto

    df2 = df.set_index('codigo')
    st.session_state['data2'] = df2
    df2 = st.session_state['data2']

def dados_vendas():
    df2 = st.session_state['data2']
    df3 = st.session_state['data3']
    
    col1,col2,col3,col4,col5,col6 = st.columns(6)
    cod = col1.number_input('Código do produto:', min_value = 1, max_value = 100000 )
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
        
def pagina_principal():
    st.title('**BOX Comodoro**')

    btn = authenticator.logout()
    if btn:
        st.session_state["authentication_status"] == None
    
    tab1,tab2,tab3 = st.tabs(['Estoque', 'Vendas','Histórico de Vendas'])

    tab1.title('Estoque')
    
    with tab1:
        inserindo_dados()
        df = st.session_state['data']
        df2 = st.session_state['data2']
        df2.to_excel('files/estoque.xlsx')

        st.dataframe(df.set_index('codigo'))
        
    tab2.title('Vendas')

    with tab2:
        dados_vendas()
        df3 = st.session_state['data3']
        df3.to_excel('files/venda.xlsx')
        
        col1,col2,col3,col4,col5 = st.columns(5)
        soma = df3['valor_venda'].sum()
        col1.metric('Valor Total', f'R$ {soma:.2f}')
        venda = col2.button('Fechar venda')
        if venda:
            data = datetime.datetime.now()
            csv = df3.to_csv(f'files/historico_vendas/venda+{data.day}+{data.month}+{data.year}+{data.hour}+{data.minute}+{data.second}.csv')
            df3 = pd.read_excel('files/nova_venda.xlsx')
            st.session_state['data3'] = df3
            df3 = st.session_state['data3']
            df3 = df3.set_index('codigo_produto')
            df3.to_excel('files/venda.xlsx')
            st.session_state['data3'] = df3
            df3 = st.session_state['data3']
            
        st.dataframe(df3)

    tab3.title('Histórico de vendas')
    with tab3:
       pass
    
def main():
    if st.session_state["authentication_status"]:
    
        df = pd.read_excel('files/estoque.xlsx')
        st.session_state['data'] = df
        df = st.session_state['data']
        df3 = pd.read_excel('files/venda.xlsx')
        st.session_state['data3'] = df3
        df3 = st.session_state['data3']
        
        pagina_principal()
  
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect.")

    elif st.session_state["authentication_status"] == None:
        st.warning("Please insert username and password")

if __name__ == '__main__':
    main()
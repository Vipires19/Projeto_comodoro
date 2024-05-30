import streamlit as st

df = st.session_state['data']

st.markdown('# Filtro Criminal')
st.divider()

crimes = df['Crime'].value_counts().index
crime = st.sidebar.selectbox('Crime', crimes)
df_crime = df[df['Crime'] == crime]
tipos = df_crime['Tipo do veículo'].value_counts().index
tipo = st.sidebar.selectbox('Tipo do veículo', tipos)
df_tipo = df_crime[df_crime['Tipo do veículo'] == tipo]
locs = df_tipo['Localizado?'].value_counts().index
loc = st.sidebar.selectbox('Localizado?', locs)
df_loc = df_tipo[df_tipo['Localizado?'] == loc]

col1,col2,col3 = st.columns(3)
weeks = df_loc['Dia da semana'].value_counts().index
week = col1.selectbox('Dia da semana', weeks)
df_week = df_loc[df_loc['Dia da semana'] == week]
periodos = df_week['Período'].value_counts().index
periodo = col2.selectbox('Dia da semana', periodos)
df_peri = df_week[df_week['Período'] == periodo]
cias = df_peri['CIA PM'].value_counts().index
cia = col3.selectbox('Cia PM', cias)
df_cia = df_peri[df_peri['CIA PM'] == cia]

dfcol = ['Dia','Hora','Período', 'Crime','Tipo do veículo','Marca','Modelo', 'Placa','Ano','Endereço','Bairro','Subsetor','Localizado?','Data da Recuperação', 'Bairro da recuperação', 'Ambiente']
st.dataframe(df_cia[dfcol],
             column_config= {'Data da Recuperação' : st.column_config.DateColumn()})

ocr = df_cia['Endereço'].value_counts().index
ocrs = st.selectbox('Endereço da ocorrência', ocr)
df_ocr = df_cia[df_cia['Endereço'] == ocrs]
st.markdown(f'**Bairro**: {list(df_ocr["Bairro"])[0]}')
sector = list(df_ocr['Subsetor'])[0].split('.')[-1]
st.markdown(f'**Setor**: {sector}')
car = list(df_ocr['Modelo'])
mar = list(df_ocr['Marca'])
tipe = list(df_ocr['Tipo do veículo'])
placa = list(df_ocr['Placa'])
car_num = placa[0].split(placa[0][2])[1]
car_let = placa[0].split(placa[0][3])[0]
placa = car_let + '-' + car_num
year = list(df_ocr['Ano'])
vit = list(df_ocr['Vítima'])
locd = list(df_ocr['Localizado?'])
recu = list(df_ocr['Bairro da recuperação'])
data_rec = list(df_ocr['Data da Recuperação'])[0].date()
fla = list(df_ocr['Flagrante?'])[0]
ladrao = list(df_ocr['N° de agressores'])[0]
se = list(df_ocr['Sexo dos agressores'])[0]
clad = list(df_ocr['Cor'])[0]
gun = list(df_ocr['Arma utilizada'])[0]
trans = list(df_ocr['Transporte utilizado'])[0]
cvu = list(df_ocr['Cor do veículo utilizado'])[0]
dataocr = list(df_ocr['Dia'])[0]
mesocr = list(df_ocr.index.value_counts().index)[0]

st.markdown(f'**Dia do fato**: {dataocr}')
st.markdown(f'**Mes**: {mesocr}')
st.header('**Veículo levado**:')
col1,col2,col3 = st.columns(3)
col1.markdown(f'**Modelo**: {car[0].split(" ")[1]}')
col1.markdown(f'**Marca**: {mar[0]}')
col1.markdown(f'**Placa**: {placa}')
col2.markdown(f'**Tipo**: {tipe[0]}')
col2.markdown(f'**Ano do Veículo**: {year[0]}')
col2.markdown(f'**Vítima**: {vit[0]}')
col3.markdown(f'**Localizado?**: {locd[0]}')
col3.markdown(f'**Bairro onde foi localizado**: {recu[0]}')
col3.markdown(f'**Data em que foi localizado**: {data_rec}')
col2.divider()
col2.markdown(f'**Flagrante?**: {fla}')
col2.markdown(f'**N° de agressores**: {ladrao}')
col2.markdown(f'**Sexo dos agressores**: {se}')
col2.markdown(f'**Cor**: {clad}')
col3.divider()
col3.markdown(f'**Arma utilizada**: {gun}')
col3.markdown(f'**Transporte utilizado**: {trans}')
col3.markdown(f'**Cor do veículo utilizado**: {cvu}')
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import geopandas as gpd
import joblib

# Carragando o modelo

model = joblib.load('model/model.pkl')

# Carregando os dados

df = pd.read_csv('data/acidentes.txt')


st.title('Previsões')

st.write("Aqui você pode simular acidentes de trânsito e ver a previsão da classificação do acidente,"
         " Mostrando a probabilidade do acidente ser com vitimas ilesas, com vitimas feridas e com vitimas fatais")



df.loc[df['causa_acidente'] == 'Ausência de reação do condutor', 'causa_acidente'] = 'Reação tardia ou ineficiente do condutor'
df.loc[df['causa_acidente'] == 'Ingestão de álcool pelo condutor', 'causa_acidente'] = 'Ingestão de Álcool'
df.loc[df['causa_acidente'] == 'Demais falhas mecânicas ou elétricas', 'causa_acidente'] = 'Defeito Mecânico no Veículo'

causa_acidentes = df['causa_acidente'].unique()
tipos_acidentes = df['tipo_acidente'].unique()


tipo_veiculos = ['Automóvel', 'Motocicleta', 'Caminhão', 'Camioneta/Caminhonete',
       'Bicicleta', 'Ônibus', 'Ciclomotor', 'Reboque', 'Pedestre',
        'Trator'] 

regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
regiao = st.selectbox('Região', regioes)

maiores_br = df['br'].value_counts()[df['br'].value_counts() > 1000].index

df = df[df['br'].isin(maiores_br)]

brs = df['br'].unique()
brs_filtradas = df[df['regiao'] == regiao]['br'].unique()
br = st.selectbox('BR', brs_filtradas)

tipo_acidente = st.selectbox('Tipo de Acidente', tipos_acidentes)

causa_acidente = st.selectbox('Causa do Acidente', causa_acidentes)

uso_solo = st.selectbox('Urbano ou Rural', ['Urbano', 'Rural'])

tipo_veiculo = st.selectbox('Tipo de Veículo', tipo_veiculos)

hora = st.selectbox('Hora', range(24))

input_data = pd.DataFrame({
    'regiao': [regiao],
    'tipo_acidente': [tipo_acidente],
    'causa_acidente': [causa_acidente],
    'uso_solo': [uso_solo],
    'br': [br],
    'tipo_veiculo': [tipo_veiculo],
    'hora': [hora]
})

label_to_class = {
    0: 'Com Vítimas Fatais',
    1: 'Com Vítimas Feridas',
    2: 'Sem Vítimas'
}

if st.button('Fazer Previsão'):
    probabilidades = model.predict_proba(input_data)

    # Exibir as probabilidades para cada classe
    for i, prob in enumerate(probabilidades[0]):
        st.write(f"Probabilidade do acidente ser considerado {label_to_class[i]}: {prob * 100:.2f}%")


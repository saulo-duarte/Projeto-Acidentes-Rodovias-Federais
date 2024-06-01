from scipy.stats import chi2_contingency
import numpy as np
import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import pymannkendall as mk

st.logo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRo-jThbvam4VNl--sYlWeTE89wKpfWQE2NRQ&s")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-image: url('https://img.freepik.com/premium-photo/dark-blue-navy-color-vivid-gradient-background_1077288-1946.jpg');
        background-size: cover;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        color: yellow;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def carregar_dados():
    df1 = pd.read_csv("Dados_prf_simplificado_parte1.txt", low_memory=False)
    df2 = pd.read_csv("Dados_prf_simplificado_parte2.txt", low_memory=False)
    df = pd.concat([df1, df2], ignore_index=True)
    return df


df = carregar_dados()

df = df[['id', 'data_inversa']]
df['data_inversa'] = pd.to_datetime(df['data_inversa'])

# criando a coluna de ano

df['ano'] = df['data_inversa'].dt.year

# Fazendo a contagem de acidentes por dia

df = df.groupby('ano').size().reset_index(name='acidentes')

# Fazendo teste de hipótese para verificar se a o aumento de acidentes é significativo

# Criando uma tabela de contingência

contingency_table = pd.crosstab(df['ano'], df['acidentes'])

# Teste de hipótese

chi2, p, dof, expected = chi2_contingency(contingency_table)

# Verificando se a hipótese nula é rejeitada

if p < 0.05:
    st.write(f"A hipótese nula é rejeitada. O aumento de acidentes é significativo| {p}")
else:
    st.write(f"A hipótese nula não é rejeitada. O aumento de acidentes não é significativo|{p}")

# Teste de tendência de Mann-Kendall

result = mk.original_test(df['acidentes'])

if result.slope > 0:
    st.write("Há uma tendência de aumento de acidentes")
else:
    st.write("Não há uma tendência de aumento de acidentes")

nomes = ['Tendência','Presença de tendência','p-valor','Estatística do teste','Tau Kendall','Pontuação Kendall','Variância S','Declive','Intercepto']
for i,j in zip(nomes,result): 
    st.write(i,":",j)
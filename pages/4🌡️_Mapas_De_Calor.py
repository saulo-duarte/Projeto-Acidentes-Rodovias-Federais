import os

import duckdb
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    DB_USER = st.secrets.db_credentials.POSTGRES_USER
    DB_PASSWORD = st.secrets.db_credentials.POSTGRES_PASSWORD
    DB_HOST = st.secrets.db_credentials.POSTGRES_HOST
    DB_PORT = st.secrets.db_credentials.POSTGRES_PORT
    DB_NAME = st.secrets.db_credentials.POSTGRES_DB 

    connection_str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(connection_str)

    query_acidentes = """
    SELECT * 
    FROM relational.acidentes
    INNER JOIN relational.envolvidos
    ON acidentes.id = envolvidos.id_acidente
    """

    df_acidentes = pd.read_sql(query_acidentes, con=engine)
    return df_acidentes

df = load_data()

st.markdown("""
    <style>
        .custom-title {
            font-family: 'Segoe UI Bold', Tahoma, Geneva, Verdana, sans-serif;
            margin-left: 20px;
            text-align: center;
        }
    </style>
    <div style='display: flex; align-items: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Prf_brasao_novo.jpg/738px-Prf_brasao_novo.jpg' width='100'>
        <h1 class='custom-title'>Mapas de Calor - Acidentes em Rodovias Federais</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown("----")


df = load_data()

df_filtrado = df.copy()
conn = duckdb.connect()
conn.register('df_filtrado', df_filtrado)

total_acidentes = df_filtrado["id"].nunique()

if total_acidentes > 1000:
    total_acidentes = '{:,.3f} K'.format(total_acidentes / 1000)

query_acidentes_com_vitimas = """
    SELECT 
        COUNT(DISTINCT id) AS Acidente_com_vitimas
        FROM df_filtrado
        WHERE mortos > 1;"""

result_cartao1 = conn.execute(query_acidentes_com_vitimas).fetchone()

if result_cartao1:
    total_acidentes_com_vitimas = result_cartao1[0]
    
    if total_acidentes_com_vitimas > 1000:
        total_acidentes_com_vitimas = '{:,.3f} K'.format(total_acidentes_com_vitimas / 1000)


total_envolvidos =  df_filtrado[["mortos", "feridos_leves", "feridos_graves", "ilesos"]].sum().sum()

if total_envolvidos > 1000000:
    total_envolvidos = '{:,.3f} MI'.format(total_envolvidos / 1000000)

elif total_envolvidos > 1000:
        total_envolvidos = '{:,.3f} K'.format(total_envolvidos / 1000)

total_feridos = df_filtrado[["feridos_leves", "feridos_graves"]].sum().sum()

if total_feridos > 1000:
        total_feridos = '{:,.3f} K'.format(total_feridos / 1000)

total_mortos = df_filtrado['mortos'].sum()

if total_mortos > 1000:
     total_mortos = '{:,.3f} K'.format(total_mortos / 1000)

square_style = """
    padding: 20px;
    border: 6px solid #ff5900;
    border-radius: 50px; 
    background-color: #8B0000;
    width: fit-content;
    margin: auto;
"""

st.markdown(f'<div style="{square_style}"> \
             <div style="display: inline-block; text-align: center; height: 100%; vertical-align: top;"> \
             <div style="border: 3.5px solid #ff2436; border-radius: 15px; padding: 15px; background-color: #fc4c00; height: 100%;"> \
             <h3 style="color:yellow; font-family: Segoe UI Semibold; font-size: 25px;">Total Acidentes</h3> \
             <h2 style="color:white; margin: 5px 0; font-size: 28px">{total_acidentes}</h2> \
             </div> \
             </div> \
             <div style="display: inline-block; text-align: center; height: 100%; vertical-align: top;"> \
             <div style="border: 3.5px solid #ff2436; border-radius: 15px; padding: 15px; background-color: #fc4c00; height: 100%;"> \
             <h3 style="color:yellow; font-family: Segoe UI Semibold; font-size: 25px;">Acidentes c/ Vítimas</h3> \
             <h2 style="color:white; margin: 5px 0; font-size: 28px">{total_acidentes_com_vitimas}</h2> \
             </div> \
             </div> \
             <div style="display: inline-block; text-align: center; height: 100%; vertical-align: top;"> \
             <div style="border: 3.5px solid #ff2436; border-radius: 15px; padding: 15px; background-color: #fc4c00; height: 100%;"> \
             <h3 style="color:yellow; font-family: Segoe UI Semibold; font-size: 25px;">Total Envolvidos</h3> \
             <h2 style="color:white; margin: 5px 0; font-size: 28px">{total_envolvidos}</h2> \
             </div> \
             </div> \
             <div style="display: inline-block; text-align: center; height: 100%; vertical-align: top;"> \
             <div style="border: 3.5px solid #ff2436; border-radius: 15px; padding: 15px; background-color: #fc4c00; height: 100%;"> \
             <h3 style="color:yellow; font-family: Segoe UI Semibold; font-size: 25px;">Total Feridos</h3> \
             <h2 style="color:white; margin: 5px 0; font-size: 28px">{total_feridos}</h2> \
             </div> \
             </div> \
             <div style="display: inline-block; text-align: center; height: 100%; vertical-align: top;"> \
             <div style="border: 3.5px solid #ff2436; border-radius: 15px; padding: 15px; background-color: #fc4c00; height: 100%;"> \
             <h3 style="color:yellow; font-family: Segoe UI Semibold; font-size: 25px;"> Total Óbitos</h3> \
             <h2 style="color:white; margin: 5px 0; font-size: 28px">{total_mortos}</h2> \
             </div>', unsafe_allow_html=True)
st.markdown("----")
# ----- Gráfico 1 com rodovias


col1, col2 = st.columns(2)
with col1:
    st.image("pic/densidade_acidentes.png", use_column_width=True)
with col2:
    with open('pic/grafico_densidade_acidentes.html', 'r') as file:
        html_content = file.read()
    st.components.v1.html(html_content, height=800)

st.markdown("## Acidentes Com Mortos")
st.markdown("------")

col3, col4 = st.columns(2)
with col3:
    st.image("pic/densidade_acidentes_com_mortos.png", use_column_width=True)
with col4:
    with open('pic/grafico_densidade_acidentes_com_mortos.html', 'r') as file:
        html_content = file.read()
    st.components.v1.html(html_content, height=800)


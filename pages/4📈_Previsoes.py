import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

@st.cache_data
def carregar_dados():
    df1 = pd.read_csv("Dados_prf_simplificado_parte1.txt", low_memory=False)
    df2 = pd.read_csv("Dados_prf_simplificado_parte2.txt", low_memory=False)
    df = pd.concat([df1, df2], ignore_index=True)
    return df

df = carregar_dados()

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
        <h1 class='custom-title'>Acidentes em Rodovias Federais</h1>
    </div>
""", unsafe_allow_html=True)

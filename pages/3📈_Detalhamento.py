from scipy.stats import chi2_contingency
import numpy as np
import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

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
def load_data():
    DB_USER = st.secrets.db_credentials.POSTGRES_USER
    DB_PASSWORD = st.secrets.db_credentials.POSTGRES_PASSWORD
    DB_HOST = st.secrets.db_credentials.POSTGRES_HOST
    DB_PORT = st.secrets.db_credentials.POSTGRES_PORT
    DB_NAME = st.secrets.db_credentials.POSTGRES_DB 

    connection_str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(connection_str)

    query_acidentes = """
    SELECT * FROM relational.acidentes
    INNER JOIN relational.envolvidos
    ON acidentes.id = envolvidos.id_acidente;
    """

    df_acidentes = pd.read_sql(query_acidentes, con=engine)
    return df_acidentes

df = load_data()


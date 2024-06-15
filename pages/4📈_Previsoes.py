import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import geopandas as gpd

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


df = carregar_dados()

geojson = gpd.read_file("brazil_geo.json")

accidents_per_state = df.groupby('uf').size().reset_index(name='num_accidents')

# Realizar o merge dos dados de acidentes com o GeoDataFrame
merged_data = geojson.merge(accidents_per_state, how='left', left_on='id', right_on='uf')

fig = px.choropleth(
    merged_data,
    geojson=merged_data.set_geometry('geometry'),
    locations=merged_data.index,
    color='num_accidents',
    color_continuous_scale='Darkmint',
    labels={'num_accidents': 'Número de Acidentes'},
    hover_name='name',
    hover_data={'num_accidents': True},
)

fig.update_geos(fitbounds='locations', visible=False, projection_type='orthographic')

st.title("Mapa de Acidentes no Brasil")

st.plotly_chart(fig, use_container_width=True)


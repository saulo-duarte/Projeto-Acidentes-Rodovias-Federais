import os

import duckdb
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
from sklearn.neighbors import KDTree

st.set_page_config(layout="wide")

@st.cache_data
def carregar_dados():
    df1 = pd.read_csv("Dados_prf_simplificado_parte1.txt", low_memory=False)
    df2 = pd.read_csv("Dados_prf_simplificado_parte2.txt", low_memory=False)
    df = pd.concat([df1, df2], ignore_index=True)
    return df

@st.cache_data
def carregar_mapa():
    os.environ['SHAPE_RESTORE_SHX'] = 'YES'
    file_path = "rodo_snv.shp"
    rodovias = gpd.read_file(file_path)
    return rodovias


st.markdown("""
    <style>
        body {
            zoom: 0.8;
        }
    </style>
""", unsafe_allow_html=True)


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


df = carregar_dados()
rodovias = carregar_mapa()

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

raio_pesquisa_km1 = 5

grid_size1 = 0.02
df['lat_grid1'] = np.floor(df['latitude'] / grid_size1) * grid_size1
df['lon_grid1'] = np.floor(df['longitude'] / grid_size1) * grid_size1

unique_cells1 = df[['lat_grid1', 'lon_grid1']].drop_duplicates().values

densidade_acidentes1 = np.zeros(len(unique_cells1))
tree1 = KDTree(unique_cells1, leaf_size=10)

for i, cell in enumerate(unique_cells1):
    vizinhos = tree1.query_radius([cell], r=raio_pesquisa_km1)
    densidade_acidentes1[i] = len(vizinhos[0])

densidades_dict1 = {tuple(cell): densidade for cell, densidade in zip(unique_cells1, densidade_acidentes1)}
df['densidade_acidentes1'] = df[['lat_grid1', 'lon_grid1']].apply(lambda row: densidades_dict1[tuple(row)], axis=1)

plot_colors1 = [(0, "white"), 
               (0.2, "#c4bb00"),  
               (0.4, "#ff8000"),   
               (0.6, "#ff5100"),  
               (0.8, "#ff2a00"),
               (1, "#4a0000")  
              ]
cmap1 = LinearSegmentedColormap.from_list("custom", plot_colors1)

grafico1 = plt.figure(figsize=(10, 8))
map = Basemap(llcrnrlon=-75, llcrnrlat=-35, urcrnrlon=-25, urcrnrlat=5, resolution='i', projection='merc')
map.drawcoastlines()
map.drawcountries()

for geometry in rodovias['geometry']:
    lon, lat = zip(*geometry.coords)
    x, y = map(lon, lat)
    map.plot(x, y, marker=None, color='navy', linewidth=1)

x, y = map(df['longitude'].values, df['latitude'].values)
sc = map.scatter(x, y, s=30, c=df['densidade_acidentes1'], cmap=cmap1, alpha=0.7, edgecolors='none',
                 vmin=0, vmax=np.percentile(df['densidade_acidentes1'], 98))

cbar = plt.colorbar(sc, orientation='vertical')
plt.title('Acidentes em Rodovias Brasileiras')

# ---------------- Gráfico 2

raio_pesquisa_km2 = 0.03

tree2 = KDTree(df[['latitude', 'longitude']].values)

vizinhos_proximos2 = tree2.query_radius(df[['latitude', 'longitude']].values, r=raio_pesquisa_km2)

densidade_acidentes2 = [len(x) for x in vizinhos_proximos2]

df['densidade_acidentes_2'] = densidade_acidentes2
grafico2 = go.Figure(go.Densitymapbox(
    lat=df['latitude'], 
    lon=df['longitude'], 
    z=df['densidade_acidentes_2'],  
    radius=10,
    colorscale="YlOrRd",
    zmin=0,
    zmax=np.percentile(df['densidade_acidentes1'], 98)
))
grafico2.update_layout(
    mapbox_style="carto-positron",
    mapbox_center={"lat": -15, "lon": -55},
    mapbox_zoom=3,
    title={
        'text': "Utilize zoom para mais precisão",
        'font': {'size': 20}
    },
    margin={"r":50,"t":50,"l":50,"b":50},
    width=700,  
    height=650,
    title_x=0.4,  
)
# ----------------- Estrutura Parte 1
col1 , col2 = st.columns(2)
with col1:
     st.pyplot(grafico1, use_container_width=True)
with col2:
     st.plotly_chart(grafico2, use_container_width=True)

st.markdown("## Acidentes Com Mortos")
st.markdown("------")

# ------------------- Gráfico 3

raio_pesquisa_km3 = 5

grid_size3 = 0.02 
df['lat_grid3'] = np.floor(df['latitude'] / grid_size3) * grid_size3
df['lon_grid3'] = np.floor(df['longitude'] / grid_size3) * grid_size3

df_filtered3 = df[df['mortos'] >= 1]

unique_cells3 = df_filtered3[['lat_grid3', 'lon_grid3']].drop_duplicates().values

densidade_acidentes3 = np.zeros(len(unique_cells3))
tree3 = KDTree(unique_cells3, leaf_size=10)

for i, cell in enumerate(unique_cells3):
    vizinhos = tree3.query_radius([cell], r=raio_pesquisa_km3)
    densidade_acidentes3[i] = len(vizinhos[0])

densidades_dict3 = {tuple(cell): densidade for cell, densidade in zip(unique_cells3, densidade_acidentes3)}
df_filtered3['densidade_acidentes'] = df_filtered3[['lat_grid3', 'lon_grid3']].apply(lambda row: densidades_dict3[tuple(row)], axis=1)

plot_colors = [(0, "white"), 
               (0.2, "#c4bb00"),  
               (0.4, "#ff8000"),   
               (0.6, "#ff5100"),  
               (0.8, "#ff2a00"),
               (1, "#4a0000")  
              ]
cmap = LinearSegmentedColormap.from_list("custom", plot_colors)

grafico3 = plt.figure(figsize=(10, 8))
map = Basemap(llcrnrlon=-75, llcrnrlat=-35, urcrnrlon=-25, urcrnrlat=5, resolution='i', projection='merc')
map.drawcoastlines()
map.drawcountries()

for geometry in rodovias['geometry']:
    lon, lat = zip(*geometry.coords)
    x, y = map(lon, lat)
    map.plot(x, y, marker=None, color='navy', linewidth=1)

x, y = map(df_filtered3['longitude'].values, df_filtered3['latitude'].values)
sc = map.scatter(x, y, s=30, c=df_filtered3['densidade_acidentes'], cmap=cmap, alpha=0.7, edgecolors='none',
                 vmin=0, vmax=np.percentile(df_filtered3['densidade_acidentes'], 98))

cbar = plt.colorbar(sc, orientation='vertical')
plt.title('Acidentes Com Mortes em Rodovias Brasileiras')

# --------------- Gráfico 4
raio_pesquisa_km4 = 0.8

df_filtered4 = df[df['mortos'] >= 1]

tree4 = KDTree(df_filtered4[['latitude', 'longitude']].values)

vizinhos_proximos4 = tree4.query_radius(df_filtered4[['latitude', 'longitude']].values, r=raio_pesquisa_km4)  # Corrigido para usar raio_pesquisa_km4

densidade_acidentes4 = [len(x) for x in vizinhos_proximos4]

df_filtered4['densidade_acidentes_4'] = densidade_acidentes4

grafico4 = go.Figure(go.Densitymapbox(
    lat=df_filtered4['latitude'], 
    lon=df_filtered4['longitude'], 
    z=df_filtered4['densidade_acidentes_4'], 
    radius=10,
    colorscale="YlOrRd",
    zmin=0,
    zmax=np.percentile(df_filtered3['densidade_acidentes'], 98) 
    ))

grafico4.update_layout(
    mapbox_style="carto-positron",
    mapbox_center={"lat": -15, "lon": -55},
    mapbox_zoom=3,
    title="Utilize zoom para mais precisão",
    margin={"r":50,"t":50,"l":50,"b":50},
    width=700,  
    height=650,
    title_x=0.4,  
)

col3, col4 = st.columns(2)

with col3:
    st.pyplot(grafico3, use_container_width=True)
with col4:
     st.plotly_chart(grafico4, use_container_width=True)

import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout="wide")

@st.cache_data
def carregar_dados():
    df1 = pd.read_csv("Dados_prf_simplificado_parte1.txt", low_memory=False)
    df2 = pd.read_csv("Dados_prf_simplificado_parte2.txt", low_memory=False)
    df = pd.concat([df1, df2], ignore_index=True)
    return df

@st.cache_data
def carregar_dados2():
    df1 = pd.read_csv("Dados_sexo_parte1.txt", low_memory=False)
    df2 = pd.read_csv("Dados_sexo_parte2.txt", low_memory=False)
    df = pd.concat([df1, df2], ignore_index=True)
    return df

df = carregar_dados()

df_sexo = carregar_dados2()

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
        <h1 class='custom-title'>Óbitos em Rodovias Federais</h1>
    </div>
""", unsafe_allow_html=True)
# ----------------------  Filtros
st.markdown("----")
st.sidebar.markdown("# Filtros - 1")

df_filtrado = df.copy()
municipio_selecionado = []

estado_selecionado = st.sidebar.multiselect("Selecione os estados", df["uf"].unique())

regiao_selecionada = st.sidebar.multiselect("Selecione as regiões", df["regiao"].unique())

br_selecionada = st.sidebar.multiselect("Selecione as rodovias", df["br"].unique())

tipo_veiculo_selecionado = st.sidebar.multiselect("Selecione o tipo de veículo", df['tipo_veiculo'].unique())

condicao_tempo_selecionado = st.sidebar.multiselect("Selecione a condição meteorológica", df['condicao_metereologica'].unique())

fase_dia_selecionado = st.sidebar.multiselect("Selecione a fase do dia", df['fase_dia'].unique())

if regiao_selecionada:
    estados_regiao_selecionada = df[df["regiao"].isin(regiao_selecionada)]["uf"].unique()
    estado_selecionado.extend(estados_regiao_selecionada)
    estado_selecionado = list(set(estado_selecionado))

    municipios_disponiveis = df[df["uf"].isin(estado_selecionado)]["municipio"].unique()
    municipio_selecionado = st.sidebar.multiselect("Selecione o(s) Município(s)", municipios_disponiveis)


if estado_selecionado and not regiao_selecionada: 
    municipios_disponiveis = df[df["uf"].isin(estado_selecionado)]["municipio"].unique()
    municipio_selecionado = st.sidebar.multiselect("Selecione o(s) Município(s)", municipios_disponiveis)

if estado_selecionado:
    df_filtrado = df_filtrado[df_filtrado["uf"].isin(estado_selecionado)]

if municipio_selecionado:
    df_filtrado = df_filtrado[df_filtrado["municipio"].isin(municipio_selecionado)]

if br_selecionada:
     df_filtrado = df_filtrado[df_filtrado["br"].isin(br_selecionada)]

if tipo_veiculo_selecionado:
     df_filtrado = df_filtrado[df_filtrado["tipo_veiculo"].isin(tipo_veiculo_selecionado)]

if condicao_tempo_selecionado:
    df_filtrado = df_filtrado[df_filtrado["condicao_metereologica"].isin(condicao_tempo_selecionado)]

if fase_dia_selecionado:
    df_filtrado = df_filtrado[df_filtrado["fase_dia"].isin(fase_dia_selecionado)]


conn = duckdb.connect()
conn.register('df_filtrado', df_filtrado)
# ------------------ 
query_acidentes_com_vitimas = """
    SELECT 
        COUNT(DISTINCT id) AS Acidente_com_vitimas
        FROM df_filtrado
        WHERE mortos >= 1;"""

result_cartao1 = conn.execute(query_acidentes_com_vitimas).fetchone()

if result_cartao1:
    total_acidentes_com_vitimas = result_cartao1[0]
    
    if total_acidentes_com_vitimas > 1000:
        total_acidentes_com_vitimas = '{:,.3f} K'.format(total_acidentes_com_vitimas / 1000)

total_mortos = df_filtrado['mortos'].sum()

mortos_por_dia = round(total_mortos / (365 * 4))
if mortos_por_dia < 1:
    mortos_por_dia = '< 1'

if total_mortos > 1000:
     total_mortos = '{:,.3f} K'.format(total_mortos / 1000)

square_style = """
    padding: 20px;
    border: 6px solid #4848cf;
    border-radius: 50px; 
    background-color: #8B0000; 
"""

square_style = """
    padding: 20px;
    border: 6px solid #ff5900;
    border-radius: 50px; 
    background-color: #8B0000;
    width: fit-content;
    margin: auto;
"""
st.markdown(f'<div style="{square_style}"> \
             <div style="display: inline-block; text-align: center; vertical-align: top;"> \
             <div style="border: 3.5px solid #FF1493; border-radius: 15px; padding: 15px; background-color: #DC143C;"> \
             <h3 style="color:yellow; font-family: Segoe UI Semibold; font-size: 25px;"><strong>Acidentes c/ Mortos</strong></h3> \
             <h2 style="color:white; margin: 5px 0; font-size: 28px">{total_acidentes_com_vitimas}</h2> \
             </div> \
             </div> \
             <div style="display: inline-block; text-align: center; vertical-align: top;"> \
             <div style="border: 3.5px solid #FF1493; border-radius: 15px; padding: 15px; background-color: #DC143C;"> \
             <h3 style="color:yellow; font-family: Segoe UI Semibold; font-size: 25px;"><strong>Total Óbitos</strong></h3> \
             <h2 style="color:white; margin: 5px 0; font-size: 28px"><strong>{total_mortos}</strong></h2> \
             </div> \
             </div> \
             <div style="display: inline-block; text-align: center; vertical-align: top;"> \
             <div style="border: 3.5px solid #FF1493; border-radius: 15px; padding: 15px; background-color: #DC143C;"> \
             <h3 style="color:yellow; font-family: Segoe UI Semibold; font-size: 25px;"><strong>Mortos por dia</strong></h3> \
             <h2 style="color:white; margin: 5px 0; font-size: 28px"><strong>{mortos_por_dia}</strong></h2> \
             </div> \
             </div> \
             <div style="display: inline-block; text-align: center; vertical-align: top;"> \
             <div style="border: 3.5px solid #FF1493; border-radius: 15px; padding: 15px; background-color: #DC143C;"> \
             <h3 style="color:yellow; font-family: Segoe UI Semibold; font-size: 25px;"><strong>Taxa de Mortalidade</strong></h3> \
             <h2 style="color:white; margin: 5px 0; font-size: 28px"><strong>5%</strong></h2> \
             </div>', unsafe_allow_html=True)

# -------------- Gráficos
st.markdown("---")


consulta1 = """
   SELECT 
    STRFTIME('%Y', CAST(data_inversa AS DATE)) AS Ano,
    COUNT(DISTINCT id) AS Total_acidentes_por_ano
FROM df_filtrado
WHERE mortos >= 1 
GROUP BY Ano;
"""

grafico1 = conn.execute(consulta1)
result_df1 = grafico1.fetch_df()
result_df1 = result_df1.sort_values(by=['Ano'])

fig1 = px.bar(result_df1, x='Ano', y='Total_acidentes_por_ano', 
             labels={'Total_acidentes_por_ano': '', 'Ano': 'Ano'},
             title='Óbitos por Ano')

fig1.update_traces(marker_color='#ba4a63')

fig1.update_layout( 
    title={'x': 0.4,'font': {'size': 30}},
    xaxis_title='Ano',
    xaxis_tickangle=-45,
    width= 400, 
    height=400,
    bargap=0.2,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    margin=dict(l=20, r=0, t=50, b=50),
    uirevision='Traces'
)

fig1.update_xaxes(type='category')

#  --------------------- Gráfico dos meses -------------------------------
# Dados do segundo gráfico
consulta2 = """
   SELECT 
    STRFTIME('%m', CAST(data_inversa AS DATE)) AS Mes_Numero,
    STRFTIME('%Y', CAST(data_inversa AS DATE)) AS Ano,
    COUNT(DISTINCT id) AS Numero_de_Acidentes
   FROM df_filtrado
   WHERE mortos >= 1 
   GROUP BY Mes_Numero, Ano;
"""

result2 = conn.execute(consulta2)
result_df2 = result2.fetch_df()

meses_portugues = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
result_df2['Mes'] = result_df2['Mes_Numero'].astype(int).map(lambda x: meses_portugues[x-1])
result_df2 = result_df2.sort_values(by='Mes_Numero')
result_df2 = result_df2.sort_values(by=['Ano', 'Mes_Numero'])

fig2 = px.line(result_df2, x='Mes', y='Numero_de_Acidentes', color='Ano',
               labels={'Numero_de_Acidentes': '', 'Mes': 'Mês', 'Ano': 'Ano'},
               title='Acidentes por Mês nos Últimos Três Anos',
               color_discrete_sequence=['#f6ff00','#ffbb00', '#f04000', '#a10005'])

fig2.update_traces(line_width=3)

fig2.update_layout(
    title={'x': 0.1, 'font': {'size': 30}}, 
    xaxis_title='', 
    yaxis_title='',
    width=800,
    height=400,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    margin=dict(l=0, r=0, t=50, b=50),
    legend=dict(
        title='Ano',
        orientation='h', 
        yanchor='bottom', 
        y=1.02, 
        xanchor='right', 
        x=1,
        font=dict(size=20),
        traceorder="normal",
        itemsizing='constant'
    ))
# --------------------------- Gráfico dos dias da semana -----------------------

# Dados do segundo gráfico
consulta3 = """
   SELECT 
    STRFTIME('%w', CAST(data_inversa AS DATE)) AS Dia_Semana_Numero,
    CASE STRFTIME('%w', CAST(data_inversa AS DATE))
        WHEN '0' THEN 'Domingo'
        WHEN '1' THEN 'Segunda'
        WHEN '2' THEN 'Terça'
        WHEN '3' THEN 'Quarta'
        WHEN '4' THEN 'Quinta'
        WHEN '5' THEN 'Sexta'
        ELSE 'Sábado'
    END AS Dia_Semana,
    COUNT(DISTINCT id) AS Numero_de_Acidentes
   FROM df_filtrado
   WHERE mortos >= 1 
   GROUP BY Dia_Semana_Numero
   ORDER BY CAST(Dia_Semana_Numero AS INTEGER);
"""


result3 = conn.execute(consulta3)
result_df3 = result3.fetch_df()


fig3 = px.bar(result_df3, x='Dia_Semana', y='Numero_de_Acidentes', 
             labels={'Numero_de_Acidentes': '', 'Dia_semana': 'Dia da Semana'},
             title='Acidentes Por Dia da Semana')

cor_fim_de_semana = '#82142c'

fig3.data[0].marker.color = [cor_fim_de_semana if dia == 'Sábado' or dia == 'Domingo' else '#ba4a63' for dia in result_df3['Dia_Semana']]

fig3.update_layout(
    title={'x': 0.1,'font': {'size': 30}},
    xaxis_title='', 
    width=500,  
    height=400,
    bargap=0.2,  
    xaxis=dict(tickfont=dict(size=15)),
    yaxis=dict(tickfont=dict(size=15)),
    margin=dict(l=0, r=0, t=50, b=50),
    uirevision='Traces'
)

fig3.add_trace(
    go.Scatter(
        x=result_df3['Dia_Semana'],
        y=result_df3['Numero_de_Acidentes'],
        mode='lines',
        line=dict(color='#011e47', width=2.5, shape='spline'),
        showlegend=False
)
)

consulta4 = """
    SELECT
        uso_solo AS Urbano_Rural,
        COUNT(DISTINCT id) AS Total_Acidentes
    FROM df_filtrado
    WHERE mortos >= 1 
    GROUP BY Urbano_Rural;"""

result4 = conn.execute(consulta4)
result_df4 = result4.fetch_df()

fig4 = go.Figure(data=[go.Pie(labels=result_df4['Urbano_Rural'], values=result_df4['Total_Acidentes'])])


cores = {'Rural': '#578755', 'Urbano': '#32346b'}

fig4.update_traces(marker=dict(colors=[cores[x] for x in result_df4['Urbano_Rural']]), textfont=dict(size=20))

fig4.update_layout(title='Zonas Urbanas ou Rural',
                   title_font_size=30, 
                   title_x=0.15,
                   height=350, 
                   width=400,
                   margin=dict(l=0, r=0, t=50, b=50),
                   uirevision='Traces')


col1, col2, col3 = st.columns(3)


with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig4, use_container_width=True)
with col3:
    st.plotly_chart(fig3, use_container_width=True)

st.plotly_chart(fig2, use_container_width=True)

st.title("Comparações Gerais")
st.markdown("-------")
# ---------------------------------------------
#Detalhes

df['data_inversa'] = pd.to_datetime(df['data_inversa'])
endDate = pd.to_datetime(df['data_inversa']).max()
startDate = pd.to_datetime(df['data_inversa']).min()
col5, col6 = st.columns(2)
with col5:
    date1 = st.date_input("Data inicial", startDate.date())

with col6:
    date2 = st.date_input("Data final", endDate.date())

df_filtrado2 = df.copy()

df_filtrado2 = df.loc[(df['data_inversa'] >= pd.Timestamp(date1)) & (df['data_inversa'] <= pd.Timestamp(date2))]


st.sidebar.markdown("----------")
st.sidebar.title("Filtros - 2")


dt_regiao_selecionada = st.sidebar.multiselect("Selecione as regiões", df["regiao"].unique(), key="regiao")
dt_estado_selecionado = st.sidebar.multiselect("Selecione os estados", df["uf"].unique(), key="uf")
dt_veiculo_selecionado = st.sidebar.multiselect("Selecione os tipos de veículos", df['tipo_veiculo'].unique(), key='veiculo')
dt_condicao_tempo_selecionado = st.sidebar.multiselect("Selecione a condição meteorológica", df["condicao_metereologica"].unique(), key='tempo')
dt_fase_dia_selecionado = st.sidebar.multiselect("Selecione a fase do dia", df["fase_dia"].unique(), key='fase_dia')

if dt_regiao_selecionada:
    dt_estado_selecionado.extend(df[df["regiao"].isin(dt_regiao_selecionada)]["uf"].unique())
    df_sexo = df_sexo[df_sexo['regiao'].isin(dt_regiao_selecionada)]

if dt_estado_selecionado:
    dt_municipios_disponiveis = df[df["uf"].isin(dt_estado_selecionado)]["municipio"].unique()
    dt_municipio_selecionado = st.sidebar.multiselect("Selecione o(s) Município(s)", dt_municipios_disponiveis)

    if dt_municipio_selecionado:
        df_filtrado2 = df_filtrado2[df_filtrado2["municipio"].isin(dt_municipio_selecionado)]
        df_sexo = df_sexo[df_sexo["municipio"].isin(dt_municipio_selecionado)]

if dt_estado_selecionado:
    df_filtrado2 = df_filtrado2[df_filtrado2["uf"].isin(dt_estado_selecionado)]
    df_sexo = df_sexo[df_sexo['uf'].isin(dt_estado_selecionado)]

if dt_condicao_tempo_selecionado:
    df_filtrado2 = df_filtrado2[df_filtrado2["condicao_metereologica"].isin(dt_condicao_tempo_selecionado)]
    df_sexo = df_sexo[df_sexo['condicao_metereologica'].isin(dt_condicao_tempo_selecionado)]

if dt_fase_dia_selecionado:
    df_filtrado2 = df_filtrado2[df_filtrado2["fase_dia"].isin(dt_fase_dia_selecionado)]
    df_sexo = df_sexo[df_sexo['fase_dia'].isin(dt_fase_dia_selecionado)]

if dt_veiculo_selecionado:
    df_filtrado2 = df_filtrado2[df_filtrado2["tipo_veiculo"].isin(dt_veiculo_selecionado)]
    df_sexo = df_sexo[df_sexo['tipo_veiculo'].isin(dt_veiculo_selecionado)]


# Gráficos -------------------------------
consulta5 = """
    SELECT 
        regiao AS Regiao,
        COUNT(DISTINCT id) AS Total_Acidentes
        FROM df_filtrado2
        WHERE mortos >= 1 
        GROUP BY regiao
        ORDER BY Total_Acidentes ASC;
    """
result5 = conn.execute(consulta5)
result_df5 = result5.fetch_df()

fig5 = px.bar(result_df5, x="Total_Acidentes", y="Regiao", orientation='h')

fig5.update_traces(marker_color='#db7900')
fig5.update_layout(
    title='Regiões',
    xaxis_title='',
    yaxis_title='',
    title_x=0.4,
    title_font_size=30,
    height=400,
    width=450,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    margin=dict(l=0, r=0, t=50, b=50)
)

consulta6 = """
    SELECT 
        uf AS Estado,
        COUNT(DISTINCT id) AS Total_Acidentes
        FROM df_filtrado2
        WHERE mortos >= 1 
        GROUP BY Estado
        ORDER BY Total_Acidentes ASC;
    """

result6 = conn.execute(consulta6)
result_df6 = result6.fetch_df()

fig6 = px.bar(result_df6, x="Total_Acidentes", y="Estado", orientation='h')

fig6.update_traces(marker_color='#db7900')
fig6.update_layout(
    title='Estados',
    xaxis_title='',
    yaxis_title='',
    title_font_size=30,
    title_x=0.4,
    height=400,
    width=450,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    margin=dict(l=0, r=0, t=50, b=50)
)

consulta7 = """
    SELECT 
        municipio AS Municipio,
        COUNT(DISTINCT id) AS Total_Acidentes
        FROM df_filtrado2
        WHERE mortos >= 1 
        GROUP BY Municipio
        ORDER BY Total_Acidentes DESC LIMIT 10;
    """

result7 = conn.execute(consulta7)
result_df7 = result7.fetch_df().sort_values(by='Total_Acidentes')


fig7 = px.bar(result_df7, x="Total_Acidentes", y="Municipio", orientation='h')

fig7.update_traces(marker_color='#db7900')
fig7.update_layout(
    title='TOP 10 Municipios',
    xaxis_title='',
    yaxis_title='',
    title_font_size=30,
    title_x=0.4,
    height=400,
    width=450,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    margin=dict(l=0, r=0, t=50, b=50)
)
col7, col10, col13 = st.columns(3)

with col7:
    st.plotly_chart(fig5, use_container_width=True)
with col10:
    st.plotly_chart(fig6, use_container_width=True)
with col13:
     st.plotly_chart(fig7, use_container_width=True)

consulta8 =""" 
    SELECT
        CONCAT('BR ', CAST(br AS TEXT)) AS BR,  -- Concatenando o texto 'BR' com o número da coluna br
        COUNT(DISTINCT id) AS Total_Acidentes
    FROM df_filtrado2
    WHERE mortos >= 1 
    GROUP BY BR
    ORDER BY Total_Acidentes DESC LIMIT 10;
"""

result8 = conn.execute(consulta8)
result_df8 = result8.fetch_df().sort_values(by='Total_Acidentes')

fig8 = px.bar(result_df8, x="Total_Acidentes", y="BR", orientation='h')

fig8.update_traces(marker_color='#6e0000')
fig8.update_layout(
    title='TOP 10 BR',
    xaxis_title='',
    yaxis_title='',
    title_font_size=30,
    title_x=0.4,
    height=400,
    width=450,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    margin=dict(l=0, r=0, t=50, b=50)
)

df_sexo.loc[df_sexo['sexo'] == 'Não Informado', 'sexo'] = 'Ignorado'

consulta9 =""" 
    SELECT
        sexo AS sexo,
        COUNT(id) AS Total_Acidentes
    FROM df_sexo
    WHERE mortos = 1
    GROUP BY sexo;
"""


result9 = conn.execute(consulta9)
result_df9 = result9.fetch_df()


fig9 = go.Figure(data=[go.Pie(labels=result_df9['sexo'], values=result_df9['Total_Acidentes'])])
cores = {'Masculino': '#0085de', 'Feminino': '#ff2bdc', 'Ignorado': '#afabcf'}
fig9.update_traces(marker=dict(colors=[cores[x] for x in result_df9['sexo']]), textfont=dict(size=16))


fig9.update_layout(title='sexo',
                   title_font_size=30, 
                   title_x=0.35,
                   height=350, 
                   width=400,
                   margin=dict(l=0, r=20, t=50, b=50),
                   uirevision='Traces',
                  )

consulta10 = """
    SELECT 
        fase_dia AS horario,
        COUNT(DISTINCT id) AS Total_Acidentes
        FROM df_filtrado2
        WHERE mortos >= 1 
        GROUP BY fase_dia
        ORDER BY Total_Acidentes DESC;
"""

result10 = conn.execute(consulta10)
result_df10 = result10.fetch_df().sort_values(by='Total_Acidentes')

fig10 = px.bar(result_df10, x="Total_Acidentes", y="horario", orientation='h')

fig10.update_traces(marker_color='#6e0000')
fig10.update_layout(
    title='Horários',
    xaxis_title='',
    yaxis_title='',
    title_font_size=30,
    title_x=0.4,
    height=400,
    width=450,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    margin=dict(l=0, r=0, t=50, b=50)
)
col10,col11,col14 = st.columns(3)

with col10:
    st.plotly_chart(fig8,use_container_width=True)
with col11:
    st.plotly_chart(fig9,use_container_width=True)
with col14:
    st.plotly_chart(fig10,use_container_width=True)

consulta11 =""" 
    SELECT
        causa_acidente AS Causa_Acidente,
        COUNT(DISTINCT id) AS Total_Acidentes
    FROM df_filtrado2
    WHERE mortos >= 1 
    GROUP BY Causa_Acidente
    ORDER BY Total_Acidentes DESC LIMIT 10;
"""

result11 = conn.execute(consulta11)
result_df11 = result11.fetch_df().sort_values(by='Total_Acidentes')
result_df11['Causa_Acidente'] = result_df11['Causa_Acidente'].str.slice(0, 46)


fig11 = px.bar(result_df11, x="Total_Acidentes", y="Causa_Acidente", orientation='h')

fig11.update_traces(marker_color='#130161')
fig11.update_layout(
    title='TOP 10 Causas Acidentes',
    xaxis_title='',
    yaxis_title='',
    title_font_size=30,
    title_x=0.4,
    height=400,
    width=450,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    margin=dict(l=0, r=0, t=50, b=50)
)

consulta12 =""" 
    SELECT
        tipo_acidente AS Tipo_Acidente,
        COUNT(DISTINCT id) AS Total_Acidentes
    FROM df_filtrado2
    WHERE mortos >= 1 
    GROUP BY Tipo_Acidente
    ORDER BY Total_Acidentes DESC LIMIT 10;
"""

result12 = conn.execute(consulta12)
result_df12 = result12.fetch_df().sort_values(by='Total_Acidentes')

fig12 = px.bar(result_df12, x="Total_Acidentes", y="Tipo_Acidente", orientation='h')

fig12.update_traces(marker_color='#130161')
fig12.update_layout(
    title='TOP 10 Acidentes',
    xaxis_title='',
    yaxis_title='',
    title_font_size=30,
    title_x=0.4,
    height=400,
    width=450,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    margin=dict(l=0, r=0, t=50, b=50)
)

col13, col14 = st.columns(2)

with col13:
    st.plotly_chart(fig11, use_container_width=True)
with col14:
    st.plotly_chart(fig12, use_container_width=True)


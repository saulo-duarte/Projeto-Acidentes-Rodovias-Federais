import streamlit as st

st.set_page_config(layout="wide")

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
st.markdown("""  
    ## Prefácio
            
    Neste projeto pessoal de análise de dados, explorei SQL, Python e uma variedade de bibliotecas, incluindo Pandas, NumPy e Plotly, para investigar e visualizar conjuntos de dados governamentais da Polícia Rodoviária Federal, referentes aos anos de 2021 a 2023, com o objetivo de obter insights e compreender as tendências e padrões presentes nos dados.
    
    ### Fonte dos Dados e Objetivo do Projeto

    Os dados analisados foram obtidos a partir do site do governo, fornecendo uma fonte confiável e abrangente para a análise. O objetivo principal deste projeto é extrair insights valiosos a partir desses dados governamentais, apresentando-os de forma clara e compreensível. 
            
    Dados disponível em: [Gov-PRF](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf)

    ## Desenvolvimento

    O processo de análise de dados envolve várias etapas. Primeiramente, os dados são coletados do site do governo e carregados na aplicação. Em seguida, eles são pré-processados e explorados utilizando as bibliotecas Pandas e NumPy. Durante essa fase, realizei tarefas como limpeza de dados, manipulação de formatos e tratamento de valores ausentes.

    Após o pré-processamento, os dados são visualizados através de gráficos interativos utilizando a biblioteca Plotly. Essas visualizações ajudam a identificar padrões, tendências e correlações nos dados, fornecendo insights valiosos para tomadas de decisão.

    Também utilizei o PowerBI para realizar visualizações após o tratamento do dados, disponível em [Link](https://app.powerbi.com/view?r=eyJrIjoiM2Y0MDY3NmQtZjNiOC00YWNhLWE2NzUtOGM3NGY0ZGIyOGFjIiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9&pageName=ReportSection8edd04b2e68794eb13ed).

    ## Funcionalidades Adicionais

    
    Além das análises e visualizações de dados, a aplicação oferece funcionalidades adicionais na barra lateral, como a navegação entre as páginas e filtros interativos. Esses filtros permitem que os usuários personalizem a visualização dos dados de acordo com suas necessidades específicas, proporcionando uma experiência de análise personalizada e profunda. Além disso, os gráficos gerados pelo Plotly oferecem recursos avançados, como a possibilidade de utilizar o zoom nos gráficos ou até mesmo deixá-los em tela cheia, permitindo uma análise mais detalhada e imersiva.

    Para conhecer mais sobre mim e minha experiência em análise de dados, confira meu perfil no [LinkedIn](https://www.linkedin.com/in/saulo-duarte-0a2720261/)
    """,
    unsafe_allow_html=True
)
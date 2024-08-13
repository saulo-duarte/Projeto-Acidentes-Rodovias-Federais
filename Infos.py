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

    O processo de análise de dados envolve várias etapas. Primeiramente, os dados são coletados do site do governo e carregados, em seguida, são limpos e importados para um banco de dados PostgeSQL utilizando uma imagem Docker. Após a importação dos dados, são realizadas análises exploratórias e visualizações de dados para identificar padrões e tendências. 
    Por fim, os insights obtidos são apresentados de forma clara e concisa, utilizando gráficos interativos e filtros personalizados para facilitar a interpretação dos dados, além da criação de um modelo de Machine Learning para prever a gravidade dos acidentes.
    """ , unsafe_allow_html=True)

st.image("images/Diagrama_Projeto.png")
    ## Funcionalidades Adicionais
st.markdown("""
    ## Funcionalidades Adicionais
    Além das análises e visualizações de dados, a aplicação oferece funcionalidades adicionais na barra lateral, como a navegação entre as páginas e filtros interativos. Esses filtros permitem que os usuários personalizem a visualização dos dados de acordo com suas necessidades específicas, proporcionando uma experiência de análise personalizada e profunda. Além disso, os gráficos gerados pelo Plotly oferecem recursos avançados, como a possibilidade de utilizar o zoom nos gráficos ou até mesmo deixá-los em tela cheia, permitindo uma análise mais detalhada e imersiva.

    Para conhecer mais sobre mim e minha experiência em análise de dados, confira meu perfil no [LinkedIn](https://www.linkedin.com/in/saulo-duarte-0a2720261/)
    Meu github: [GitHub](https://github.com/saulo-duarte) & Meu Portfólio: [Portfólio](https://sauloduarte.carrd.co/#)
    """,
    unsafe_allow_html=True
)

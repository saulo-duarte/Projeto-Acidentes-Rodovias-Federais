## Projeto Acidentes em Rodovias Federais

![image](https://www.paranaportal.com.br/wp-content/uploads/2024/07/cresce-numero-mortes-acidentes-rodovias-federais-parana.png)

### Objetivo

O objetivo deste projeto é analisar os dados de acidentes em rodovias federais do Brasil, disponibilizados pela Polícia Rodoviária Federal (PRF), com o intuito de identificar padrões e características dos acidentes, bem como as possíveis causas e consequências. A análise dos dados será realizada Python e suas bibliotecas para análise de dados, como Pandas, Numpy, Matplotlib, plotly, e sklearn para machine learning.

### Tecnologias Utilizadas 🔧

- Python (Pandas, Numpy, Matplotlib, Plotly, Sklearn, streamlit, etc)
- Docker
- PostgreSQL
- PowerBI
- Git



### **Perguntas a serem respondidas**

- Há sazonalidade nos acidentes?

- A quantidade de acidentes vem aumentando, diminuindo ou se mantem estável ao longo dos anos?

- Quais regiões do Brasil possuem mais acidentes?

- Quais regiões possuem mais acidentes graves?

- Quais tipos de acidentes e causas são mais comuns?

- Quais acidentes são mais mortais?

- Qual são as principais características dos acidentes mais graves?

### Pipeline

![images](images/Diagrama_Projeto.png)

1. **Coleta de Dados**

Os dados foram coletados diretamente do site da PRF, disponíveis em: https://portal.prf.gov.br/dados-abertos-acidentes. O dataset utilizado é referente ao ano de 2020 a 2023, e contém informações sobre os acidentes ocorridos nas rodovias federais do Brasil.

2. **Limpeza e Pré-processamento**

Nesta etapa, os dados foram tratados e limpos, removendo valores nulos, duplicados e outliers. Além disso, foram realizadas transformações e ajustes necessários para a análise.

3. **Modelagem de dados**

Os dados foram modelados e importados para o banco de dados PostgreSQL, utilizando o docker para a criação do container. Em seguida, foram realizadas consultas SQL para a extração de informações relevantes.

![image](images/Data_Modelling.png)



4. **Análise Exploratória**

A análise exploratória dos dados foi realizada com o intuito de identificar padrões e características dos acidentes, bem como as possíveis causas e consequências. Foram utilizadas técnicas de visualização de dados para facilitar a interpretação dos resultados.


5. **Machine Learning**

Foi aplicado um modelo de machine learning para prever a gravidade dos acidentes, com base nas características dos acidentes. Para isso, foram utilizadas técnicas de pré-processamento de dados, seleção de features e treinamento do modelo.

6. **Visualização**

Por fim, os resultados obtidos foram apresentados utilizando streamlit e PowerBI para a criação de dashboards interativos, facilitando a visualização e interpretação dos dados.

### Insights

Praticamente não houve variação no número de acidentes ao longo dos anos, apenas em 2023 houve um aumento significativo.
    
![](images/acidentes_por_ano.png)

É possível observar que nos meses de janeiro, julho, outubro e dezembro há um aumento no número de acidentes, o que pode estar relacionado ao período de férias e festas de final de ano.

![](images/acidentes_por_mes.png)

Fica mais evidente quando o gráfico fica segmentado por ano. Além disso é possível observar que a tentativa de "lockdown" surtiu efeito em 2020, com uma queda apartir de março, porém após julho os números voltaram a subir.

![](images/acidentes_por_mes_e_ano.png)

Nos dias da semana, é possível observar que os finais de semana (sábado e domingo) possuem um maior número de acidentes, o que pode estar relacionado ao aumento do fluxo de veículos nas rodovias, seguido pelo dia de sexta-feira.

![](images/acidentes_por_dia_da_semana.png)

Mantendo sempre a mesma tendência independente do ano.

![image](images/acidentes_por_dia_da_semana_e_ano.png)

Os horários de pico para acidentes são entre 16h e 19h, o que pode estar relacionado ao horário de saída do trabalho e ao aumento do fluxo de veículos nas rodovias.

![](images/acidentes_por_hora.png)

Porém os horários que apresentam maior gravidade são entre 22hrs até as 5hrs, o que pode estar relacionado a diversos fatores, como a falta de visibilidade, cansaço e ingestão de álcool, além das pistas estarem mais livres, permitindo que os veículos atinjam maiores velocidades.

A tabela a seguir apresenta os 5 horarios com maior taxa de mortalidade de cada ano analisado.

![](images/tabela_mortalidade_horario.png)

**Regionalização**

A região com maior número de acidentes é a região sudeste, seguida pela região sul e nordeste. Já a região norte é a que possui o menor número de acidentes.

![](images/acidentes_por_regiao.png)

Porém, a região nordeste é a que possui a maior taxa de mortalidade, seguida pela região norte e centro-oeste. Já a região sul é a que possui a menor taxa de mortalidade.

![image](images/taxa_mortalidade_regiao.png)

Olhando para os estados, Minas Gerais é o estado com o maior número de acidentes, seguido por Santa Catarina e Paraná. Já o estado de Roraima é o que possui o menor número de acidentes.

![](images/acidentes_por_estado.png)


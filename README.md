## Projeto Acidentes em Rodovias Federais

![image](https://www.paranaportal.com.br/wp-content/uploads/2024/07/cresce-numero-mortes-acidentes-rodovias-federais-parana.png)

### Objetivo

O objetivo deste projeto é analisar os dados de acidentes em rodovias federais do Brasil, disponibilizados pela Polícia Rodoviária Federal (PRF), com o intuito de identificar padrões e características dos acidentes, bem como as possíveis causas e consequências. A análise dos dados será realizada Python e suas bibliotecas para análise de dados, como Pandas, Numpy, Matplotlib, plotly, e sklearn para machine learning.

### Tópicos

- [Tecnologias](#Tecnologias-Utilizadas-🔧)
- [Pipeline](#Pipeline)
- [Perguntas a serem respondidas](#Perguntas-a-serem-respondidas)
- [Insights](#Insights)

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

## Pipeline

![images](images/Diagrama_Projeto.png)

1. **Coleta de Dados**

Os dados foram coletados diretamente do site da PRF, disponíveis em: https://portal.prf.gov.br/dados-abertos-acidentes. O dataset utilizado é referente ao ano de 2020 a 2023, e contém informações sobre os acidentes ocorridos nas rodovias federais do Brasil.

### 2. **Limpeza e Pré-processamento**

Nesta etapa, os dados foram tratados e limpos, removendo valores nulos, duplicados e outliers. Além disso, foram realizadas transformações e ajustes necessários para a análise.

### 3. **Modelagem de dados**

Os dados foram modelados e importados para o banco de dados PostgreSQL, utilizando o docker para a criação do container. Em seguida, foram realizadas consultas SQL para a extração de informações relevantes. A modelagem dos dados foi feita da seguinte forma:

- **Acidentes**: informações sobre os acidentes, como data, hora, tipo, causa, gravidade, etc.

- **Envolvidos**: informações sobre os envolvidos nos acidentes, como condutores, passageiros, pedestres, etc.

Com o intuito de diminuir a redundância de dados, foi criada uma tabela de dimensão para armazenar as informações dos envolvidos, e uma tabela fato para armazenar as informações dos acidentes.

![image](images/Data_Modelling.png)



4. **Análise Exploratória**

A análise exploratória dos dados foi realizada com o intuito de identificar padrões e características dos acidentes, bem como as possíveis causas e consequências. Foram utilizadas técnicas de visualização de dados para facilitar a interpretação dos resultados.


5. **Machine Learning**

Foi aplicado um modelo de machine learning para prever a gravidade dos acidentes, com base nas características dos acidentes. Para isso, foram utilizadas técnicas de pré-processamento de dados, seleção de features e treinamento do modelo.

6. **Visualização**

Por fim, os resultados obtidos foram apresentados utilizando streamlit e PowerBI para a criação de dashboards interativos, facilitando a visualização e interpretação dos dados.

## Insights

Ao analisar os dados, observou-se que praticamente não houve variação no número de acidentes ao longo dos anos, exceto em 2023, quando houve um aumento significativo.
     
![](images/acidentes_por_ano.png)

A distribuição mensal dos acidentes revela que nos meses de janeiro, julho, outubro e dezembro há um aumento no número de acidentes, **relacionado aos períodos de férias e festas de fim de ano**.

![](images/acidentes_por_mes.png)

Esse padrão fica mais evidente quando o gráfico é segmentado por ano. Além disso, observa-se que a tentativa de "*lockdown*" em 2020 resultou em uma queda no número de acidentes a partir de março. No entanto, após julho, os números voltaram a subir.

![](images/acidentes_por_mes_e_ano.png)

Analisando os dias da semana, percebe-se que os **finais de semana** (sábado e domingo) têm um maior número de acidentes, o que pode estar relacionado ao aumento do fluxo de veículos nas rodovias. A sexta-feira também apresenta um número elevado de acidentes.

![](images/acidentes_por_dia_da_semana.png)

Mantendo sempre a mesma tendência independente do ano.

![image](images/acidentes_por_dia_da_semana_e_ano.png)

Os horários de pico para acidentes são entre 16h e 19h, o que pode estar relacionado ao horário de saída do trabalho e ao aumento do fluxo de veículos nas rodovias.

![](images/acidentes_por_hora.png)

Entretanto, os horários que apresentam **maior gravidade são entre 22h e 5h**. Esse aumento na gravidade pode estar relacionado a diversos fatores, como falta de visibilidade, cansaço e ingestão de álcool, além das pistas mais livres, permitindo que os veículos atinjam maiores velocidades.

A tabela a seguir apresenta os 5 horarios com maior taxa de mortalidade de cada ano analisado.

![](images/tabela_mortalidade_horario.png)

**Regionalização**

A região com maior número de acidentes é a região sudeste, seguida pela região sul e nordeste. Já a região norte é a que possui o menor número de acidentes.

![](images/acidentes_por_regiao.png)

Porém, a **região nordeste é a que possui a maior taxa de mortalidade**, seguida pela região norte e centro-oeste. Já a região sul é a que possui a menor taxa de mortalidade.

![image](images/taxa_mortalidade_regiao.png)

Olhando para os estados, Minas Gerais é o estado com o maior número de acidentes, seguido por Santa Catarina e Paraná. Já os estados do norte possuem o menor número de acidentes, pois possuem uma menor densidade populacional e menor fluxo de veículos, o que influencia diretamente no número de acidentes. Além da possibilidade de subnotificação de acidentes.

![](images/acidentes_por_estado.png)

No entanto, os estados do norte e nordeste apresentam mais que o dobro de taxa de mortalidade em relação aos estados do sul e sudeste. Isso pode estar relacionado a diversos fatores, como a qualidade das rodovias, a falta de sinalização, a imprudência dos motoristas e a falta de atendimento médico adequado.

![image](images/taxa_mortalidade_estados.png)

Olhando para os 10 municipios com maior número de acidentes, é possível observar que a maioria deles estão localizados na região sudeste, seguido pela região sul e nordeste.

![](images/top_10_municipios_com_mais_acidentes.png)

As BRs com maior número de acidentes são a BR-116, BR-101, BR-040 e BR-381, que são rodovias que cortam diversos estados possuem um grande fluxo de veículos. Porém essas rodovias não são as que possuem a maior taxa de mortalidade.

![](images/brs_com_mais_acidentes.png)

Porém essas rodovias não são as que possuem a maior taxa de mortalidade.

![](images/taxa_mortalidade_br.png)

**Causas de acidentes**

Os tipos de acidentes mais comuns são a colisão traseira, colisão lateral e colisão frontal, que são acidentes que podem ocorrer em diversas situações, como ultrapassagens indevidas, desrespeito à sinalização e excesso de velocidade.

![](images/causa_acidentes.png)

Porém é possível observar que os acidentes com maior taxa de mortalidade são causas por descuidos dos motoristas e pedestres, podendo ser evitados com mais atenção e cuidado.

![](images/taxa_mortalidade_causa.png)

**Tipos de acidentes**

Os tipos de acidentes mais comuns são a colisão traseira, saída da pista e tombamento, que são acidentes que podem ocorrer em diversas situações, como falta de atenção, ultrapassagens indevidas, desrespeito à sinalização e excesso de velocidade.

![](images/tipos_acidentes.png)

Porém é possível observar que os acidentes com maior taxa de mortalidade são os atropelamentos e colisão frontal, que são acidentes que podem ser mais graves e fatais.

![](images/mortalidade_tipo_acidente.png)
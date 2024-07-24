SELECT DATE_PART('YEAR', data_completa) AS ano,
	COUNT(*) total_acidentes
FROM relational.acidentes
GROUP BY ano
ORDER BY total_acidentes DESC;

SELECT DATE_PART('MONTH', data_completa) AS Mes,
	COUNT(*) total_acidentes
FROM relational.acidentes
GROUP BY mes
ORDER BY total_acidentes DESC;

WITH acidentes_mes_ano AS( 

    SELECT 
        DATE_PART('MONTH', data_completa) AS mes,
        DATE_PART('YEAR', data_completa) AS ano,
        COUNT(*) AS total_acidentes
    FROM relational.acidentes
    GROUP BY mes, ano
    ORDER BY mes, ano
    ),

variacao_acidentes AS(

    SELECT
        mes,
        ano,
        LAG(ano) OVER (PARTITION BY mes ORDER BY ano) AS ano_anterior,
        total_acidentes,
        LAG(total_acidentes) OVER (PARTITION BY mes ORDER BY ano) AS total_acidentes_mes_anterior,
        (total_acidentes - LAG(total_acidentes) OVER (PARTITION BY mes ORDER BY ano)) AS variacao_acidentes,
        (total_acidentes - LAG(total_acidentes) OVER (PARTITION BY mes ORDER BY ano))::DECIMAL /
            NULLIF(LAG(total_acidentes) OVER (PARTITION BY mes ORDER BY ano), 0) * 100 AS variacao_percentual
    FROM acidentes_mes_ano
    )

SELECT *
FROM variacao_acidentes
WHERE variacao_acidentes IS NOT NULL
ORDER BY variacao_percentual DESC
LIMIT 10;

WITH acidentes_semana_ano AS( 
    SELECT 
        DATE_PART('DOW', data_completa) AS semana,
        DATE_PART('YEAR', data_completa) AS ano,
        COUNT(*) AS total_acidentes
    FROM relational.acidentes
    GROUP BY semana, ano
    ORDER BY semana, ano
),

variacao_acidentes_semana AS(
    SELECT
        semana,
        ano,
        LAG(ano) OVER (PARTITION BY semana ORDER BY ano) AS ano_anterior,
        total_acidentes,
        LAG(total_acidentes) OVER(PARTITION BY semana ORDER BY ano) AS total_acidentes_semana_anterior,
        (total_acidentes - LAG(total_acidentes) OVER(PARTITION BY semana ORDER BY ano)) AS variacao_acidentes,
        ROUND((total_acidentes - LAG(total_acidentes) OVER(PARTITION BY semana ORDER BY ano))::DECIMAL / 
            NULLIF(LAG(total_acidentes) OVER(PARTITION BY semana ORDER BY ano), 0) * 100, 2) AS varicao_percentual
    FROM acidentes_semana_ano
    )

SELECT 
	CASE
		WHEN semana = 0 THEN 'Domingo'
		WHEN semana = 1 THEN 'Segunda'
		WHEN semana = 2 THEN 'Terça'
		WHEN semana = 3 THEN 'Quarta'
		WHEN semana = 4 THEN 'Quinta'
		WHEN semana = 5 THEN 'Sexta'
		WHEN semana = 6 THEN 'Sabado'
	END dia_semana, *
FROM variacao_acidentes_semana
WHERE variacao_acidentes IS NOT NULL

CREATE VIEW acidentes_hora AS
    SELECT DATE_PART('HOUR', data_completa) AS hora,
        COUNT(*) total_acidentes
    FROM relational.acidentes
    GROUP BY hora
    ORDER BY total_acidentes;

SELECT *
FROM acidentes_hora
ORDER BY hora;

WITH acidentes_hora_ferias AS( 
    SELECT 
        DATE_PART('HOUR', data_completa) AS hora,
        DATE_PART('MONTH', data_completa) AS mes,
        COUNT(*) AS total_acidentes
    FROM relational.acidentes
	WHERE DATE_PART('MONTH', data_completa) IN (1, 7, 12)
    GROUP BY hora, mes
    ORDER BY hora, mes
),

top_5_horarios_por_ferias AS (
    SELECT 
        *,
        RANK() OVER (PARTITION BY mes ORDER BY total_acidentes DESC) AS ranking_mes,
		RANK() OVER (ORDER BY total_acidentes DESC)
    FROM acidentes_hora_ferias
)

SELECT *
FROM top_5_horarios_por_ferias
WHERE ranking_mes <= 5
ORDER BY mes, ranking_mes;

-- Com óbitos

SELECT DATE_PART('YEAR', data_completa) AS ano,
	COUNT(*) total_acidentes
FROM relational.acidentes
WHERE classificacao_acidente = 'Com Vítimas Fatais'
GROUP BY ano
ORDER BY total_acidentes DESC;

SELECT DATE_PART('MONTH', data_completa) AS Mes,
	COUNT(*) total_acidentes
FROM relational.acidentes
WHERE classificacao_acidente = 'Com Vítimas Fatais'
GROUP BY mes
ORDER BY total_acidentes DESC;

WITH acidentes_mes_ano AS( 

    SELECT 
        DATE_PART('MONTH', data_completa) AS mes,
        DATE_PART('YEAR', data_completa) AS ano,
        COUNT(*) AS total_acidentes
    WHERE classificacao_acidente = 'Com Vítimas Fatais'
    FROM relational.acidentes
    GROUP BY mes, ano
    ORDER BY mes, ano
    ),

variacao_acidentes AS(

    SELECT
        mes,
        ano,
        LAG(ano) OVER (PARTITION BY mes ORDER BY ano) AS ano_anterior,
        total_acidentes,
        LAG(total_acidentes) OVER (PARTITION BY mes ORDER BY ano) AS total_acidentes_mes_anterior,
        (total_acidentes - LAG(total_acidentes) OVER (PARTITION BY mes ORDER BY ano)) AS variacao_acidentes,
        (total_acidentes - LAG(total_acidentes) OVER (PARTITION BY mes ORDER BY ano))::DECIMAL /
            NULLIF(LAG(total_acidentes) OVER (PARTITION BY mes ORDER BY ano), 0) * 100 AS variacao_percentual
    FROM acidentes_mes_ano
    )

SELECT *
FROM variacao_acidentes
WHERE variacao_acidentes IS NOT NULL
ORDER BY variacao_percentual DESC
LIMIT 10;

SELECT
    DATE_PART('HOUR', data_completa) AS hora,
    COUNT(*) total_acidentes
FROM relational.acidentes
WHERE classificacao_acidente = 'Com Vítimas Fatais'
GROUP BY hora
ORDER BY hora;

WITH acidentes_hora_ferias AS( 
    SELECT 
        DATE_PART('HOUR', data_completa) AS hora,
        DATE_PART('MONTH', data_completa) AS mes,
        COUNT(*) AS total_acidentes
    FROM relational.acidentes
	WHERE DATE_PART('MONTH', data_completa) IN (1, 7, 12) AND classificacao_acidente = 'Com Vítimas Fatais'
    GROUP BY hora, mes
    ORDER BY hora, mes
),

top_5_horarios_por_ferias AS (
    SELECT 
        *,
        RANK() OVER (PARTITION BY mes ORDER BY total_acidentes DESC) AS ranking_mes,
		RANK() OVER (ORDER BY total_acidentes DESC)
    FROM acidentes_hora_ferias
)

SELECT *
FROM top_5_horarios_por_ferias
WHERE ranking_mes <= 5
ORDER BY mes, ranking_mes;
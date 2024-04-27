-- Total juntando os anos de 2021 a 2023

SELECT 
    COUNT(DISTINCT id) as Total_acidentes
FROM acidentes_rodovias_prf;

-- Total agrupado por anos

SELECT 
    YEAR(data_inversa) AS Ano,
    COUNT(DISTINCT id) AS Total_acidentes_por_ano
FROM acidentes_rodovias_prf
GROUP BY Ano;

-- Total Agrupado por meses (geral)

SELECT
    MONTHNAME(data_inversa) AS Mes,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY Mes
ORDER BY Total_acidentes DESC;

-- Total Agrupado por meses (diferenciado por ano)

SELECT 
    YEAR(data_inversa) AS Ano,
    MONTHNAME(data_inversa) AS Mes,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY Ano, Mes
ORDER BY Total_acidentes DESC LIMIT 10;

-- DIA SEMANA, FASEDIA

SELECT 
    dia_semana AS Dia_Semana,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY Dia_Semana
ORDER BY Total_acidentes DESC;

SELECT 
    fase_dia AS Fase_Dia,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY fase_dia
ORDER BY Total_acidentes DESC;

SELECT
    uf AS Estado,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY Estado
ORDER BY Total_Obitos DESC;

SELECT
    br as BR,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY br
ORDER BY Total_acidentes DESC;

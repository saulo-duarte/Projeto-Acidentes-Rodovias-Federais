SELECT
    SUM(mortos) AS Total_Mortes
FROM acidentes_rodovias_prf;

SELECT
    YEAR(data_inversa) AS Ano,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY Ano
ORDER BY Total_Obitos DESC;

SELECT 
    MONTHNAME(data_inversa) AS Mes,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY Mes
ORDER BY Total_Obitos DESC;

SELECT 
    dia_semana AS dia_semana,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY dia_semana
ORDER BY Total_Obitos DESC;

SELECT
    regiao AS Regiao,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY regiao
ORDER BY Total_Obitos DESC;

SELECT
    uf AS Estado,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY Estado
ORDER BY Total_Obitos DESC;

SELECT
    municipio AS Municipio,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY municipio
ORDER BY Total_Obitos DESC
LIMIT 20;

SELECT
    br AS BR,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY BR
ORDER BY Total_Obitos DESC;

SELECT
    uso_solo AS Tipo_localidade,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY uso_solo;

SELECT
    tipo_envolvido AS Envolvido,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY Envolvido
HAVING Total_Obitos > 0;

SELECT
    sexo AS Sexo,
    SUM(mortos) AS Total_Obitos
FROM acidentes_rodovias_prf
GROUP BY sexo
HAVING Total_Obitos > 0;

SELECT 
    idade AS Idade,
    COUNT(CASE WHEN mortos = 1 THEN 1 END) AS Mortes
FROM acidentes_rodovias_prf
GROUP BY idade
LIMIT 5;
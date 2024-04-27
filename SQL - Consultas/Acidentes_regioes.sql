-- Acidentes agrupados por estados

SELECT 
    uf as Estado,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY Estado
ORDER BY Total_acidentes DESC;

-- Acidentes Agrupados por estados e ano

SELECT 
    YEAR(data_inversa) AS Ano,
    uf as Estado,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY Ano, Estado
ORDER BY Total_acidentes DESC;

-- Acidentes Agrupados por estado e mes

SELECT
    MONTHNAME(data_inversa) AS Mes,
    uf AS Estado,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY Estado, Mes
ORDER BY Total_acidentes DESC;

-- Regiões geográficas
SELECT
    regiao,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY regiao
ORDER BY Total_acidentes DESC;

-- Regiões e os tipos de acidente mais comum
SELECT
    regiao,
    COUNT(DISTINCT id) AS Total_acidentes,
    (
        SELECT tipo_acidente
        FROM acidentes_rodovias_prf AS sub
        WHERE sub.regiao = main.regiao
        GROUP BY tipo_acidente
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS Causa_mais_comum
FROM acidentes_rodovias_prf AS main
GROUP BY regiao
ORDER BY Total_acidentes DESC;

-- Municipios
SELECT
    municipio,
    COUNT(DISTINCT id) AS Total_acidentes,
    (
        SELECT tipo_acidente
        FROM acidentes_rodovias_prf AS sub
        WHERE sub.municipio = main.municipio
        GROUP BY tipo_acidente
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS Causa_mais_comum
FROM acidentes_rodovias_prf AS main
GROUP BY municipio
ORDER BY Total_acidentes DESC;
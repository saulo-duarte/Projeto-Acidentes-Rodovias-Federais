-- Total de Acidentes por BR
SELECT 
    br as BR,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY br
ORDER BY Total_acidentes DESC;

-- Total de acidentes por ano
SELECT 
    YEAR(data_inversa) AS Ano,
    br AS BR,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY br, Ano, uf
HAVING Total_acidentes > 100
ORDER BY Total_acidentes DESC;

-- Acidentes por BR e Estado
SELECT 
    br AS BR,
    uf AS Estado,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY br, uf
HAVING Total_acidentes > 500
ORDER BY Total_acidentes DESC;

SELECT 
    BR,
    Causa_Acidente,
    Total_acidentes
FROM (
    SELECT 
        br AS BR,
        causa_acidente AS Causa_Acidente,
        COUNT(DISTINCT id) AS Total_acidentes,
        ROW_NUMBER() OVER (PARTITION BY br ORDER BY COUNT(DISTINCT id) DESC) AS row_num
    FROM acidentes_rodovias_prf
    GROUP BY br, causa_acidente
) AS ranked
WHERE row_num <= 5
ORDER BY Total_acidentes DESC, br ASC;


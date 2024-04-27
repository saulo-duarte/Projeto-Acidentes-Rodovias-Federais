-- Total Acidentes
SELECT 
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
WHERE regiao = 'centro_oeste';

-- Total de Acidentes com mortes
SELECT
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE mortos >= 1 AND regiao = 'centro_oeste';

-- Acidentes por Estado
SELECT
    uf AS Estado,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
WHERE regiao = 'centro_oeste'
GROUP BY uf
ORDER BY Total_acidentes DESC;

-- Acidentes com mortes por estado
SELECT
    uf AS Estado,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'centro_oeste' AND mortos >= 1
GROUP BY uf
ORDER BY Acidentes_Com_Mortes DESC;

-- Acidentes por BR
SELECT
    br AS BR,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
WHERE regiao = 'centro_oeste'
GROUP BY br
ORDER BY Total_acidentes DESC;

-- Acidentes com mortes por BR
SELECT
    br AS BR,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'centro_oeste' AND mortos >=1
GROUP BY br
ORDER BY Acidentes_Com_Mortes DESC;

-- Acidentes por municipio
SELECT
    municipio AS Municipio,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
WHERE regiao = 'centro_oeste'
GROUP BY municipio
ORDER BY Total_acidentes DESC;

-- Acidentes por municipio com mortes
SELECT
    municipio AS Municipio,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'centro_oeste' AND mortos >=1
GROUP BY municipio
ORDER BY Acidentes_Com_Mortes DESC;


SELECT
    uf AS Estado,
    causa_acidente AS Causa_do_Acidente,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'centro_oeste' AND mortos >= 1
GROUP BY uf, causa_acidente
ORDER BY Acidentes_Com_Mortes DESC;

SELECT
    municipio AS Municipio,
    causa_acidente AS Causa_do_Acidente,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'centro_oeste' AND mortos >= 1
GROUP BY municipio, causa_acidente
ORDER BY Acidentes_Com_Mortes DESC;

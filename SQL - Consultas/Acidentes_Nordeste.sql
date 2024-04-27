SELECT 
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
WHERE regiao = 'nordeste';

SELECT
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE mortos >= 1 AND regiao = 'nordeste';

SELECT
    uf AS Estado,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
WHERE regiao = 'nordeste'
GROUP BY uf
ORDER BY Total_acidentes DESC;

SELECT
    uf AS Estado,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'nordeste' AND mortos >= 1
GROUP BY uf
ORDER BY Acidentes_Com_Mortes DESC;

SELECT
    br AS BR,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
WHERE regiao = 'nordeste'
GROUP BY br
ORDER BY Total_acidentes DESC;

SELECT
    br AS BR,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'nordeste' AND mortos >=1
GROUP BY br
ORDER BY Acidentes_Com_Mortes DESC;

SELECT
    municipio AS Municipio,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
WHERE regiao = 'nordeste'
GROUP BY municipio
ORDER BY Total_acidentes DESC;

SELECT
    municipio AS Municipio,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'nordeste' AND mortos >=1
GROUP BY municipio
ORDER BY Acidentes_Com_Mortes DESC;

SELECT
    uf AS Estado,
    causa_acidente AS Causa_do_Acidente,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'nordeste' AND mortos >= 1
GROUP BY uf, causa_acidente
ORDER BY Acidentes_Com_Mortes DESC;

SELECT
    municipio AS Municipio,
    causa_acidente AS Causa_do_Acidente,
    COUNT(DISTINCT id) AS Acidentes_Com_Mortes
FROM acidentes_rodovias_prf
WHERE regiao = 'nordeste' AND mortos >= 1
GROUP BY municipio, causa_acidente
ORDER BY Acidentes_Com_Mortes DESC;

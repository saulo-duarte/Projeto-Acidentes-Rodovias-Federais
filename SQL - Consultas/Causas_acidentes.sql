/* Causas dos acidentes, tipos de acidentes, influência do tempo,
dias da semana e condição meteorológica*/

-- Total de acidentes por causa
SELECT 
    causa_acidente AS Causa_Acidente,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY causa_acidente
ORDER BY Total_acidentes DESC;

-- Total de acidentes por tipo de acidente
SELECT
    tipo_acidente,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY tipo_acidente
ORDER BY Total_acidentes DESC;

-- Total de acidentes agrupado por causa e tipo de acidente
SELECT 
    causa_acidente AS Causa_Acidente,
    tipo_acidente AS Tipo_Acidente,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY causa_acidente, tipo_acidente
HAVING Total_acidentes > 20
ORDER BY Total_acidentes;


-- 5 maiores causas de acidente por dia da semana
SELECT Dia_Semana, Causa_Acidente, Total_acidentes
FROM (
    SELECT
        dia_semana AS Dia_Semana,
        causa_acidente AS Causa_Acidente,
        COUNT(DISTINCT id) AS Total_acidentes,
        ROW_NUMBER() OVER (PARTITION BY dia_semana ORDER BY COUNT(DISTINCT id) DESC) AS row_num
    FROM acidentes_rodovias_prf
    WHERE fase_dia = 'plena noite'
    GROUP BY dia_semana, causa_acidente
) AS ranked
WHERE row_num <= 5
ORDER BY FIELD(Dia_Semana, 'domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado'), Total_acidentes DESC;

-- 5 maiores causas de acidente por fase do dia
SELECT 
    Fase_Dia, 
    Causa_Acidente, 
    Total_acidentes
FROM (
    SELECT
        fase_dia AS Fase_Dia,
        causa_acidente AS Causa_Acidente,
        COUNT(DISTINCT id) AS Total_acidentes,
        ROW_NUMBER() OVER (PARTITION BY fase_dia ORDER BY COUNT(DISTINCT id) DESC) AS row_num
    FROM acidentes_rodovias_prf
    WHERE fase_dia IS NOT NULL
    GROUP BY fase_dia, causa_acidente
) AS ranked
WHERE row_num <= 5
ORDER BY fase_dia ASC, Total_acidentes DESC;

-- Total de acidentes por condição meteorológica
SELECT
    condicao_metereologica AS Condicoes_Metereologicas,
    COUNT(DISTINCT id) AS Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY condicao_metereologica
ORDER BY Total_acidentes DESC;

-- 5 Maiores causas de acidentes por condição meteorológica
SELECT 
    Condicao_Meteorologica, 
    Causa_Acidente, 
    Total_acidentes
FROM (
    SELECT
        condicao_metereologica AS Condicao_Meteorologica,
        causa_acidente AS Causa_Acidente,
        COUNT(DISTINCT id) AS Total_acidentes,
        ROW_NUMBER() OVER (PARTITION BY condicao_metereologica ORDER BY COUNT(DISTINCT id) DESC) AS row_num
    FROM acidentes_rodovias_prf
    WHERE condicao_metereologica IS NOT NULL
    GROUP BY condicao_metereologica, causa_acidente
) AS ranked
WHERE row_num <= 5
ORDER BY Condicao_Meteorologica ASC, Total_acidentes DESC;
SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    YEAR(data_inversa) AS Ano
FROM acidentes_rodovias_prf
GROUP BY Ano
ORDER BY Taxa_De_Obito DESC;

SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    MONTHNAME(data_inversa) AS Mes
FROM acidentes_rodovias_prf
GROUP BY Mes
ORDER BY Taxa_De_Obito DESC;

SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    regiao AS regiao
FROM acidentes_rodovias_prf
GROUP BY Regiao
ORDER BY Taxa_De_Obito DESC;

SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    uf AS Estado
FROM acidentes_rodovias_prf
GROUP BY Estado
ORDER BY Taxa_De_Obito DESC;

SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    municipio AS Municipio
FROM acidentes_rodovias_prf
GROUP BY municipio
ORDER BY Taxa_De_Obito DESC LIMIT 20;


SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    br AS BR
FROM acidentes_rodovias_prf
GROUP BY br
ORDER BY Taxa_De_Obito DESC;

SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    sexo
FROM acidentes_rodovias_prf
GROUP BY sexo
HAVING Taxa_De_Obito >= 0
ORDER BY Taxa_De_Obito DESC;

SELECT 
    fase_dia AS Fase_do_Dia,
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito
FROM acidentes_rodovias_prf
GROUP BY fase_dia
ORDER BY Taxa_De_Obito DESC;

SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    uso_solo AS Tipo_localidade
FROM acidentes_rodovias_prf
GROUP BY uso_solo
ORDER BY Taxa_De_Obito DESC;

SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    tracado_via
FROM acidentes_rodovias_prf
GROUP BY tracado_via
ORDER BY Taxa_De_Obito DESC;

SELECT 
    SUM(mortos) / 
    (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)) *100 AS Taxa_De_Obito,
    tipo_acidente
FROM acidentes_rodovias_prf
GROUP BY tipo_acidente
ORDER BY Taxa_De_Obito DESC LIMIT 10;
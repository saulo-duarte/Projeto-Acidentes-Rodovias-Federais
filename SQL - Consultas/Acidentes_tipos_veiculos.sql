-- Total de acidentes por veiculo
SELECT
    tipo_veiculo AS Veiculo,
    COUNT(DISTINCT id) as Total_acidentes
FROM acidentes_rodovias_prf
GROUP BY Veiculo
ORDER BY Total_acidentes DESC;

-- Veiculos com mais mortes
SELECT
    tipo_veiculo AS Veiculo,
    SUM(mortos) AS Total_Mortos
FROM acidentes_rodovias_prf
GROUP BY Veiculo
ORDER BY Total_Mortos DESC;

-- Taxa de mortalidade por veiculo
SELECT
    tipo_veiculo AS Veiculo,
    ROUND(SUM(mortos) / (SUM(feridos_leves) + SUM(feridos_graves) + SUM(ilesos) + SUM(mortos)), 2) * 100 AS Taxa_de_morte_por_veiculo
FROM acidentes_rodovias_prf
GROUP BY Veiculo
ORDER BY Taxa_de_morte_por_veiculo DESC;


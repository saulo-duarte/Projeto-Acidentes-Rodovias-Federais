CREATE VIEW infos_acidentes_br AS
WITH total_acidentes_br AS (
    SELECT 
        br,
        COUNT(*) AS total_acidentes
    FROM relational.acidentes
    GROUP BY br
),

total_envolvidos AS (
    SELECT
        acidentes.br AS BR,
        COUNT(*) AS total_envolvidos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON envolvidos.id_acidente = acidentes.id
    GROUP BY acidentes.br
)

SELECT 
    acidentes.br AS BR,
    total.total_acidentes,
    COALESCE(SUM(envolvidos.feridos_leves), 0) AS total_feridos_leves,
    COALESCE(SUM(envolvidos.feridos_graves), 0) AS total_feridos_graves,
    COALESCE(SUM(envolvidos.mortos), 0) AS total_mortos,
    ROUND(COALESCE(SUM(envolvidos.mortos)::DECIMAL / total_envolvidos.total_envolvidos * 100, 0), 2) AS taxa_mortalidade
FROM relational.acidentes
INNER JOIN total_acidentes_br total ON acidentes.br = total.br
INNER JOIN relational.envolvidos ON envolvidos.id_acidente = acidentes.id
INNER JOIN total_envolvidos ON acidentes.br = total_envolvidos.br
GROUP BY acidentes.br, total.total_acidentes, total_envolvidos.total_envolvidos
ORDER BY total.total_acidentes DESC;

SELECT * 
FROM infos_acidentes_br;

WITH br_mais_obitos AS (
    SELECT br
    FROM infos_acidentes_br
    WHERE total_acidentes > 100
    ORDER BY taxa_mortalidade DESC
    LIMIT 10
)

SELECT 
    br AS BR,
	causa_acidente,
	SUM(mortos) AS total_mortos
FROM relational.acidentes
INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
WHERE br IN (SELECT br FROM br_mais_obitos)
GROUP BY br, causa_acidente
HAVING SUM(mortos) > 5
ORDER BY br, total_mortos DESC;
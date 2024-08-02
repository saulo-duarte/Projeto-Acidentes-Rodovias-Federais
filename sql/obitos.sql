SELECT
    SUM(mortos)
FROM relational.envolvidos;

CREATE VIEW total_envolvidos AS
    SELECT
        COUNT(*) AS total_envolvidos
    FROM relational.envolvidos;

SELECT
    SUM(mortos) / total_envolvidos.total_envolvidos AS taxa_mortalidade
FROM relational.envolvidos, total_envolvidos;

WITH total_envolvidos_ano AS (
    SELECT
        DATE_PART('YEAR', acidentes.data_completa) AS ano,
        COUNT(*) AS total_envolvidos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY ano
),
total_mortos_ano AS (
    SELECT
        DATE_PART('YEAR', acidentes.data_completa) AS ano,
        SUM(envolvidos.mortos) AS total_mortos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY ano
),
taxa_mortalidade_ano AS (
    SELECT
        te.ano,
        te.total_envolvidos,
        ROUND(tm.total_mortos::DECIMAL / te.total_envolvidos * 100, 2) AS taxa_mortalidade
    FROM total_envolvidos_ano te
    INNER JOIN total_mortos_ano tm ON te.ano = tm.ano
)

SELECT
    ano,
	
    taxa_mortalidade
FROM taxa_mortalidade_ano
ORDER BY ano;

WITH total_envolvidos_mes AS (
    SELECT
        DATE_PART('MONTH', acidentes.data_completa) AS mes,
        COUNT(*) AS total_envolvidos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY mes
    ),

total_mortos_mes AS (
    SELECT
        DATE_PART('MONTH', acidentes.data_completa) AS mes,
        SUM(envolvidos.mortos) AS total_mortos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY mes
    ),

taxa_mortalidade_mes AS (
    SELECT
        tem.mes,
        tem.total_envolvidos,
        tmm.total_mortos,
        ROUND(tmm.total_mortos::DECIMAL / tem.total_envolvidos * 100, 2) AS taxa_mortalidade
    FROM total_envolvidos_mes tem
    INNER JOIN total_mortos_mes tmm ON tem.mes = tmm.mes
    )

SELECT
    *
FROM taxa_mortalidade_mes
ORDER BY mes;

WITH total_envolvidos_semana AS (
    SELECT
        DATE_PART('DOW', acidentes.data_completa) AS semana,
        COUNT(*) AS total_envolvidos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY semana
    ),

total_mortos_semana AS (
    SELECT
        DATE_PART('DOW', acidentes.data_completa) AS semana,
        SUM(envolvidos.mortos) AS total_mortos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY semana
    ),

taxa_mortalidade_semana AS (
    SELECT
        tes.semana,
        tes.total_envolvidos,
        tms.total_mortos,
        ROUND(tms.total_mortos::DECIMAL / tes.total_envolvidos * 100, 2) AS taxa_mortalidade
    FROM total_envolvidos_semana tes
    INNER JOIN total_mortos_semana tms ON tes.semana = tms.semana
    )

SELECT
    *,
    CASE 
        WHEN semana = 0 THEN 'Domingo'
        WHEN semana = 1 THEN 'Segunda-feira'
        WHEN semana = 2 THEN 'Terça-feira'
        WHEN semana = 3 THEN 'Quarta-feira'
        WHEN semana = 4 THEN 'Quinta-feira'
        WHEN semana = 5 THEN 'Sexta-feira'
        WHEN semana = 6 THEN 'Sábado'
    END AS dia_semana
FROM taxa_mortalidade_semana
ORDER BY semana;

WITH total_envolvidos_hora AS (
    SELECT
        DATE_PART('HOUR', acidentes.data_completa) AS hora,
        COUNT(*) AS total_envolvidos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY hora
    ),

total_mortos_hora AS (
    SELECT
        DATE_PART('HOUR', acidentes.data_completa) AS hora,
        SUM(envolvidos.mortos) AS total_mortos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY hora
    ),

taxa_mortalidade_hora AS (
    SELECT
        teh.hora,
        teh.total_envolvidos,
        tmh.total_mortos,
        ROUND(tmh.total_mortos::DECIMAL / teh.total_envolvidos * 100, 2) AS taxa_mortalidade
    FROM total_envolvidos_hora teh
    INNER JOIN total_mortos_hora tmh ON teh.hora = tmh.hora
    )

SELECT
    *,
    RANK() OVER(ORDER BY taxa_mortalidade_hora) AS ranking
FROM taxa_mortalidade_hora
ORDER BY hora;

WITH total_envolvidos_hora_ano AS (
    SELECT
        DATE_PART('HOUR', acidentes.data_completa) AS hora,
        DATE_PART('YEAR', acidentes.data_completa) AS ano,
        COUNT(*) AS total_envolvidos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY hora, ano
    ),

total_mortos_hora_ano AS (
    SELECT
        DATE_PART('HOUR', acidentes.data_completa) AS hora,
        DATE_PART('YEAR', acidentes.data_completa) AS ano,
        SUM(envolvidos.mortos) AS total_mortos
    FROM relational.acidentes
    INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
    GROUP BY hora, ano
    ),

taxa_mortalidade_hora_ano AS (
    SELECT
        teha.hora,
        teha.ano,
        teha.total_envolvidos,
        tmha.total_mortos,
        ROUND(tmha.total_mortos::DECIMAL / teha.total_envolvidos * 100, 2) AS taxa_mortalidade
    FROM total_envolvidos_hora_ano teha
    INNER JOIN total_mortos_hora_ano tmha ON teha.hora = tmha.hora AND teha.ano = tmha.ano
    )

SELECT
    *,
    RANK() OVER(PARTITION BY ano ORDER BY taxa_mortalidade DESC) AS ranking
FROM taxa_mortalidade_hora_ano
ORDER BY ranking
LIMIT 20;

-- Tipos de acidentes
CREATE VIEW mortalidade_acidentes AS
WITH total_envolvidos_causa_acidente AS (
    SELECT
        ac.causa_acidente,
        COUNT(*) AS total_envolvidos
    FROM relational.acidentes ac
    INNER JOIN relational.envolvidos en ON ac.id = en.id_acidente
    GROUP BY causa_acidente
    ),

total_mortos_causa_acidente AS (
    SELECT
        ac.causa_acidente,
        SUM(en.mortos) AS total_mortos
    FROM relational.acidentes ac
    INNER JOIN relational.envolvidos en ON ac.id = en.id_acidente
    GROUP BY causa_acidente
    HAVING SUM(en.mortos) > 0
    ),

taxa_mortalidade_causa_acidente AS (
    SELECT
        tec.causa_acidente,
        tec.total_envolvidos,
        tmc.total_mortos,
        ROUND(tmc.total_mortos::DECIMAL / tec.total_envolvidos * 100, 2) AS taxa_mortalidade
    FROM total_envolvidos_causa_acidente tec
    INNER JOIN total_mortos_causa_acidente tmc ON tec.causa_acidente = tmc.causa_acidente
    )

SELECT
    *
FROM taxa_mortalidade_causa_acidente
ORDER BY taxa_mortalidade DESC;

WITH mortalidade_tipo_acidente AS (
    SELECT
        ac.tipo_acidente,
        COUNT(*) AS total_envolvidos,
        SUM(en.mortos) AS total_mortos,
        ROUND(SUM(en.mortos)::DECIMAL / COUNT(*) * 100, 2) AS taxa_mortalidade
    FROM relational.acidentes ac
    INNER JOIN relational.envolvidos en ON ac.id = en.id_acidente
    GROUP BY tipo_acidente
    HAVING SUM(en.mortos) > 0
    )

SELECT
    *
FROM mortalidade_tipo_acidente
ORDER BY taxa_mortalidade DESC;

-- Condição do metereologica

WITH total_envolvidos_condicao_metereologica AS (
    SELECT
        ac.condicao_metereologica,
        COUNT(*) AS total_envolvidos
    FROM relational.acidentes ac
    INNER JOIN relational.envolvidos en ON ac.id = en.id_acidente
    GROUP BY condicao_metereologica
    ),

total_mortos_condicao_metereologica AS (
    SELECT
        ac.condicao_metereologica,
        SUM(en.mortos) AS total_mortos
    FROM relational.acidentes ac
    INNER JOIN relational.envolvidos en ON ac.id = en.id_acidente
    GROUP BY condicao_metereologica
    HAVING SUM(en.mortos) > 0
    ),

taxa_mortalidade_condicao_metereologica AS (
    SELECT
        tec.condicao_metereologica,
        tec.total_envolvidos,
        tmc.total_mortos,
        ROUND(tmc.total_mortos::DECIMAL / tec.total_envolvidos * 100, 2) AS taxa_mortalidade
    FROM total_envolvidos_condicao_metereologica tec
    INNER JOIN total_mortos_condicao_metereologica tmc ON tec.condicao_metereologica = tmc.condicao_metereologica
    )

SELECT
    *
FROM taxa_mortalidade_condicao_metereologica
ORDER BY taxa_mortalidade DESC;

    
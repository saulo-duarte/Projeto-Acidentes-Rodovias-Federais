CREATE VIEW acidentes_fatais_regiao AS
	SELECT
		regiao,
		COUNT(*) AS total_acidentes_fatais
	FROM relational.acidentes
	WHERE classificacao_acidente = 'Com Vítimas Fatais'
	GROUP BY regiao;


CREATE VIEW acidentes_fatais_estado AS
	SELECT 
		estado,
		COUNT(*) AS total_acidentes_fatais
	FROM relational.acidentes
	WHERE classificacao_acidente = 'Com Vítimas Fatais'
	GROUP BY estado;


CREATE VIEW acidentes_fatais_municipio AS
	SELECT 
		municipio,
		COUNT(*) AS total_acidentes_fatais
	FROM relational.acidentes
	WHERE classificacao_acidente = 'Com Vítimas Fatais'
	GROUP BY municipio
	HAVING COUNT(*) > 25;


CREATE VIEW total_acidentes_regiao AS
	SELECT regiao, COUNT(*) AS total_acidentes
	FROM relational.acidentes
	GROUP BY regiao;


CREATE VIEW total_acidentes_estado AS
	SELECT
		estado,
		COUNT(*) AS total_acidentes
	FROM relational.acidentes
	GROUP BY estado;


CREATE VIEW total_acidentes_municipio AS
		SELECT 
			municipio,
			COUNT(*) AS total_acidentes
		FROM relational.acidentes
		GROUP BY municipio;


SELECT *
FROM total_acidentes_regiao;

SELECT *
FROM acidentes_fatais_regiao;

SELECT *
FROM total_acidentes_estado;

SELECT *
FROM acidentes_fatais_estado;

SELECT *
FROM total_acidentes_municipio;

SELECT *
FROM acidentes_fatais_municipio;

SELECT 
	tam.municipio, 
	afm.total_acidentes_fatais::DECIMAL / tam.total_acidentes * 100 AS taxa_mortalidade
FROM total_acidentes_municipio tam
RIGHT JOIN acidentes_fatais_municipio afm
	ON tam.municipio = afm.municipio
ORDER BY taxa_mortalidade DESC;

SELECT 
    at.regiao,
    af.total_acidentes_fatais::DECIMAL / at.total_acidentes * 100 AS taxa_mortalidade
FROM 
    total_acidentes_regiao at
LEFT JOIN 
    acidentes_fatais_regiao af ON at.regiao = af.regiao
ORDER BY taxa_mortalidade DESC;


SELECT 
	tae.estado, 
	afe.total_acidentes_fatais::DECIMAL / tae.total_acidentes * 100 AS taxa_mortalidade
FROM total_acidentes_estado tae
LEFT JOIN acidentes_fatais_estado afe
	ON tae.estado = afe.estado
ORDER BY taxa_mortalidade DESC;

WITH acidentes_fatais_municipio AS (
    SELECT 
        estado,
        municipio,
        COUNT(*) AS total_acidentes_fatais
    FROM relational.acidentes
    WHERE classificacao_acidente = 'Com Vítimas Fatais'
    GROUP BY estado, municipio
	HAVING COUNT(*) > 10
),

total_acidentes_municipio AS (
    SELECT 
        estado,
        municipio,
        COUNT(*) AS total_acidentes
    FROM relational.acidentes
    GROUP BY estado, municipio
),

taxa_mortalidade_municipio AS (
    SELECT 
        tam.estado,
        tam.municipio, 
        COALESCE(afm.total_acidentes_fatais::DECIMAL, 0) / tam.total_acidentes * 100 AS taxa_mortalidade,
        ROW_NUMBER() OVER (PARTITION BY tam.estado ORDER BY COALESCE(afm.total_acidentes_fatais::DECIMAL, 0) / tam.total_acidentes DESC) AS rn,
		tam.total_acidentes
    FROM total_acidentes_municipio tam
    LEFT JOIN acidentes_fatais_municipio afm
    ON tam.estado = afm.estado AND tam.municipio = afm.municipio
)

SELECT 
    estado,
    municipio, 
	total_acidentes,
    taxa_mortalidade
FROM 
    taxa_mortalidade_municipio
WHERE 
    rn <= 3
ORDER BY 
    estado, taxa_mortalidade DESC;

WITH total_envolvidos_estado_ano AS (
	SELECT
		ac.estado,
		DATE_PART('YEAR', ac.data_completa) AS ano,
		COUNT(*) AS total_envolvidos
	FROM relational.acidentes ac
	INNER JOIN relational.envolvidos en ON ac.id = en.id_acidente
	GROUP BY ac.estado, ano
),

total_mortos_estado_ano AS (
	SELECT
		ac.estado,
		DATE_PART('YEAR', ac.data_completa) AS ano,
		SUM(en.mortos) AS total_mortos
	FROM relational.acidentes ac
	INNER JOIN relational.envolvidos en ON ac.id = en.id_acidente
	GROUP BY ac.estado, ano
),

taxa_mortalidade_estado_ano AS (
	SELECT
		temea.estado,
		temea.ano,
		temea.total_envolvidos,
		tmea.total_mortos,
		ROUND(tmea.total_mortos::DECIMAL / temea.total_envolvidos * 100, 2) AS taxa_mortalidade
	FROM total_envolvidos_estado_ano temea
	INNER JOIN total_mortos_estado_ano tmea
	ON temea.estado = tmea.estado AND temea.ano = tmea.ano
)

SELECT
	*
FROM taxa_mortalidade_estado_ano
ORDER BY taxa_mortalidade;

-- Investigando a taxa de mortalidade no nordeste

SELECT
	*,
	RANK() OVER(ORDER BY taxa_mortalidade) AS ranking
FROM taxa_mortalidade_estado_ano
WHERE estado IN ('MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA', 'AM', 'AP', 'RR', 'RM', 'AC')
ORDER BY estado, ano;

-- Tipos de acidentes no maranhão e bahia
WITH causa_acidente_BA_MA AS (
	SELECT 
		estado,
		causa_acidente,
		COUNT(*) AS total_envolvidos,
		SUM(mortos) AS total_mortos,
		ROW_NUMBER() OVER(PARTITION BY estado ORDER BY SUM(mortos) DESC) AS rn
	FROM relational.acidentes ac
	INNER JOIN relational.envolvidos en ON ac.id = en.id_acidente
	WHERE ac.estado IN ('MA', 'BA')
	GROUP BY causa_acidente, estado
	ORDER BY total_envolvidos DESC
)

SELECT
	*
FROM causa_acidente_BA_MA
WHERE rn <= 10;

-- Tipos de acidentes no maranhão e bahia

WITH tipo_acidente_BA_MA AS(

	SELECT
		estado,
		tipo_acidente,
		COUNT(*) AS total_envolvidos,
		SUM(mortos) AS total_mortos,
		ROW_NUMBER() OVER(PARTITION BY estado ORDER BY SUM(mortos) DESC) AS rn
	FROM relational.acidentes ac
	INNER JOIN relational.envolvidos en ON ac.id = en.id_acidente
	WHERE ac.estado IN ('MA', 'BA')
	GROUP BY tipo_acidente, estado
	ORDER BY total_envolvidos DESC
)

SELECT
	*
FROM tipo_acidente_BA_MA
WHERE rn <= 10;

-- Tipos de veiculos
WITH tipo_veiculo_nordeste AS (
    SELECT
        tipo_veiculo,
        COUNT(*) AS total_envolvidos,
        SUM(mortos) AS total_mortos,
        ROUND(SUM(mortos)::DECIMAL / COUNT(*) * 100, 2) AS taxa_mortalidade_nordeste
    FROM relational.envolvidos
    INNER JOIN relational.acidentes ON envolvidos.id_acidente = acidentes.id
    WHERE regiao = 'Nordeste'
    GROUP BY tipo_veiculo
    ORDER BY total_envolvidos DESC
),

tipo_veiculo_norte AS (
	SELECT
		tipo_veiculo,
		ROUND(SUM(mortos)::DECIMAL / COUNT(*) * 100, 2) AS taxa_mortalidade
	FROM relational.envolvidos
	INNER JOIN relational.acidentes ON envolvidos.id_acidente = acidentes.id
	WHERE regiao = 'Norte'
	GROUP BY tipo_veiculo
),

tipo_veiculo_sudeste AS (
	SELECT
		tipo_veiculo,
		ROUND(SUM(mortos)::DECIMAL / COUNT(*) * 100, 2) AS taxa_mortalidade
	FROM relational.envolvidos
	INNER JOIN relational.acidentes ON envolvidos.id_acidente = acidentes.id
	WHERE regiao = 'Sudeste'
	GROUP BY tipo_veiculo
),

tipo_veiculo_sul AS (
	SELECT
		tipo_veiculo,
		ROUND(SUM(mortos)::DECIMAL / COUNT(*) * 100, 2) AS taxa_mortalidade
	FROM relational.envolvidos
	INNER JOIN relational.acidentes ON envolvidos.id_acidente = acidentes.id
	WHERE regiao = 'Sul'
	GROUP BY tipo_veiculo
),

tipo_veiculo_centro_oeste AS (
	SELECT
		tipo_veiculo,
		ROUND(SUM(mortos)::DECIMAL / COUNT(*) * 100, 2) AS taxa_mortalidade
	FROM relational.envolvidos
	INNER JOIN relational.acidentes ON envolvidos.id_acidente = acidentes.id
	WHERE regiao = 'Centro-Oeste'
	GROUP BY tipo_veiculo
),

tipo_veiculo_brasil AS (
    SELECT
        tipo_veiculo,
        ROUND(SUM(mortos)::DECIMAL / COUNT(*) * 100, 2) AS taxa_mortalidade
    FROM relational.envolvidos
    INNER JOIN relational.acidentes ON envolvidos.id_acidente = acidentes.id
    WHERE regiao <> 'Nordeste'
    GROUP BY tipo_veiculo
)

SELECT
	n.tipo_veiculo,
	n.total_envolvidos,
	n.total_mortos,
	n.taxa_mortalidade_nordeste,
	b.taxa_mortalidade AS taxa_mortalidade_brasil,
	no.taxa_mortalidade AS taxa_mortalidade_norte,
	s.taxa_mortalidade AS taxa_mortalidade_sudeste,
	su.taxa_mortalidade AS taxa_mortalidade_sul,
	co.taxa_mortalidade AS taxa_mortalidade_centro_oeste
FROM tipo_veiculo_nordeste n
INNER JOIN tipo_veiculo_brasil b
    ON n.tipo_veiculo = b.tipo_veiculo
INNER JOIN tipo_veiculo_norte no
	ON n.tipo_veiculo = no.tipo_veiculo
INNER JOIN tipo_veiculo_sudeste s
	ON n.tipo_veiculo = s.tipo_veiculo
INNER JOIN tipo_veiculo_sul su
	ON n.tipo_veiculo = su.tipo_veiculo
INNER JOIN tipo_veiculo_centro_oeste co
	ON n.tipo_veiculo = co.tipo_veiculo
ORDER BY n.total_envolvidos DESC;


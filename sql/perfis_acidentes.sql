-- Perfil dos acidentes graves

SELECT
    causa_acidente,
    tipo_acidente,
    SUM(feridos_graves) AS total_feridos_graves,
FROM relational.acidentes
INNER JOIN relational.envolvidos ON acidentes.id = envolvidos.id_acidente
GROUP BY causa_acidente, tipo_acidente
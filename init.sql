SET DATESTYLE TO PostgreSQL,European;

CREATE SCHEMA IF NOT EXISTS Relational;
CREATE TABLE Relational.Acidentes(
    id INT PRIMARY KEY,
    data_completa TIMESTAMP,
    regiao VARCHAR(30),
    estado VARCHAR(2),
    municipio VARCHAR(40),
    br VARCHAR(12),
    km DECIMAL(8,4),
    causa_acidente VARCHAR(120),
    tipo_acidente VARCHAR(60),
    classificacao_acidente VARCHAR(25),
    fase_dia VARCHAR(25),
    sentido_via VARCHAR(15),
    condicao_metereologica VARCHAR(25),
    tipo_pista VARCHAR(25),
    tracado_via VARCHAR(25),
    uso_solo VARCHAR(25),
    delegacia VARCHAR(25),
    latitude DECIMAL(11,8),
    longitude DECIMAL(11,8)
);

CREATE SEQUENCE Relational.id_envolvidos;
CREATE TABLE Relational.Envolvidos(
    id_envolvidos INT DEFAULT NEXTVAL('Relational.id_envolvidos'::regclass) PRIMARY KEY,
    id_acidente INT REFERENCES Relational.Acidentes(id),
    tipo_envolvido VARCHAR(40),
    tipo_veiculo VARCHAR(30),
    idade SMALLINT,
    sexo VARCHAR(10),
    ilesos SMALLINT,
    feridos_leves SMALLINT,
    feridos_graves SMALLINT,
    mortos SMALLINT
);

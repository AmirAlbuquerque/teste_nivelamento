-- Active: 1743008087358@@127.0.0.1@5432@ans_data
CREATE DATABASE ans_data;
-- Cria Tabela de Demostrativos Contábeis
CREATE TABLE demo_contabeis(
    id SERIAL PRIMARY KEY,
    data_oco DATE,
    registro_ans INT,
    conta_contabil INT,
    descricao VARCHAR(255),
    saldo_inicial TEXT,
    saldo_final TEXT
); 
-- Cria a tabela de operadoras ativas
CREATE TABLE operadoras_ativas(
    id SERIAL PRIMARY KEY,
    registro_ans INT,
    cnpj DECIMAL(15),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(100),
    numero VARCHAR(30),
    complemento VARCHAR(40),
    bairro VARCHAR(30),
    cidade VARCHAR(50),
    uf VARCHAR(2),
    cep INT,
    ddd INT,
    telefone VARCHAR(50),
    fax VARCHAR(40),
    email VARCHAR(50),
    representante VARCHAR(50),
    cargo_representante VARCHAR(40),
    regiao_comercializacao INT,
    data_registro_ans DATE
);

-- Importar dados para demo_contabeis - 1° Trimestre 2023
COPY demo_contabeis(data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final)
FROM 'C:\TCC\teste\1T2023.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
-- Importar dados para demo_contabeis - 2° Trimestre 2023
COPY demo_contabeis(data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final)
FROM 'C:\TCC\teste\2T2023.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
-- Importar dados para demo_contabeis - 3° Trimestre 2023
COPY demo_contabeis(data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final)
FROM 'C:\TCC\teste\3T2023.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
-- Importar dados para demo_contabeis - 4° Trimestre 2023
COPY demo_contabeis(data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final)
FROM 'C:\TCC\teste\4T2023.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
-- Importar dados para demo_contabeis - 1° Trimestre 2024
COPY demo_contabeis(data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final)
FROM 'C:\TCC\teste\1T2024.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
-- Importar dados para demo_contabeis - 2° Trimestre 2024
COPY demo_contabeis(data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final)
FROM 'C:\TCC\teste\2T2024.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
-- Importar dados para demo_contabeis - 3° Trimestre 2024
COPY demo_contabeis(data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final)
FROM 'C:\TCC\teste\3T2024.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
-- Importar dados para demo_contabeis - 4° Trimestre 2024
COPY demo_contabeis(data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final)
FROM 'C:\TCC\teste\4T2024.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- Altera de virgula para ponto nas colunas de saldo
UPDATE demo_contabeis
SET saldo_inicial = REPLACE(saldo_inicial, ',', '.')::DECIMAL(15,2),
    saldo_final = REPLACE(saldo_final, ',', '.')::DECIMAL(15,2);

-- Altera a coluna saldo final e inicial para tipo decimal
ALTER TABLE demo_contabeis 
ALTER COLUMN saldo_inicial TYPE DECIMAL(15,2) USING saldo_inicial::DECIMAL(15,2),
ALTER COLUMN saldo_final TYPE DECIMAL(15,2) USING saldo_final::DECIMAL(15,2);

-- Importar dados para operadoras_ativas
COPY operadoras_ativas(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, email, representante, cargo_representante, regiao_comercializacao, data_registro_ans)
FROM 'C:\TCC\teste\Relatorio_cadop.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- Cria nova tabela com a soma total por registro_ans do último trimestre
CREATE TABLE soma_total_trimestre AS
SELECT
    d.registro_ans,
    d.descricao,
    SUM(d.saldo_final) AS total_saldo_final,
    SUM(d.saldo_inicial) AS total_saldo_inicial
FROM demo_contabeis d
WHERE d.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
AND d.data_oco = '2024-10-01'
GROUP BY d.registro_ans, d.descricao
ORDER BY d.registro_ans

-- Cria nova tabela com a soma total por registro_ans do último ano
CREATE TABLE soma_total_anual AS
SELECT
    d.registro_ans,
    d.descricao,
    SUM(d.saldo_final) AS total_saldo_final,
    SUM(d.saldo_inicial) AS total_saldo_inicial
FROM demo_contabeis d
WHERE d.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
AND d.data_oco BETWEEN '2023-04-01' AND '2024-04-01'
GROUP BY d.registro_ans, d.descricao
ORDER BY d.registro_ans

-- Retorna as 10 operadoras com as maiores despesas do último trimestre
CREATE TABLE resultado_trimestral AS
SELECT
    oa.razao_social,
    stt.registro_ans,
    MAX(stt.total_saldo_final-stt.total_saldo_inicial) AS despesa,
    stt.descricao
FROM soma_total_trimestre stt
JOIN operadoras_ativas oa ON stt.registro_ans = oa.registro_ans
GROUP BY stt.registro_ans, oa.razao_social, stt.descricao
ORDER BY despesa DESC
LIMIT 10;

-- Retorna as 10 operadoras com as maiores despesas do último ano
CREATE TABLE resultado_anual AS
SELECT
    oa.razao_social,
    sta.registro_ans,
    MAX(sta.total_saldo_final-sta.total_saldo_inicial) AS despesa,
    sta.descricao
FROM soma_total_anual sta
JOIN operadoras_ativas oa ON sta.registro_ans = oa.registro_ans
GROUP BY sta.registro_ans, oa.razao_social, sta.descricao
ORDER BY despesa DESC
LIMIT 10;
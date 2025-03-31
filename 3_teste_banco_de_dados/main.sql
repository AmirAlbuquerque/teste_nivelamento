-- Active: 1743008087358@@127.0.0.1@5432@ans_dados
CREATE DATABASE ans_dados;
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

-- Importar dados para demo_contabeis
DO $$ 
DECLARE 
    -- Arquivos para importar
    arquivos TEXT[] := ARRAY[
        '1T2023.csv', '2T2023.csv', '3T2023.csv', '4T2023.csv',
        '1T2024.csv', '2T2024.csv', '3T2024.csv', '4T2024.csv'];
    arquivo TEXT;
    caminho_base TEXT := 'C:\Users\Public\teste_nivelamento\3_teste_banco_de_dados\db\';
    caminho_completo TEXT;
    qtd_linhas INT := 0;
BEGIN
    -- Criar tabela temporária para importação bruta
    CREATE TEMP TABLE temp_demo_contabeis (
        data_oco DATE,
        registro_ans INT,
        conta_contabil INT,
        descricao VARCHAR(255),
        saldo_inicial TEXT,
        saldo_final TEXT
    );
    -- Loop para importar arquivos .CSV
    FOREACH arquivo IN ARRAY arquivos LOOP
        caminho_completo := caminho_base || arquivo;
        RAISE NOTICE 'Processando arquivo: %...', caminho_completo;
        BEGIN
            EXECUTE format(
                'COPY temp_demo_contabeis(data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final) 
                FROM %L DELIMITER '';'' CSV HEADER ENCODING ''UTF8'';',
                caminho_completo);
            GET DIAGNOSTICS qtd_linhas = ROW_COUNT;
            RAISE NOTICE 'Arquivo % importado com % linhas', arquivo, qtd_linhas;
        EXCEPTION WHEN OTHERS THEN
            RAISE WARNING 'Erro ao processar arquivo %: %', arquivo, SQLERRM;
            CONTINUE;  -- Continua para o próximo arquivo mesmo com erro
        END;
    END LOOP;
    -- Inserir os dados convertidos corretamente na tabela final
    INSERT INTO demo_contabeis (data_oco, registro_ans, conta_contabil, descricao, saldo_inicial, saldo_final)
    SELECT data_oco, registro_ans, conta_contabil, descricao, 
           REPLACE(saldo_inicial, ',', '.')::DECIMAL(15,2), 
           REPLACE(saldo_final, ',', '.')::DECIMAL(15,2)
    FROM temp_demo_contabeis;
    -- Altera a coluna saldo final e inicial para tipo decimal
    ALTER TABLE demo_contabeis 
    ALTER COLUMN saldo_inicial TYPE DECIMAL(15,2) USING saldo_inicial::DECIMAL(15,2),
    ALTER COLUMN saldo_final TYPE DECIMAL(15,2) USING saldo_final::DECIMAL(15,2);
    -- Remover a tabela temporária ao final
    DROP TABLE temp_demo_contabeis;
END $$;

-- Importar dados para operadoras_ativas
COPY operadoras_ativas(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, email, representante, cargo_representante, regiao_comercializacao, data_registro_ans)
FROM 'C:\Users\Public\teste_nivelamento\3_teste_banco_de_dados\db\Relatorio_cadop.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- Cria tabela temporária com a soma total por registro_ans do último trimestre
CREATE TEMP TABLE temp_soma_total_trimestral AS
    SELECT
        d.registro_ans,
        d.descricao,
        SUM(d.saldo_final) AS total_saldo_final,
        SUM(d.saldo_inicial) AS total_saldo_inicial
    FROM demo_contabeis d
    WHERE d.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
    AND d.data_oco = '2024-10-01'
    GROUP BY d.registro_ans, d.descricao
    ORDER BY d.registro_ans;

-- Cria a tabela resultado_trimestral se ela não existir
CREATE TABLE IF NOT EXISTS resultado_trimestral (
    razao_social VARCHAR(255),
    registro_ans INT,
    despesa NUMERIC,
    descricao VARCHAR(255)
);

-- Limpa os dados se existe
TRUNCATE TABLE resultado_trimestral;

-- Insere os novos dados
INSERT INTO resultado_trimestral
SELECT
    oa.razao_social,
    stt.registro_ans,
    (stt.total_saldo_inicial - stt.total_saldo_final) AS despesa,
    stt.descricao
FROM temp_soma_total_trimestral stt
JOIN operadoras_ativas oa ON stt.registro_ans = oa.registro_ans
GROUP BY stt.registro_ans, oa.razao_social, stt.descricao
ORDER BY despesa DESC
LIMIT 10;

-- Remover a tabela temporária ao final
DROP TABLE temp_soma_total_trimestral;

-- Retorna as 10 operadoras com as maiores despesas do último ano
CREATE TEMP TABLE temp_soma_total_anual AS
    SELECT
        d.registro_ans,
        d.descricao,
        SUM(d.saldo_final) AS total_saldo_final,
        SUM(d.saldo_inicial) AS total_saldo_inicial
    FROM demo_contabeis d
    WHERE d.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
    AND d.data_oco BETWEEN '2023-04-01' AND '2024-04-01'
    GROUP BY d.registro_ans, d.descricao
    ORDER BY d.registro_ans;

-- Cria a tabela se ela não existir
CREATE TABLE IF NOT EXISTS resultado_anual (
    razao_social VARCHAR(255),
    registro_ans INT,
    despesa NUMERIC,
    descricao VARCHAR(255)
);

-- Limpa os dados se existe
TRUNCATE TABLE resultado_anual;

-- Insere os novos dados
INSERT INTO resultado_anual
SELECT
    oa.razao_social,
    sta.registro_ans,
    (sta.total_saldo_inicial - sta.total_saldo_final) AS despesa,
    sta.descricao
FROM temp_soma_total_anual sta
JOIN operadoras_ativas oa ON sta.registro_ans = oa.registro_ans
GROUP BY sta.registro_ans, oa.razao_social, sta.descricao
ORDER BY despesa DESC
LIMIT 10;

-- Remover a tabela temporária ao final
DROP TABLE temp_soma_total_anual;
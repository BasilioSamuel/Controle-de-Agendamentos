-- 1. Cria o banco de dados somente se ele ainda não existir
CREATE DATABASE IF NOT EXISTS sistema_atendimento;

-- 2. Seleciona o banco de dados para usar
USE sistema_atendimento;

-- 3. Cria a tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,         -- ID único para cada usuário
    nome VARCHAR(100) NOT NULL UNIQUE,                 -- Nome de login (não pode repetir)
    senha VARCHAR(255) NOT NULL                        -- Senha (iremos armazenar criptografada)
);

-- 4. Cria a tabela de atendimentos
CREATE TABLE IF NOT EXISTS atendimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,                 -- ID único do atendimento
    dia_semana VARCHAR(20),                            -- Dia da semana do atendimento
    nome_crianca VARCHAR(100)                          -- Nome da criança atendida
);

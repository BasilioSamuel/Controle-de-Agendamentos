CREATE DATABASE sistema_atendimento;
USE sistema_atendimento;


CREATE TABLE usuarios (
id_usuario INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL
);
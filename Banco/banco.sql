CREATE TABLE IF NOT EXISTS usuario 
(
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(15) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    foto BYTEA,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categoria
(
    id_categoria SERIAL PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) CHECK (tipo in ('receita', 'despesa')),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS receita 
(
    id_receita SERIAL PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    data_receita DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS despesa 
(
    id_despesa SERIAL PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    data_despesa DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS metas 
(
    id_meta SERIAL PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    data_meta DATE NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public.portifolio 
(
    id_portifolio SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao VARCHAR(700) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    valor_gasto  NUMERIC(10, 2) NOT NULL,
    valor_retorno  NUMERIC(10, 2) NOT NULL,
    data_inicio DATE,
    data_fim DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);
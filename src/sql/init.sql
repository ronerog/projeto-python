-- Criação da tabela de usuários
CREATE TABLE usuarios ( 
  id SERIAL PRIMARY KEY, 
  login VARCHAR(30) UNIQUE NOT NULL, 
  senha VARCHAR(255) NOT NULL 
);

-- Inserção de usuários
INSERT INTO usuarios (login, senha) VALUES
('admin', '123456'),
('user1', 'senha1');


-- Criação da tabela de fornecedores
CREATE TABLE fornecedores (
  fornecedor_id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  telefone VARCHAR(20),
  email VARCHAR(100),
  cnpj VARCHAR(20)
);

-- Inserção de fornecedores
INSERT INTO fornecedores (nome, telefone, email, cnpj) VALUES
('Fornecedor A', '11999999999', 'a@fornecedor.com', '00.000.000/0001-00'),
('Fornecedor B', '21988888888', 'b@fornecedor.com', '11.111.111/0001-11');


-- Criação da tabela de produtos
CREATE TABLE produtos (
  produto_id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  preco_venda DECIMAL(10, 2) NOT NULL
);

-- Inserção de produtos
INSERT INTO produtos (nome, preco_venda) VALUES
('Produto X', 10.00),
('Produto Y', 15.50),
('Produto Z', 25.00);


-- Criação da tabela de entrada de produtos
CREATE TABLE entrada_produtos (
  entrada_id SERIAL PRIMARY KEY,
  produto_id INTEGER NOT NULL REFERENCES produtos(produto_id),
  fornecedor_id INTEGER REFERENCES fornecedores(fornecedor_id),
  quantidade INTEGER NOT NULL,
  preco_custo DECIMAL(10, 2) NOT NULL,
  data_entrada DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Inserção de entradas de produtos
INSERT INTO entrada_produtos (produto_id, fornecedor_id, quantidade, preco_custo)
VALUES
(1, 1, 100, 7.50),
(2, 2, 50, 10.00);


-- Criação da tabela de vendas
CREATE TABLE vendas (
  venda_id SERIAL PRIMARY KEY,
  data_venda DATE NOT NULL DEFAULT CURRENT_DATE,
  total_geral DECIMAL(10, 2)
);

-- Inserção de vendas
INSERT INTO vendas (total_geral) VALUES
(100.00),
(155.00);


-- Criação da tabela de itens da venda
CREATE TABLE itens_venda (
  item_id SERIAL PRIMARY KEY,
  venda_id INTEGER NOT NULL REFERENCES vendas(venda_id),
  produto_id INTEGER NOT NULL REFERENCES produtos(produto_id),
  quantidade INTEGER NOT NULL,
  preco_unitario DECIMAL(10, 2) NOT NULL,
  preco_total DECIMAL(10, 2) GENERATED ALWAYS AS (quantidade * preco_unitario) STORED
);

-- Inserção de itens de venda
INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario) VALUES
(1, 1, 5, 10.00),
(1, 2, 2, 15.00),
(2, 3, 3, 25.00);
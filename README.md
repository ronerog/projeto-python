# Sistema de Cadastro e Gerenciamento

Um sistema simples para gerenciamento de usuários e produtos em Python.

## Descrição

Este projeto implementa um sistema de cadastro de usuários e gerenciamento de produtos via linha de comando (CLI). O sistema possui autenticação de usuários e funcionalidades completas de CRUD (Create, Read, Update, Delete) para produtos.

---

## Funcionalidades

### Usuários

- Cadastro de novos usuários  
- Login com autenticação  
- Validação de dados de usuário  

### Produtos

- Listar todos os produtos  
- Buscar produtos por nome ou ID  
- Cadastrar novos produtos  
- Editar produtos existentes  
- Excluir produtos  

---

## Estrutura do Projeto

```
projeto/
│
├── src/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada do programa
│   ├── login.py             # Funções de autenticação
│   ├── cadastro.py          # Funções de cadastro de usuários
│   ├── produtos.py          # Funções de gerenciamento de produtos
│   │
│   └── data/
│       ├── usuarios.py      # Banco de dados de usuários
│       └── produtos.py      # Banco de dados de produtos
│
├── .gitignore
└── README.md
```

---

## Como Usar

1. Clone o repositório  
2. Navegue até a pasta do projeto  
3. Execute o programa principal:

```bash
python -m src.main
```

4. Siga as instruções na interface de linha de comando:
   - Faça login com um usuário existente ou crie um novo usuário  
   - Acesse o menu de produtos após o login  
   - Gerencie produtos conforme necessário  

---

## Usuários Pré-cadastrados

- **adm** / `adm`  
- **maria** / `senha123`  
- **joao** / `abc123`  
- **teste** / `teste123`  
- **desenvolvedor** / `dev2025`  

---

## Regras de Validação

### Usuários

- Nome de usuário: 3–15 caracteres, apenas letras minúsculas e números  
- Senha: 5–100 caracteres, sem espaços em branco  

### Produtos

- Nome: mínimo 2 caracteres, não pode ser apenas números  
- Preço: deve ser um valor numérico maior que zero
- Quantdidade: deve ser um valor inteiro maior que zero    

---

## Requisitos

- Python 3.6 ou superior  

---
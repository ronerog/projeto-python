# Sistema de Cadastro e Gerenciamento

Um sistema simples para gerenciamento de usuários e produtos em Python.

---

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
- Buscar produtos por nome
- Cadastrar novos produtos  
- Editar produtos existentes  
- Excluir produtos  

---

## Estrutura do Projeto

```
projeto/
│
├── setup/                  # Scripts para setup do ambiente e Docker
│   └── docker/               
│     ├── __init__.py
│     ├── install.py          # Funcão para instalar e iniciar Docker via Winget no terminal
│   ├── setup.py              # Entry-point de instalação via terminal
│
├── src/                    # Código-fonte principal
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada do programa
│   ├── login.py             # Funções de autenticação
│   ├── cadastro.py          # Funções de cadastro de usuários
│   ├── produtos.py          # Funções de gerenciamento de produtos
│   └── data/
│       ├── usuarios.py      # Banco de dados de usuários
│       └── produtos.py      # Banco de dados de produtos
│
├── venv/                   # Ambiente virtual
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Como Usar

### 🛠️ Passo a passo para rodar o sistema:

1. **Ative o ambiente virtual:**

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Instale os utilitários (caso esteja sem Docker instalado):**

   ```powershell
   cd setup
   pip install .
   install-docker
   ```

3. **Volte para o diretório principal e entre na pasta `src`:**

   ```powershell
   cd ..
   cd src
   ```

4. **Suba os containers com Docker Compose:**

   ```powershell
   docker-compose up --build
   ```

5. **Acesse o container da aplicação e execute o programa:**

   ```powershell
   docker exec -it src-app-1 python main.py
   ```

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
- Quantidade: deve ser um valor inteiro maior que zero  

---

## Requisitos

- Docker

---
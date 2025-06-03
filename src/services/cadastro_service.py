import bcrypt
from data.conexao_banco import criar_conexao

def validacao_usuario(usuario):
    if len(usuario) < 3:
        raise ValueError("Nome do usuário não pode ter menos de 3 caracteres")
    if len(usuario) > 15:
        raise ValueError("Nome do usuário não pode ter mais de 15 caracteres")
    if usuario != usuario.lower():
        raise ValueError("Não é permitido letras maiúsculas")
    if not usuario.isalnum():
        raise ValueError("Não é permitido espaços em branco ou caracteres especiais")

def validacao_senha(senha):
    if len(senha) < 5:
        raise ValueError("A senha não pode ter menos de 5 caracteres")
    if len(senha) > 100:
        raise ValueError("A senha não pode ter mais de 100 caracteres")
    if not senha.strip():
        raise ValueError("Não é permitido espaços em branco")

def cadastrar(usuario, senha):
    erros = []

    try:
        validacao_usuario(usuario)
    except ValueError as e:
        erros.append(str(e))

    try:
        validacao_senha(senha)
    except ValueError as e:
        erros.append(str(e))

    if erros:
        return {"sucesso": False, "erros": erros}

    conn = criar_conexao()
    if conn is None:
        return {"sucesso": False, "erros": ["Erro ao conectar ao banco"]}

    try:
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM usuarios WHERE login = %s", (usuario,))
        if cur.fetchone():
            return {"sucesso": False, "erros": ["Usuário já existe"]}

        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cur.execute("INSERT INTO usuarios (login, senha) VALUES (%s, %s)", (usuario, senha_hash))
        conn.commit()
        return {"sucesso": True, "mensagem": "Usuário cadastrado com sucesso"}
    
    except Exception as e:
        return {"sucesso": False, "erros": [str(e)]}
    
    finally:
        cur.close()
        conn.close()

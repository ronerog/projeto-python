from data.usuarios import usuarios_db

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
        try:
            validacao_usuario(usuario)
        except ValueError as e:
            erros.append(str(e))

        try:
            validacao_senha(senha)
        except ValueError as e:
            erros.append(str(e))

        for user in usuarios_db:
            if user["login"] == usuario:
                erros.append("Usuário já existe")
                
        if erros:
            return {"sucesso": False, "erros": erros}

        novo_usuario = {'login': usuario, 'senha': senha}
        usuarios_db.append(novo_usuario)
        return {"sucesso": True, "mensagem": "Usuário cadastrado com sucesso"}

    except Exception as e:
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}

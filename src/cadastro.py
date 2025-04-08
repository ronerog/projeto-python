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
    lista = []
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

        if erros:
            return {"sucesso": False, "erros": erros}

        login = {'login': usuario, 'senha': senha}
        lista.append(login)
        return {"sucesso": True}

    except Exception as e:
        return {"sucesso": False, "erro": f"Erro inesperado: {str(e)}"}

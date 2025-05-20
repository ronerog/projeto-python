from data.usuarios import usuarios_db

def verificar_login(usuario, senha):
    try:
        for user in usuarios_db:
            if user["login"] == usuario and user["senha"] == senha:
                return {"sucesso": True, "mensagem": "Login efetuado com sucesso"}
        return {"sucesso": False, "erros": ["Usuário ou senha inválidos"]}
    except Exception as e:
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}
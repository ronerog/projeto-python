import bcrypt
from data.conexao_banco import criar_conexao

def verificar_login(usuario, senha):
    try:
        conn = criar_conexao()
        if conn is None:
            return {"sucesso": False, "erros": ["Erro ao conectar ao banco"]}

        cur = conn.cursor()
        cur.execute("SELECT senha FROM usuarios WHERE login = %s", (usuario,))
        resultado = cur.fetchone()

        if resultado is None:
            return {"sucesso": False, "erros": ["Usuário ou senha inválidos"]}

        senha_hash = resultado[0]
        if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
            return {"sucesso": True, "mensagem": "Login efetuado com sucesso"}
        else:
            return {"sucesso": False, "erros": ["Usuário ou senha inválidos"]}

    except Exception as e:
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

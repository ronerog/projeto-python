def verificar_login(usuario, senha):
    try:
        if(usuario == 'adm' and senha == 'adm' ):
            print("Login efetuado com sucesso")
        else: 
            print("Tente novamente...")
    except:
        usuario
from login import verificar_login
from cadastro import cadastrar

def inicio():
    login = False
    
    print("Menu Inicial")
    print("_________________________________________")
    print("Aperte 1 para Login")
    print("Aperte 2 para se Cadastrar")
    print("_________________________________________")
    entrada = int(input())
    
    if(entrada == 1):
        usuario = input("Coloque seu usuário: ")
        senha = input("Coloque sua senha: ")
        resultado = verificar_login(usuario, senha)
        if resultado["sucesso"] is False:
             for erro in resultado["erros"]:
                print(f"Erro: {erro}")
        else:
            print("Login Efetuado")
            # CONTINUAR LOGICA, CHAMAR MENU DE PRODUTOS
    elif(entrada == 2):
        usuario = input("Registre seu usuário: ")
        senha = input("Registre sua senha: ")
        resultado = cadastrar(usuario, senha)
        if resultado["sucesso"] is False:
             for erro in resultado["erros"]:
                print(f"Erro: {erro}")
        else:
            print("Cadastrado com sucesso")
    else:
        print("Digite 1 para login ou 2 para cadastrar")
inicio()
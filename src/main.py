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
        login = verificar_login(usuario, senha)
    elif(entrada == 2):
        usuario = input("Registre seu usuário: ")
        senha = input("Registre sua senha: ")
        cadastrar(usuario, senha)
    else:
        print("Digite 1 para login ou 2 para cadastrar")
inicio()
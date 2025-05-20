from services.login_service import verificar_login
from services.cadastro_service import cadastrar
from services.produtos_service import listar_todos_produtos, buscar_produto, editar_produto, excluir_produto, cadastrar_produto

def inicio():
    login = False
    
    while True:
        print("\n___________ MENU INICIAL ___________")
        print("-----------------------------------")
        print("1. Entrar")
        print("2. Cadastrar")
        print("0. Sair")
        print("-----------------------------------")
        
        try:
            entrada = int(input("Escolha uma opção: "))
            
            if entrada == 0:
                print("Saindo do sistema...")
                break
                
            elif entrada == 1:
                usuario = input("Coloque seu usuário: ")
                senha = input("Coloque sua senha: ")
                resultado = verificar_login(usuario, senha)
                
                if resultado["sucesso"] is False:
                    for erro in resultado["erros"]:
                        print(f"Erro: {erro}")
                else:
                    print("\nLogin Efetuado com Sucesso!")
                    menu_produtos_logado()
                        
            elif entrada == 2:
                usuario = input("Registre seu usuário: ")
                senha = input("Registre sua senha: ")
                resultado = cadastrar(usuario, senha)
                
                if resultado["sucesso"] is False:
                    for erro in resultado["erros"]:
                        print(f"Erro: {erro}")
                else:
                    print("\nCadastrado com sucesso")
            else:
                print("Digite 1 para login, 2 para cadastrar ou 0 para sair")
                
        except ValueError:
            print("Por favor, digite apenas números")

def menu_produtos_logado():
    while True:
        print("\n===== MENU DE PRODUTOS =====")
        print("1 - Listar todos os produtos")
        print("2 - Buscar produto")
        print("3 - Cadastrar novo produto")
        print("4 - Editar produto")
        print("5 - Excluir produto")
        print("0 - Voltar ao menu principal")
        
        try:
            opcao = int(input('Selecione uma opção: '))
            
            if opcao == 0:
                print("\nVoltando ao menu principal...")
                break
            elif opcao == 1:
                resultado = listar_todos_produtos()
                if resultado["sucesso"] is False:
                    for erro in resultado["erros"]:
                        print(f"Erro: {erro}")
            elif opcao == 2:
                nome = input("Digite o nome do produto: ")
                resultado = buscar_produto(nome=nome)
                if resultado["sucesso"]:
                    produto = resultado["produto"]
                    print(f"\nProduto encontrado:")
                    print(f"ID: {produto['id']}")
                    print(f"Nome: {produto['nome']}")
                    print(f"Preço: R$ {produto['preco']:.2f}")
                    print(f"Quantidade: {produto['quantidade']} unidade(s)")
                else:
                    for erro in resultado["erros"]:
                        print(f"Erro: {erro}")
            elif opcao == 3:
                nome = input("Digite o nome do novo produto: ")
                preco = input("Digite o preço do produto: ")
                quantidade = input("Digite a quantidade do produto: ")
                
                resultado = cadastrar_produto(nome, preco, quantidade)
                if resultado["sucesso"]:
                    print(resultado["mensagem"])
                else:
                    for erro in resultado["erros"]:
                        print(f"Erro: {erro}")
            elif opcao == 4:
                id_produto = int(input("Digite o ID do produto que deseja editar: "))
                nome = input("Novo nome (deixe em branco para manter o atual): ")
                preco = input("Novo preço (deixe em branco para manter o atual): ")
                quantidade = input("Nova quantidade (deixe em branco para manter o atual): ")
                
                resultado = editar_produto(id_produto, nome, preco, quantidade)
                if resultado["sucesso"]:
                    print(resultado["mensagem"])
                else:
                    for erro in resultado["erros"]:
                        print(f"Erro: {erro}")
            elif opcao == 5:
                nome = input("Digite o nome do produto que deseja excluir: ")
                resultado = excluir_produto(nome)
                if resultado["sucesso"]:
                    print(resultado["mensagem"])
                else:
                    for erro in resultado["erros"]:
                        print(f"Erro: {erro}")
            else:
                print('Selecione uma opção válida')
                
        except ValueError:
            print("Por favor, digite apenas números")

if __name__ == "__main__":
    inicio()
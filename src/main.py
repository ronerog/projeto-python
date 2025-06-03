from services.login_service import verificar_login
from services.cadastro_service import cadastrar
from services.produtos_service import listar_todos_produtos, buscar_produto, editar_produto, excluir_produto, cadastrar_produto, adicionar_fornecedor, listar_fornecedores, excluir_fornecedor

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
        print("6 - Adicionar fornecedor")
        print("7 - Listar fornecedores")
        print("8 - Excluir fornecedor")
        print("0 - Voltar ao menu principal")
        
        try:
            opcao = int(input('Selecione uma opção: '))
            
            if opcao == 0:
                print("\nVoltando ao menu principal...")
                break

            elif opcao == 1:
                resultado = listar_todos_produtos()
                
                if resultado["sucesso"]:
                    produtos = resultado["produtos"]
                    for produto in produtos:
                        print(produto)
                else:
                    for erro in resultado["erros"]:
                        print(f"Erro: {erro}")

            elif opcao == 2:
                nome = input("Digite o nome do produto: ")
                resultado = buscar_produto(nome=nome)
                if resultado["sucesso"]:
                    produtos = resultado["produtos"]
                    for produto in produtos:
                        print(f"\nProduto encontrado:")
                        print(f"ID: {produto['produto_id']}")
                        print(f"Nome: {produto['nome']}")
                        print(f"Preço: R$ {produto['preco_venda']:.2f}")
                        print(f"Quantidade: {produto['quantidade']} unidade(s)")
                        fornecedor_id = produto.get('fornecedor_id')
                        if fornecedor_id is not None:
                            print(f"Fornecedor ID: {fornecedor_id}")
                        else:
                            print("Fornecedor ID: Não informado")
                else:
                    print(f"Erro: {resultado['mensagem']}")

            elif opcao == 3:
                nome = input("Digite o nome do novo produto: ")
                preco = input("Digite o preço do produto: ")
                quantidade = input("Digite a quantidade do produto: ")
                fornecedor_id = input("Digite o ID do fornecedor: ")

                produto = {
                    'nome': nome,
                    'preco_venda': preco,
                    'quantidade': quantidade,
                    'fornecedor_id': int(fornecedor_id) if fornecedor_id.strip().isdigit() else None
                }


                resultado = cadastrar_produto(produto)

                if resultado["sucesso"]:
                    print(resultado["mensagem"])
                else:
                    print(f"Erro: {resultado['mensagem']}")

            elif opcao == 4:
                id_produto = int(input("Digite o ID do produto que deseja editar: "))
                nome = input("Novo nome (deixe em branco para manter o atual): ")
                preco = input("Novo preço (deixe em branco para manter o atual): ")
                quantidade = input("Nova quantidade (deixe em branco para manter o atual): ")
                fornecedor_id = input("Novo fornecedor (digite o ID ou deixe em branco): ")

                novos_dados = {}
                if nome.strip():
                    novos_dados['nome'] = nome
                if preco.strip():
                    try:
                        novos_dados['preco_venda'] = float(preco)
                    except ValueError:
                        print("Preço inválido.")
                        return
                if quantidade.strip():
                    try:
                        novos_dados['quantidade'] = int(quantidade)
                    except ValueError:
                        print("Quantidade inválida.")
                        return
                if fornecedor_id.strip():
                    try:
                        novos_dados['fornecedor_id'] = int(fornecedor_id)
                    except ValueError:
                        print("ID do fornecedor inválido.")
                        return

                resultado = editar_produto(id_produto, novos_dados)
                if resultado["sucesso"]:
                    print(resultado["mensagem"])
                else:
                    print(f"Erro: {resultado['mensagem']}")


            elif opcao == 5:
                id = input("Digite o ID do produto que deseja excluir: ")
                resultado = excluir_produto(id)
                if resultado["sucesso"]:
                    print(resultado["mensagem"])
                else:
                        print(f"Erro: {resultado['mensagem']}")

            elif opcao == 6:
                nome_fornecedor = input("Digite o nome do fornecedor: ")
                telefone = input("Digite o número de telefone (apenas números): ")
                email = input("Digite o email: ")
                cnpj = input("Digite o CNPJ (apenas números): ")

                fornecedor = {
                        'nome_fornecedor': nome_fornecedor,
                        'telefone': telefone,
                        'email': email,
                        'cnpj': cnpj
                    }

                resultado = adicionar_fornecedor(fornecedor)

                if not resultado["sucesso"]:
                    print(f"Erro: {resultado['mensagem']}")

            elif opcao == 7:
                resultado = listar_fornecedores()
                fornecedores = resultado["fornecedores"]
                for fornecedor in fornecedores:
                    print(fornecedor)
                if resultado["sucesso"] is False:
                    for erro in resultado["erros"]:
                        print(f"Erro: {erro}")

            elif opcao == 8:
                id = input("Digite o ID do fornecedor que deseja excluir: ")
                resultado = excluir_fornecedor(id)
                if resultado["sucesso"]:
                    print(resultado["mensagem"])
                else:
                        print(f"Erro: {resultado['mensagem']}")

            else:
                print('Selecione uma opção válida')
                
        except ValueError:
            print("Por favor, digite apenas números")

if __name__ == "__main__":
    inicio()
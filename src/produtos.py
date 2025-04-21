from data.produtos import produtos_db
import re

def validacao_produto(nome, preco, quantidade):
    erros = []
    if nome.isdigit():
        erros.append("Nome do produto deve ser uma string")

    if not nome or len(nome) < 2:
        erros.append("Nome do produto não pode ter menos de 2 caracteres")
    
    if re.search(r'\s{2,}', nome):
        erros.append("Nome do produto não pode conter espaços em branco consecutivos")
    
    try:
        preco_float = float(preco)
        if preco_float <= 0:
            erros.append("Preço deve ser maior que zero")
    except ValueError:
        erros.append("Preço deve ser um valor numérico válido")
    
    try:
        quatidade_int = int(quantidade)
        if quatidade_int < 0:
            erros.append("Quantidade deve ser maior ou igual a zero")
    except ValueError:
        erros.append("Quantidade deve ser um valor inteiro válido")

    return erros

def cadastrar_produto(nome, preco, quantidade):
    try:
        erros = validacao_produto(nome, preco, quantidade)
        
        # AQUI COLOCAMOS CASO JA EXISTA UM PRODUTO COM MESMO NOME, POIS NAO TEMOS DIFERENCIACAO COMO MARCA ETC.
        for produto in produtos_db:
            if produto["nome"] == nome:
                erros.append("Produto com este nome já existe")
        
        if erros:
            return {"sucesso": False, "erros": erros}
            
        proximo_id = 1
        if produtos_db:
            proximo_id = max(produto['id'] for produto in produtos_db) + 1
        
        produto = {
            'id': proximo_id,
            'nome': nome,
            'preco': float(preco),
            'quantidade': quantidade
        }
        produtos_db.append(produto)
        return {"sucesso": True, "mensagem": "\nProduto cadastrado com sucesso"}
    
    except Exception as e:
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}

def excluir_produto(nome):
    try:
        for i, produto in enumerate(produtos_db):
            if produto['nome'] == nome:
                produtos_db.pop(i)
                return {"sucesso": True, "mensagem": "\nProduto excluído com sucesso"}
        return {"sucesso": False, "erros": ["Produto não encontrado"]}
    except Exception as e:
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}

def editar_produto(id, nome=None, preco=None, quantidade=None):
    try:
        for i, produto in enumerate(produtos_db):
            if produto['id'] == id:
                erros = []
                
                # AQUI COLOCAMOS CASO JA EXISTA UM PRODUTO COM MESMO NOME, POIS NAO TEMOS DIFERENCIACAO COMO MARCA ETC.
                if nome:
                    for p in produtos_db:
                        if p['nome'] == nome and p['id'] != id:
                            erros.append("Já existe um produto com este nome")
                        if re.search(r'\s{2,}', nome):
                            erros.append("Nome do produto não pode conter espaços em branco consecutivos")
                if preco:
                    try:
                        preco_float = float(preco)
                        if preco_float <= 0:
                            erros.append("Preço deve ser maior que zero")
                    except ValueError:
                        erros.append("Preço inválido")
                
                if quantidade:
                    try:
                        quatidade_int = int(quantidade)
                        if quatidade_int <= 0:
                            erros.append("Quantidade deve ser maior ou igual a zero")
                    except ValueError:
                        erros.append("Quantidade inválida")
                
                if erros:
                    return {"sucesso": False, "erros": erros}
                
                if nome:
                    produtos_db[i]['nome'] = nome
                if preco:
                    produtos_db[i]['preco'] = float(preco)
                if quantidade:
                    produtos_db[i]['quantidade'] = int(quantidade)
                
                if not nome and not preco and not quantidade:
                    return {"sucesso": False, "erros": ["Nenhuma alteração realizada"]}
                    
                return {"sucesso": True, "mensagem": "\nProduto atualizado com sucesso"}
        return {"sucesso": False, "erros": ["Produto não encontrado"]}
    except Exception as e:
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}

def buscar_produto(nome=None, id=None):
    try:
        if nome:
            for produto in produtos_db:
                if produto['nome'] == nome:
                    return {"sucesso": True, "produto": produto}
        elif id:
            for produto in produtos_db:
                if produto['id'] == id:
                    return {"sucesso": True, "produto": produto}
        return {"sucesso": False, "erros": ["Produto não encontrado"]}
    except Exception as e:
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}

def listar_todos_produtos():
    try:
        if not produtos_db:
            return {"sucesso": False, "erros": ["Nenhum produto cadastrado"]}
        
        print("\n=============== LISTA DE PRODUTOS ===============")
        print("ID | NOME       | PREÇO  | QUANTIDADE(unidade(s))")
        print("-------------------------------------------------")
        
        for produto in produtos_db:
            nome_formatado = produto['nome']
            preco_formatado = f"R$ {produto['preco']:.2f}"
            print(f"{produto['id']}| {nome_formatado} | {preco_formatado} | {produto['quantidade']}")
        
        print("=================================================\n")
        return {"sucesso": True, "mensagem": f"Total de {len(produtos_db)} produtos listados"}
    
    except Exception as e:
        print("Erro ao listar produtos")
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}
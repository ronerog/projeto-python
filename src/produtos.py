from data.produtos import produtos_db

def validacao_produto(nome, preco):
    erros = []
    if nome.isdigit():
        erros.append("Nome do produto deve ser uma string")

    if not nome or len(nome) < 2:
        erros.append("Nome do produto não pode ter menos de 2 caracteres")
    
    try:
        preco_float = float(preco)
        if preco_float <= 0:
            erros.append("Preço deve ser maior que zero")
    except ValueError:
        erros.append("Preço deve ser um valor numérico válido")
    
    return erros

def cadastrar_produto(nome, preco):
    try:
        erros = validacao_produto(nome, preco)
        
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
            'preco': float(preco)
        }
        produtos_db.append(produto)
        return {"sucesso": True, "mensagem": "Produto cadastrado com sucesso"}
    
    except Exception as e:
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}

def excluir_produto(nome):
    try:
        for i, produto in enumerate(produtos_db):
            if produto['nome'] == nome:
                produtos_db.pop(i)
                return {"sucesso": True, "mensagem": "Produto excluído com sucesso"}
        return {"sucesso": False, "erros": ["Produto não encontrado"]}
    except Exception as e:
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}

def editar_produto(id, nome=None, preco=None):
    try:
        for i, produto in enumerate(produtos_db):
            if produto['id'] == id:
                erros = []
                
                # AQUI COLOCAMOS CASO JA EXISTA UM PRODUTO COM MESMO NOME, POIS NAO TEMOS DIFERENCIACAO COMO MARCA ETC.
                if nome:
                    for p in produtos_db:
                        if p['nome'] == nome and p['id'] != id:
                            erros.append("Já existe um produto com este nome")
                
                if preco:
                    try:
                        preco_float = float(preco)
                        if preco_float <= 0:
                            erros.append("Preço deve ser maior que zero")
                    except ValueError:
                        erros.append("Preço inválido")
                
                if erros:
                    return {"sucesso": False, "erros": erros}
                
                if nome:
                    produtos_db[i]['nome'] = nome
                if preco:
                    produtos_db[i]['preco'] = float(preco)
                
                if not nome and not preco:
                    return {"sucesso": False, "erros": ["Nenhuma alteração realizada"]}
                    
                return {"sucesso": True, "mensagem": "Produto atualizado com sucesso"}
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
        
        print("\n===== LISTA DE PRODUTOS =====")
        print("ID  | NOME                | PREÇO")
        print("-----------------------------------")
        
        for produto in produtos_db:
            nome_formatado = produto['nome']
            preco_formatado = f"R$ {produto['preco']:.2f}"
            print(f"{produto['id']}| {nome_formatado} | {preco_formatado}")
        
        print("===========================\n")
        return {"sucesso": True, "mensagem": f"Total de {len(produtos_db)} produtos listados"}
    
    except Exception as e:
        print("Erro ao listar produtos")
        return {"sucesso": False, "erros": [f"Erro inesperado: {str(e)}"]}
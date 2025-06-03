import psycopg2
from data.conexao_banco import criar_conexao

def validacao_produto(produto):
    if not produto.get('nome'):
        return {'sucesso': False, 'mensagem': "O campo nome é obrigatório."}
    if not isinstance(produto.get('nome'), str) or produto['nome'].strip() == "":
        return {'sucesso': False, 'mensagem': "O nome do produto não pode ser vazio."}
    if 'preco_venda' not in produto:
        return {'sucesso': False, 'mensagem': "O campo preco_venda é obrigatório."}
    try:
        preco = float(produto['preco_venda'])
    except (ValueError, TypeError):
        return {'sucesso': False, 'mensagem': "O campo preco_venda deve ser um número."}
    if preco < 0:
        return {'sucesso': False, 'mensagem': "O preco_venda não pode ser negativo."}
    return {'sucesso': True}

def validacao_produto(produto):
    if not produto.get('nome'):
        return {'sucesso': False, 'mensagem': "O campo nome é obrigatório."}
    if not isinstance(produto.get('nome'), str) or produto['nome'].strip() == "":
        return {'sucesso': False, 'mensagem': "O nome do produto não pode ser vazio."}
    if 'preco_venda' not in produto:
        return {'sucesso': False, 'mensagem': "O campo preco_venda é obrigatório."}
    try:
        preco = float(produto['preco_venda'])
    except (ValueError, TypeError):
        return {'sucesso': False, 'mensagem': "O campo preco_venda deve ser um número."}
    if preco < 0:
        return {'sucesso': False, 'mensagem': "O preco_venda não pode ser negativo."}
    
    if 'quantidade' in produto:
        try:
            qtd = int(produto['quantidade'])
        except (ValueError, TypeError):
            return {'sucesso': False, 'mensagem': "O campo quantidade deve ser um número inteiro."}
        if qtd < 0:
            return {'sucesso': False, 'mensagem': "A quantidade não pode ser negativa."}

    return {'sucesso': True}

def cadastrar_produto(produto):
    validacao = validacao_produto(produto)
    if not validacao['sucesso']:
        return validacao

    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        query = """
            INSERT INTO produtos (nome, preco_venda)
            VALUES (%s, %s) RETURNING produto_id;
        """
        cursor.execute(query, (produto['nome'], produto['preco_venda']))
        produto_id = cursor.fetchone()[0]

        query_entrada = """
            INSERT INTO entrada_produtos (produto_id, quantidade, preco_custo)
            VALUES (%s, %s, %s);
        """
        cursor.execute(query_entrada, (
            produto_id,
            produto['quantidade'],
            produto['preco_venda']
        ))

        conn.commit()
        return {
            'sucesso': True,
            'mensagem': "Produto cadastrado com sucesso.",
            'produto_id': produto_id
        }

    except Exception as e:
        return {'sucesso': False, 'mensagem': f"Erro ao cadastrar o produto: {e}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def excluir_produto(produto_id):
    
    if not produto_id or not str(produto_id).isdigit():
        return {'sucesso': False, 'mensagem': "ID do produto inválido. Por favor, informe um número inteiro."}
    
    conn = None
    cursor = None
    try:
        produto_id = int(produto_id)
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM produtos WHERE produto_id = %s;", (produto_id,))
        resultado = cursor.fetchone()
        if not resultado:
            return {'sucesso': False, 'mensagem': "Produto não encontrado."}
        nome_produto = resultado[0]
        cursor.execute("DELETE FROM produtos WHERE produto_id = %s;", (produto_id,))
        conn.commit()
        return {'sucesso': True, 'mensagem': f"Produto '{nome_produto}' excluído com sucesso."}
    except Exception as e:
        return {'sucesso': False, 'mensagem': f"Erro ao excluir o produto: {e}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def editar_produto(produto_id, novos_dados):
    if not novos_dados:
        return {'sucesso': False, 'mensagem': "Nenhum dado para atualizar."}

    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM produtos WHERE produto_id = %s;", (produto_id,))
        if not cursor.fetchone():
            return {'sucesso': False, 'mensagem': "Produto não encontrado."}

        campos = []
        valores = []
        if 'nome' in novos_dados:
            campos.append("nome = %s")
            valores.append(novos_dados['nome'])
        if 'preco_venda' in novos_dados:
            try:
                preco = float(novos_dados['preco_venda'])
                if preco < 0:
                    return {'sucesso': False, 'mensagem': "O preco_venda não pode ser negativo."}
                campos.append("preco_venda = %s")
                valores.append(preco)
            except (ValueError, TypeError):
                return {'sucesso': False, 'mensagem': "O campo preco_venda deve ser um número válido."}

        if campos:
            valores.append(produto_id)
            query = f"UPDATE produtos SET {', '.join(campos)} WHERE produto_id = %s;"
            cursor.execute(query, tuple(valores))

        if 'quantidade' in novos_dados:
            quantidade = int(novos_dados['quantidade'])
            if quantidade < 0:
                return {'sucesso': False, 'mensagem': "A quantidade não pode ser negativa."}
            cursor.execute("""
                INSERT INTO entrada_produtos (produto_id, quantidade, preco_custo)
                VALUES (%s, %s, 0);
            """, (produto_id, quantidade))

        conn.commit()
        return {'sucesso': True, 'mensagem': "Produto atualizado com sucesso."}
    except Exception as e:
        return {'sucesso': False, 'mensagem': f"Erro ao atualizar o produto: {e}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_produto(nome):
    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        query = """
            SELECT p.produto_id, p.nome, p.preco_venda, COALESCE(SUM(e.quantidade), 0) AS quantidade
            FROM produtos p
            LEFT JOIN entrada_produtos e ON p.produto_id = e.produto_id
            WHERE p.nome ILIKE %s
            GROUP BY p.produto_id, p.nome, p.preco_venda;
        """
        cursor.execute(query, (f'%{nome}%',))
        rows = cursor.fetchall()
        if not rows:
            return {'sucesso': False, 'mensagem': "Produto não encontrado."}
    
        produtos = []
        for row in rows:
            produtos.append({
                'produto_id': row[0],
                'nome': row[1],
                'preco_venda': float(row[2]),
                'quantidade': int(row[3])
            })
        return {'sucesso': True, 'produtos': produtos}

    except Exception as e:
        return {'sucesso': False, 'mensagem': f"Erro ao buscar o produto: {e}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def listar_todos_produtos():
    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        query = """
            SELECT p.produto_id, p.nome, p.preco_venda, COALESCE(SUM(e.quantidade), 0) AS quantidade
            FROM produtos p
            LEFT JOIN entrada_produtos e ON p.produto_id = e.produto_id
            GROUP BY p.produto_id, p.nome, p.preco_venda
            ORDER BY p.produto_id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        produtos = []
        for row in rows:
            produtos.append({
                'produto_id': row[0],
                'nome': row[1],
                'preco_venda': float(row[2]),
                'quantidade': int(row[3])
            })
        return {'sucesso': True, 'produtos': produtos}
    except Exception as e:
        return {'sucesso': False, 'mensagem': f"Erro ao listar produtos: {e}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

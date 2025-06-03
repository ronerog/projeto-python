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

    if 'fornecedor_id' not in produto:
        return {'sucesso': False, 'mensagem': "O campo fornecedor_id é obrigatório."}

    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM fornecedores WHERE fornecedor_id = %s;", (produto['fornecedor_id'],))
        if not cursor.fetchone():
            return {'sucesso': False, 'mensagem': "Fornecedor não encontrado."}
        
        query = """
            INSERT INTO produtos (nome, preco_venda)
            VALUES (%s, %s) RETURNING produto_id;
        """
        cursor.execute(query, (produto['nome'], produto['preco_venda']))
        produto_id = cursor.fetchone()[0]

        query_entrada = """
            INSERT INTO entrada_produtos (produto_id, fornecedor_id, quantidade, preco_custo)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query_entrada, (
            produto_id,
            produto['fornecedor_id'],
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

            fornecedor_id = novos_dados.get('fornecedor_id')
            if fornecedor_id is None:
                return {'sucesso': False, 'mensagem': "Fornecedor não informado para nova quantidade."}

            cursor.execute("SELECT * FROM fornecedores WHERE fornecedor_id = %s;", (fornecedor_id,))
            if not cursor.fetchone():
                return {'sucesso': False, 'mensagem': "Fornecedor não encontrado."}

            cursor.execute("""
                INSERT INTO entrada_produtos (produto_id, quantidade, preco_custo, fornecedor_id)
                VALUES (%s, %s, 0, %s);
            """, (produto_id, quantidade, fornecedor_id))

        elif 'fornecedor_id' in novos_dados:
            fornecedor_id = novos_dados['fornecedor_id']
            cursor.execute("SELECT * FROM fornecedores WHERE fornecedor_id = %s;", (fornecedor_id,))
            if not cursor.fetchone():
                    return {'sucesso': False, 'mensagem': "Fornecedor não encontrado."}

            cursor.execute("""
                INSERT INTO entrada_produtos (produto_id, quantidade, preco_custo, fornecedor_id)
                VALUES (%s, %s, 0, %s);
            """, (produto_id, 0, fornecedor_id))

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
            SELECT p.produto_id, p.nome, p.preco_venda, 
                   COALESCE(SUM(e.quantidade), 0) AS quantidade,
                   MAX(e.fornecedor_id) AS fornecedor_id
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
                'quantidade': int(row[3]),
                'fornecedor_id': row[4]
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

        cursor.execute("""
            SELECT p.produto_id, p.nome, p.preco_venda,
                   COALESCE(SUM(e.quantidade), 0) AS quantidade_total,
                   MAX(e.fornecedor_id) AS fornecedor_id
            FROM produtos p
            LEFT JOIN entrada_produtos e ON p.produto_id = e.produto_id
            GROUP BY p.produto_id, p.nome, p.preco_venda
            ORDER BY p.produto_id;
        """)

        produtos = []
        for row in cursor.fetchall():
            produto = {
                'produto_id': row[0],
                'nome': row[1],
                'preco_venda': float(row[2]),
                'quantidade': row[3],
                'fornecedor_id': row[4]
            }
            produtos.append(produto)

        return {'sucesso': True, 'produtos': produtos}

    except Exception as e:
        return {'sucesso': False, 'erros': [str(e)]}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def validacao_fornecedor(fornecedor):
    if not fornecedor.get('nome_fornecedor'):
        return {'sucesso': False, 'mensagem': "O campo nome é obrigatório."}
    if not isinstance(fornecedor.get('nome_fornecedor'), str) or fornecedor['nome_fornecedor'].strip() == "":
        return {'sucesso': False, 'mensagem': "O nome do fornecedor não pode ser vazio."}
    if 'telefone' not in fornecedor:
        return {'sucesso': False, 'mensagem': "O campo telefone é obrigatório."}
    try:
        fone = int(fornecedor['telefone'])
    except (ValueError, TypeError):
        return {'sucesso': False, 'mensagem': "O campo telefone deve ser um número."}
    if fone < 0:
        return {'sucesso': False, 'mensagem': "O telefone é inválido."}
    fone_str = str(fone)
    if not fone_str.isdigit() and len(fone_str) == 11:
        return {'sucesso': False, 'mensagem': "O telefone deve ter 11 digitos."}
    if not fornecedor.get('email'):
        return {'sucesso': False, 'mensagem': "O campo email é obrigatório."}
    if not isinstance(fornecedor.get('email'), str) or fornecedor['email'].strip() == "":
        return {'sucesso': False, 'mensagem': "O email não pode ser vazio."}
    if 'cnpj' not in fornecedor:
        return {'sucesso': False, 'mensagem': "O campo CNPJ é obrigatório."}
    try:
        pj = int(fornecedor['cnpj'])
    except (ValueError, TypeError):
        return {'sucesso': False, 'mensagem': "O campo CNPJ deve ser um número."}
    if pj < 0:
        return {'sucesso': False, 'mensagem': "O CNPJ é inválido."}
    pj_str = str(pj)
    if not pj_str.isdigit() and len(pj_str) == 14:
        return {'sucesso': False, 'mensagem': "O CNPJ deve ter 14 digitos."}
    
    return {'sucesso': True}

def adicionar_fornecedor(fornecedor):
    validacao = validacao_fornecedor(fornecedor)
    if not validacao['sucesso']:
        return validacao
    
    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        query = """
            INSERT INTO fornecedores (nome, telefone, email, cnpj)
            VALUES (%s, %s, %s, %s) RETURNING fornecedor_id;
        """
        cursor.execute(query, (fornecedor['nome_fornecedor'], fornecedor['telefone'], fornecedor['email'], fornecedor['cnpj']))
        fornecedor_id = cursor.fetchone()[0]

        conn.commit()
        return {
            'sucesso': True,
            'mensagem': "Fornecedor cadastrado com sucesso.",
            'fornecedor_id': fornecedor_id
        }

    except Exception as e:
        return {'sucesso': False, 'mensagem': f"Erro ao cadastrar o fornecedor: {e}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def listar_fornecedores():
    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        query = """
            SELECT f.fornecedor_id, f.nome, f.telefone, f.email, f.cnpj
            FROM fornecedores f
            GROUP BY f.fornecedor_id, f.nome, f.telefone, f.email, f.cnpj
            ORDER BY f.fornecedor_id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        fornecedores = []
        for row in rows:
            fornecedores.append({
                'fornecedor_id': row[0],
                'nome': row[1],
                'telefone': row[2],
                'email': row[3],
                'cnpj': row[4]
            })
        return {'sucesso': True, 'fornecedores': fornecedores}
    except Exception as e:
        return {'sucesso': False, 'mensagem': f"Erro ao listar fornecedores: {e}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def excluir_fornecedor(fornecedor_id):
    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM fornecedores WHERE fornecedor_id = %s;", (fornecedor_id,))
        resultado = cursor.fetchone()
        if not resultado:
            return {'sucesso': False, 'mensagem': "Fornecedor não encontrado."}
        nome_fornecedor = resultado[0]
        cursor.execute("DELETE FROM fornecedores WHERE fornecedor_id = %s;", (fornecedor_id,))
        conn.commit()
        return {'sucesso': True, 'mensagem': f"Fornecedor '{nome_fornecedor}' excluído com sucesso."}
    except Exception as e:
        return {'sucesso': False, 'mensagem': f"Erro ao excluir fornecedor: {e}"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
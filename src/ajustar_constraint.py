from data.conexao_banco import criar_conexao # ou ajuste conforme seu arquivo de conexão

def ajustar_fk_itens_venda():
    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        # Remove a constraint antiga
        cursor.execute("ALTER TABLE itens_venda DROP CONSTRAINT itens_venda_produto_id_fkey;")

        # Cria a nova constraint com ON DELETE CASCADE
        cursor.execute("""
            ALTER TABLE itens_venda
            ADD CONSTRAINT itens_venda_produto_id_fkey
            FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
            ON DELETE CASCADE;
        """)

        conn.commit()
        print("Constraint da tabela itens_venda atualizada com sucesso!")
    except Exception as e:
        print(f"Erro ao ajustar constraint itens_venda: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    ajustar_fk_itens_venda()
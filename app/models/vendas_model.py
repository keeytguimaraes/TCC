# Importa conexão
from app.database.conexao import conectar


# ==========================
# LISTAR VENDAS
# ==========================
def listar_vendas():

    # Conecta banco
    conexao = conectar()

    # Cursor dicionário
    cursor = conexao.cursor(
        dictionary=True
    )

    # SQL
    sql = """
        SELECT *

        FROM venda

        ORDER BY id DESC
    """

    # Executa
    cursor.execute(sql)

    # Busca vendas
    vendas = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna
    return vendas


# ==========================
# CADASTRAR VENDA
# ==========================
def cadastrar_venda(

    produto_id,

    quantidade,

    tipo_venda,

    valor_recebido,

    status_pagamento
):

    # Conecta banco
    conexao = conectar()

    # Cursor dicionário
    cursor = conexao.cursor(
        dictionary=True
    )

    # ----------------------
    # BUSCA PRODUTO
    # ----------------------
    sql_produto = """
        SELECT *

        FROM produto

        WHERE id = %s
    """

    # Executa
    cursor.execute(
        sql_produto,
        (produto_id,)
    )

    # Busca produto
    produto = cursor.fetchone()

    # ----------------------
    # PREÇO UNITÁRIO
    # ----------------------
    preco_unitario = (
        float(
            produto["preco_venda"]
        )
    )

    # ----------------------
    # SE FOR CAIXA
    # ----------------------
    if tipo_venda == "caixa":

        preco_unitario = (
            preco_unitario
            *
            produto[
                "quantidade_por_caixa"
            ]
        )

    # ----------------------
    # SUBTOTAL
    # ----------------------
    subtotal = (
        preco_unitario
        * int(quantidade)
    )

    # ----------------------
    # TROCO
    # ----------------------
    troco = (
        float(valor_recebido)
        - subtotal
    )

    # ----------------------
    # INSERT VENDA
    # ----------------------
    sql_venda = """
        INSERT INTO venda (

            valor_total,
            valor_recebido,
            troco,
            status_pagamento

        )
        VALUES (%s, %s, %s, %s)
    """

    # Executa
    cursor.execute(
        sql_venda,
        (
            subtotal,
            valor_recebido,
            troco,
            status_pagamento
        )
    )

    # ID venda
    venda_id = cursor.lastrowid

    # ----------------------
    # INSERT PRODUTO_VENDA
    # ----------------------
    sql_produto_venda = """
        INSERT INTO produto_venda (

            venda_id,
            produto_id,

            quantidade,
            tipo_venda,

            preco_unitario,
            subtotal

        )
        VALUES (
            %s, %s,
            %s, %s,
            %s, %s
        )
    """

    # Executa
    cursor.execute(
        sql_produto_venda,
        (
            venda_id,
            produto_id,

            quantidade,
            tipo_venda,

            preco_unitario,
            subtotal
        )
    )

    # ----------------------
    # BAIXA ESTOQUE
    # ----------------------
    sql_estoque = """
        SELECT *

        FROM estoque

        WHERE produto_id = %s

        ORDER BY id DESC

        LIMIT 1
    """

    # Executa
    cursor.execute(
        sql_estoque,
        (produto_id,)
    )

    # Busca estoque
    estoque = cursor.fetchone()

    # Quantidade atual
    atual_unidade = (
        estoque[
            "quantidade_atual_unidade"
        ]
    )

    atual_caixa = (
        estoque[
            "quantidade_atual_caixa"
        ]
    )

    # ----------------------
    # VENDA UNIDADE
    # ----------------------
    if tipo_venda == "unidade":

        novo_estoque = (
            atual_unidade
            - int(quantidade)
        )

        sql_update = """
            UPDATE estoque

            SET
                quantidade_atual_unidade = %s

            WHERE id = %s
        """

        cursor.execute(
            sql_update,
            (
                novo_estoque,
                estoque["id"]
            )
        )

    # ----------------------
    # VENDA CAIXA
    # ----------------------
    else:

        novo_estoque = (
            atual_caixa
            - int(quantidade)
        )

        sql_update = """
            UPDATE estoque

            SET
                quantidade_atual_caixa = %s

            WHERE id = %s
        """

        cursor.execute(
            sql_update,
            (
                novo_estoque,
                estoque["id"]
            )
        )

    # Salva banco
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()
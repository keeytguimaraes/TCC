from app.database.conexao import conectar

# ==========================
# LISTAR PRODUTOS
# ==========================
def listar_produtos_movimentacao():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT
            id,
            nome
        FROM produto
        WHERE ativo = TRUE
        ORDER BY nome
    """

    cursor.execute(sql)

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return produtos


# ==========================
# CADASTRAR MOVIMENTAÇÃO
# ==========================
def cadastrar_movimentacao(

    produto_id,
    tipo_movimentacao,
    quantidade_caixa,
    quantidade_unidade,
    quantidade_fracionada,
    motivo

):

    conexao = conectar()

    cursor = conexao.cursor()

    # ==========================
    # SALVA MOVIMENTAÇÃO
    # ==========================
    sql = """
INSERT INTO movimentacao_estoque (

    produto_id,
    tipo_movimentacao,
    quantidade_caixa,
    quantidade_unidade,
    quantidade_fracionada,
    motivo

)

VALUES (%s, %s, %s, %s, %s, %s)
"""

    cursor.execute(

    sql,

    (

        produto_id,
        tipo_movimentacao,
        quantidade_caixa,
        quantidade_unidade,
        quantidade_fracionada,
        motivo

    )
)

    # ==========================
    # BUSCA ÚLTIMO ESTOQUE
    # ==========================
    sql_estoque = """
        SELECT *

        FROM estoque

        WHERE produto_id = %s

        ORDER BY id DESC

        LIMIT 1
    """


    cursor.execute(

        sql_estoque,

        (
            produto_id,
        )
    )

    estoque = cursor.fetchone()

    if not estoque:

        conexao.commit()

        cursor.close()
        conexao.close()

        return
    
    # ==========================
    # BUSCA PRODUTO
    # ==========================
    sql_produto = """
    SELECT quantidade_por_caixa
    FROM produto
    WHERE id = %s
"""

    cursor.execute(
    sql_produto,
    (produto_id,)
)

    produto = cursor.fetchone()

    quantidade_por_caixa = produto[0] or 1

    # ==========================
    # COLUNAS DA TABELA
    # ==========================
    estoque_id = estoque[0]

    quantidade_atual_caixa = estoque[9] or 0

    quantidade_atual_unidade = estoque[10] or 0

    quantidade_atual_fracionada = estoque[17] or 0

    # ==========================
    # TOTAL DA MOVIMENTAÇÃO
    # ==========================

    movimentacao_total = (

    (quantidade_caixa * quantidade_por_caixa)

    + quantidade_unidade

)

    # ==========================
    # VALIDA ESTOQUE
    # ==========================

    if tipo_movimentacao != "ajuste_manual":

        if movimentacao_total > quantidade_atual_unidade:

            raise Exception(
            "Quantidade maior que o estoque disponível."
        )

        if quantidade_fracionada > quantidade_atual_fracionada:

           raise Exception(
            "Quantidade fracionada maior que o estoque."
        )

    # ==========================
    # CONVERTE ESTOQUE PARA TOTAL
    # ==========================

    total_unidades = quantidade_atual_unidade

    # ==========================
    # AJUSTA ESTOQUE
    # ==========================

    movimentacao_total = (

    (quantidade_caixa * quantidade_por_caixa)

    + quantidade_unidade

    + quantidade_fracionada

)

    if tipo_movimentacao == "ajuste_manual":

       total_unidades += movimentacao_total

    else:

       total_unidades -= movimentacao_total

    # ==========================
    # AJUSTA FRACIONADO
    # ==========================

    if tipo_movimentacao == "ajuste_manual":

        quantidade_atual_fracionada += quantidade_fracionada

    else:

        quantidade_atual_fracionada -= quantidade_fracionada
    
    # Evita negativo

    if total_unidades < 0:

        total_unidades = 0

    # ==========================
    # RECALCULA CAIXAS E UNIDADES
    # ==========================

    quantidade_atual_caixa = (

    total_unidades // quantidade_por_caixa

)
    quantidade_atual_unidade = total_unidades
    
    # ==========================
    # ATUALIZA ESTOQUE
    # ==========================
    sql_update = """
UPDATE estoque

SET

    quantidade_atual_caixa = %s,
    quantidade_atual_unidade = %s,
    quantidade_fracionada = %s,

    saida = saida + %s

WHERE id = %s
"""
    cursor.execute(

    sql_update,

    (

        quantidade_atual_caixa,
        quantidade_atual_unidade,
        quantidade_atual_fracionada,

        quantidade_caixa
        + quantidade_unidade
        + quantidade_fracionada,

        estoque_id

    )
)

    conexao.commit()

    cursor.close()

    conexao.close()

# ==========================
# HISTÓRICO MOVIMENTAÇÃO
# ==========================
def listar_movimentacoes():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            m.*,

            p.nome

        FROM movimentacao_estoque m

        INNER JOIN produto p
            ON p.id = m.produto_id

        ORDER BY
            m.data_movimentacao DESC
    """

    cursor.execute(sql)

    movimentacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return movimentacoes
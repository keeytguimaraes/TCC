# Importa conexão
from app.database.conexao import conectar


# ==========================
# LISTAR CONTAS PENDENTES
# ==========================
def listar_contas_pendentes():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
    SELECT

        venda.id,

        venda.nome_cliente_temporario,

        venda.valor_total,

        venda.data_venda

    FROM venda

    WHERE

        venda.status_pagamento = 'Pendente'

        AND

        venda.nome_cliente_temporario IS NOT NULL

    ORDER BY venda.id DESC
"""
    cursor.execute(sql)

    contas = cursor.fetchall()

    cursor.close()

    conexao.close()

    return contas
# ==========================
# BUSCAR PRODUTOS DA VENDA
# ==========================
def buscar_produtos_venda(

    venda_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            produto.nome,

            produto_venda.quantidade,

            produto_venda.tipo_venda

        FROM produto_venda

        INNER JOIN produto

            ON produto.id =
            produto_venda.produto_id

        WHERE produto_venda.venda_id = %s
    """

    cursor.execute(

        sql,

        (
            venda_id,
        )
    )

    produtos = cursor.fetchall()

    cursor.close()

    conexao.close()

    return produtos

    
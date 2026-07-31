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

    # ==========================
# BUSCAR CONTA ABERTA
# ==========================
def buscar_conta_aberta(cliente_id):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

        FROM conta

        WHERE cliente_id = %s

        AND status_conta = 'aberta'

        LIMIT 1
    """

    cursor.execute(

        sql,

        (
            cliente_id,
        )
    )

    conta = cursor.fetchone()

    cursor.close()

    conexao.close()

    return conta


# ==========================
# CRIAR CONTA
# ==========================
def criar_conta(cliente_id):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        INSERT INTO conta (

            cliente_id,

            status_conta,

            saldo_devedor

        )

        VALUES (

            %s,

            'aberta',

            0
        )
    """

    cursor.execute(

        sql,

        (
            cliente_id,
        )
    )

    conexao.commit()

    conta_id = cursor.lastrowid

    cursor.close()

    conexao.close()

    return conta_id


# ==========================
# ATUALIZAR SALDO
# ==========================
def atualizar_saldo_conta(

    conta_id,

    valor
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE conta

        SET

            saldo_devedor = saldo_devedor + %s

        WHERE id = %s
    """

    cursor.execute(

        sql,

        (
            valor,

            conta_id
        )
    )

    conexao.commit()

    cursor.close()

    conexao.close()


# ==========================
# BUSCAR CONTA POR ID
# ==========================
def buscar_conta_por_id(

    conta_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

        FROM conta

        WHERE id = %s
    """

    cursor.execute(

        sql,

        (
            conta_id,
        )
    )

    conta = cursor.fetchone()

    cursor.close()

    conexao.close()

    return conta
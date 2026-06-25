# Importa conexão
from app.database.conexao import conectar


# ==========================
# LISTAR FIADOS
# ==========================
def listar_fiados():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            venda.id,

            cliente.nome,

            venda.valor_total,

            venda.saldo_devedor,

            venda.data_venda

        FROM venda

        INNER JOIN cliente

            ON cliente.id =
            venda.cliente_id

        WHERE

            venda.status_pagamento =
            'Pendente'

            AND

            venda.cliente_id
            IS NOT NULL

        ORDER BY venda.id DESC
    """

    cursor.execute(sql)

    fiados = cursor.fetchall()

    cursor.close()

    conexao.close()

    return fiados


# ==========================
# BUSCAR PRODUTOS DO FIADO
# ==========================
def buscar_produtos_fiado(

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
# BUSCAR FIADO POR ID
# ==========================
def buscar_fiado_por_id(

    venda_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

        FROM venda

        WHERE id = %s
    """

    cursor.execute(

        sql,

        (
            venda_id,
        )
    )

    fiado = cursor.fetchone()

    cursor.close()

    conexao.close()

    return fiado

# ==========================
# RECEBER PAGAMENTO FIADO
# ==========================
def atualizar_saldo_fiado(

    venda_id,

    novo_saldo,

    status_pagamento
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE venda

        SET

            saldo_devedor = %s,

            status_pagamento = %s

        WHERE id = %s
    """

    cursor.execute(

        sql,

        (
            novo_saldo,
            status_pagamento,
            venda_id
        )
    )

    conexao.commit()

    cursor.close()

    conexao.close()

# ==========================
# REGISTRAR RECEBIMENTO
# ==========================
def registrar_recebimento_fiado(

    venda_id,

    valor_recebido
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        INSERT INTO recebimento_fiado (

            venda_id,

            valor_recebido

        )
        VALUES (%s, %s)
    """

    cursor.execute(

        sql,

        (
            venda_id,

            valor_recebido
        )
    )

    conexao.commit()

    cursor.close()

    conexao.close()

# ==========================
# BUSCAR RECEBIMENTOS
# ==========================
def buscar_recebimentos_fiado(

    venda_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            valor_recebido,

            data_recebimento

        FROM recebimento_fiado

        WHERE venda_id = %s

        ORDER BY data_recebimento DESC
    """

    cursor.execute(

        sql,

        (
            venda_id,
        )
    )

    recebimentos = cursor.fetchall()

    cursor.close()

    conexao.close()

    return recebimentos
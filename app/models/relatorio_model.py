from app.database.conexao import conectar


# ==========================
# TOTAL VENDIDO HOJE
# ==========================
def total_vendido_hoje():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            COALESCE(
                SUM(valor_total),
                0
            ) AS total

        FROM venda

        WHERE DATE(data_venda) =
        CURDATE()

        AND status_pagamento =
        'Pago'
    """

    cursor.execute(sql)

    resultado = cursor.fetchone()

    cursor.close()

    conexao.close()

    return resultado["total"]


# ==========================
# TOTAL VENDIDO MÊS
# ==========================
def total_vendido_mes():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            COALESCE(
                SUM(valor_total),
                0
            ) AS total

        FROM venda

        WHERE MONTH(data_venda) =
        MONTH(CURDATE())

        AND YEAR(data_venda) =
        YEAR(CURDATE())

        AND status_pagamento =
        'Pago'
    """

    cursor.execute(sql)

    resultado = cursor.fetchone()

    cursor.close()

    conexao.close()

    return resultado["total"]


# ==========================
# TOTAL FIADOS
# ==========================
def total_fiados():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            COALESCE(
                SUM(saldo_devedor),
                0
            ) AS total

        FROM venda

        WHERE cliente_id IS NOT NULL

        AND saldo_devedor > 0
    """

    cursor.execute(sql)

    resultado = cursor.fetchone()

    cursor.close()

    conexao.close()

    return resultado["total"]


# ==========================
# TOTAL PENDÊNCIAS
# ==========================
def total_pendencias():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            COALESCE(
                SUM(saldo_devedor),
                0
            ) AS total

        FROM venda

        WHERE conta_id IS NOT NULL

        AND saldo_devedor > 0
    """

    cursor.execute(sql)

    resultado = cursor.fetchone()

    cursor.close()

    conexao.close()

    return resultado["total"]
# ==========================
# FIADOS - QUANTIDADE
# ==========================
def grafico_fiados_quantidade():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            status_pagamento,

            COUNT(*) AS total

        FROM venda

        WHERE cliente_id IS NOT NULL

        GROUP BY status_pagamento
    """

    cursor.execute(sql)

    dados = cursor.fetchall()

    cursor.close()

    conexao.close()

    return dados
# ==========================
# FIADOS - VALOR
# ==========================
def grafico_fiados_valor():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            COALESCE(
                SUM(valor_total - saldo_devedor),
                0
            ) AS valor_pago,

            COALESCE(
                SUM(saldo_devedor),
                0
            ) AS valor_aberto

        FROM venda

        WHERE cliente_id IS NOT NULL
    """

    cursor.execute(sql)

    dados = cursor.fetchone()

    cursor.close()

    conexao.close()

    return dados
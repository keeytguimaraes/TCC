from app.database.conexao import conectar


def buscar_vendas_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            v.id,

            v.data_venda,

            COALESCE(
                c.nome,
                'Consumidor Final'
            ) AS cliente,

            v.valor_total,

            v.status_pagamento

        FROM venda v

        LEFT JOIN cliente c
            ON v.cliente_id = c.id

        WHERE DATE(v.data_venda)
        BETWEEN %s AND %s
    """

    if tipo_vendas == "pagas":

        sql += """
        AND v.status_pagamento = 'Pago'
    """

    elif tipo_vendas == "pendentes":

        sql += """
        AND v.status_pagamento = 'Pendente'
    """
    sql += """
    ORDER BY v.data_venda DESC
"""

    cursor.execute(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados

def total_vendas_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            COUNT(*) AS total

        FROM venda

        WHERE DATE(data_venda)
        BETWEEN %s AND %s
    """

    if tipo_vendas == "pagas":

        sql += """
        AND status_pagamento = 'Pago'
    """

    elif tipo_vendas == "pendentes":

        sql += """
        AND status_pagamento = 'Pendente'
    """

    cursor.execute(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado["total"]

def faturamento_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

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

        WHERE DATE(data_venda)
        BETWEEN %s AND %s
    """

    if tipo_vendas == "pagas":

        sql += """
        AND status_pagamento = 'Pago'
    """

    elif tipo_vendas == "pendentes":

        sql += """
        AND status_pagamento = 'Pendente'
    """

    cursor.execute(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado["total"]

def ticket_medio_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            COALESCE(
                AVG(valor_total),
                0
            ) AS ticket

        FROM venda

        WHERE DATE(data_venda)
        BETWEEN %s AND %s
    """

    if tipo_vendas == "pagas":

        sql += """
        AND status_pagamento = 'Pago'
    """

    elif tipo_vendas == "pendentes":

        sql += """
        AND status_pagamento = 'Pendente'
    """

    cursor.execute(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado["ticket"]

def quantidade_pagas_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            COUNT(*) AS total

        FROM venda

        WHERE DATE(data_venda)
        BETWEEN %s AND %s

        AND status_pagamento =
        'Pago'
    """

    cursor.execute(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado["total"]

def quantidade_pendentes_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            COUNT(*) AS total

        FROM venda

        WHERE DATE(data_venda)
        BETWEEN %s AND %s

        AND status_pagamento =
        'Pendente'
    """

    cursor.execute(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado["total"]

def total_recebido_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

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

        WHERE DATE(data_venda)
        BETWEEN %s AND %s

        AND status_pagamento =
        'Pago'
    """

    cursor.execute(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado["total"]

def total_pendente_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

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

        WHERE DATE(data_venda)
        BETWEEN %s AND %s

        AND status_pagamento =
        'Pendente'
    """

    cursor.execute(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado["total"]
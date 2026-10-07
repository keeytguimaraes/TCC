from app.database.conexao import conectar
from psycopg2.extras import RealDictCursor


def buscar_vendas_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
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
        AND v.status_pagamento = 'pago'
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
        cursor_factory=RealDictCursor
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
        AND status_pagamento = 'pago'
    """

    elif tipo_vendas == "pendentes":

        sql += """
        AND status_pagamento = 'pendente'
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
        cursor_factory=RealDictCursor
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
        AND status_pagamento = 'pago'
    """

    elif tipo_vendas == "pendentes":

        sql += """
        AND status_pagamento = 'pendente'
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
        cursor_factory=RealDictCursor
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
        AND status_pagamento = 'pago'
    """

    elif tipo_vendas == "pendentes":

        sql += """
        AND status_pagamento = 'pendente'
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
        cursor_factory=RealDictCursor
    )

    sql = """
        SELECT

            COUNT(*) AS total

        FROM venda

        WHERE DATE(data_venda)
        BETWEEN %s AND %s

        AND status_pagamento =
        'pago'
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
        cursor_factory=RealDictCursor
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
        cursor_factory=RealDictCursor
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
        'pago'
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
        cursor_factory=RealDictCursor
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

def buscar_vendas_dia(
    data
):

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
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

            v.valor_recebido,

            v.troco,

            v.status_pagamento

        FROM venda v

        LEFT JOIN cliente c
            ON v.cliente_id = c.id

        WHERE DATE(
            v.data_venda
        ) = %s

        ORDER BY
            v.data_venda
    """

    cursor.execute(
        sql,
        (data,)
    )

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados

def resumo_fechamento_dia(
    data
):

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    sql = """
       SELECT

            COUNT(*) AS total_vendas,

            COALESCE(
                SUM(valor_total),
                0
            ) AS total_vendido,

            COALESCE(
                SUM(
                    CASE
                        WHEN status_pagamento = 'pago'
                        THEN valor_total
                        ELSE 0
                    END
                ),
                0
            ) AS total_pago,

            COALESCE(
                SUM(
                    CASE
                        WHEN cliente_id IS NOT NULL
                        AND status_pagamento = 'pendente'
                        THEN valor_total
                        ELSE 0
                    END
                ),
                0
            ) AS total_fiado,

            COALESCE(
                SUM(
                    CASE
                        WHEN conta_pendente_id IS NOT NULL
                        AND status_pagamento = 'pendente'
                        THEN valor_total
                        ELSE 0
                    END
                ),
                0
            ) AS total_conta_pendente,

            COALESCE(
                SUM(troco),
                0
            ) AS total_troco,

            COALESCE(
                AVG(valor_total),
                0
            ) AS ticket_medio

        FROM venda

        WHERE DATE(data_venda) = %s
    """

    cursor.execute(
        sql,
        (data,)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado
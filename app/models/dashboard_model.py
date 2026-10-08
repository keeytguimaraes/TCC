from app.database.conexao import conectar
from psycopg2.extras import RealDictCursor

def buscar_indicadores_dashboard():

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    dados = {}

    # =====================
    # VENDIDO HOJE
    # =====================

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(valor_total),
                0
            ) AS total
        FROM venda
        WHERE DATE(data_venda) = CURRENT_DATE
    """)

    dados["vendido_hoje"] = (
        cursor.fetchone()["total"]
    )

    # =====================
    # VENDIDO MÊS
    # =====================

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(valor_total),
                0
            ) AS total
        FROM venda
        WHERE
            EXTRACT(
                MONTH FROM data_venda
            ) = EXTRACT(
                MONTH FROM CURRENT_DATE
            )
        AND
            EXTRACT(
                YEAR FROM data_venda
            ) = EXTRACT(
                YEAR FROM CURRENT_DATE
            )
    """)

    dados["vendido_mes"] = (
        cursor.fetchone()["total"]
    )

    # =====================
    # FIADOS
    # =====================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM conta
        WHERE status_conta = 'aberta'
    """)

    dados["fiados_abertos"] = (
        cursor.fetchone()["total"]
    )

    # =====================
    # CONTAS PENDENTES
    # =====================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM conta_pendente
        WHERE status = 'aberta'
    """)

    dados["contas_pendentes"] = (
        cursor.fetchone()["total"]
    )

    # =====================
    # ESTOQUE BAIXO
    # =====================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM estoque
        WHERE quantidade_atual_unidade <= 10
    """)

    dados["estoque_baixo"] = (
        cursor.fetchone()["total"]
    )

    cursor.close()
    conexao.close()

    return dados

# =====================
# ADMINISTRADOR
# =====================

def buscar_dashboard_administrador():

    dados = buscar_indicadores_dashboard()

    dados["ultimas_vendas"] = (
        buscar_ultimas_vendas()
    )

    dados["ultimas_movimentacoes"] = (
        buscar_ultimas_movimentacoes()
    )

    dados["alertas"] = (
        buscar_alertas_dashboard()
    )

    return dados

# =====================
# GERENTE
# =====================

def buscar_dashboard_gerente():

    dados = buscar_indicadores_dashboard()

    dados["ultimas_vendas"] = (
        buscar_ultimas_vendas()
    )

    dados["ultimas_movimentacoes"] = (
        buscar_ultimas_movimentacoes()
    )

    return dados


# =====================
# FUNCIONÁRIO
# =====================

def buscar_dashboard_funcionario(
    usuario_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    dados = {}

    # =====================
    # VENDAS DELE HOJE
    # =====================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM venda
        WHERE usuario_id = %s
        AND DATE(data_venda) = CURRENT_DATE
    """,
    (usuario_id,)
    )

    dados["vendas_hoje"] = (
        cursor.fetchone()["total"]
    )

    # =====================
    # VALOR VENDIDO HOJE
    # =====================

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(valor_total),
                0
            ) AS total
        FROM venda
        WHERE usuario_id = %s
        AND DATE(data_venda) = CURRENT_DATE
    """,
    (usuario_id,)
    )

    dados["valor_vendido"] = (
        cursor.fetchone()["total"]
    )

    # =====================
    # ÚLTIMAS VENDAS
    # =====================

    cursor.execute("""
        SELECT
            id,
            valor_total,
            data_venda
        FROM venda
        WHERE usuario_id = %s
        ORDER BY data_venda DESC
        LIMIT 5
    """,
    (usuario_id,)
    )

    dados["ultimas_vendas"] = (
        cursor.fetchall()
    )

    # =====================
    # CONTAS PENDENTES
    # =====================

    cursor.execute("""
        SELECT
            id,
            nome_cliente_temporario,
            data_abertura
        FROM conta_pendente
        WHERE usuario_id = %s
        ORDER BY data_abertura DESC
        LIMIT 5
    """,
    (usuario_id,)
    )

    dados["ultimas_contas"] = (
        cursor.fetchall()
    )

    cursor.close()
    conexao.close()

    return dados

def buscar_ultimas_vendas():

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute("""
        SELECT
            id,
            valor_total,
            data_venda
        FROM venda
        ORDER BY data_venda DESC
        LIMIT 5
    """)

    vendas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return vendas

def buscar_ultimas_movimentacoes():

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute("""
        SELECT
            tipo_movimentacao,
            motivo,
            data_movimentacao
        FROM movimentacao_estoque
        ORDER BY data_movimentacao DESC
        LIMIT 5
    """)

    movimentacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return movimentacoes

def buscar_alertas_dashboard():

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    alertas = []

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM estoque
        WHERE quantidade_atual_unidade <= 10
    """)

    estoque_baixo = (
        cursor.fetchone()["total"]
    )

    if estoque_baixo > 0:

        alertas.append(
            f"{estoque_baixo} produto(s) com estoque baixo"
        )

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM conta_pendente
        WHERE status = 'aberta'
    """)

    pendentes = (
        cursor.fetchone()["total"]
    )

    if pendentes > 0:

        alertas.append(
            f"{pendentes} conta(s) pendente(s)"
        )

    cursor.close()
    conexao.close()

    return alertas
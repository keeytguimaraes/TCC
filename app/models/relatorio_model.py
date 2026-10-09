
# ============================================================
# MODEL DE RELATÓRIOS
# ============================================================
# Este arquivo reúne as consultas utilizadas para gerar
# indicadores e gráficos financeiros do SIGC.
#
# Funcionalidades:
# - Calcular o total vendido no dia atual.
# - Calcular o total vendido no mês atual.
# - Calcular o total de saldos devedores de fiados.
# - Calcular o total de pendências sem cliente vinculado.
# - Consultar a quantidade de vendas agrupadas por status.
# - Consultar os valores pagos e em aberto dos fiados.
#
# Este model realiza consultas ao banco de dados e devolve
# os resultados para a camada responsável pelos relatórios.
# ============================================================


# Importa a função responsável por abrir uma conexão
# com o banco de dados PostgreSQL.
from app.database.conexao import conectar

# Permite acessar os resultados das consultas pelo nome
# das colunas, como resultado["total"].
from psycopg2.extras import RealDictCursor


# ============================================================
# TOTAL VENDIDO HOJE
# ============================================================

def total_vendido_hoje():
    """
    Calcula o valor total das vendas pagas na data atual.

    A consulta considera:
    - Vendas cuja data corresponde ao dia atual do banco.
    - Vendas com status_pagamento igual a 'pago'.

    Retorno:
        Valor total das vendas encontradas.
        Se não houver vendas correspondentes, retorna zero.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna o resultado como dicionário.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Soma o valor_total das vendas realizadas hoje e pagas.
    #
    # DATE(data_venda) considera apenas a parte da data,
    # desconsiderando a hora armazenada no campo.
    #
    # CURRENT_DATE representa a data atual do banco de dados.
    #
    # COALESCE substitui o resultado NULL da soma por zero
    # quando não existem vendas correspondentes.
    sql = """
        SELECT
            COALESCE(
                SUM(valor_total),
                0
            ) AS total

        FROM venda

        WHERE DATE(data_venda) = CURRENT_DATE

        AND status_pagamento = 'pago'
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera o único resultado produzido pela soma.
    resultado = cursor.fetchone()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna somente o valor calculado pela consulta.
    return resultado["total"]


# ============================================================
# TOTAL VENDIDO NO MÊS
# ============================================================

def total_vendido_mes():
    """
    Calcula o valor total das vendas pagas no mês e no ano atuais.

    A consulta compara separadamente:
    - O mês da data da venda com o mês atual.
    - O ano da data da venda com o ano atual.

    A comparação do ano impede que vendas de um mesmo mês,
    mas de anos anteriores, sejam incluídas no resultado.

    Retorno:
        Valor total das vendas pagas no período.
        Retorna zero quando não existem vendas correspondentes.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Soma as vendas pagas que pertencem ao mês e ao ano atuais.
    #
    # EXTRACT(MONTH FROM data_venda) obtém o mês da venda.
    # EXTRACT(YEAR FROM data_venda) obtém o ano da venda.
    #
    # CURRENT_DATE fornece a data atual utilizada na comparação.
    sql = """
        SELECT
            COALESCE(
                SUM(valor_total),
                0
            ) AS total

        FROM venda

        WHERE EXTRACT(MONTH FROM data_venda) =
              EXTRACT(MONTH FROM CURRENT_DATE)

        AND EXTRACT(YEAR FROM data_venda) =
            EXTRACT(YEAR FROM CURRENT_DATE)

        AND status_pagamento = 'pago'
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera o resultado da soma.
    resultado = cursor.fetchone()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Devolve o valor total calculado.
    return resultado["total"]


# ============================================================
# TOTAL DE FIADOS
# ============================================================

def total_fiados():
    """
    Calcula a soma dos saldos devedores das vendas que possuem
    cliente vinculado e saldo devedor positivo.

    A consulta considera:
    - cliente_id preenchido.
    - saldo_devedor maior que zero.

    Retorno:
        Soma dos saldos devedores encontrados.
        Retorna zero quando não há registros correspondentes.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Soma os saldos devedores das vendas que possuem um
    # cliente associado e saldo devedor positivo.
    #
    # Esta consulta mantém os critérios originais e não filtra
    # o resultado pelo status_pagamento.
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

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera o resultado da soma.
    resultado = cursor.fetchone()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna o total dos saldos devedores encontrados.
    return resultado["total"]


# ============================================================
# TOTAL DE PENDÊNCIAS
# ============================================================

def total_pendencias():
    """
    Calcula a soma dos saldos devedores de vendas pendentes
    que não possuem cliente vinculado.

    A consulta considera:
    - cliente_id igual a NULL.
    - status_pagamento igual a 'pendente'.
    - saldo_devedor maior que zero.

    Retorno:
        Soma dos saldos devedores encontrados.
        Retorna zero quando não existem registros correspondentes.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Soma os saldos devedores das vendas que correspondem
    # aos critérios de pendência definidos na consulta.
    sql = """
        SELECT
            COALESCE(
                SUM(saldo_devedor),
                0
            ) AS total

        FROM venda

        WHERE cliente_id IS NULL

        AND status_pagamento = 'pendente'

        AND saldo_devedor > 0
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera o resultado da soma.
    resultado = cursor.fetchone()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Retorna o total calculado.
    return resultado["total"]


# ============================================================
# GRÁFICO DE FIADOS — QUANTIDADE POR STATUS
# ============================================================

def grafico_fiados_quantidade():
    """
    Conta quantas vendas com cliente vinculado existem em
    cada status de pagamento.

    A consulta agrupa os registros pelo campo status_pagamento.

    Retorno:
        Lista de dicionários contendo:
        - status_pagamento;
        - total de vendas naquele status.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Agrupa as vendas pelo status de pagamento e conta
    # quantos registros existem em cada grupo.
    #
    # O filtro cliente_id IS NOT NULL mantém somente as vendas
    # associadas a um cliente.
    #
    # COUNT(*) conta os registros de venda de cada grupo.
    sql = """
        SELECT
            status_pagamento,
            COUNT(*) AS total

        FROM venda

        WHERE cliente_id IS NOT NULL

        GROUP BY status_pagamento
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera os grupos e suas respectivas quantidades.
    dados = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna os dados para montar o gráfico.
    return dados


# ============================================================
# GRÁFICO DE FIADOS — VALORES PAGOS E EM ABERTO
# ============================================================

def grafico_fiados_valor():
    """
    Calcula os valores pagos e em aberto das vendas que possuem
    cliente vinculado.

    A consulta calcula:
    - valor_pago: soma de valor_total menos saldo_devedor.
    - valor_aberto: soma dos saldos devedores.

    Retorno:
        Dicionário contendo valor_pago e valor_aberto.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Calcula os valores utilizados no gráfico.
    #
    # valor_pago:
    # Soma a diferença entre o valor total da venda e seu
    # saldo devedor.
    #
    # valor_aberto:
    # Soma os saldos devedores das vendas consideradas.
    #
    # COALESCE substitui resultados NULL por zero.
    #
    # O filtro mantém somente as vendas com cliente vinculado.
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

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera o único registro com os dois valores calculados.
    dados = cursor.fetchone()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Retorna os valores para a camada que monta o gráfico.
    return dados


# ============================================================
# MODEL DE RELATÓRIOS PDF
# ============================================================
# Este arquivo reúne as consultas utilizadas para gerar
# relatórios PDF de vendas e fechamento diário.
#
# Funcionalidades:
# - Consultar vendas dentro de um período.
# - Contar vendas de um período.
# - Calcular o faturamento de um período.
# - Calcular o ticket médio de um período.
# - Contar vendas pagas e pendentes.
# - Calcular os valores de vendas pagas e pendentes.
# - Consultar as vendas de uma data específica.
# - Calcular os indicadores do fechamento diário.
#
# As funções retornam os dados para o controller responsável
# por montar o relatório e gerar o arquivo PDF.
# ============================================================


# Importa a função responsável por conectar ao PostgreSQL.
from app.database.conexao import conectar

# Permite acessar os resultados das consultas pelo nome
# das colunas, como resultado["total_vendas"].
from psycopg2.extras import RealDictCursor


# ============================================================
# FUNÇÕES AUXILIARES DE CONSULTA
# ============================================================

def _consultar_todos(sql, parametros=()):
    """
    Executa uma consulta SQL e retorna todos os registros.

    Parâmetros:
        sql:
            Instrução SQL que será executada.

        parametros:
            Tupla com os valores utilizados nos parâmetros
            da consulta. O valor padrão é uma tupla vazia.

    Retorno:
        Lista de dicionários com todos os registros encontrados.

    Esta função centraliza a abertura e o fechamento dos
    recursos utilizados nas consultas que retornam várias linhas.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que transforma cada registro retornado
    # em um dicionário, permitindo acessar os campos pelo nome.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Executa a consulta com os parâmetros recebidos.
    # Os parâmetros são enviados separadamente do SQL.
    cursor.execute(sql, parametros)

    # Recupera todos os registros retornados pela consulta.
    dados = cursor.fetchall()

    # Fecha o cursor e a conexão após recuperar os resultados.
    cursor.close()
    conexao.close()

    # Retorna a lista de registros para a função solicitante.
    return dados


def _consultar_um(sql, parametros=()):
    """
    Executa uma consulta SQL e retorna um único registro.

    Parâmetros:
        sql:
            Instrução SQL que será executada.

        parametros:
            Tupla com os valores utilizados na consulta.

    Retorno:
        Dicionário com o registro encontrado ou None caso
        a consulta não retorne nenhuma linha.

    Esta função é utilizada para consultas de totais, médias
    e resumos que retornam um único registro.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Executa a consulta com os parâmetros recebidos.
    cursor.execute(sql, parametros)

    # Recupera somente o primeiro registro.
    resultado = cursor.fetchone()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Retorna o registro encontrado.
    return resultado


# ============================================================
# BUSCAR VENDAS DE UM PERÍODO
# ============================================================

def buscar_vendas_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):
    """
    Busca as vendas realizadas entre duas datas.

    Parâmetros:
        data_inicial:
            Data inicial do período.

        data_final:
            Data final do período.

        tipo_vendas:
            Define se a consulta deve considerar vendas pagas,
            pendentes ou todos os registros do período.

    Retorno:
        Lista de vendas contendo identificador, data, cliente,
        valor total e status do pagamento.

    Quando não existe um cliente associado, o nome apresentado
    no resultado será 'Consumidor Final'.
    """

    # Consulta os dados das vendas e relaciona cada registro
    # ao cliente correspondente, quando houver.
    #
    # O LEFT JOIN permite incluir vendas sem cliente vinculado.
    #
    # COALESCE substitui o nome NULL pelo texto 'Consumidor Final'.
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

        WHERE DATE(v.data_venda) BETWEEN %s AND %s
    """

    # Define os parâmetros da consulta na ordem dos marcadores:
    # primeiro a data inicial e depois a data final.
    parametros = [
        data_inicial,
        data_final
    ]

    # Quando o tipo solicitado é "pagas", limita os resultados
    # às vendas cujo status seja exatamente 'pago'.
    if tipo_vendas == "pagas":
        sql += """
            AND v.status_pagamento = 'pago'
        """

    # Quando o tipo solicitado é "pendentes", utiliza o status
    # 'Pendente', preservando a condição do código original.
    elif tipo_vendas == "pendentes":
        sql += """
            AND v.status_pagamento = 'Pendente'
        """

    # Ordena as vendas pela data, começando pelas mais recentes.
    sql += """
        ORDER BY v.data_venda DESC
    """

    # Executa a consulta e retorna todas as vendas encontradas.
    return _consultar_todos(sql, tuple(parametros))


# ============================================================
# TOTAL DE VENDAS DE UM PERÍODO
# ============================================================

def total_vendas_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):
    """
    Conta quantas vendas existem no período informado.

    O filtro de status depende do valor de tipo_vendas:
    - "pagas": considera status 'pago'.
    - "pendentes": considera status 'pendente'.

    Retorno:
        Número de vendas que correspondem aos filtros.
    """

    # COUNT(*) conta os registros que atendem aos filtros.
    sql = """
        SELECT
            COUNT(*) AS total

        FROM venda

        WHERE DATE(data_venda) BETWEEN %s AND %s
    """

    # Armazena os parâmetros das datas.
    parametros = [
        data_inicial,
        data_final
    ]

    # Acrescenta o filtro de vendas pagas quando solicitado.
    if tipo_vendas == "pagas":
        sql += """
            AND status_pagamento = 'pago'
        """

    # Acrescenta o filtro de pendências quando solicitado.
    # A grafia 'pendente' é mantida como no código original.
    elif tipo_vendas == "pendentes":
        sql += """
            AND status_pagamento = 'pendente'
        """

    # Executa a consulta, que retorna um único registro.
    resultado = _consultar_um(sql, tuple(parametros))

    # Retorna apenas a quantidade calculada.
    return resultado["total"]


# ============================================================
# FATURAMENTO DE UM PERÍODO
# ============================================================

def faturamento_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):
    """
    Calcula a soma do valor_total das vendas no período.

    O filtro de status depende de tipo_vendas:
    - "pagas": considera vendas com status 'pago'.
    - "pendentes": considera vendas com status 'pendente'.

    Retorno:
        Soma dos valores totais das vendas encontradas.
        Quando não existem registros, retorna zero.
    """

    # Soma os valores das vendas dentro do intervalo de datas.
    #
    # COALESCE substitui NULL por zero caso a soma não tenha
    # valores para calcular.
    sql = """
        SELECT
            COALESCE(
                SUM(valor_total),
                0
            ) AS total

        FROM venda

        WHERE DATE(data_venda) BETWEEN %s AND %s
    """

    # Inicializa os parâmetros com as datas do período.
    parametros = [
        data_inicial,
        data_final
    ]

    # Aplica o filtro de pagamento quando solicitado.
    if tipo_vendas == "pagas":
        sql += """
            AND status_pagamento = 'pago'
        """

    # Aplica o filtro de pendências quando solicitado.
    elif tipo_vendas == "pendentes":
        sql += """
            AND status_pagamento = 'pendente'
        """

    # Executa a consulta e recupera o total calculado.
    resultado = _consultar_um(sql, tuple(parametros))

    # Retorna o valor total.
    return resultado["total"]


# ============================================================
# TICKET MÉDIO DE UM PERÍODO
# ============================================================

def ticket_medio_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):
    """
    Calcula o valor médio das vendas no período informado.

    A média é calculada pelo banco usando AVG(valor_total).

    O filtro de status depende de tipo_vendas:
    - "pagas": considera vendas com status 'pago'.
    - "pendentes": considera vendas com status 'pendente'.

    Retorno:
        Média dos valores das vendas encontradas.
        Quando não existem vendas, retorna zero.
    """

    # AVG calcula a média dos valores totais das vendas.
    #
    # COALESCE retorna zero quando não há valores para calcular.
    sql = """
        SELECT
            COALESCE(
                AVG(valor_total),
                0
            ) AS ticket

        FROM venda

        WHERE DATE(data_venda) BETWEEN %s AND %s
    """

    # Armazena as datas utilizadas no filtro.
    parametros = [
        data_inicial,
        data_final
    ]

    # Filtra as vendas pagas, caso tenham sido solicitadas.
    if tipo_vendas == "pagas":
        sql += """
            AND status_pagamento = 'pago'
        """

    # Filtra as vendas pendentes, caso tenham sido solicitadas.
    elif tipo_vendas == "pendentes":
        sql += """
            AND status_pagamento = 'pendente'
        """

    # Executa a consulta de média.
    resultado = _consultar_um(sql, tuple(parametros))

    # Retorna o ticket médio calculado.
    return resultado["ticket"]


# ============================================================
# QUANTIDADE DE VENDAS PAGAS NO PERÍODO
# ============================================================

def quantidade_pagas_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):
    """
    Conta as vendas pagas entre as datas informadas.

    Observação:
        O parâmetro tipo_vendas é mantido por compatibilidade
        com as chamadas existentes, mas não é utilizado nesta
        consulta, conforme o código original.

    Retorno:
        Quantidade de vendas com status 'pago' no período.
    """

    # Conta as vendas no intervalo e aplica o filtro fixo
    # de status_pagamento igual a 'pago'.
    sql = """
        SELECT
            COUNT(*) AS total

        FROM venda

        WHERE DATE(data_venda) BETWEEN %s AND %s

        AND status_pagamento = 'pago'
    """

    # Executa a consulta utilizando as datas recebidas.
    resultado = _consultar_um(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    # Retorna a quantidade de vendas pagas.
    return resultado["total"]


# ============================================================
# QUANTIDADE DE VENDAS PENDENTES NO PERÍODO
# ============================================================

def quantidade_pendentes_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):
    """
    Conta as vendas pendentes entre as datas informadas.

    Observação:
        O parâmetro tipo_vendas é mantido por compatibilidade
        com as chamadas existentes, mas não é utilizado nesta
        consulta, conforme o código original.

    Retorno:
        Quantidade de vendas cujo status seja 'Pendente'.
    """

    # Conta as vendas do período com o status 'Pendente'.
    # A inicial maiúscula é mantida conforme o código original.
    sql = """
        SELECT
            COUNT(*) AS total

        FROM venda

        WHERE DATE(data_venda) BETWEEN %s AND %s

        AND status_pagamento = 'Pendente'
    """

    # Executa a consulta para o intervalo solicitado.
    resultado = _consultar_um(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    # Retorna a quantidade de pendências encontradas.
    return resultado["total"]


# ============================================================
# TOTAL RECEBIDO NO PERÍODO
# ============================================================

def total_recebido_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):
    """
    Soma o valor_total das vendas pagas no período.

    Observação:
        O parâmetro tipo_vendas é mantido por compatibilidade
        com as chamadas existentes, mas não é utilizado nesta
        consulta, conforme o código original.

    Retorno:
        Soma dos valores totais das vendas com status 'pago'.
    """

    # Soma os valores das vendas pagas dentro do intervalo.
    #
    # Esta consulta soma valor_total, não valor_recebido.
    # Essa escolha é preservada conforme o código original.
    sql = """
        SELECT
            COALESCE(
                SUM(valor_total),
                0
            ) AS total

        FROM venda

        WHERE DATE(data_venda) BETWEEN %s AND %s

        AND status_pagamento = 'pago'
    """

    # Executa a consulta usando as datas informadas.
    resultado = _consultar_um(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    # Retorna a soma calculada.
    return resultado["total"]


# ============================================================
# TOTAL PENDENTE NO PERÍODO
# ============================================================

def total_pendente_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):
    """
    Soma o valor_total das vendas pendentes no período.

    Observação:
        O parâmetro tipo_vendas é mantido por compatibilidade
        com as chamadas existentes, mas não é utilizado nesta
        consulta, conforme o código original.

    Retorno:
        Soma dos valores totais das vendas com status 'Pendente'.
    """

    # Soma os valores totais das vendas pendentes no intervalo.
    #
    # A grafia 'Pendente' é mantida conforme o código original.
    sql = """
        SELECT
            COALESCE(
                SUM(valor_total),
                0
            ) AS total

        FROM venda

        WHERE DATE(data_venda) BETWEEN %s AND %s

        AND status_pagamento = 'Pendente'
    """

    # Executa a consulta com as datas recebidas.
    resultado = _consultar_um(
        sql,
        (
            data_inicial,
            data_final
        )
    )

    # Retorna o total calculado.
    return resultado["total"]


# ============================================================
# BUSCAR VENDAS DE UM DIA
# ============================================================

def buscar_vendas_dia(data):
    """
    Busca todas as vendas realizadas em uma data específica.

    Parâmetro:
        data: data que será consultada.

    Retorno:
        Lista de vendas contendo:
        - Identificador;
        - Data e hora da venda;
        - Nome do cliente ou 'Consumidor Final';
        - Valor total;
        - Valor recebido;
        - Troco;
        - Status do pagamento.

    As vendas são ordenadas pela data em ordem crescente.
    """

    # Consulta os dados das vendas e o nome do cliente associado.
    #
    # O LEFT JOIN permite retornar vendas sem cliente vinculado.
    # COALESCE substitui o nome ausente por 'Consumidor Final'.
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

        WHERE DATE(v.data_venda) = %s

        ORDER BY v.data_venda
    """

    # Executa a consulta para a data informada.
    dados = _consultar_todos(sql, (data,))

    # Retorna a lista de vendas daquele dia.
    return dados


# ============================================================
# RESUMO DO FECHAMENTO DIÁRIO
# ============================================================

def resumo_fechamento_dia(data):
    """
    Calcula os indicadores de fechamento para uma data.

    Indicadores retornados:
    - total_vendas: quantidade de vendas realizadas.
    - total_vendido: soma do valor_total de todas as vendas.
    - total_pago: soma dos valores das vendas com status 'pago'.
    - total_fiado: soma de vendas pendentes com cliente vinculado.
    - total_conta_pendente: soma de vendas pendentes com
      conta_pendente_id preenchido.
    - total_troco: soma dos valores de troco.
    - ticket_medio: média do valor_total das vendas.

    Parâmetro:
        data: data utilizada para filtrar as vendas.

    Retorno:
        Dicionário com os indicadores calculados para o dia.
    """

    # A consulta calcula todos os indicadores em um único SELECT.
    #
    # COUNT(*) conta os registros de venda.
    #
    # SUM(valor_total) calcula o total vendido.
    #
    # CASE WHEN permite somar valor_total somente quando
    # a condição especificada é verdadeira.
    #
    # COALESCE substitui resultados NULL por zero.
    #
    # AVG(valor_total) calcula o ticket médio das vendas
    # registradas na data consultada.
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

    # Executa a consulta para a data escolhida.
    resultado = _consultar_um(sql, (data,))

    # Retorna o dicionário com os indicadores do fechamento.
    return resultado

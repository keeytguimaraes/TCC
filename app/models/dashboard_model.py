# ==================================================
# IMPORTA FUNÇÃO RESPONSÁVEL POR CRIAR CONEXÃO
# COM O BANCO DE DADOS
# ==================================================
from app.database.conexao import conectar

# ==================================================
# PERMITE QUE OS RESULTADOS DAS CONSULTAS
# SEJAM RETORNADOS COMO DICIONÁRIOS
#
# Exemplo:
#
# resultado["nome"]
#
# ao invés de:
#
# resultado[0]
# ==================================================
from psycopg2.extras import RealDictCursor


# ==================================================
# CONSTANTE UTILIZADA COMO PADRÃO PARA
# TODOS OS CURSORES DO SISTEMA
#
# Isso evita repetir RealDictCursor
# em todas as funções.
# ==================================================
CURSOR_PADRAO = RealDictCursor


# ==================================================
# CRIAR CURSOR
# ==================================================
def criar_cursor():

    """
    Responsável por criar:

    - conexão com banco
    - cursor configurado com RealDictCursor

    Retorna:

    conexao
    cursor
    """

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=CURSOR_PADRAO
    )

    return conexao, cursor


# ==================================================
# INDICADORES GERAIS DO DASHBOARD
# ==================================================
def buscar_indicadores_dashboard():

    """
    Busca os principais indicadores utilizados
    pelos dashboards de administrador e gerente.

    Indicadores retornados:

    - vendido hoje
    - vendido mês
    - fiados abertos
    - contas pendentes
    - estoque baixo
    """

    conexao, cursor = criar_cursor()

    dados_dashboard = {}

    # ==================================================
    # TOTAL VENDIDO HOJE
    # ==================================================

    # Soma todas as vendas realizadas
    # na data atual.
    #
    # CURRENT_DATE retorna apenas a data.
    #
    # COALESCE garante que o retorno seja
    # 0 caso não existam vendas.
    cursor.execute("""
        SELECT
            COALESCE(
                SUM(valor_total),
                0
            ) AS total
        FROM venda
        WHERE DATE(data_venda) = CURRENT_DATE
    """)

    dados_dashboard["vendido_hoje"] = (
        cursor.fetchone()["total"]
    )

    # ==================================================
    # TOTAL VENDIDO NO MÊS
    # ==================================================

    # Soma todas as vendas do mês atual.
    #
    # O filtro verifica:
    #
    # - mês atual
    # - ano atual
    #
    # evitando misturar meses de anos
    # diferentes.
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

    dados_dashboard["vendido_mes"] = (
        cursor.fetchone()["total"]
    )

    # ==================================================
    # FIADOS EM ABERTO
    # ==================================================

    # Conta quantas contas de fiado
    # continuam abertas.
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM conta
        WHERE status_conta = 'aberta'
    """)

    dados_dashboard["fiados_abertos"] = (
        cursor.fetchone()["total"]
    )

    # ==================================================
    # CONTAS PENDENTES
    # ==================================================

    # Conta quantas contas pendentes
    # ainda estão abertas.
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM conta_pendente
        WHERE status = 'aberta'
    """)

    dados_dashboard["contas_pendentes"] = (
        cursor.fetchone()["total"]
    )

    # ==================================================
    # ESTOQUE BAIXO
    # ==================================================

    # Conta quantos produtos possuem
    # quantidade igual ou inferior a 10 unidades.
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM estoque
        WHERE quantidade_atual_unidade <= 10
    """)

    dados_dashboard["estoque_baixo"] = (
        cursor.fetchone()["total"]
    )

    cursor.close()
    conexao.close()

    return dados_dashboard


# ==================================================
# GERAR MENSAGEM DO DASHBOARD
# ==================================================
def gerar_mensagem_dashboard(
    dados_dashboard
):

    """
    Gera a mensagem exibida para
    administradores.

    Recebe os indicadores calculados
    anteriormente e monta um resumo.
    """

    return f"""
Bom dia!

Hoje existem {dados_dashboard['contas_pendentes']} conta(s) pendente(s)
e {dados_dashboard['estoque_baixo']} produto(s) com estoque baixo.
"""

# ==================================================
# DASHBOARD ADMINISTRADOR
# ==================================================
def buscar_dashboard_administrador():

    """
    Monta todos os dados necessários
    para o dashboard do administrador.

    O administrador possui acesso
    completo ao sistema.
    """

    # Busca indicadores gerais
    dados_dashboard = (
        buscar_indicadores_dashboard()
    )

    # Busca últimas vendas realizadas
    dados_dashboard["ultimas_vendas"] = (
        buscar_ultimas_vendas()
    )

    # Busca últimas movimentações
    dados_dashboard["ultimas_movimentacoes"] = (
        buscar_ultimas_movimentacoes()
    )

    # Busca alertas importantes
    dados_dashboard["alertas"] = (
        buscar_alertas_dashboard()
    )

    # Gera mensagem personalizada
    dados_dashboard["mensagem"] = (
        gerar_mensagem_dashboard(
            dados_dashboard
        )
    )

    return dados_dashboard

# ==================================================
# DASHBOARD GERENTE
# ==================================================
def buscar_dashboard_gerente():

    """
    Monta os dados exibidos
    para usuários do perfil gerente.
    """

    dados_dashboard = (
        buscar_indicadores_dashboard()
    )

    dados_dashboard["ultimas_vendas"] = (
        buscar_ultimas_vendas()
    )

    dados_dashboard["ultimas_movimentacoes"] = (
        buscar_ultimas_movimentacoes()
    )

    dados_dashboard["mensagem"] = f"""
Bem-vinda!

Existem {dados_dashboard['estoque_baixo']} produto(s)
com estoque baixo e
{dados_dashboard['contas_pendentes']} conta(s) pendente(s).
"""

    return dados_dashboard

# ==================================================
# DASHBOARD FUNCIONÁRIO
# ==================================================
def buscar_dashboard_funcionario(
    usuario_id
):

    """
    Responsável por montar os dados
    exibidos para usuários do perfil
    funcionário.

    Diferente do administrador e gerente,
    o funcionário visualiza apenas
    informações relacionadas às suas
    próprias atividades.

    Dados exibidos:

    - Quantidade de vendas realizadas hoje
    - Valor vendido hoje
    - Últimas vendas realizadas
    - Últimas contas pendentes abertas
    - Mensagem motivacional
    """

    # Cria conexão com o banco de dados
    # e cursor configurado para retornar
    # resultados como dicionário.
    conexao, cursor = criar_cursor()

    # Dicionário que armazenará todos os
    # dados enviados para a página.
    dados_dashboard = {}

    # ==================================================
    # QUANTIDADE DE VENDAS REALIZADAS HOJE
    # ==================================================

    # Conta quantas vendas foram realizadas
    # pelo funcionário logado na data atual.
    #
    # O filtro utiliza:
    #
    # usuario_id = funcionário atual
    # CURRENT_DATE = data de hoje
    cursor.execute(
        """
        SELECT COUNT(*) AS total

        FROM venda

        WHERE usuario_id = %s

        AND DATE(data_venda) = CURRENT_DATE
        """,
        (usuario_id,)
    )

    # Recupera o resultado retornado
    # pela consulta e armazena dentro
    # do dicionário principal.
    dados_dashboard["vendas_hoje"] = (
        cursor.fetchone()["total"]
    )

    # ==================================================
    # VALOR TOTAL VENDIDO HOJE
    # ==================================================

    # Soma o valor total de todas as vendas
    # realizadas pelo funcionário na data atual.
    #
    # COALESCE evita que o banco retorne
    # NULL quando não houver vendas.
    cursor.execute(
        """
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

    # Armazena o valor vendido no dia.
    dados_dashboard["valor_vendido"] = (
        cursor.fetchone()["total"]
    )

    # ==================================================
    # ÚLTIMAS VENDAS DO FUNCIONÁRIO
    # ==================================================

    # Busca as 5 vendas mais recentes
    # realizadas pelo funcionário.
    #
    # ORDER BY DESC:
    # mais recente primeiro.
    #
    # LIMIT 5:
    # apenas os cinco registros mais recentes.
    cursor.execute(
        """
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

    # Recupera todos os registros encontrados.
    dados_dashboard["ultimas_vendas"] = (
        cursor.fetchall()
    )

    # ==================================================
    # ÚLTIMAS CONTAS PENDENTES
    # ==================================================

    # Busca as últimas contas pendentes
    # abertas pelo funcionário.
    #
    # Essas contas representam clientes
    # temporários que ainda não efetuaram
    # o pagamento.
    cursor.execute(
        """
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

    # Armazena a lista das contas encontradas.
    dados_dashboard["ultimas_contas"] = (
        cursor.fetchall()
    )

    # ==================================================
    # MENSAGEM EXIBIDA NO DASHBOARD
    # ==================================================

    # Cria uma mensagem simples utilizando
    # a quantidade de vendas realizadas hoje.
    #
    # Essa mensagem serve apenas para deixar
    # o dashboard mais amigável para o usuário.
    dados_dashboard["mensagem"] = (
        f"Você realizou "
        f"{dados_dashboard['vendas_hoje']} venda(s) hoje. "
        f"Continue o ótimo trabalho!"
    )

    # Fecha cursor.
    cursor.close()

    # Fecha conexão.
    conexao.close()

    # Retorna todos os dados preparados.
    return dados_dashboard

# ==================================================
# ÚLTIMAS VENDAS
# ==================================================
def buscar_ultimas_vendas():

    """
    Busca as 5 vendas mais recentes do sistema.

    Esta função é utilizada pelos dashboards
    de administrador e gerente para exibir
    rapidamente as últimas movimentações de venda.

    Informações retornadas:

    - Data da venda
    - Valor total
    - Status do pagamento
    - Nome do responsável pela venda
    """

    # Cria conexão com o banco de dados
    # e cursor configurado para retornar
    # resultados em formato de dicionário.
    conexao, cursor = criar_cursor()

    # Consulta responsável por retornar
    # as últimas vendas registradas.
    #
    # LEFT JOIN é utilizado para trazer
    # o nome do usuário responsável.
    #
    # COALESCE evita valores NULL caso
    # o usuário não esteja definido.
    cursor.execute("""
        SELECT

            v.data_venda,

            v.valor_total,

            v.status_pagamento,

            COALESCE(
                u.nome,
                'Não informado'
            ) AS responsavel

        FROM venda v

        LEFT JOIN usuario u
            ON u.id = v.usuario_id

        ORDER BY v.data_venda DESC

        LIMIT 5
    """)

    # Recupera todos os registros encontrados.
    vendas = cursor.fetchall()

    # Libera recursos.
    cursor.close()
    conexao.close()

    # Retorna a lista de vendas.
    return vendas


# ==================================================
# ÚLTIMAS MOVIMENTAÇÕES DE ESTOQUE
# ==================================================
def buscar_ultimas_movimentacoes():

    """
    Busca as últimas movimentações de estoque.

    Essas movimentações podem representar:

    - Entrada de produtos
    - Saída de produtos
    - Ajustes manuais
    - Correções de estoque

    Informações retornadas:

    - Data da movimentação
    - Tipo da movimentação
    - Produto
    - Responsável
    """

    # Cria conexão com banco.
    conexao, cursor = criar_cursor()

    # Consulta responsável por buscar
    # as últimas movimentações registradas.
    #
    # INNER JOIN:
    # Obtém o nome do produto.
    #
    # LEFT JOIN:
    # Obtém o usuário responsável.
    cursor.execute("""
        SELECT

            m.data_movimentacao,

            m.tipo_movimentacao,

            p.nome AS produto,

            COALESCE(
                u.nome,
                'Não informado'
            ) AS responsavel

        FROM movimentacao_estoque m

        INNER JOIN produto p
            ON p.id = m.produto_id

        LEFT JOIN usuario u
            ON u.id = m.usuario_id

        ORDER BY
            m.data_movimentacao DESC

        LIMIT 5
    """)

    # Recupera os registros encontrados.
    movimentacoes = cursor.fetchall()

    # Fecha recursos do banco.
    cursor.close()
    conexao.close()

    # Retorna a lista de movimentações.
    return movimentacoes


# ==================================================
# ALERTAS DO DASHBOARD
# ==================================================
def buscar_alertas_dashboard():

    """
    Gera uma lista de alertas que serão
    exibidos no dashboard administrativo.

    Atualmente são verificados:

    - Produtos com estoque baixo
    - Contas pendentes abertas

    Novos alertas podem ser adicionados
    futuramente nesta função.
    """

    # Cria conexão e cursor.
    conexao, cursor = criar_cursor()

    # Lista onde serão armazenados
    # todos os alertas encontrados.
    alertas = []

    # ==================================================
    # ALERTA DE ESTOQUE BAIXO
    # ==================================================

    # Conta quantos produtos possuem
    # estoque igual ou inferior a 10 unidades.
    cursor.execute("""
        SELECT COUNT(*) AS total

        FROM estoque

        WHERE quantidade_atual_unidade <= 10
    """)

    estoque_baixo = (
        cursor.fetchone()["total"]
    )

    # Caso exista pelo menos um produto
    # com estoque baixo, adiciona um alerta.
    if estoque_baixo > 0:

        alertas.append(
            f"{estoque_baixo} produto(s) com estoque baixo"
        )

    # ==================================================
    # ALERTA DE CONTAS PENDENTES
    # ==================================================

    # Conta quantas contas pendentes
    # ainda estão abertas.
    cursor.execute("""
        SELECT COUNT(*) AS total

        FROM conta_pendente

        WHERE status = 'aberta'
    """)

    pendentes = (
        cursor.fetchone()["total"]
    )

    # Se existirem contas pendentes,
    # adiciona um alerta correspondente.
    if pendentes > 0:

        alertas.append(
            f"{pendentes} conta(s) pendente(s)"
        )

    # Fecha recursos do banco.
    cursor.close()
    conexao.close()

    # Retorna a lista completa de alertas.
    return alertas
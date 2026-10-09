
# ============================================================
# MODEL DE SINUCA
# ============================================================
# Este arquivo contém as funções responsáveis pelo acesso
# aos dados relacionados à sinuca no SIGC.
#
# Funcionalidades:
# - Buscar a configuração da sinuca.
# - Atualizar as configurações da sinuca.
# - Buscar as fichas vinculadas a uma venda.
# - Consultar os indicadores do relatório de sinuca.
#
# O model executa consultas e alterações no banco de dados.
# As rotas e os controllers utilizam essas funções para atender
# às solicitações da aplicação.
# ============================================================


# Importa a função responsável por abrir uma conexão
# com o banco de dados PostgreSQL.
from app.database.conexao import conectar

# Permite retornar os resultados das consultas como dicionários.
from psycopg2.extras import RealDictCursor


# ============================================================
# FUNÇÕES AUXILIARES DE CONSULTA
# ============================================================

def _consultar_um(sql, parametros=()):
    """
    Executa uma consulta SQL e retorna um único registro.

    Parâmetros:
        sql: instrução SQL que será executada.
        parametros: valores utilizados na consulta.

    Retorno:
        Dicionário com o registro encontrado ou None caso
        a consulta não retorne nenhuma linha.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que transforma o resultado em dicionário.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Executa a consulta com os parâmetros recebidos.
    cursor.execute(sql, parametros)

    # Recupera somente o primeiro registro encontrado.
    resultado = cursor.fetchone()

    # Fecha o cursor e a conexão após concluir a consulta.
    cursor.close()
    conexao.close()

    # Retorna o registro encontrado.
    return resultado


def _consultar_todos(sql, parametros=()):
    """
    Executa uma consulta SQL e retorna todos os registros.

    Parâmetros:
        sql: instrução SQL que será executada.
        parametros: valores utilizados na consulta.

    Retorno:
        Lista de dicionários com os registros encontrados.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor de dicionários para acessar as colunas
    # pelo nome, em vez de utilizar posições numéricas.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Executa a consulta com os parâmetros recebidos.
    cursor.execute(sql, parametros)

    # Recupera todos os registros encontrados.
    dados = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna a lista de registros.
    return dados


# ============================================================
# BUSCAR CONFIGURAÇÃO DA SINUCA
# ============================================================

def buscar_config_sinuca():
    """
    Busca a configuração registrada para a sinuca.

    A consulta retorna o primeiro registro encontrado na tabela
    sinuca_config.

    Retorno:
        Dicionário com as configurações ou None caso a tabela
        não contenha registros.
    """

    # Consulta todas as colunas da configuração.
    #
    # LIMIT 1 mantém o comportamento original, retornando
    # no máximo um registro.
    sql = """
        SELECT *
        FROM sinuca_config
        LIMIT 1
    """

    # Executa a consulta e retorna o registro encontrado.
    return _consultar_um(sql)


# ============================================================
# ATUALIZAR CONFIGURAÇÃO DA SINUCA
# ============================================================

def atualizar_config_sinuca(
    nome,
    valor_ficha,
    percentual_comercio
):
    """
    Atualiza os dados de configuração da sinuca.

    Parâmetros:
        nome: nome utilizado para identificar a sinuca.
        valor_ficha: valor de cada ficha.
        percentual_comercio: percentual destinado ao comércio.

    A atualização é direcionada ao registro cujo id seja 1,
    conforme a implementação original.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar o UPDATE.
    cursor = conexao.cursor()

    # Atualiza o nome, o valor da ficha e o percentual do comércio.
    #
    # O WHERE id = 1 mantém a regra existente de atualizar
    # especificamente o registro de configuração identificado
    # pelo número 1.
    sql = """
        UPDATE sinuca_config
        SET
            nome = %s,
            valor_ficha = %s,
            percentual_comercio = %s
        WHERE id = 1
    """

    # Executa a atualização com os valores recebidos.
    cursor.execute(
        sql,
        (
            nome,
            valor_ficha,
            percentual_comercio
        )
    )

    # Confirma as alterações no banco de dados.
    conexao.commit()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()


# ============================================================
# BUSCAR FICHAS DE UMA VENDA
# ============================================================

def pegar_fichas_venda(venda_id):
    """
    Busca os registros de fichas associados a uma venda.

    Parâmetro:
        venda_id: identificador da venda consultada.

    Retorno:
        Lista de dicionários com os registros encontrados
        na tabela sinuca_venda.
    """

    # Consulta todos os campos dos registros de fichas
    # relacionados ao identificador da venda.
    sql = """
        SELECT *
        FROM sinuca_venda
        WHERE venda_id = %s
    """

    # Executa a consulta usando o identificador informado.
    return _consultar_todos(sql, (venda_id,))


# ============================================================
# RELATÓRIO DA SINUCA
# ============================================================

def pegar_relatorio_sinuca():
    """
    Calcula os indicadores gerais das vendas de fichas pagas.

    Indicadores:
        total_fichas:
            Soma da quantidade de fichas vendidas em registros
            cujo status_pagamento seja 'pago'.

        valor_arrecadado:
            Soma do valor_total dos registros cujo status de
            pagamento seja 'pago'.

    Retorno:
        Dicionário contendo os dois indicadores calculados.
    """

    # Soma a quantidade de fichas e os valores totais dos
    # registros pagos da tabela sinuca_venda.
    #
    # SUM calcula a soma de cada coluna.
    #
    # Esta consulta não utiliza COALESCE. Portanto, se não
    # existirem registros correspondentes, os valores das
    # somas poderão ser None, conforme o comportamento do SQL.
    sql = """
        SELECT
            SUM(quantidade_fichas) AS total_fichas,
            SUM(valor_total) AS valor_arrecadado

        FROM sinuca_venda

        WHERE status_pagamento = 'pago'
    """

    # Executa a consulta e retorna o registro com os indicadores.
    return _consultar_um(sql)

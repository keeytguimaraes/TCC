from app.database.conexao import conectar


# ==========================
# BUSCAR CONFIGURAÇÃO DA SINUCA
# ==========================
def buscar_config_sinuca():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *
        FROM sinuca_config
        LIMIT 1
    """

    cursor.execute(sql)

    config = cursor.fetchone()

    cursor.close()
    conexao.close()

    return config

# ==========================
# ATUALIZAR CONFIGURAÇÃO
# ==========================
def atualizar_config_sinuca(

    nome,

    valor_ficha,

    percentual_comercio
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE sinuca_config

        SET

            nome = %s,

            valor_ficha = %s,

            percentual_comercio = %s

        WHERE id = 1
    """

    cursor.execute(

        sql,

        (

            nome,

            valor_ficha,

            percentual_comercio
        )
    )

    conexao.commit()

    cursor.close()

    conexao.close()

# ==========================
# BUSCAR INFORMAÇÕES DA FICHA PARA VENDA
# ==========================
def pegar_fichas_venda(venda_id):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *
        FROM sinuca_venda
        WHERE venda_id = %s
    """

    cursor.execute(
        sql,
        (venda_id,)
    )

    fichas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return fichas

# ==========================
# RELATÓRIO DA SINUCA
# ==========================
def pegar_relatorio_sinuca():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            SUM(quantidade_fichas)
                AS total_fichas,

            SUM(valor_total)
                AS valor_arrecadado

        FROM sinuca_venda

        WHERE status_pagamento = 'Pago'
    """

    cursor.execute(sql)

    dados = cursor.fetchone()

    cursor.close()
    conexao.close()

    return dados
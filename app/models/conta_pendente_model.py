from app.database.conexao import conectar


# ==========================
# BUSCAR CONTA ABERTA
# ==========================
def buscar_conta_pendente_aberta(nome):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

        FROM conta_pendente

        WHERE nome_cliente_temporario = %s

        AND status = 'Aberta'

        LIMIT 1
    """

    cursor.execute(
        sql,
        (nome,)
    )

    conta = cursor.fetchone()

    cursor.close()
    conexao.close()

    return conta


# ==========================
# CRIAR CONTA
# ==========================
def criar_conta_pendente(nome):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        INSERT INTO conta_pendente (

            nome_cliente_temporario

        )

        VALUES (%s)
    """

    cursor.execute(
        sql,
        (nome,)
    )

    conexao.commit()

    conta_id = cursor.lastrowid

    cursor.close()
    conexao.close()

    return conta_id


# ==========================
# FECHAR CONTA
# ==========================
def fechar_conta_pendente(
    conta_id
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE conta_pendente

        SET status = 'Fechada'

        WHERE id = %s
    """

    cursor.execute(
        sql,
        (conta_id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()
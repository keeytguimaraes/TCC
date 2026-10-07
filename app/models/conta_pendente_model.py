from app.database.conexao import conectar
from psycopg2.extras import RealDictCursor

# ==========================
# BUSCAR CONTA ABERTA
# ==========================
def buscar_conta_pendente_aberta(nome):

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    sql = """
        SELECT *

        FROM conta_pendente

        WHERE nome_cliente_temporario = %s

        AND status = 'aberta'

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

    from flask import session

    usuario_id = session["usuario_id"]

    sql = """
    INSERT INTO conta_pendente (

        nome_cliente_temporario,
        status,
        usuario_id

    )

    VALUES (

        %s,
        'aberta',
        %s

    )

    RETURNING id
"""

    cursor.execute(
    sql,
    (nome,usuario_id)
)

    conta_id = cursor.fetchone()[0]

    conexao.commit()

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

        SET status = 'Quitada'

        WHERE id = %s
    """

    cursor.execute(
        sql,
        (conta_id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()
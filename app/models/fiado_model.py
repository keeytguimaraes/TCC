# Importa conexão
from app.database.conexao import conectar


# ==========================
# LISTAR FIADOS
# ==========================
def listar_fiados():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
    SELECT

        conta.id,

        cliente.nome,

        conta.saldo_devedor,

        conta.status_conta,

        conta.data_abertura

    FROM conta

    INNER JOIN cliente

        ON cliente.id = conta.cliente_id

    WHERE

        conta.status_conta = 'aberta'

    ORDER BY conta.id DESC
"""

    cursor.execute(sql)

    fiados = cursor.fetchall()

    cursor.close()

    conexao.close()

    return fiados


# ==========================
# BUSCAR PRODUTOS DO FIADO
# ==========================
def buscar_produtos_fiado(

    conta_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

    produto.nome,

    produto_venda.quantidade,

    produto_venda.tipo_venda,

    venda.id AS venda_id

FROM venda

INNER JOIN produto_venda

    ON venda.id = produto_venda.venda_id

INNER JOIN produto

    ON produto.id = produto_venda.produto_id

WHERE venda.conta_id = %s
    """

    cursor.execute(

         sql,

        (
        conta_id,
        )
    )

    produtos = cursor.fetchall()

    cursor.close()

    conexao.close()

    return produtos

# ==========================
# BUSCAR FIADO POR ID
# ==========================
def buscar_fiado_por_id(

    conta_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

FROM conta

WHERE id = %s
    """

    cursor.execute(

        sql,

        (
            conta_id,
        )
    )

    fiado = cursor.fetchone()

    cursor.close()

    conexao.close()

    return fiado

# ==========================
# RECEBER PAGAMENTO FIADO
# ==========================
def atualizar_saldo_fiado(

    conta_id,

    novo_saldo,

    status_conta
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
    UPDATE conta

    SET

        saldo_devedor = %s,

        status_conta = %s

    WHERE id = %s
"""

    cursor.execute(

    sql,

    (

        novo_saldo,

        status_conta,

        conta_id

    )
)

    conexao.commit()

    cursor.close()

    conexao.close()

# ==========================
# REGISTRAR RECEBIMENTO
# ==========================
def registrar_recebimento_fiado(

    conta_id,

    valor_recebido
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
    INSERT INTO recebimento_fiado (

        conta_id,

        valor_recebido

    )

    VALUES (%s, %s)
"""

    cursor.execute(

    sql,

    (

        conta_id,

        valor_recebido

    )
)
    conexao.commit()

    cursor.close()

    conexao.close()

# ==========================
# BUSCAR RECEBIMENTOS
# ==========================
def buscar_recebimentos_fiado(

    conta_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            valor_recebido,

            data_recebimento

        FROM recebimento_fiado

        WHERE conta_id = %s

        ORDER BY data_recebimento DESC
    """

    cursor.execute(

    sql,

    (

        conta_id,

    )
)

    recebimentos = cursor.fetchall()

    cursor.close()

    conexao.close()

    return recebimentos
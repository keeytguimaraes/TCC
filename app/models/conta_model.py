# Importa conexão
from app.database.conexao import conectar


# ==========================
# LISTAR CONTAS PENDENTES
# ==========================
def listar_contas_pendentes():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            cp.id,
            cp.nome_cliente_temporario,
            cp.data_abertura,

            COALESCE(
                SUM(v.valor_total),
                0
            ) AS valor_total

        FROM conta_pendente cp

        LEFT JOIN venda v

            ON v.conta_pendente_id = cp.id

        WHERE cp.status = 'Aberta'

        GROUP BY

            cp.id,
            cp.nome_cliente_temporario,
            cp.data_abertura

        ORDER BY cp.id DESC
    """

    cursor.execute(sql)

    contas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return contas
# ==========================
# BUSCAR PRODUTOS DA VENDA
# ==========================
def buscar_produtos_venda(

    venda_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            produto.nome,

            produto_venda.quantidade,

            produto_venda.tipo_venda

        FROM produto_venda

        INNER JOIN produto

            ON produto.id =
            produto_venda.produto_id

        WHERE produto_venda.venda_id = %s
    """

    cursor.execute(

        sql,

        (
            venda_id,
        )
    )

    produtos = cursor.fetchall()

    cursor.close()

    conexao.close()

    return produtos

    # ==========================
# BUSCAR CONTA ABERTA
# ==========================
def buscar_conta_aberta(cliente_id):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

        FROM conta

        WHERE cliente_id = %s

        AND status_conta = 'aberta'

        LIMIT 1
    """

    cursor.execute(

        sql,

        (
            cliente_id,
        )
    )

    conta = cursor.fetchone()

    cursor.close()

    conexao.close()

    return conta


# ==========================
# CRIAR CONTA
# ==========================
def criar_conta(cliente_id):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        INSERT INTO conta (

            cliente_id,

            status_conta,

            saldo_devedor

        )

        VALUES (

            %s,

            'aberta',

            0
        )
    """

    cursor.execute(

        sql,

        (
            cliente_id,
        )
    )

    conexao.commit()

    conta_id = cursor.lastrowid

    cursor.close()

    conexao.close()

    return conta_id


# ==========================
# ATUALIZAR SALDO
# ==========================
def atualizar_saldo_conta(
    cursor,
    conta_id,
    valor
):

    sql = """
        UPDATE conta
        SET saldo_devedor = saldo_devedor + %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            valor,
            conta_id
        )
    )


# ==========================
# BUSCAR CONTA POR ID
# ==========================
def buscar_conta_por_id(

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

    conta = cursor.fetchone()

    cursor.close()

    conexao.close()

    return conta

def buscar_fichas_pendentes(venda_id):

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
# BUSCAR CONTA PENDENTE ABERTA
# ==========================
def buscar_conta_pendente_aberta(nome_cliente):

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
        (nome_cliente,)
    )

    conta = cursor.fetchone()

    cursor.close()
    conexao.close()

    return conta


# ==========================
# CRIAR CONTA PENDENTE
# ==========================
def criar_conta_pendente(nome_cliente):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        INSERT INTO conta_pendente (

            nome_cliente_temporario,
            status

        )

        VALUES (

            %s,
            'Aberta'

        )
    """

    cursor.execute(
        sql,
        (nome_cliente,)
    )

    conexao.commit()

    conta_id = cursor.lastrowid

    cursor.close()
    conexao.close()

    return conta_id

# ==========================
# BUSCAR CONTA PENDENTE
# ==========================
def buscar_conta_pendente_por_id(conta_id):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

        FROM conta_pendente

        WHERE id = %s
    """

    cursor.execute(
        sql,
        (conta_id,)
    )

    conta = cursor.fetchone()

    cursor.close()
    conexao.close()

    return conta

# ==========================
# BUSCAR VENDAS DA CONTA
# ==========================
def buscar_vendas_conta_pendente(conta_id):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

        FROM venda

        WHERE conta_pendente_id = %s

        ORDER BY data_venda ASC
    """

    cursor.execute(
        sql,
        (conta_id,)
    )

    vendas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return vendas
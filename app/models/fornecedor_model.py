# Importa conexão
from app.database.conexao import conectar


# ==========================
# LISTAR FORNECEDORES
# ==========================
def listar_fornecedores():

    # Conecta banco
    conexao = conectar()

    # Cursor dicionário
    cursor = conexao.cursor(
        dictionary=True
    )

    # SQL
    sql = """
        SELECT *

        FROM fornecedor

        ORDER BY nome
    """

    # Executa SQL
    cursor.execute(sql)

    # Busca dados
    fornecedores = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna dados
    return fornecedores


# ==========================
# CADASTRAR FORNECEDOR
# ==========================
def cadastrar_fornecedor(

    nome,
    telefone,
    observacao
):

    # Conecta banco
    conexao = conectar()

    # Cursor
    cursor = conexao.cursor()

    # SQL
    sql = """
        INSERT INTO fornecedor (

            nome,
            telefone,
            observacao

        )
        VALUES (%s, %s, %s)
    """

    # Executa
    cursor.execute(
        sql,
        (
            nome,
            telefone,
            observacao
        )
    )

    # Salva
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()
    
    # ==========================
# BUSCAR FORNECEDOR POR ID
# ==========================
def buscar_fornecedor_por_id(

    id_fornecedor
):

    # Conecta banco
    conexao = conectar()

    # Cursor dicionário
    cursor = conexao.cursor(
        dictionary=True
    )

    # SQL
    sql = """
        SELECT *

        FROM fornecedor

        WHERE id = %s
    """

    # Executa
    cursor.execute(
        sql,
        (id_fornecedor,)
    )

    # Busca fornecedor
    fornecedor = cursor.fetchone()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna fornecedor
    return fornecedor


# ==========================
# EDITAR FORNECEDOR
# ==========================
def editar_fornecedor(

    id_fornecedor,

    nome,
    telefone,
    observacao
):

    # Conecta banco
    conexao = conectar()

    # Cursor
    cursor = conexao.cursor()

    # SQL
    sql = """
        UPDATE fornecedor

        SET

            nome = %s,
            telefone = %s,
            observacao = %s

        WHERE id = %s
    """

    # Executa
    cursor.execute(
        sql,
        (
            nome,
            telefone,
            observacao,
            id_fornecedor
        )
    )

    # Salva
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()
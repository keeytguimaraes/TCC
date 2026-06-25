# Importa conexão com banco
from app.database.conexao import conectar


# ==========================
# LISTAR PRODUTOS
# ==========================
def listar_produtos():

    # Conecta no banco
    conexao = conectar()

    # Cursor em formato dicionário
    cursor = conexao.cursor(
        dictionary=True
    )

    # SQL
    sql = """
        SELECT *
        FROM produto
    """

    # Executa SQL
    cursor.execute(sql)

    # Busca produtos
    produtos = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna lista
    return produtos


# ==========================
# CADASTRAR PRODUTO
# ==========================
def cadastrar_produto(
    nome,
    categoria,
    preco_venda,
    quantidade_por_caixa
):

    # Conecta banco
    conexao = conectar()

    # Cria cursor
    cursor = conexao.cursor()

    # SQL
    sql = """
        INSERT INTO produto (
            nome,
            categoria,
            preco_venda,
            quantidade_por_caixa
        )
        VALUES (%s, %s, %s, %s)
    """

    # Executa SQL
    cursor.execute(
        sql,
        (
            nome,
            categoria,
            preco_venda,
            quantidade_por_caixa
        )
    )

    # Salva no banco
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()


# ==========================
# LISTAR CATEGORIAS
# ==========================
def listar_categorias():

    # Conecta banco
    conexao = conectar()

    # Cursor dicionário
    cursor = conexao.cursor(
        dictionary=True
    )

    # SQL
    sql = """
        SELECT DISTINCT categoria

        FROM produto

        ORDER BY categoria
    """

    # Executa
    cursor.execute(sql)

    # Busca categorias
    categorias = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna
    return categorias
# ==========================
# BUSCAR PRODUTO POR ID
# ==========================
def buscar_produto_por_id(

    produto_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

        FROM produto

        WHERE id = %s
    """

    cursor.execute(

        sql,

        (
            produto_id,
        )
    )

    produto = cursor.fetchone()

    cursor.close()

    conexao.close()

    return produto
# ==========================
# EDITAR PRODUTO
# ==========================
def editar_produto(

    produto_id,

    nome,

    categoria,

    preco_venda,

    quantidade_por_caixa
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE produto

        SET

            nome = %s,

            categoria = %s,

            preco_venda = %s,

            quantidade_por_caixa = %s

        WHERE id = %s
    """

    cursor.execute(

        sql,

        (

            nome,

            categoria,

            preco_venda,

            quantidade_por_caixa,

            produto_id
        )
    )

    conexao.commit()

    cursor.close()

    conexao.close()
# ==========================
# INATIVAR PRODUTO
# ==========================
def inativar_produto(

    produto_id
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE produto

        SET ativo = FALSE

        WHERE id = %s
    """

    cursor.execute(

        sql,

        (
            produto_id,
        )
    )

    conexao.commit()

    cursor.close()

    conexao.close()
    
def ativar_produto(

    produto_id
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE produto

        SET ativo = TRUE

        WHERE id = %s
    """

    cursor.execute(

        sql,

        (
            produto_id,
        )
    )

    conexao.commit()

    cursor.close()

    conexao.close()
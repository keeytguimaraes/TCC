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
# Importa conexão com banco
from app.database.conexao import conectar


# ==========================
# LISTAR PRODUTOS
# ==========================
def listar_produtos():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
    SELECT
    p.*,

    COALESCE(
        e.quantidade_atual_caixa,
        0
    ) AS estoque_caixa,

    COALESCE(
        e.quantidade_atual_unidade,
        0
    ) AS estoque_unidade,

    COALESCE(
        e.quantidade_fracionada,
        0
    ) AS estoque_fracionado

FROM produto p

LEFT JOIN estoque e
ON e.id = (

    SELECT MAX(id)

    FROM estoque

    WHERE produto_id = p.id
)
"""

    cursor.execute(sql)

    produtos = cursor.fetchall()

    cursor.close()

    conexao.close()

    return produtos


# ==========================
# CADASTRAR PRODUTO
# ==========================
def cadastrar_produto(
    nome,
    categoria,
    sabor,
    tipo_embalagem,
    volume,
    preco_venda,
    preco_caixa,
    quantidade_por_caixa,
    estoque_minimo,
    vende_por_dose,
    vende_por_unidade,
    volume_dose_ml,
    preco_dose,
    preco_unidade,
    quantidade_por_unidade,
    imagem
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
            sabor,
            tipo_embalagem,
            volume,
            preco_venda,
            preco_caixa,
            quantidade_por_caixa,
            estoque_minimo,
            vende_por_dose,
            vende_por_unidade,
            volume_dose_ml,
            preco_dose,
            preco_unidade,
            quantidade_por_unidade,
            imagem

        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Executa SQL
    cursor.execute(
        sql,
        (
    nome,
    categoria,
    sabor,
    tipo_embalagem,
    volume,
    preco_venda,
    preco_caixa,
    quantidade_por_caixa,
    estoque_minimo,
    vende_por_dose,
    vende_por_unidade,
    volume_dose_ml,
    preco_dose,
    preco_unidade,
    quantidade_por_unidade,
    imagem
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

    sabor,

    tipo_embalagem,

    volume,

    preco_venda,

    preco_caixa,

    quantidade_por_caixa,

    vende_por_dose,

    vende_por_unidade,

    quantidade_por_unidade,

    volume_dose_ml,

    preco_dose,

    preco_unidade
):

    conexao = conectar()

    cursor = conexao.cursor()

    # ==========================
    # BUSCA PREÇO ATUAL
    # ==========================
    sql_preco = """
        SELECT preco_venda

        FROM produto

        WHERE id = %s
    """

    cursor.execute(

        sql_preco,

        (
            produto_id,
        )
    )

    produto = cursor.fetchone()

    preco_antigo = produto[0]

    # ==========================
    # REGISTRA HISTÓRICO
    # ==========================
    if float(preco_antigo) != float(preco_venda):

        sql_historico = """
            INSERT INTO historico_preco (

                produto_id,
                preco_antigo,
                preco_novo

            )
            VALUES (%s, %s, %s)
        """

        cursor.execute(

            sql_historico,

            (
                produto_id,
                preco_antigo,
                preco_venda
            )
        )

    # ==========================
    # ATUALIZA PRODUTO
    # ==========================
    sql = """
UPDATE produto

SET

    nome = %s,
    categoria = %s,
    sabor = %s,
    tipo_embalagem = %s,
    volume = %s,
    preco_venda = %s,
    preco_caixa = %s,
    quantidade_por_caixa = %s,

    vende_por_dose = %s,
    vende_por_unidade = %s,

    volume_dose_ml = %s,

    preco_dose = %s,
    quantidade_por_unidade = %s,
    preco_unidade = %s

WHERE id = %s
"""

    cursor.execute(

    sql,

    (

        nome,
    categoria,
    sabor,
    tipo_embalagem,
    volume,
    preco_venda,
    preco_caixa,
    quantidade_por_caixa,

    vende_por_dose,
    vende_por_unidade,

    volume_dose_ml,

    preco_dose,
    preco_unidade,

    quantidade_por_unidade,

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

# ==========================
# LISTAR PRODUTOS ATIVOS
# ==========================
def listar_produtos_ativos():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT
            p.*,

            COALESCE(
                SUM(
                    e.quantidade_atual_caixa
                ),
                0
            ) AS estoque_caixa,

            COALESCE(
                SUM(
                    e.quantidade_atual_unidade
                ),
                0
            ) AS estoque_unidade

        FROM produto p

        LEFT JOIN estoque e
            ON p.id = e.produto_id

        WHERE p.ativo = TRUE

        GROUP BY p.id
    """

    cursor.execute(sql)

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return produtos


# ==========================
# LISTAR PRODUTOS INATIVOS
# ==========================
def listar_produtos_inativos():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
    SELECT
        p.*,

        COALESCE(
            SUM(
                e.quantidade_atual_caixa
            ),
            0
        ) AS estoque_caixa,

        COALESCE(
            SUM(
                e.quantidade_atual_unidade
            ),
            0
        ) AS estoque_unidade

    FROM produto p

    LEFT JOIN estoque e
        ON p.id = e.produto_id

    WHERE p.ativo = FALSE

    GROUP BY p.id
"""

    cursor.execute(sql)

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return produtos

# ==========================
# LISTAR PRODUTOS PARA VENDA
# ==========================
def listar_produtos_venda():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            p.*,

            e.quantidade_atual_caixa
                AS estoque_caixa,

            e.quantidade_atual_unidade
                AS estoque_unidade

        FROM produto p

        LEFT JOIN estoque e
            ON e.id = (

                SELECT MAX(id)

                FROM estoque

                WHERE produto_id = p.id

            )

        WHERE
    p.ativo = TRUE

    AND

    COALESCE(
        e.quantidade_atual_unidade,
        0
    ) > 0

        ORDER BY p.nome
    """

    cursor.execute(sql)

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return produtos

# ==========================
# HISTÓRICO DE PREÇOS
# ==========================
def buscar_historico_preco(produto_id):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *

        FROM historico_preco

        WHERE produto_id = %s

        ORDER BY data_alteracao DESC
    """

    cursor.execute(

        sql,

        (
            produto_id,
        )
    )

    historico = cursor.fetchall()

    cursor.close()
    conexao.close()

    return historico
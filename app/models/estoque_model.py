# Importa conexão banco
from app.database.conexao import conectar


# ==========================
# LISTAR ESTOQUE
# ==========================
def listar_estoque():

    # Conecta banco
    conexao = conectar()

    # Cursor dicionário
    cursor = conexao.cursor(
        dictionary=True
    )

    # SQL
    sql = """
        SELECT
    estoque.id,

    produto.nome,
    produto.categoria,

    estoque.tipo_entrada,

    origem_compra.nome AS origem_compra,

    fornecedor.nome AS fornecedor,

    estoque.nome_origem,

    estoque.quantidade_recebida_caixa,
    estoque.quantidade_recebida_unidade,

    estoque.quantidade_atual_caixa,
    estoque.quantidade_atual_unidade,

    estoque.preco_total_compra,
    estoque.preco_por_caixa,
    estoque.preco_por_unidade,

    estoque.data_entrada

FROM estoque

INNER JOIN produto
ON estoque.produto_id = produto.id

LEFT JOIN fornecedor
ON estoque.fornecedor_id = fornecedor.id

LEFT JOIN origem_compra
ON estoque.origem_compra_id = origem_compra.id

ORDER BY estoque.id DESC
    """

    # Executa SQL
    cursor.execute(sql)

    # Busca dados
    estoque = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna dados
    return estoque


# ==========================
# CADASTRAR ESTOQUE
# ==========================
def cadastrar_estoque(

    produto_id,

    origem_compra_id,
    nome_origem,

    fornecedor_id,
    tipo_entrada,

    quantidade_recebida_caixa,
    quantidade_recebida_unidade,

    preco_total_compra,
    data_entrada
):

    # Conecta banco
    conexao = conectar()

    # Cursor
    cursor = conexao.cursor()

    # --------------------------
    # BUSCA ESTOQUE ATUAL
    # --------------------------
    sql_buscar = """
    SELECT
        quantidade_atual_caixa,
        quantidade_atual_unidade

    FROM estoque

    WHERE produto_id = %s

    ORDER BY id DESC

    LIMIT 1
"""

    cursor.execute(
        sql_buscar,
        (produto_id,)
    )

    estoque_atual = (
        cursor.fetchone()
    )

    # Se já existe
    if estoque_atual:

        atual_caixa = (
            estoque_atual[0]
        )

        atual_unidade = (
            estoque_atual[1]
        )

    # Se não existe
    else:

        atual_caixa = 0
        atual_unidade = 0

    # --------------------------
    # BUSCA QUANTIDADE CAIXA
    # --------------------------
    sql_produto = """
        SELECT quantidade_por_caixa

        FROM produto

        WHERE id = %s
    """

    cursor.execute(
        sql_produto,
        (produto_id,)
    )

    produto = (
        cursor.fetchone()
    )

    quantidade_por_caixa = (
        produto[0]
    )

    # --------------------------
    # CONVERSÃO
    # --------------------------
    caixas = int(
        quantidade_recebida_caixa
    )

    unidades_digitadas = int(
        quantidade_recebida_unidade
    )

    unidades_da_caixa = (
        caixas
        * quantidade_por_caixa
    )

    total_unidades_recebidas = (
        unidades_da_caixa
        + unidades_digitadas
    )

    # --------------------------
    # NOVO ESTOQUE
    # --------------------------
    nova_caixa = (
        atual_caixa
        + caixas
    )

    nova_unidade = (
        atual_unidade
        + total_unidades_recebidas
    )

    # --------------------------
    # PREÇOS
    # --------------------------

# Se for bonificação
    if tipo_entrada == "bonificacao":

     preco_total = 0
     preco_por_caixa = 0
     preco_por_unidade = 0

# Compra normal
    else:

     preco_total = float(
        preco_total_compra
    )

    # Evita divisão por zero
    if caixas > 0:

        preco_por_caixa = (
            preco_total
            / caixas
        )

    else:

        preco_por_caixa = 0

    # Evita divisão por zero
    if total_unidades_recebidas > 0:

        preco_por_unidade = (
            preco_total
            / total_unidades_recebidas
        )

    else:

        preco_por_unidade = 0
    # --------------------------
    # INSERT
    # --------------------------
    sql_insert = """
    INSERT INTO estoque (

        produto_id,

        origem_compra_id,
        nome_origem,

        fornecedor_id,
        tipo_entrada,

        quantidade_recebida_caixa,
        quantidade_recebida_unidade,

        quantidade_atual_caixa,
        quantidade_atual_unidade,

        preco_total_compra,
        preco_por_caixa,
        preco_por_unidade,

        data_entrada

    )
    VALUES (

        %s, %s, %s,

        %s, %s,

        %s, %s,

        %s, %s,

        %s, %s, %s,

        %s
    )
"""

    cursor.execute(
    sql_insert,
    (
        produto_id,

        origem_compra_id,
        nome_origem,

        fornecedor_id,
        tipo_entrada,

        caixas,
        total_unidades_recebidas,

        nova_caixa,
        nova_unidade,

        preco_total,
        preco_por_caixa,
        preco_por_unidade,

        data_entrada
    )
)

    # Salva
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # ==========================
# BAIXAR ESTOQUE
# ==========================
def baixar_estoque(

    produto_id,

    quantidade,

    tipo_venda
):

    conexao = conectar()

    cursor = conexao.cursor()

    # --------------------------
    # BUSCA ÚLTIMO ESTOQUE
    # --------------------------
    sql_buscar = """
        SELECT

        quantidade_atual_caixa,

        quantidade_atual_unidade

        FROM estoque

        WHERE produto_id = %s

        ORDER BY id DESC

        LIMIT 1
    """

    cursor.execute(

        sql_buscar,

        (
                produto_id,
        )
    )


    estoque = cursor.fetchone()

    if not estoque:

        cursor.close()

        conexao.close()

        return

    atual_caixa = estoque[0]

    atual_unidade = estoque[1]

    # --------------------------
    # QUANTIDADE POR CAIXA
    # --------------------------
    sql_produto = """
        SELECT quantidade_por_caixa

        FROM produto

        WHERE id = %s
    """

    cursor.execute(

        sql_produto,

        (
            produto_id,
        )
    )

    produto = cursor.fetchone()

    quantidade_por_caixa = produto[0]

    # --------------------------
    # CONVERSÃO
    # --------------------------
    quantidade = int(
        quantidade
    )

    if tipo_venda == "caixa":

        baixa_caixa = quantidade

        baixa_unidade = (
            quantidade
            * quantidade_por_caixa
        )

    else:

        baixa_caixa = (
            quantidade
            // quantidade_por_caixa
        )

        baixa_unidade = quantidade

    # --------------------------
    # NOVO ESTOQUE
    # --------------------------
    nova_caixa = (
        atual_caixa
        - baixa_caixa
    )

    nova_unidade = (
        atual_unidade
        - baixa_unidade
    )

    # Evita negativo
    if nova_caixa < 0:

        nova_caixa = 0

    if nova_unidade < 0:

        nova_unidade = 0

    # --------------------------
    # REGISTRA HISTÓRICO
    # --------------------------
    sql_insert = """
    INSERT INTO estoque (

        produto_id,

        tipo_movimentacao,

        quantidade_recebida_caixa,

        quantidade_recebida_unidade,

        quantidade_atual_caixa,

        quantidade_atual_unidade,

        data_entrada

    )
    VALUES (

        %s,

        'saida',

        0,

        0,

        %s,

        %s,

        NOW()
    )

    """

    cursor.execute(

        sql_insert,

        (
            produto_id,

            nova_caixa,

            nova_unidade
        )
    )

    conexao.commit()

    cursor.close()

    conexao.close()

    # ==========================
# BUSCAR ÚLTIMO ESTOQUE
# ==========================
def buscar_estoque_atual(

    produto_id
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT

            quantidade_atual_caixa,

            quantidade_atual_unidade

        FROM estoque

        WHERE produto_id = %s

        ORDER BY id DESC

        LIMIT 1
    """

    cursor.execute(

        sql,

        (
            produto_id,
        )
    )

    estoque = cursor.fetchone()

    cursor.close()

    conexao.close()

    return estoque
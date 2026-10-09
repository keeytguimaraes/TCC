
# ============================================================
# MODELO DE VENDAS — SIGC
# ============================================================
# Este arquivo contém as operações relacionadas às vendas:
#
# - Listar as vendas realizadas;
# - Consultar o histórico de vendas;
# - Cadastrar uma venda;
# - Registrar os produtos de cada venda;
# - Atualizar o estoque após uma venda;
# - Buscar os produtos e os detalhes de uma venda;
# - Consultar os produtos registrados em todas as vendas.
#
# As regras de negócio permanecem nas funções existentes.
# Este modelo é responsável por executar as consultas e
# alterações no banco de dados PostgreSQL.
# ============================================================


# Importa a função responsável por abrir uma conexão
# com o banco de dados PostgreSQL do SIGC.
from app.database.conexao import conectar

# Permite que as consultas SELECT retornem os registros
# como dicionários, possibilitando acessar os campos
# pelo nome, por exemplo: venda["valor_total"].
from psycopg2.extras import RealDictCursor


# ============================================================
# LISTAR VENDAS
# ============================================================
def listar_vendas():
    """
    Retorna a listagem principal das vendas cadastradas.

    A consulta reúne informações da venda, o nome do cliente
    registrado e o nome temporário associado a uma conta
    pendente, quando houver.

    Os relacionamentos com cliente e conta_pendente utilizam
    LEFT JOIN. Assim, a venda pode aparecer mesmo quando não
    existe um registro correspondente nessas tabelas.

    Retorno:
        Lista de dicionários com os dados selecionados.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna os resultados como dicionários.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Seleciona os campos necessários para a listagem.
    #
    # O alias "v" representa a tabela venda.
    # O alias "c" representa a tabela cliente.
    # O alias "cp" representa a tabela conta_pendente.
    #
    # Os aliases tornam a consulta mais curta e deixam claro
    # de qual tabela cada campo está sendo obtido.
    sql = """
        SELECT
            v.id,
            v.data_venda,
            v.valor_total,
            v.valor_recebido,
            v.troco,
            v.status_pagamento,
            v.desconto_venda,

            c.nome AS cliente_nome,

            cp.nome_cliente_temporario

        FROM venda v

        LEFT JOIN cliente c
            ON c.id = v.cliente_id

        LEFT JOIN conta_pendente cp
            ON cp.id = v.conta_pendente_id

        ORDER BY v.data_venda DESC
    """

    # Executa a consulta SQL.
    cursor.execute(sql)

    # Recupera todas as vendas retornadas pelo banco.
    vendas = cursor.fetchall()

    # Fecha o cursor e libera os recursos da conexão.
    cursor.close()
    conexao.close()

    # Devolve a lista para a função que solicitou os dados.
    return vendas


# ============================================================
# HISTÓRICO DE VENDAS
# ============================================================
def listar_historico_vendas():
    """
    Retorna o histórico completo das vendas.

    Diferentemente de listar_vendas(), esta função utiliza
    v.* para selecionar todas as colunas da tabela venda.

    Também busca:
        - Nome do cliente cadastrado;
        - Nome temporário da conta pendente;
        - Nome do usuário associado à venda.

    Retorno:
        Lista de dicionários com os dados das vendas e
        as informações complementares dos relacionamentos.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Utiliza um cursor que transforma cada linha retornada
    # pelo PostgreSQL em um dicionário.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Monta a consulta do histórico.
    #
    # O LEFT JOIN permite que a venda continue aparecendo
    # mesmo se não houver um cliente, uma conta pendente
    # ou um usuário relacionado.
    sql = """
        SELECT
            v.*,

            c.nome AS cliente_nome,

            cp.nome_cliente_temporario,

            u.nome AS usuario

        FROM venda v

        LEFT JOIN cliente c
            ON c.id = v.cliente_id

        LEFT JOIN conta_pendente cp
            ON cp.id = v.conta_pendente_id

        LEFT JOIN usuario u
            ON u.id = v.usuario_id

        ORDER BY v.data_venda DESC
    """

    # Executa a consulta no banco de dados.
    cursor.execute(sql)

    # Recupera todos os registros do histórico.
    vendas = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna os dados para o controller ou a rota.
    return vendas


# ============================================================
# CADASTRAR VENDA
# ============================================================
def cadastrar_venda(
    produto_id,
    quantidade,
    tipo_venda,
    valor_recebido,
    status_pagamento
):
    """
    Registra uma venda de um produto e atualiza o estoque.

    Parâmetros:
        produto_id:
            ID do produto vendido.

        quantidade:
            Quantidade comercializada.

        tipo_venda:
            Tipo de venda, como "unidade" ou "caixa".

        valor_recebido:
            Valor informado como recebido na venda.

        status_pagamento:
            Situação do pagamento que será registrada.

    Fluxo executado:
        1. Busca os dados do produto.
        2. Determina o preço unitário ou o preço da caixa.
        3. Calcula o subtotal.
        4. Calcula o troco.
        5. Registra a venda.
        6. Registra o produto relacionado à venda.
        7. Busca o registro de estoque mais recente.
        8. Atualiza a quantidade em estoque.
        9. Confirma as alterações no banco.

    Observação:
        Esta função preserva o fluxo original de venda de
        um único produto por chamada.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna resultados como dicionários.
    # Isso permite acessar os dados usando os nomes das colunas.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # --------------------------------------------------------
    # 1. BUSCAR O PRODUTO
    # --------------------------------------------------------
    # Antes de calcular a venda, precisamos consultar os dados
    # do produto para obter seu preço e a quantidade por caixa.
    sql_produto = """
        SELECT *
        FROM produto
        WHERE id = %s
    """

    # O parâmetro é enviado separadamente para o PostgreSQL.
    cursor.execute(
        sql_produto,
        (produto_id,)
    )

    # Recupera o produto correspondente ao ID informado.
    produto = cursor.fetchone()

    # --------------------------------------------------------
    # 2. DEFINIR O PREÇO UNITÁRIO DA VENDA
    # --------------------------------------------------------
    # Inicialmente, utiliza o preço de venda cadastrado
    # para o produto.
    preco_unitario = float(
        produto["preco_venda"]
    )

    # Quando o tipo de venda for "caixa", multiplica o preço
    # pelo número de unidades que compõem uma caixa.
    #
    # Para os demais tipos, mantém o comportamento original:
    # o preço inicial continua sendo o preco_venda do produto.
    if tipo_venda == "caixa":
        preco_unitario = (
            preco_unitario
            * produto["quantidade_por_caixa"]
        )

    # --------------------------------------------------------
    # 3. CALCULAR O SUBTOTAL
    # --------------------------------------------------------
    # Multiplica o preço calculado pela quantidade vendida.
    #
    # A conversão para int é mantida conforme o código original.
    subtotal = (
        preco_unitario
        * int(quantidade)
    )

    # --------------------------------------------------------
    # 4. CALCULAR O TROCO
    # --------------------------------------------------------
    # Calcula a diferença entre o valor recebido e o subtotal.
    # O resultado é registrado na tabela venda.
    troco = (
        float(valor_recebido)
        - subtotal
    )

    # --------------------------------------------------------
    # 5. REGISTRAR A VENDA
    # --------------------------------------------------------
    # Cria o registro principal da venda.
    #
    # RETURNING id solicita que o PostgreSQL devolva o ID
    # gerado para o novo registro.
    sql_venda = """
        INSERT INTO venda (
            valor_total,
            valor_recebido,
            troco,
            status_pagamento
        )
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """

    # Executa o INSERT com os dados calculados.
    cursor.execute(
        sql_venda,
        (
            subtotal,
            valor_recebido,
            troco,
            status_pagamento
        )
    )

    # Como o cursor utiliza RealDictCursor, o resultado de
    # RETURNING id é um registro acessível pela chave "id".
    # Assim, recuperamos o identificador da venda criada.
    venda_id = cursor.fetchone()["id"]

    # --------------------------------------------------------
    # 6. REGISTRAR O PRODUTO DA VENDA
    # --------------------------------------------------------
    # A tabela produto_venda relaciona o registro principal
    # da venda ao produto comercializado.
    #
    # Também registra a quantidade, o tipo da venda, o preço
    # utilizado no cálculo e o subtotal correspondente.
    sql_produto_venda = """
        INSERT INTO produto_venda (
            venda_id,
            produto_id,
            quantidade,
            tipo_venda,
            preco_unitario,
            subtotal
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql_produto_venda,
        (
            venda_id,
            produto_id,
            quantidade,
            tipo_venda,
            preco_unitario,
            subtotal
        )
    )

    # --------------------------------------------------------
    # 7. BUSCAR O REGISTRO MAIS RECENTE DO ESTOQUE
    # --------------------------------------------------------
    # A consulta seleciona o registro de estoque mais recente
    # associado ao produto, considerando o maior ID.
    #
    # LIMIT 1 garante que apenas um registro seja recuperado.
    sql_estoque = """
        SELECT *
        FROM estoque
        WHERE produto_id = %s
        ORDER BY id DESC
        LIMIT 1
    """

    cursor.execute(
        sql_estoque,
        (produto_id,)
    )

    # Recupera os dados do estoque selecionado.
    estoque = cursor.fetchone()

    # Obtém as quantidades atuais registradas nesse estoque.
    atual_unidade = estoque[
        "quantidade_atual_unidade"
    ]

    atual_caixa = estoque[
        "quantidade_atual_caixa"
    ]

    # --------------------------------------------------------
    # 8. ATUALIZAR O ESTOQUE CONFORME O TIPO DE VENDA
    # --------------------------------------------------------

    # VENDA POR UNIDADE:
    # Diminui a quantidade de unidades pelo número vendido.
    if tipo_venda == "unidade":

        novo_estoque = (
            atual_unidade
            - int(quantidade)
        )

        # Atualiza somente a quantidade em unidades.
        # A cláusula WHERE identifica o registro de estoque
        # específico que foi recuperado anteriormente.
        sql_update = """
            UPDATE estoque
            SET quantidade_atual_unidade = %s
            WHERE id = %s
        """

        cursor.execute(
            sql_update,
            (
                novo_estoque,
                estoque["id"]
            )
        )

    # VENDA POR CAIXA OU OUTRO TIPO:
    # Preserva a regra original: qualquer tipo diferente
    # de "unidade" entra neste bloco e reduz as caixas.
    else:

        novo_estoque = (
            atual_caixa
            - int(quantidade)
        )

        # Atualiza somente a quantidade de caixas.
        sql_update = """
            UPDATE estoque
            SET quantidade_atual_caixa = %s
            WHERE id = %s
        """

        cursor.execute(
            sql_update,
            (
                novo_estoque,
                estoque["id"]
            )
        )

    # --------------------------------------------------------
    # 9. CONFIRMAR A TRANSAÇÃO
    # --------------------------------------------------------
    # Confirma as operações executadas nesta conexão:
    # INSERT da venda, INSERT do produto vendido e UPDATE
    # do estoque.
    conexao.commit()

    # Libera os recursos utilizados.
    cursor.close()
    conexao.close()


# ============================================================
# BUSCAR PRODUTOS DE UMA VENDA
# ============================================================
def buscar_produtos_venda(venda_id):
    """
    Busca os produtos associados a uma venda específica.

    Parâmetros:
        venda_id: ID da venda cujos produtos serão consultados.

    A consulta relaciona produto_venda com produto para
    recuperar o nome de cada produto comercializado.

    Retorno:
        Lista de dicionários contendo nome, quantidade,
        tipo de venda, preço unitário e subtotal.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Configura o cursor para retornar os registros
    # em formato de dicionário.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Consulta os produtos vinculados à venda informada.
    sql = """
        SELECT
            produto.nome,
            produto_venda.quantidade,
            produto_venda.tipo_venda,
            produto_venda.preco_unitario,
            produto_venda.subtotal

        FROM produto_venda

        INNER JOIN produto
            ON produto.id = produto_venda.produto_id

        WHERE produto_venda.venda_id = %s
    """

    # Executa a consulta usando o ID da venda como parâmetro.
    cursor.execute(
        sql,
        (venda_id,)
    )

    # Recupera todos os produtos encontrados.
    produtos = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna os produtos para a função que solicitou os dados.
    return produtos


# ============================================================
# BUSCAR DETALHES DE UMA VENDA
# ============================================================
def buscar_detalhes_venda(venda_id):
    """
    Busca os detalhes dos registros de produto_venda
    associados a uma venda.

    Parâmetros:
        venda_id: ID da venda que será consultada.

    Diferentemente de buscar_produtos_venda(), esta função
    seleciona todas as colunas de produto_venda e acrescenta
    o nome do produto.

    Retorno:
        Lista de dicionários com os dados dos itens da venda.
    """

    # Estabelece a conexão com o PostgreSQL.
    conexao = conectar()

    # Cria um cursor que retorna os resultados como dicionários.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # O alias "pv" representa produto_venda.
    # O alias "p" representa produto.
    #
    # O INNER JOIN relaciona cada item registrado à sua
    # respectiva informação de produto.
    sql = """
        SELECT
            pv.*,
            p.nome

        FROM produto_venda pv

        INNER JOIN produto p
            ON p.id = pv.produto_id

        WHERE pv.venda_id = %s
    """

    # Executa a consulta para a venda informada.
    cursor.execute(
        sql,
        (venda_id,)
    )

    # Recupera os itens encontrados.
    produtos = cursor.fetchall()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Entrega os detalhes ao controller ou à rota.
    return produtos


# ============================================================
# BUSCAR PRODUTOS DE TODAS AS VENDAS
# ============================================================
def buscar_produtos_todas_vendas():
    """
    Busca os produtos registrados em todas as vendas.

    A consulta relaciona produto_venda e produto para retornar
    informações sobre cada item comercializado.

    Retorno:
        Lista de dicionários contendo:
        - ID da venda;
        - Nome do produto;
        - Quantidade;
        - Tipo de venda;
        - Preço unitário;
        - Subtotal.

    Observação:
        A consulta original não possui WHERE nem ORDER BY.
        Portanto, esta função não filtra as vendas por período
        ou situação de pagamento, nem define uma ordenação.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Utiliza RealDictCursor para facilitar o acesso aos campos
    # pelo nome nos controllers e nas rotas.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Busca os itens de todas as vendas registrados em
    # produto_venda e associa cada um ao nome do produto.
    sql = """
        SELECT
            pv.venda_id,
            p.nome,
            pv.quantidade,
            pv.tipo_venda,
            pv.preco_unitario,
            pv.subtotal

        FROM produto_venda pv

        INNER JOIN produto p
            ON p.id = pv.produto_id
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera todos os itens retornados.
    produtos = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna a lista completa de produtos das vendas.
    return produtos

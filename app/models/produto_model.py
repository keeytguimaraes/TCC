
# ============================================================
# MODEL DE PRODUTOS
# ============================================================
# Este arquivo concentra as operações de acesso ao banco de
# dados relacionadas aos produtos do SIGC.
#
# Funcionalidades:
# - Listar produtos e suas quantidades de estoque.
# - Cadastrar produtos.
# - Listar categorias cadastradas.
# - Buscar um produto pelo identificador.
# - Editar os dados e os preços de um produto.
# - Inativar e reativar produtos.
# - Listar produtos ativos e inativos.
# - Listar produtos disponíveis para venda.
# - Consultar o histórico de preços.
#
# O model executa as consultas SQL e retorna os dados.
# As rotas e os controllers continuam responsáveis por
# controlar as requisições e utilizar os resultados.
# ============================================================


# Importa a função que abre uma conexão com o banco PostgreSQL.
from app.database.conexao import conectar

# Permite retornar os resultados das consultas como dicionários.
# Exemplo: produto["nome"] ou produto["preco_venda"].
from psycopg2.extras import RealDictCursor


# ============================================================
# LISTAR PRODUTOS
# ============================================================

def listar_produtos():
    """
    Lista os produtos cadastrados e apresenta as quantidades
    do registro de estoque mais recente de cada produto.

    Retorno:
        Lista de dicionários com os dados do produto e os campos:
        - estoque_caixa;
        - estoque_unidade;
        - estoque_fracionado.

    Quando não existe registro de estoque, as quantidades
    retornam como zero.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna os resultados como dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta os dados dos produtos e as quantidades do estoque.
    #
    # A subconsulta SELECT MAX(id) identifica o registro de
    # estoque com o maior identificador para cada produto.
    #
    # O LEFT JOIN permite listar produtos mesmo quando ainda
    # não existe um registro de estoque relacionado.
    #
    # COALESCE substitui valores NULL por zero nos campos
    # de quantidade, facilitando o uso desses dados.
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

    # Executa a consulta SQL.
    cursor.execute(sql)

    # Recupera todos os produtos encontrados.
    produtos = cursor.fetchall()

    # Fecha o cursor e a conexão após a consulta.
    cursor.close()
    conexao.close()

    # Retorna a lista de produtos para quem chamou a função.
    return produtos


# ============================================================
# CADASTRAR PRODUTO
# ============================================================

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
    """
    Cadastra um novo produto no banco de dados.

    Os parâmetros representam os dados cadastrais, os preços,
    as configurações de embalagem e venda e a imagem do produto.

    Esta função não cria um registro na tabela estoque.
    O cadastro do produto e o abastecimento do estoque são
    operações distintas no sistema.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar a inserção.
    cursor = conexao.cursor()

    # Insere os dados recebidos na tabela produto.
    #
    # A ordem dos campos no INSERT corresponde à ordem dos
    # parâmetros enviados em cursor.execute().
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
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s
        )
    """

    # Executa a inserção utilizando parâmetros separados.
    # Essa forma evita montar manualmente a consulta SQL
    # com os valores recebidos.
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

    # Confirma a gravação do produto no banco.
    conexao.commit()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()


# ============================================================
# LISTAR CATEGORIAS
# ============================================================

def listar_categorias():
    """
    Lista as categorias existentes na tabela produto.

    DISTINCT evita retornar a mesma categoria mais de uma vez.

    Retorno:
        Lista de dicionários com as categorias encontradas,
        ordenadas alfabeticamente.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Seleciona somente os valores distintos da coluna categoria.
    #
    # A ordenação organiza as categorias pelo nome.
    sql = """
        SELECT DISTINCT categoria
        FROM produto
        ORDER BY categoria
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera todas as categorias encontradas.
    categorias = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna a lista de categorias.
    return categorias


# ============================================================
# BUSCAR PRODUTO POR ID
# ============================================================

def buscar_produto_por_id(produto_id):
    """
    Busca os dados de um produto pelo seu identificador.

    Parâmetro:
        produto_id: identificador do produto no banco.

    Retorno:
        Dicionário com os dados do produto ou None se não
        existir um registro correspondente.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Utiliza um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Seleciona todas as colunas do produto solicitado.
    sql = """
        SELECT *
        FROM produto
        WHERE id = %s
    """

    # Executa a consulta para o identificador recebido.
    cursor.execute(sql, (produto_id,))

    # Recupera um único produto.
    produto = cursor.fetchone()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Retorna o produto encontrado ou None.
    return produto


# ============================================================
# EDITAR PRODUTO
# ============================================================

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
    """
    Atualiza os dados de um produto existente.

    Antes de atualizar o produto, a função consulta o preço
    de venda atual e verifica se ele mudou.

    Quando o preço de venda é diferente do preço anterior,
    registra a alteração na tabela historico_preco.

    Em seguida, atualiza os dados cadastrais, os preços e as
    configurações de venda do produto.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar as consultas e alterações.
    cursor = conexao.cursor()

    # --------------------------------------------------------
    # 1. BUSCAR O PREÇO DE VENDA ATUAL
    # --------------------------------------------------------

    # Consulta o preço que está armazenado antes da edição.
    # Esse valor será comparado ao novo preço informado.
    sql_preco = """
        SELECT preco_venda
        FROM produto
        WHERE id = %s
    """

    # Executa a consulta para o produto que será editado.
    cursor.execute(sql_preco, (produto_id,))

    # Recupera o resultado da consulta.
    produto = cursor.fetchone()

    # Obtém o preço atual a partir da primeira coluna retornada.
    #
    # A lógica original pressupõe que o produto existe.
    # Se não existir, produto será None e este acesso provocará
    # um erro, como ocorria no código anterior.
    preco_antigo = produto[0]

    # --------------------------------------------------------
    # 2. REGISTRAR O HISTÓRICO DE PREÇOS
    # --------------------------------------------------------

    # Compara o preço anterior com o novo preço.
    #
    # A conversão para float é mantida conforme o código
    # original para realizar a comparação numérica.
    if float(preco_antigo) != float(preco_venda):

        # Insere um registro no histórico quando o preço muda.
        sql_historico = """
            INSERT INTO historico_preco (
                produto_id,
                preco_antigo,
                preco_novo
            )
            VALUES (%s, %s, %s)
        """

        # Registra o identificador do produto, o preço anterior
        # e o preço novo informado.
        cursor.execute(
            sql_historico,
            (
                produto_id,
                preco_antigo,
                preco_venda
            )
        )

    # --------------------------------------------------------
    # 3. ATUALIZAR OS DADOS DO PRODUTO
    # --------------------------------------------------------

    # Atualiza os dados cadastrais, os preços e as configurações
    # de embalagem e venda.
    #
    # A coluna estoque_minimo não é atualizada aqui porque
    # ela não fazia parte do UPDATE original.
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

    # ATENÇÃO:
    # A ordem dos parâmetros abaixo foi organizada para
    # corresponder à ordem das colunas no UPDATE.
    #
    # No código recebido, preco_unidade e quantidade_por_unidade
    # estavam em posições incompatíveis com a ordem do SQL.
    # Aqui, os valores são associados às respectivas colunas,
    # evitando gravar o preço no campo de quantidade ou vice-versa.
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
            quantidade_por_unidade,
            preco_unidade,
            produto_id
        )
    )

    # Confirma tanto o registro de histórico, quando existente,
    # quanto a atualização dos dados do produto.
    conexao.commit()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()


# ============================================================
# INATIVAR PRODUTO
# ============================================================

def inativar_produto(produto_id):
    """
    Inativa um produto sem excluir seu registro do banco.

    Parâmetro:
        produto_id: identificador do produto a ser inativado.

    A função altera o campo ativo para zero.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar a atualização.
    cursor = conexao.cursor()

    # Marca o produto como inativo.
    sql = """
        UPDATE produto
        SET ativo = 0
        WHERE id = %s
    """

    # Executa a atualização para o produto informado.
    cursor.execute(sql, (produto_id,))

    # Confirma a alteração.
    conexao.commit()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()


# ============================================================
# ATIVAR PRODUTO
# ============================================================

def ativar_produto(produto_id):
    """
    Reativa um produto anteriormente inativado.

    Parâmetro:
        produto_id: identificador do produto a ser reativado.

    A função altera o campo ativo para um.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar a atualização.
    cursor = conexao.cursor()

    # Corrige a sintaxe do UPDATE para atribuir o valor 1
    # ao campo ativo.
    sql = """
        UPDATE produto
        SET ativo = 1
        WHERE id = %s
    """

    # Executa a atualização para o produto informado.
    cursor.execute(sql, (produto_id,))

    # Confirma a alteração.
    conexao.commit()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()


# ============================================================
# LISTAR PRODUTOS ATIVOS
# ============================================================

def listar_produtos_ativos():
    """
    Lista os produtos ativos e soma as quantidades de estoque
    presentes nos registros relacionados a cada produto.

    Retorno:
        Lista de produtos com os campos adicionais:
        - estoque_caixa;
        - estoque_unidade.

    A soma foi mantida conforme a consulta original.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Seleciona os produtos ativos e calcula as somas das
    # quantidades presentes na tabela estoque.
    #
    # COALESCE retorna zero quando a soma é NULL.
    #
    # O GROUP BY agrupa os resultados por produto para que
    # as funções SUM calculem um resultado por produto.
    sql = """
        SELECT
            p.*,

            COALESCE(
                SUM(e.quantidade_atual_caixa),
                0
            ) AS estoque_caixa,

            COALESCE(
                SUM(e.quantidade_atual_unidade),
                0
            ) AS estoque_unidade

        FROM produto p

        LEFT JOIN estoque e
            ON p.id = e.produto_id

        WHERE p.ativo = 1

        GROUP BY p.id
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera todos os produtos ativos encontrados.
    produtos = cursor.fetchall()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Retorna a lista de produtos.
    return produtos


# ============================================================
# LISTAR PRODUTOS INATIVOS
# ============================================================

def listar_produtos_inativos():
    """
    Lista os produtos inativos e soma as quantidades de estoque
    presentes nos registros relacionados a cada produto.

    Retorno:
        Lista de produtos inativos com os campos adicionais:
        - estoque_caixa;
        - estoque_unidade.

    A consulta mantém a soma utilizada no código original.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta os produtos inativos e calcula as somas de
    # caixas e unidades dos registros de estoque relacionados.
    sql = """
        SELECT
            p.*,

            COALESCE(
                SUM(e.quantidade_atual_caixa),
                0
            ) AS estoque_caixa,

            COALESCE(
                SUM(e.quantidade_atual_unidade),
                0
            ) AS estoque_unidade

        FROM produto p

        LEFT JOIN estoque e
            ON p.id = e.produto_id

        WHERE p.ativo = 0

        GROUP BY p.id
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera todos os produtos inativos.
    produtos = cursor.fetchall()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Retorna a lista encontrada.
    return produtos


# ============================================================
# LISTAR PRODUTOS PARA VENDA
# ============================================================

def listar_produtos_venda():
    """
    Lista os produtos ativos que possuem quantidade positiva
    de unidades no registro de estoque mais recente.

    Os produtos são ordenados pelo nome.

    Retorno:
        Lista de produtos com os dados cadastrais e os campos
        estoque_caixa e estoque_unidade.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor de dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta os produtos e relaciona cada um ao registro
    # de estoque mais recente.
    #
    # O LEFT JOIN mantém a possibilidade de encontrar produtos
    # sem registro de estoque, mas o filtro de quantidade abaixo
    # exclui os produtos sem unidades disponíveis.
    sql = """
        SELECT
            p.*,

            e.quantidade_atual_caixa AS estoque_caixa,

            e.quantidade_atual_unidade AS estoque_unidade

        FROM produto p

        LEFT JOIN estoque e
            ON e.id = (
                SELECT MAX(id)
                FROM estoque
                WHERE produto_id = p.id
            )

        WHERE
            p.ativo = 1

            AND COALESCE(
                e.quantidade_atual_unidade,
                0
            ) > 0

        ORDER BY p.nome
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera os produtos disponíveis para venda.
    produtos = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna a lista de produtos.
    return produtos


# ============================================================
# BUSCAR HISTÓRICO DE PREÇOS
# ============================================================

def buscar_historico_preco(produto_id):
    """
    Busca o histórico de alterações de preço de um produto.

    Parâmetro:
        produto_id: identificador do produto consultado.

    Retorno:
        Lista de registros do histórico de preços, ordenados
        da alteração mais recente para a mais antiga.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor que retorna os resultados como dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta todos os registros de histórico relacionados
    # ao produto informado.
    #
    # A ordenação pela data, em ordem decrescente, apresenta
    # primeiro as alterações mais recentes.
    sql = """
        SELECT *
        FROM historico_preco
        WHERE produto_id = %s
        ORDER BY data_alteracao DESC
    """

    # Executa a consulta para o produto solicitado.
    cursor.execute(sql, (produto_id,))

    # Recupera todos os registros encontrados.
    historico = cursor.fetchall()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Retorna o histórico de preços.
    return historico

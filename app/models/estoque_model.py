
# ============================================================
# MODEL DE ESTOQUE
# ============================================================
# Este arquivo contém as funções responsáveis por consultar e
# atualizar as informações de estoque no banco de dados.
#
# O model é responsável pelo acesso aos dados:
# - Executa consultas SQL.
# - Insere registros no banco.
# - Consulta quantidades e preços.
# - Registra as alterações de estoque.
#
# As regras de negócio são mantidas conforme o código original.
# ============================================================


# Importa a função responsável por abrir uma conexão com o banco.
from app.database.conexao import conectar

# Permite que os resultados das consultas sejam retornados como
# dicionários, facilitando o acesso pelo nome de cada coluna.
from psycopg2.extras import RealDictCursor


# ============================================================
# LISTAR ESTOQUE
# ============================================================

def listar_estoque():
    """
    Lista os registros de entrada de estoque cadastrados.

    Retorna informações sobre:
    - Produto e categoria.
    - Tipo de entrada.
    - Origem da compra e fornecedor.
    - Quantidades recebidas e quantidades atuais.
    - Preços registrados.
    - Data de entrada.

    Os registros mais recentes são apresentados primeiro.
    """

    # Abre uma conexão com o banco de dados PostgreSQL.
    conexao = conectar()

    # Cria um cursor que transforma cada registro retornado
    # pelo banco em um dicionário.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta os registros de estoque e relaciona cada registro
    # com seu produto, fornecedor e origem de compra.
    #
    # INNER JOIN:
    # Exige que exista um produto relacionado ao registro.
    #
    # LEFT JOIN:
    # Permite que o registro apareça mesmo quando não existe
    # fornecedor ou origem de compra relacionado.
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

    # Executa a consulta SQL.
    cursor.execute(sql)

    # Recupera todos os registros encontrados.
    estoque = cursor.fetchall()

    # Encerra o cursor após concluir a consulta.
    cursor.close()

    # Encerra a conexão com o banco de dados.
    conexao.close()

    # Devolve a lista de registros para a função que chamou o model.
    return estoque


# ============================================================
# CADASTRAR ESTOQUE
# ============================================================

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
    """
    Registra uma nova entrada de estoque para um produto.

    O procedimento:
    1. Consulta o último registro de estoque do produto.
    2. Obtém as configurações de embalagem do produto.
    3. Converte as quantidades recebidas.
    4. Calcula as novas quantidades em estoque.
    5. Calcula os preços da entrada.
    6. Insere um novo registro no banco de dados.

    O registro anterior não é sobrescrito: uma nova linha é
    inserida para preservar o histórico de estoque.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor comum, que retorna os resultados em tuplas.
    # Nesse caso, os valores são acessados pelas posições [0], [1]
    # e [2], conforme a ordem das colunas selecionadas.
    cursor = conexao.cursor()

    # --------------------------------------------------------
    # 1. BUSCAR O ESTOQUE ATUAL DO PRODUTO
    # --------------------------------------------------------

    # Busca o registro mais recente desse produto.
    # Ele contém as quantidades que serão usadas como ponto
    # de partida para calcular o novo estoque.
    sql_buscar = """
        SELECT
            quantidade_atual_caixa,
            quantidade_atual_unidade,
            quantidade_fracionada

        FROM estoque

        WHERE produto_id = %s

        ORDER BY id DESC

        LIMIT 1
    """

    # O %s é um parâmetro da consulta PostgreSQL.
    # O valor de produto_id é enviado separadamente, evitando
    # a montagem manual da instrução SQL.
    cursor.execute(sql_buscar, (produto_id,))

    # Recupera apenas o registro mais recente.
    estoque_atual = cursor.fetchone()

    # Se já existe um registro para o produto, utiliza as
    # quantidades atuais encontradas no banco.
    if estoque_atual:
        atual_caixa = estoque_atual[0]
        atual_unidade = estoque_atual[1]
        atual_fracionada = estoque_atual[2]

    # Se o produto ainda não possui registros de estoque,
    # considera que todas as quantidades atuais são zero.
    else:
        atual_caixa = 0
        atual_unidade = 0
        atual_fracionada = 0

    # --------------------------------------------------------
    # 2. BUSCAR AS CONFIGURAÇÕES DO PRODUTO
    # --------------------------------------------------------

    # Obtém as informações necessárias para converter caixas,
    # unidades e doses.
    sql_produto = """
        SELECT
            quantidade_por_caixa,
            quantidade_por_unidade,
            vende_por_dose,
            volume_dose_ml

        FROM produto

        WHERE id = %s
    """

    # Consulta as configurações do produto informado.
    cursor.execute(sql_produto, (produto_id,))

    # Recupera os dados do produto.
    produto = cursor.fetchone()

    # Cada posição corresponde à ordem das colunas no SELECT.
    quantidade_por_caixa = produto[0]
    quantidade_por_unidade = produto[1]
    vende_por_dose = produto[2]
    volume_dose_ml = produto[3]

    # --------------------------------------------------------
    # 3. CONVERTER AS QUANTIDADES RECEBIDAS
    # --------------------------------------------------------

    # Converte a quantidade de caixas para um número inteiro.
    caixas = int(quantidade_recebida_caixa)

    # Converte a quantidade digitada em unidades para inteiro.
    unidades_digitadas = int(quantidade_recebida_unidade)

    # Calcula quantas unidades existem nas caixas recebidas.
    #
    # Exemplo:
    # 2 caixas × 12 unidades por caixa = 24 unidades.
    unidades_da_caixa = caixas * quantidade_por_caixa

    # Soma as unidades que vieram nas caixas às unidades
    # informadas separadamente no cadastro.
    total_unidades_recebidas = (
        unidades_da_caixa + unidades_digitadas
    )

    # --------------------------------------------------------
    # 4. CALCULAR A QUANTIDADE FRACIONADA RECEBIDA
    # --------------------------------------------------------

    # Quando o produto possui uma quantidade de referência para
    # conversão por unidade, calcula o total fracionado recebido.
    if quantidade_por_unidade:
        quantidade_fracionada_recebida = (
            total_unidades_recebidas * quantidade_por_unidade
        )

    # Quando não há essa configuração, o total fracionado
    # recebido é considerado zero.
    else:
        quantidade_fracionada_recebida = 0

    # --------------------------------------------------------
    # 5. CALCULAR AS NOVAS QUANTIDADES DE ESTOQUE
    # --------------------------------------------------------

    # Soma as caixas recebidas às caixas que já estavam
    # registradas no estoque.
    nova_caixa = atual_caixa + caixas

    # Soma o total de unidades recebidas à quantidade de
    # unidades do último registro de estoque.
    #
    # A soma segue a lógica existente no sistema.
    nova_unidade = atual_unidade + total_unidades_recebidas

    # Soma a quantidade fracionada recebida à quantidade
    # fracionada que já estava registrada.
    nova_fracionada = (
        atual_fracionada + quantidade_fracionada_recebida
    )

    # --------------------------------------------------------
    # 6. CALCULAR OS PREÇOS DA ENTRADA
    # --------------------------------------------------------

    # Uma bonificação é registrada com valores de compra iguais
    # a zero, conforme a regra atual do sistema.
    if tipo_entrada == "bonificacao":
        preco_total = 0
        preco_por_caixa = 0
        preco_por_unidade = 0

    # Para os demais tipos de entrada, utiliza o valor total
    # informado no cadastro.
    else:
        preco_total = float(preco_total_compra)

        # Calcula o preço médio por caixa somente quando
        # pelo menos uma caixa foi recebida.
        # Isso evita uma divisão por zero.
        if caixas > 0:
            preco_por_caixa = preco_total / caixas
        else:
            preco_por_caixa = 0

        # Calcula o preço por unidade somente quando a
        # quantidade total recebida é maior que zero.
        if total_unidades_recebidas > 0:
            preco_por_unidade = (
                preco_total / total_unidades_recebidas
            )
        else:
            preco_por_unidade = 0

    # --------------------------------------------------------
    # 7. INSERIR O NOVO REGISTRO DE ESTOQUE
    # --------------------------------------------------------

    # Insere uma nova linha com os dados da entrada e as
    # quantidades atualizadas calculadas anteriormente.
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
            quantidade_fracionada,

            preco_total_compra,
            preco_por_caixa,
            preco_por_unidade,

            data_entrada
        )
        VALUES (
            %s, %s, %s,
            %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s
        )
    """

    # Envia os valores separadamente e na mesma ordem das
    # colunas declaradas no INSERT.
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
            nova_fracionada,

            preco_total,
            preco_por_caixa,
            preco_por_unidade,

            data_entrada
        )
    )

    # Confirma a gravação do novo registro no banco.
    conexao.commit()

    # Libera o cursor e a conexão após concluir a operação.
    cursor.close()
    conexao.close()


# ============================================================
# BAIXAR ESTOQUE
# ============================================================

def baixar_estoque(
    produto_id,
    quantidade,
    tipo_venda
):
    """
    Registra a saída de estoque decorrente de uma venda.

    O procedimento:
    1. Busca o último registro de estoque.
    2. Consulta as configurações do produto.
    3. Calcula a quantidade que deve ser retirada.
    4. Calcula as novas quantidades.
    5. Impede que as quantidades registradas fiquem negativas.
    6. Insere um novo registro de histórico no banco.

    Se o produto não possuir registro de estoque, a função
    encerra a operação sem inserir um novo registro.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor para executar as consultas e o INSERT.
    cursor = conexao.cursor()

    # --------------------------------------------------------
    # 1. BUSCAR O ÚLTIMO REGISTRO DE ESTOQUE
    # --------------------------------------------------------

    # Obtém as quantidades registradas na movimentação mais
    # recente do produto.
    sql_buscar = """
        SELECT
            quantidade_atual_caixa,
            quantidade_atual_unidade,
            quantidade_fracionada

        FROM estoque

        WHERE produto_id = %s

        ORDER BY id DESC

        LIMIT 1
    """

    # Executa a consulta para o produto vendido.
    cursor.execute(sql_buscar, (produto_id,))

    # Recupera o último registro encontrado.
    estoque = cursor.fetchone()

    # Sem registro anterior, não há quantidades de referência
    # para realizar a baixa. Fecha os recursos e encerra.
    if not estoque:
        cursor.close()
        conexao.close()
        return

    # Armazena as quantidades atuais do registro encontrado.
    atual_caixa = estoque[0]
    atual_unidade = estoque[1]
    atual_fracionada = estoque[2]

    # --------------------------------------------------------
    # 2. BUSCAR AS CONFIGURAÇÕES DO PRODUTO
    # --------------------------------------------------------

    # Consulta os dados utilizados nas conversões de caixa,
    # unidade e dose.
    sql_produto = """
        SELECT
            quantidade_por_caixa,
            quantidade_por_unidade,
            vende_por_dose,
            volume_dose_ml

        FROM produto

        WHERE id = %s
    """

    # Busca as configurações do produto.
    cursor.execute(sql_produto, (produto_id,))

    # Recupera o resultado da consulta.
    produto = cursor.fetchone()

    # Separa os valores de acordo com a ordem das colunas.
    quantidade_por_caixa = produto[0]
    quantidade_por_unidade = produto[1]
    vende_por_dose = produto[2]
    volume_dose_ml = produto[3]

    # --------------------------------------------------------
    # 3. CONVERTER A QUANTIDADE VENDIDA
    # --------------------------------------------------------

    # Garante que a quantidade utilizada nos cálculos seja
    # um número inteiro, conforme a lógica atual.
    quantidade = int(quantidade)

    # Venda por caixa:
    # Retira a quantidade de caixas vendidas e calcula também
    # as unidades correspondentes às caixas.
    if tipo_venda == "caixa":
        baixa_caixa = quantidade

        baixa_unidade = (
            quantidade * quantidade_por_caixa
        )

        # A baixa por caixa não altera diretamente a quantidade
        # fracionada neste cálculo.
        baixa_fracionada = 0

    # Venda por dose:
    # A quantidade vendida é multiplicada pelo volume de
    # uma dose para calcular a saída fracionada.
    elif tipo_venda == "dose":
        baixa_caixa = 0
        baixa_unidade = 0

        baixa_fracionada = (
            quantidade * volume_dose_ml
        )

    # Outros tipos de venda:
    # Mantém o cálculo atual de caixas e unidades.
    else:
        # Calcula quantas caixas inteiras correspondem
        # à quantidade vendida.
        baixa_caixa = (
            quantidade // quantidade_por_caixa
        )

        # Registra a quantidade informada como saída de unidades.
        baixa_unidade = quantidade

        # Neste caso, não há baixa fracionada.
        baixa_fracionada = 0

    # --------------------------------------------------------
    # 4. CALCULAR AS NOVAS QUANTIDADES
    # --------------------------------------------------------

    # Subtrai as caixas que saíram das caixas atualmente
    # registradas no estoque.
    nova_caixa = atual_caixa - baixa_caixa

    # Subtrai as unidades que saíram das unidades atuais.
    nova_unidade = atual_unidade - baixa_unidade

    # Subtrai o volume fracionado vendido do total fracionado.
    nova_fracionada = (
        atual_fracionada - baixa_fracionada
    )

    # --------------------------------------------------------
    # 5. IMPEDIR QUANTIDADES NEGATIVAS
    # --------------------------------------------------------

    # Se o cálculo resultar em um número negativo, registra
    # zero para a quantidade correspondente.
    #
    # Esta é a regra existente no código original: ela limita
    # o valor gravado, mas não impede a venda em si.
    if nova_caixa < 0:
        nova_caixa = 0

    if nova_unidade < 0:
        nova_unidade = 0

    if nova_fracionada < 0:
        nova_fracionada = 0

    # --------------------------------------------------------
    # 6. REGISTRAR A BAIXA NO HISTÓRICO DE ESTOQUE
    # --------------------------------------------------------

    # Em vez de atualizar diretamente a linha anterior, insere
    # um novo registro contendo as quantidades resultantes.
    #
    # As quantidades recebidas ficam zeradas, pois este registro
    # representa uma saída, e não uma nova entrada de produtos.
    #
    # NOW() registra a data e a hora atuais no banco.
    sql_insert = """
        INSERT INTO estoque (
            produto_id,

            quantidade_recebida_caixa,
            quantidade_recebida_unidade,

            quantidade_atual_caixa,
            quantidade_atual_unidade,

            quantidade_fracionada,

            data_entrada,

            entrada,
            saida
        )
        VALUES (
            %s,
            0,
            0,
            %s,
            %s,
            %s,
            NOW(),
            0,
            %s
        )
    """

    # Insere o registro com as novas quantidades calculadas.
    # O valor de baixa_unidade é mantido no campo saida,
    # conforme a implementação original.
    cursor.execute(
        sql_insert,
        (
            produto_id,
            nova_caixa,
            nova_unidade,
            nova_fracionada,
            baixa_unidade
        )
    )

    # Confirma a gravação da saída no banco de dados.
    conexao.commit()

    # Fecha os recursos utilizados pela operação.
    cursor.close()
    conexao.close()


# ============================================================
# BUSCAR ESTOQUE ATUAL
# ============================================================

def buscar_estoque_atual(produto_id):
    """
    Busca as quantidades atuais do último registro de estoque
    de um produto específico.

    Parâmetro:
        produto_id: identificador do produto no banco de dados.

    Retorno:
        Um dicionário com as quantidades encontradas ou None
        quando não existir um registro para o produto.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna os resultados como dicionários.
    # Assim, quem chamar esta função poderá acessar os valores
    # usando o nome das colunas.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta as quantidades atuais do registro mais recente
    # associado ao produto informado.
    sql = """
        SELECT
            quantidade_atual_caixa,
            quantidade_atual_unidade,
            quantidade_fracionada

        FROM estoque

        WHERE produto_id = %s

        ORDER BY id DESC

        LIMIT 1
    """

    # Executa a consulta usando o identificador recebido.
    cursor.execute(sql, (produto_id,))

    # Recupera somente o primeiro registro encontrado.
    # Se nenhum registro existir, o resultado será None.
    estoque = cursor.fetchone()

    # Fecha o cursor e a conexão após concluir a consulta.
    cursor.close()
    conexao.close()

    # Retorna o registro encontrado para o controller ou
    # outra função que tenha solicitado essas informações.
    return estoque


# ============================================================
# LISTAR ESTOQUE ATUAL
# ============================================================

def listar_estoque_atual():
    """
    Lista os produtos cadastrados e as quantidades do estoque
    mais recente de cada produto.

    Também classifica cada produto de acordo com seu estoque:
    - nunca_abastecido: ainda não possui registro de estoque.
    - sem_estoque: quantidade atual igual a zero.
    - baixo: quantidade atual abaixo do mínimo.
    - minimo: quantidade atual igual ao mínimo.
    - normal: quantidade atual acima do mínimo.

    A classificação é adicionada ao resultado em Python,
    sem modificar os registros armazenados no banco.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Utiliza um cursor que retorna os resultados como dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Busca os produtos e relaciona cada um ao seu registro
    # de estoque mais recente.
    #
    # A subconsulta:
    #     SELECT MAX(id) FROM estoque WHERE produto_id = p.id
    #
    # encontra o maior identificador de estoque de cada produto.
    # O LEFT JOIN garante que os produtos também apareçam quando
    # ainda não possuem nenhum registro de estoque.
    sql = """
        SELECT
            p.id,
            p.nome,
            p.categoria,

            p.tipo_embalagem,
            p.sabor,
            p.volume,

            p.estoque_minimo,
            p.vende_por_dose,
            p.vende_por_unidade,

            e.quantidade_atual_caixa,
            e.quantidade_atual_unidade,
            e.quantidade_fracionada

        FROM produto p

        LEFT JOIN estoque e
            ON e.id = (
                SELECT MAX(id)
                FROM estoque
                WHERE produto_id = p.id
            )

        ORDER BY p.nome
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera todos os produtos e seus dados de estoque.
    dados = cursor.fetchall()

    # Percorre cada produto para determinar seu status de estoque.
    for produto in dados:

        # Quando a quantidade de caixas é None, significa que
        # o LEFT JOIN não encontrou um registro de estoque.
        # Nesse caso, o produto nunca foi abastecido.
        if produto["quantidade_atual_caixa"] is None:
            produto["status_estoque"] = "nunca_abastecido"

            # Interrompe somente o processamento deste produto
            # e continua com o próximo item da lista.
            continue

        # Utiliza zero como estoque mínimo quando o campo estiver
        # vazio ou contiver um valor considerado falso em Python.
        minimo = produto["estoque_minimo"] or 0

        # Utiliza zero como quantidade de unidades quando o valor
        # armazenado estiver vazio ou for None.
        estoque = produto["quantidade_atual_unidade"] or 0

        # Sem unidades disponíveis: classifica como sem estoque.
        if estoque == 0:
            produto["status_estoque"] = "sem_estoque"

        # Quantidade positiva, mas abaixo do estoque mínimo.
        elif estoque < minimo:
            produto["status_estoque"] = "baixo"

        # Quantidade exatamente igual ao estoque mínimo.
        elif estoque == minimo:
            produto["status_estoque"] = "minimo"

        # Quantidade acima do estoque mínimo.
        else:
            produto["status_estoque"] = "normal"

    # Fecha os recursos utilizados na consulta.
    cursor.close()
    conexao.close()

    # Retorna a lista de produtos já com o status calculado.
    return dados


# ============================================================
# BUSCAR DETALHES DO PRODUTO NO ESTOQUE
# ============================================================

def buscar_detalhes_produto(produto_id):
    """
    Busca os detalhes do registro de estoque mais recente
    de um produto específico.

    As informações retornadas incluem:
    - Nome, categoria, sabor e embalagem do produto.
    - Tipo e origem da entrada.
    - Nome da origem informada.
    - Quantidades recebidas e quantidades atuais.
    - Preços registrados na entrada.
    - Data de entrada.

    Parâmetro:
        produto_id: identificador do produto no banco.

    Retorno:
        Um dicionário com os detalhes encontrados ou None
        se não houver registro correspondente.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que permite acessar os campos pelo nome.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta os detalhes do produto e de sua movimentação
    # de estoque mais recente.
    #
    # A tabela produto fornece as informações do produto.
    # A tabela estoque fornece as informações da entrada.
    # A tabela origem_compra é opcional, por isso utiliza LEFT JOIN.
    sql = """
        SELECT
            p.nome,
            p.categoria,

            p.sabor,
            p.tipo_embalagem,
            p.volume,

            e.tipo_entrada,

            oc.nome AS origem,

            e.nome_origem,

            e.quantidade_recebida_caixa,
            e.quantidade_recebida_unidade,

            e.quantidade_atual_caixa,
            e.quantidade_atual_unidade,

            e.preco_total_compra,
            e.preco_por_caixa,
            e.preco_por_unidade,

            e.data_entrada

        FROM estoque e

        INNER JOIN produto p
            ON p.id = e.produto_id

        LEFT JOIN origem_compra oc
            ON oc.id = e.origem_compra_id

        WHERE e.produto_id = %s

        ORDER BY e.id DESC

        LIMIT 1
    """

    # Executa a consulta para o produto solicitado.
    cursor.execute(sql, (produto_id,))

    # Recupera somente o registro mais recente.
    dados = cursor.fetchone()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna os detalhes para a função que chamou o model.
    return dados

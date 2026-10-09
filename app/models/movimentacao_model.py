
# ============================================================
# MODEL DE MOVIMENTAÇÃO DE ESTOQUE
# ============================================================
# Este arquivo contém as funções responsáveis por:
# - Listar os produtos disponíveis para movimentação.
# - Registrar movimentações manuais de estoque.
# - Consultar o histórico das movimentações realizadas.
#
# A movimentação pode alterar as quantidades registradas no
# estoque conforme o tipo de operação informado.
#
# O histórico é armazenado na tabela movimentacao_estoque.
# As quantidades atuais são atualizadas na tabela estoque.
# ============================================================


# Importa a função responsável por conectar ao PostgreSQL.
from app.database.conexao import conectar

# Permite retornar os resultados das consultas como dicionários.
from psycopg2.extras import RealDictCursor


# ============================================================
# LISTAR PRODUTOS PARA MOVIMENTAÇÃO
# ============================================================

def listar_produtos_movimentacao():
    """
    Lista os produtos ativos que podem ser selecionados
    durante o cadastro de uma movimentação.

    Retorno:
        Lista de dicionários contendo o identificador e o
        nome de cada produto ativo, ordenados pelo nome.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna os resultados como dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Busca o identificador e o nome dos produtos ativos.
    #
    # O filtro ativo = 1 mantém a regra existente para selecionar
    # os produtos que podem aparecer nessa listagem.
    sql = """
        SELECT
            id,
            nome
        FROM produto
        WHERE ativo = 1
        ORDER BY nome
    """

    # Executa a consulta SQL.
    cursor.execute(sql)

    # Recupera todos os produtos encontrados.
    produtos = cursor.fetchall()

    # Fecha o cursor e a conexão após concluir a consulta.
    cursor.close()
    conexao.close()

    # Retorna a lista de produtos para a camada que a solicitou.
    return produtos


# ============================================================
# CADASTRAR MOVIMENTAÇÃO DE ESTOQUE
# ============================================================

def cadastrar_movimentacao(
    produto_id,
    tipo_movimentacao,
    quantidade_caixa,
    quantidade_unidade,
    quantidade_fracionada,
    motivo
):
    """
    Registra uma movimentação manual e atualiza as quantidades
    do último registro de estoque do produto.

    Parâmetros:
        produto_id:
            Identificador do produto movimentado.

        tipo_movimentacao:
            Tipo da operação. O código trata especificamente
            o valor "ajuste_manual"; os demais valores seguem
            a lógica de saída.

        quantidade_caixa:
            Quantidade de caixas movimentadas.

        quantidade_unidade:
            Quantidade de unidades movimentadas.

        quantidade_fracionada:
            Quantidade fracionada movimentada.

        motivo:
            Justificativa informada para a movimentação.

    Fluxo:
        1. Registra a movimentação no histórico.
        2. Busca o último registro de estoque do produto.
        3. Obtém a quantidade de unidades por caixa.
        4. Valida a disponibilidade, quando aplicável.
        5. Calcula as novas quantidades.
        6. Atualiza o registro de estoque.
        7. Confirma as operações no banco.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor para executar as consultas e alterações.
    cursor = conexao.cursor()

    # --------------------------------------------------------
    # 1. IDENTIFICAR O USUÁRIO RESPONSÁVEL
    # --------------------------------------------------------

    # Importa a sessão do Flask dentro da função, mantendo
    # a organização do código original.
    from flask import session

    # Obtém o identificador do usuário autenticado.
    # Esse identificador será armazenado no histórico para
    # identificar quem realizou a movimentação.
    usuario_id = session["usuario_id"]

    # --------------------------------------------------------
    # 2. REGISTRAR A MOVIMENTAÇÃO NO HISTÓRICO
    # --------------------------------------------------------

    # Insere os dados da operação na tabela movimentacao_estoque.
    #
    # O histórico registra:
    # - O produto movimentado.
    # - O tipo de movimentação.
    # - As quantidades informadas.
    # - O motivo da operação.
    # - O usuário responsável.
    sql = """
        INSERT INTO movimentacao_estoque (
            produto_id,
            tipo_movimentacao,
            quantidade_caixa,
            quantidade_unidade,
            quantidade_fracionada,
            motivo,
            usuario_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Executa a inserção usando os valores recebidos.
    cursor.execute(
        sql,
        (
            produto_id,
            tipo_movimentacao,
            quantidade_caixa,
            quantidade_unidade,
            quantidade_fracionada,
            motivo,
            usuario_id
        )
    )

    # --------------------------------------------------------
    # 3. BUSCAR O ÚLTIMO REGISTRO DE ESTOQUE
    # --------------------------------------------------------

    # Busca o registro mais recente de estoque do produto.
    #
    # A ordenação pelo identificador, em ordem decrescente,
    # coloca o registro mais recente em primeiro lugar.
    # O LIMIT 1 restringe o resultado a um único registro.
    sql_estoque = """
        SELECT *
        FROM estoque
        WHERE produto_id = %s
        ORDER BY id DESC
        LIMIT 1
    """

    # Executa a consulta para o produto movimentado.
    cursor.execute(
        sql_estoque,
        (produto_id,)
    )

    # Recupera o registro de estoque encontrado.
    estoque = cursor.fetchone()

    # Se não existir um registro de estoque, confirma o
    # histórico da movimentação, fecha os recursos e encerra.
    #
    # Esse comportamento é mantido conforme o código original:
    # a movimentação pode ficar registrada mesmo sem um registro
    # de estoque correspondente para atualizar.
    if not estoque:
        conexao.commit()

        cursor.close()
        conexao.close()

        return

    # --------------------------------------------------------
    # 4. BUSCAR A QUANTIDADE DE UNIDADES POR CAIXA
    # --------------------------------------------------------

    # Consulta a configuração do produto usada para converter
    # caixas em unidades.
    sql_produto = """
        SELECT quantidade_por_caixa
        FROM produto
        WHERE id = %s
    """

    # Executa a consulta do produto.
    cursor.execute(
        sql_produto,
        (produto_id,)
    )

    # Recupera as configurações encontradas.
    produto = cursor.fetchone()

    # Obtém a quantidade de unidades por caixa.
    #
    # O operador or 1 mantém a regra original:
    # se o valor for considerado falso, utiliza 1 como divisor
    # ou multiplicador de referência nos cálculos seguintes.
    quantidade_por_caixa = produto[0] or 1

    # --------------------------------------------------------
    # 5. IDENTIFICAR AS QUANTIDADES DO ESTOQUE
    # --------------------------------------------------------

    # O cursor utilizado nesta consulta retorna uma tupla.
    # Por isso, os campos são acessados por suas posições.
    #
    # IMPORTANTE:
    # As posições abaixo foram mantidas conforme o código
    # original. Elas dependem da ordem física das colunas
    # retornadas por SELECT * na tabela estoque.
    estoque_id = estoque[0]

    # Quantidade de caixas registrada no estoque.
    quantidade_atual_caixa = estoque[9] or 0

    # Quantidade de unidades registrada no estoque.
    quantidade_atual_unidade = estoque[10] or 0

    # Quantidade fracionada registrada no estoque.
    quantidade_atual_fracionada = estoque[17] or 0

    # --------------------------------------------------------
    # 6. CALCULAR O TOTAL DE UNIDADES DA MOVIMENTAÇÃO
    # --------------------------------------------------------

    # Converte as caixas informadas em unidades e soma as
    # unidades informadas separadamente.
    #
    # Exemplo:
    # 2 caixas × 12 unidades + 3 unidades = 27 unidades.
    #
    # Este total será utilizado para validar e atualizar
    # a quantidade de unidades no estoque.
    movimentacao_total = (
        (quantidade_caixa * quantidade_por_caixa)
        + quantidade_unidade
    )

    # --------------------------------------------------------
    # 7. VALIDAR A DISPONIBILIDADE DO ESTOQUE
    # --------------------------------------------------------

    # A validação não é executada para o tipo "ajuste_manual".
    # Nos demais tipos, o código verifica se as quantidades
    # solicitadas ultrapassam as quantidades disponíveis.
    if tipo_movimentacao != "ajuste_manual":

        # Impede uma saída cujo total convertido em unidades
        # seja maior que a quantidade atual registrada.
        if movimentacao_total > quantidade_atual_unidade:
            raise Exception(
                "Quantidade maior que o estoque disponível!"
            )

        # Impede uma saída fracionada maior que a quantidade
        # fracionada disponível no estoque.
        if quantidade_fracionada > quantidade_atual_fracionada:
            raise Exception(
                "Quantidade avulsa maior que o estoque."
            )

    # --------------------------------------------------------
    # 8. PREPARAR A QUANTIDADE ATUAL DE UNIDADES
    # --------------------------------------------------------

    # Copia a quantidade atual de unidades para uma variável
    # de cálculo. O valor original foi obtido do banco.
    total_unidades = quantidade_atual_unidade

    # --------------------------------------------------------
    # 9. APLICAR A MOVIMENTAÇÃO NAS UNIDADES
    # --------------------------------------------------------

    # Em um ajuste manual, soma as unidades movimentadas.
    if tipo_movimentacao == "ajuste_manual":
        total_unidades += movimentacao_total

    # Para os demais tipos, subtrai as unidades movimentadas.
    else:
        total_unidades -= movimentacao_total

    # --------------------------------------------------------
    # 10. APLICAR A MOVIMENTAÇÃO NAS QUANTIDADES FRACIONADAS
    # --------------------------------------------------------

    # Em um ajuste manual, adiciona a quantidade fracionada.
    if tipo_movimentacao == "ajuste_manual":
        quantidade_atual_fracionada += quantidade_fracionada

    # Nos demais tipos, retira a quantidade fracionada.
    else:
        quantidade_atual_fracionada -= quantidade_fracionada

    # --------------------------------------------------------
    # 11. IMPEDIR QUE AS QUANTIDADES FIQUEM NEGATIVAS
    # --------------------------------------------------------

    # Se o cálculo de unidades resultar em um valor negativo,
    # o valor que será gravado é limitado a zero.
    if total_unidades < 0:
        total_unidades = 0

    # Aplica a mesma regra à quantidade fracionada.
    if quantidade_atual_fracionada < 0:
        quantidade_atual_fracionada = 0

    # --------------------------------------------------------
    # 12. RECALCULAR AS CAIXAS E AS UNIDADES
    # --------------------------------------------------------

    # Calcula quantas caixas inteiras correspondem ao total
    # de unidades restante.
    #
    # A divisão inteira (//) descarta a parte fracionária.
    # Exemplo: 25 unidades // 12 por caixa = 2 caixas.
    quantidade_atual_caixa = (
        total_unidades // quantidade_por_caixa
    )

    # Mantém o total de unidades calculado como a quantidade
    # atual de unidades, conforme a lógica original.
    quantidade_atual_unidade = total_unidades

    # --------------------------------------------------------
    # 13. ATUALIZAR O REGISTRO DE ESTOQUE
    # --------------------------------------------------------

    # Atualiza as quantidades do registro de estoque mais
    # recente que foi localizado anteriormente.
    #
    # A coluna saida recebe a soma das quantidades informadas
    # na movimentação, conforme a implementação original.
    sql_update = """
        UPDATE estoque
        SET
            quantidade_atual_caixa = %s,
            quantidade_atual_unidade = %s,
            quantidade_fracionada = %s,
            saida = saida + %s
        WHERE id = %s
    """

    # Executa a atualização do registro identificado por estoque_id.
    cursor.execute(
        sql_update,
        (
            quantidade_atual_caixa,
            quantidade_atual_unidade,
            quantidade_atual_fracionada,
            (
                quantidade_caixa
                + quantidade_unidade
                + quantidade_fracionada
            ),
            estoque_id
        )
    )

    # Confirma no banco tanto o registro do histórico quanto
    # a atualização do estoque, pois ambas as operações usam
    # a mesma conexão e ainda não houve commit intermediário.
    conexao.commit()

    # Fecha o cursor e a conexão após concluir a movimentação.
    cursor.close()
    conexao.close()


# ============================================================
# LISTAR HISTÓRICO DE MOVIMENTAÇÕES
# ============================================================

def listar_movimentacoes():
    """
    Lista o histórico de movimentações de estoque.

    A consulta retorna:
    - Todas as colunas da movimentação.
    - O nome do produto movimentado.
    - O nome do usuário responsável, quando disponível.

    As movimentações mais recentes aparecem primeiro.

    Retorno:
        Lista de dicionários com os dados do histórico.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria um cursor que retorna os registros como dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta o histórico e relaciona cada movimentação
    # ao produto correspondente e ao usuário responsável.
    #
    # INNER JOIN:
    # Relaciona a movimentação a um produto existente.
    #
    # LEFT JOIN:
    # Permite retornar a movimentação mesmo quando não existe
    # um usuário correspondente ao identificador registrado.
    #
    # A ordenação decrescente pela data apresenta os registros
    # mais recentes no início da lista.
    sql = """
        SELECT
            m.*,
            p.nome,
            u.nome AS usuario

        FROM movimentacao_estoque m

        INNER JOIN produto p
            ON p.id = m.produto_id

        LEFT JOIN usuario u
            ON u.id = m.usuario_id

        ORDER BY m.data_movimentacao DESC
    """

    # Executa a consulta do histórico.
    cursor.execute(sql)

    # Recupera todas as movimentações encontradas.
    movimentacoes = cursor.fetchall()

    # Fecha os recursos utilizados na consulta.
    cursor.close()
    conexao.close()

    # Retorna o histórico para a camada que solicitou os dados.
    return movimentacoes

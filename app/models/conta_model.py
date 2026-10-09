# ==================================================
# IMPORTA FUNÇÃO RESPONSÁVEL POR CRIAR CONEXÃO
# COM O BANCO DE DADOS POSTGRESQL
# ==================================================
from app.database.conexao import conectar

# ==================================================
# REALDICTCURSOR FAZ COM QUE OS RESULTADOS DAS
# CONSULTAS RETORNEM COMO DICIONÁRIO
#
# Exemplo:
#
# {
#     "id": 1,
#     "nome": "João"
# }
#
# Ao invés de:
#
# (1, "João")
# ==================================================
from psycopg2.extras import RealDictCursor

# ==================================================
# IMPORTA A SESSÃO DO FLASK
#
# A SESSÃO ARMAZENA DADOS DO USUÁRIO LOGADO
#
# Exemplo:
#
# session["usuario_id"]
# session["perfil"]
# ==================================================
from flask import session


# ==================================================
# FUNÇÃO AUXILIAR
#
# CRIA CONEXÃO E CURSOR COM REALDICTCURSOR
#
# ISSO EVITA REPETIR O MESMO CÓDIGO EM
# DIVERSAS FUNÇÕES DO ARQUIVO
# ==================================================
def criar_cursor_dict():

    # Cria conexão com banco
    conexao = conectar()

    # Cria cursor retornando dicionários
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Retorna ambos para uso posterior
    return conexao, cursor


# ==================================================
# LISTAR CONTAS PENDENTES
# ==================================================
def listar_contas_pendentes():

    # Cria conexão e cursor
    conexao, cursor = criar_cursor_dict()

    # ------------------------------------------------
    # ESTA CONSULTA RETORNA TODAS AS CONTAS
    # PENDENTES QUE AINDA ESTÃO ABERTAS
    #
    # TAMBÉM CALCULA:
    #
    # - DIAS EM ABERTO
    # - VALOR TOTAL ACUMULADO
    #
    # A SOMA É FEITA COM BASE NAS VENDAS
    # VINCULADAS À CONTA PENDENTE
    # ------------------------------------------------
    sql = """
        SELECT

            cp.id,

            cp.nome_cliente_temporario,

            cp.data_abertura,

            (
                CURRENT_DATE -
                DATE(cp.data_abertura)
            ) AS dias_pendente,

            COALESCE(
                SUM(v.valor_total),
                0
            ) AS valor_total

        FROM conta_pendente cp

        LEFT JOIN venda v

            ON v.conta_pendente_id = cp.id

        WHERE cp.status = 'aberta'

        GROUP BY

            cp.id,
            cp.nome_cliente_temporario,
            cp.data_abertura

        ORDER BY cp.id DESC
    """

    # Executa consulta
    cursor.execute(sql)

    # Obtém todas as contas encontradas
    contas = cursor.fetchall()

    # Libera cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna lista para controller
    return contas


# ==================================================
# BUSCAR PRODUTOS DE UMA VENDA
# ==================================================
def buscar_produtos_venda(venda_id):

    # Cria conexão e cursor
    conexao, cursor = criar_cursor_dict()

    # ------------------------------------------------
    # BUSCA TODOS OS PRODUTOS QUE FORAM
    # VENDIDOS EM UMA DETERMINADA VENDA
    #
    # TAMBÉM TRAZ:
    #
    # - Nome do produto
    # - Quantidade vendida
    # - Tipo de venda
    #
    # Exemplo:
    #
    # Unidade
    # Caixa
    # Dose
    # ------------------------------------------------
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

    # Executa consulta
    cursor.execute(
        sql,
        (venda_id,)
    )

    # Busca todos os produtos encontrados
    produtos = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna produtos encontrados
    return produtos


# ==================================================
# BUSCAR FICHAS DE SINUCA DE UMA VENDA
# ==================================================
def buscar_fichas_pendentes(venda_id):

    # Cria conexão e cursor
    conexao, cursor = criar_cursor_dict()

    # ------------------------------------------------
    # BUSCA TODAS AS FICHAS DE SINUCA
    # REGISTRADAS NESTA VENDA
    #
    # UMA VENDA PODE TER:
    #
    # - Produtos
    # - Fichas
    #
    # ESTA CONSULTA RECUPERA APENAS
    # AS FICHAS DA SINUCA
    # ------------------------------------------------
    sql = """
        SELECT *

        FROM sinuca_venda

        WHERE venda_id = %s
    """

    # Executa consulta
    cursor.execute(
        sql,
        (venda_id,)
    )

    # Busca todas as fichas encontradas
    fichas = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna resultado
    return fichas

# ==================================================
# BUSCAR CONTA FIADO ABERTA DE UM CLIENTE
# ==================================================
def buscar_conta_aberta(cliente_id):

    # Cria conexão e cursor
    conexao, cursor = criar_cursor_dict()

    # ------------------------------------------------
    # PROCURA UMA CONTA FIADO QUE ESTEJA
    # ASSOCIADA AO CLIENTE INFORMADO
    #
    # A CONSULTA RETORNA APENAS CONTAS
    # COM STATUS "aberta"
    #
    # LIMIT 1 É UTILIZADO PORQUE O SISTEMA
    # DEVE POSSUIR APENAS UMA CONTA ABERTA
    # POR CLIENTE
    # ------------------------------------------------
    sql = """
        SELECT *

        FROM conta

        WHERE cliente_id = %s

        AND status_conta = 'aberta'

        LIMIT 1
    """

    # Executa consulta
    cursor.execute(
        sql,
        (cliente_id,)
    )

    # Busca o primeiro resultado encontrado
    conta = cursor.fetchone()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna conta encontrada
    return conta


# ==================================================
# CRIAR CONTA FIADO
# ==================================================
def criar_conta(cliente_id):

    # Cria conexão com banco
    conexao = conectar()

    # Cursor padrão para INSERT
    cursor = conexao.cursor()

    # ------------------------------------------------
    # CRIA UMA NOVA CONTA FIADO
    #
    # A CONTA É CRIADA COM:
    #
    # - CLIENTE INFORMADO
    # - STATUS ABERTA
    # - SALDO INICIAL ZERO
    #
    # RETURNING ID PERMITE OBTER O ID
    # GERADO PELO BANCO IMEDIATAMENTE
    # APÓS O INSERT
    # ------------------------------------------------
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

        RETURNING id
    """

    # Executa inserção
    cursor.execute(
        sql,
        (cliente_id,)
    )

    # Obtém ID da conta criada
    conta_id = cursor.fetchone()[0]

    # Salva alteração
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna ID gerado
    return conta_id


# ==================================================
# ATUALIZAR SALDO DE UMA CONTA
# ==================================================
def atualizar_saldo_conta(
    cursor,
    conta_id,
    valor
):

    # ------------------------------------------------
    # ESTA FUNÇÃO RECEBE UM CURSOR JÁ ABERTO
    #
    # E SOMA UM VALOR AO SALDO DEVEDOR
    # DA CONTA INFORMADA
    #
    # NÃO É FEITO COMMIT AQUI
    #
    # ISSO É IMPORTANTE PORQUE ESTA FUNÇÃO
    # NORMALMENTE É UTILIZADA DENTRO DE
    # PROCESSOS MAIORES QUE EXECUTAM
    # VÁRIAS CONSULTAS NA MESMA TRANSAÇÃO
    # ------------------------------------------------
    sql = """
        UPDATE conta

        SET saldo_devedor =
            saldo_devedor + %s

        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            valor,
            conta_id
        )
    )


# ==================================================
# BUSCAR CONTA POR ID
# ==================================================
def buscar_conta_por_id(conta_id):

    # Cria conexão e cursor
    conexao, cursor = criar_cursor_dict()

    # ------------------------------------------------
    # BUSCA UMA CONTA ESPECÍFICA
    #
    # O ID É A CHAVE PRIMÁRIA DA TABELA
    #
    # COMO O ID É ÚNICO,
    # UTILIZAMOS FETCHONE()
    # ------------------------------------------------
    sql = """
        SELECT *

        FROM conta

        WHERE id = %s
    """

    cursor.execute(
        sql,
        (conta_id,)
    )

    # Busca registro encontrado
    conta = cursor.fetchone()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna resultado
    return conta


# ==================================================
# BUSCAR CONTA PENDENTE ABERTA
# ==================================================
def buscar_conta_pendente_aberta(nome_cliente):

    # Cria conexão e cursor
    conexao, cursor = criar_cursor_dict()

    # ------------------------------------------------
    # PROCURA UMA CONTA PENDENTE
    # COM O MESMO NOME INFORMADO
    #
    # É UTILIZADA PARA EVITAR
    # DUPLICAÇÃO DE CONTAS
    #
    # RETORNA APENAS CONTAS
    # COM STATUS "aberta"
    # ------------------------------------------------
    sql = """
        SELECT *

        FROM conta_pendente

        WHERE nome_cliente_temporario = %s

        AND status = 'aberta'

        LIMIT 1
    """

    cursor.execute(
        sql,
        (nome_cliente,)
    )

    # Busca resultado
    conta = cursor.fetchone()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna conta encontrada
    return conta


# ==================================================
# CRIAR CONTA PENDENTE
# ==================================================
def criar_conta_pendente(nome_cliente):

    # Cria conexão com banco
    conexao = conectar()

    # Cria cursor padrão
    cursor = conexao.cursor()

    # ------------------------------------------------
    # O USUÁRIO LOGADO É RECUPERADO
    # DA SESSÃO DO FLASK
    #
    # ISSO PERMITE SABER QUEM
    # CRIOU A CONTA PENDENTE
    # ------------------------------------------------
    usuario_id = session["usuario_id"]

    # ------------------------------------------------
    # CRIA UMA NOVA CONTA PENDENTE
    #
    # DADOS REGISTRADOS:
    #
    # - Nome informado
    # - Status aberta
    # - Usuário responsável
    # ------------------------------------------------
    sql = """
        INSERT INTO conta_pendente (

            nome_cliente_temporario,
            status,
            usuario_id

        )

        VALUES (

            %s,
            'aberta',
            %s

        )

        RETURNING id
    """

    cursor.execute(
        sql,
        (
            nome_cliente,
            usuario_id
        )
    )

    # Obtém ID criado
    conta_id = cursor.fetchone()[0]

    # Salva alteração
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna ID da conta criada
    return conta_id


# ==================================================
# BUSCAR CONTA PENDENTE POR ID
# ==================================================
def buscar_conta_pendente_por_id(conta_id):

    # Cria conexão e cursor
    conexao, cursor = criar_cursor_dict()

    # ------------------------------------------------
    # BUSCA UMA CONTA PENDENTE ESPECÍFICA
    #
    # ALÉM DOS DADOS DA CONTA,
    # TAMBÉM TRAZ O NOME DO USUÁRIO
    # RESPONSÁVEL PELA ABERTURA
    #
    # ISSO É FEITO ATRAVÉS DE UM
    # LEFT JOIN COM A TABELA USUARIO
    # ------------------------------------------------
    sql = """
        SELECT

            cp.*,

            u.nome AS usuario

        FROM conta_pendente cp

        LEFT JOIN usuario u
            ON u.id = cp.usuario_id

        WHERE cp.id = %s
    """

    cursor.execute(
        sql,
        (conta_id,)
    )

    # Busca resultado encontrado
    conta = cursor.fetchone()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna conta encontrada
    return conta


# ==================================================
# BUSCAR VENDAS DE UMA CONTA PENDENTE
# ==================================================
def buscar_vendas_conta_pendente(conta_id):

    # Cria conexão e cursor
    conexao, cursor = criar_cursor_dict()

    # ------------------------------------------------
    # RECUPERA TODAS AS VENDAS
    # VINCULADAS A UMA CONTA PENDENTE
    #
    # AS VENDAS SÃO ORDENADAS PELA DATA
    # MAIS ANTIGA PRIMEIRO
    #
    # ISSO FACILITA A VISUALIZAÇÃO
    # CRONOLÓGICA DA CONTA
    # ------------------------------------------------
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

    # Busca todas as vendas encontradas
    vendas = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna lista de vendas
    return vendas

# ==================================================
# TRANSFERIR CONTA PENDENTE PARA FIADO
# ==================================================
def transferir_para_fiado(
    conta_pendente_id,
    cliente_id
):

    # ------------------------------------------------
    # ESTA FUNÇÃO É RESPONSÁVEL POR:
    #
    # 1) LOCALIZAR OU CRIAR UMA CONTA FIADO
    #    PARA O CLIENTE SELECIONADO
    #
    # 2) SOMAR O VALOR TOTAL DAS VENDAS
    #    DA CONTA PENDENTE
    #
    # 3) ADICIONAR ESSE VALOR AO SALDO
    #    DEVEDOR DA CONTA FIADO
    #
    # 4) TRANSFERIR TODAS AS VENDAS DA
    #    CONTA PENDENTE PARA A CONTA FIADO
    #
    # 5) FECHAR A CONTA PENDENTE
    #
    # AO FINAL DO PROCESSO, A CONTA
    # PENDENTE DEIXA DE EXISTIR COMO
    # CONTA ABERTA E TODA A DÍVIDA PASSA
    # A PERTENCER AO CLIENTE CADASTRADO.
    # ------------------------------------------------

    # Cria conexão com banco
    conexao = conectar()

    # Cria cursor retornando dicionários
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # ==================================================
    # ETAPA 1
    # VERIFICAR SE O CLIENTE JÁ POSSUI
    # UMA CONTA FIADO ABERTA
    # ==================================================

    sql = """
        SELECT *

        FROM conta

        WHERE cliente_id = %s

        AND status_conta = 'aberta'

        LIMIT 1
    """

    cursor.execute(
        sql,
        (cliente_id,)
    )

    conta = cursor.fetchone()

    # ------------------------------------------------
    # SE A CONTA EXISTIR:
    #
    # UTILIZA A MESMA CONTA
    #
    # SE NÃO EXISTIR:
    #
    # CRIA UMA NOVA CONTA FIADO
    # ------------------------------------------------
    if conta:

        conta_id = conta["id"]

    else:

        # Cria nova conta aberta
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

            RETURNING id
        """

        cursor.execute(
            sql,
            (cliente_id,)
        )

        # Obtém ID da conta criada
        conta_id = cursor.fetchone()[0]

    # ==================================================
    # ETAPA 2
    # CALCULAR O VALOR TOTAL DA CONTA PENDENTE
    # ==================================================

    # ------------------------------------------------
    # SOMA O SALDO DEVEDOR DE TODAS AS
    # VENDAS QUE PERTENCEM À CONTA PENDENTE
    #
    # COALESCE GARANTE QUE O RESULTADO
    # NUNCA SEJA NULL
    # ------------------------------------------------
    sql = """
        SELECT

            COALESCE(
                SUM(saldo_devedor),
                0
            ) AS total

        FROM venda

        WHERE conta_pendente_id = %s
    """

    cursor.execute(
        sql,
        (conta_pendente_id,)
    )

    total = cursor.fetchone()

    # Valor total da dívida
    saldo = total["total"]

    # ==================================================
    # ETAPA 3
    # ADICIONAR O SALDO À CONTA FIADO
    # ==================================================

    # ------------------------------------------------
    # O VALOR DA CONTA PENDENTE É SOMADO
    # AO SALDO DEVEDOR DA CONTA FIADO
    #
    # CASO O CLIENTE JÁ TENHA DÍVIDAS
    # ANTERIORES, ELAS SERÃO MANTIDAS.
    # ------------------------------------------------
    sql = """
        UPDATE conta

        SET saldo_devedor =
            saldo_devedor + %s

        WHERE id = %s
    """

    cursor.execute(
        sql,
        (
            saldo,
            conta_id
        )
    )

    # ==================================================
    # ETAPA 4
    # TRANSFERIR AS VENDAS
    # ==================================================

    # ------------------------------------------------
    # TODAS AS VENDAS DA CONTA PENDENTE
    # PASSAM A PERTENCER À CONTA FIADO
    #
    # ALTERA:
    #
    # - conta_id
    # - cliente_id
    #
    # REMOVE:
    #
    # - conta_pendente_id
    #
    # ISSO EFETIVAMENTE MOVE AS VENDAS
    # PARA O FIADO
    # ------------------------------------------------
    sql = """
        UPDATE venda

        SET

            conta_id = %s,

            cliente_id = %s,

            conta_pendente_id = NULL

        WHERE conta_pendente_id = %s
    """

    cursor.execute(
        sql,
        (
            conta_id,
            cliente_id,
            conta_pendente_id
        )
    )

    # ==================================================
    # ETAPA 5
    # FECHAR CONTA PENDENTE
    # ==================================================

    # ------------------------------------------------
    # APÓS A TRANSFERÊNCIA,
    # A CONTA PENDENTE NÃO DEVE MAIS
    # APARECER COMO ABERTA NO SISTEMA.
    #
    # POR ISSO O STATUS É ALTERADO
    # PARA "fechada".
    # ------------------------------------------------
    sql = """
        UPDATE conta_pendente

        SET status = 'fechada'

        WHERE id = %s
    """

    cursor.execute(
        sql,
        (conta_pendente_id,)
    )

    # ==================================================
    # ETAPA 6
    # SALVAR TODAS AS ALTERAÇÕES
    # ==================================================

    # Confirma todas as operações executadas
    # durante esta transferência
    conexao.commit()

    # Libera cursor
    cursor.close()

    # Fecha conexão
    conexao.close()
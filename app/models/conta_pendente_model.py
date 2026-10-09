# ==================================================
# IMPORTA FUNÇÃO RESPONSÁVEL POR CRIAR CONEXÃO
# COM O BANCO DE DADOS
# ==================================================
from app.database.conexao import conectar

# ==================================================
# FAZ COM QUE AS CONSULTAS RETORNEM
# DICIONÁRIOS AO INVÉS DE TUPLAS
#
# Exemplo:
#
# {
#     "id": 1,
#     "nome": "João"
# }
# ==================================================
from psycopg2.extras import RealDictCursor

# ==================================================
# IMPORTA A SESSÃO DO FLASK
#
# UTILIZADA PARA RECUPERAR O USUÁRIO
# LOGADO NO MOMENTO DA OPERAÇÃO
# ==================================================
from flask import session


# ==================================================
# FUNÇÃO AUXILIAR
#
# EVITA REPETIR O MESMO BLOCO DE CÓDIGO
# EM TODAS AS CONSULTAS
# ==================================================
def criar_cursor_dict():

    # Cria conexão com banco
    conexao = conectar()

    # Cria cursor retornando dicionários
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Retorna conexão e cursor
    return conexao, cursor


# ==================================================
# BUSCAR CONTA PENDENTE ABERTA
# ==================================================
def buscar_conta_pendente_aberta(nome):

    # Cria conexão e cursor
    conexao, cursor = criar_cursor_dict()

    # ------------------------------------------------
    # PROCURA UMA CONTA PENDENTE COM O
    # NOME INFORMADO E STATUS "aberta"
    #
    # ESTA FUNÇÃO É UTILIZADA PARA EVITAR
    # QUE O SISTEMA CRIE MÚLTIPLAS CONTAS
    # PENDENTES PARA O MESMO NOME
    #
    # LIMIT 1 É UTILIZADO PORQUE BASTA
    # SABER SE EXISTE UMA CONTA ABERTA
    # ------------------------------------------------
    sql = """
        SELECT *

        FROM conta_pendente

        WHERE nome_cliente_temporario = %s

        AND status = 'aberta'

        LIMIT 1
    """

    # Executa consulta
    cursor.execute(
        sql,
        (nome,)
    )

    # Obtém resultado encontrado
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
def criar_conta_pendente(nome):

    # Cria conexão com banco
    conexao = conectar()

    # Cria cursor padrão para INSERT
    cursor = conexao.cursor()

    # ------------------------------------------------
    # RECUPERA O ID DO USUÁRIO LOGADO
    #
    # O USUÁRIO SERÁ REGISTRADO COMO
    # RESPONSÁVEL PELA ABERTURA DA CONTA
    # ------------------------------------------------
    usuario_id = session["usuario_id"]

    # ------------------------------------------------
    # CRIA UMA NOVA CONTA PENDENTE
    #
    # DADOS SALVOS:
    #
    # - Nome temporário informado
    # - Status inicial "aberta"
    # - Usuário responsável
    #
    # RETURNING ID RETORNA O ID GERADO
    # PELO BANCO DE DADOS
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

    # Executa inserção
    cursor.execute(
        sql,
        (
            nome,
            usuario_id
        )
    )

    # Captura ID criado
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
# FECHAR CONTA PENDENTE
# ==================================================
def fechar_conta_pendente(conta_id):

    # Cria conexão com banco
    conexao = conectar()

    # Cria cursor padrão
    cursor = conexao.cursor()

    # ------------------------------------------------
    # ALTERA O STATUS DA CONTA PENDENTE
    # PARA "Quitada"
    #
    # APÓS ESTA ALTERAÇÃO A CONTA NÃO
    # DEVE MAIS APARECER NAS LISTAGENS
    # DE CONTAS PENDENTES ABERTAS
    # ------------------------------------------------
    sql = """
        UPDATE conta_pendente

        SET status = 'Quitada'

        WHERE id = %s
    """

    # Executa atualização
    cursor.execute(
        sql,
        (conta_id,)
    )

    # Salva alteração no banco
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()
# ==================================================
# IMPORTAÇÕES
# ==================================================

# Importa a função responsável por criar
# a conexão com o banco de dados PostgreSQL.
from app.database.conexao import conectar

# Permite que os resultados das consultas
# sejam retornados em formato de dicionário.
#
# Exemplo:
# cliente["nome"]
#
# ao invés de:
# cliente[0]
#
from psycopg2.extras import RealDictCursor


# ==================================================
# LISTAR CLIENTES ATIVOS
# ==================================================
#
# Esta função busca todos os clientes ativos
# cadastrados no sistema.
#
# Além dos dados do cliente, também verifica
# se existe uma conta de fiado aberta e retorna:
#
# - conta_aberta (True ou False)
# - saldo_devedor
#
# Essas informações são utilizadas para exibir
# indicadores diretamente na tela de clientes.
#
# ==================================================

def listar_clientes():

    # Cria conexão com o banco
    conexao = conectar()

    # Cria cursor configurado para retornar
    # os resultados em formato de dicionário.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Consulta responsável por buscar
    # todos os clientes ativos.
    #
    # O LEFT JOIN permite verificar se
    # existe uma conta aberta para o cliente.
    cursor.execute("""
        SELECT

            c.*,

            CASE
                WHEN ct.id IS NOT NULL
                THEN TRUE
                ELSE FALSE
            END AS conta_aberta,

            COALESCE(
                ct.saldo_devedor,
                0
            ) AS saldo_devedor

        FROM cliente c

        LEFT JOIN conta ct
            ON ct.cliente_id = c.id
            AND ct.status_conta = 'aberta'

        WHERE c.ativo = 1
    """)

    # Obtém todos os registros retornados
    # pela consulta SQL.
    clientes = cursor.fetchall()

    # Fecha cursor.
    cursor.close()

    # Fecha conexão.
    conexao.close()

    # Retorna lista de clientes.
    return clientes


# ==================================================
# CADASTRAR CLIENTE
# ==================================================
#
# Insere um novo cliente no banco de dados.
#
# Recebe:
# - nome
#
# O cadastro é realizado utilizando
# parâmetros SQL (%s), evitando SQL Injection.
#
# ==================================================

def cadastrar_cliente(nome):

    # Cria conexão com o banco.
    conexao = conectar()

    # Cria cursor.
    cursor = conexao.cursor()

    # Executa inserção do cliente.
    cursor.execute(
        """
        INSERT INTO cliente (nome)
        VALUES (%s)
        """,
        (nome,)
    )

    # Confirma alteração no banco.
    conexao.commit()

    # Fecha cursor.
    cursor.close()

    # Fecha conexão.
    conexao.close()


# ==================================================
# DESATIVAR CLIENTE
# ==================================================
#
# Realiza a desativação lógica do cliente.
#
# O cliente não é removido do banco.
#
# Apenas o campo ativo é alterado para 0.
#
# ==================================================

def desativar_cliente(id_cliente):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE cliente
        SET ativo = 0
        WHERE id = %s
        """,
        (id_cliente,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


# ==================================================
# EDITAR CLIENTE
# ==================================================
#
# Atualiza o nome de um cliente já existente.
#
# Recebe:
# - id_cliente
# - nome
#
# ==================================================

def editar_cliente(
    id_cliente,
    nome
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE cliente
        SET nome = %s
        WHERE id = %s
        """,
        (
            nome,
            id_cliente
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


# ==================================================
# BUSCAR CLIENTE POR ID
# ==================================================
#
# Busca um cliente específico através
# do seu identificador.
#
# Retorna:
# - Dados do cliente
# - None caso não exista
#
# ==================================================

def buscar_cliente_por_id(id_cliente):

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT *
        FROM cliente
        WHERE id = %s
        """,
        (id_cliente,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conexao.close()

    return cliente


# ==================================================
# VERIFICAR CONTA ABERTA
# ==================================================
#
# Verifica se o cliente possui
# uma conta de fiado aberta.
#
# Retorna:
#
# {
#     saldo_devedor: valor
# }
#
# ou None caso não exista conta.
#
# Esta função é utilizada antes
# de permitir a desativação de clientes.
#
# ==================================================

def cliente_tem_conta_aberta(cliente_id):

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT saldo_devedor
        FROM conta
        WHERE cliente_id = %s
        AND status_conta = 'aberta'
        LIMIT 1
        """,
        (cliente_id,)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado


# ==================================================
# LISTAR CLIENTES INATIVOS
# ==================================================
#
# Retorna todos os clientes que
# foram desativados no sistema.
#
# Utilizado na tela de clientes inativos.
#
# ==================================================

def listar_clientes_inativos():

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT *
        FROM cliente
        WHERE ativo = 0
        """
    )

    clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return clientes


# ==================================================
# REATIVAR CLIENTE
# ==================================================
#
# Reativa um cliente previamente
# desativado.
#
# O campo ativo volta para 1.
#
# ==================================================

def reativar_cliente(id_cliente):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE cliente
        SET ativo = 1
        WHERE id = %s
        """,
        (id_cliente,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()
# Importa função de conexão
from app.database.conexao import conectar


# Função para buscar todos os clientes
def listar_clientes():

    # Faz conexão com banco
    conexao = conectar()

    # Cria cursor
    # dictionary=True transforma os dados em formato de dicionário
    cursor = conexao.cursor(dictionary=True)

    # Executa SQL
    cursor.execute("""
    SELECT *
    FROM cliente
    WHERE ativo = 1
""")

    # Guarda todos os resultados
    clientes = cursor.fetchall()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna resultados
    return clientes
# Função responsável por cadastrar cliente no banco
def cadastrar_cliente(nome):

    # Cria conexão com banco
    conexao = conectar()

    # Cria cursor
    cursor = conexao.cursor()

    # Comando SQL
    # %s é usado para segurança (evita SQL Injection)
    sql = "INSERT INTO cliente (nome) VALUES (%s)"

    # Valor que será inserido
    valores = (nome,)

    # Executa SQL
    cursor.execute(sql, valores)

    # Salva alteração no banco
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna mensagem de sucesso
    return "Cliente cadastrado com sucesso!"

# ==========================================
# DESATIVAR CLIENTE
# ==========================================
def desativar_cliente(id_cliente):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE cliente
        SET ativo = 0
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (id_cliente,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    # ==========================================
# EDITAR CLIENTE
# ==========================================
def editar_cliente(id_cliente, nome):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE cliente
        SET nome = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (nome, id_cliente)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


# ==========================================
# BUSCAR CLIENTE POR ID
# ==========================================
def buscar_cliente_por_id(id_cliente):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT *
        FROM cliente
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (id_cliente,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conexao.close()

    return cliente


# ==========================================
# VERIFICAR CONTA ABERTA
# ==========================================
def cliente_tem_conta_aberta(cliente_id):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    sql = """
        SELECT saldo_devedor
        FROM conta
        WHERE cliente_id = %s
        AND status_conta = 'aberta'
        LIMIT 1
    """

    cursor.execute(
        sql,
        (cliente_id,)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado

# ==========================================
# LISTAR CLIENTES INATIVOS
# ==========================================

def listar_clientes_inativos():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM cliente
        WHERE ativo = 0
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return clientes


# ==========================================
# REATIVAR CLIENTES
# ==========================================
def reativar_cliente(id_cliente):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE cliente
        SET ativo = 1
        WHERE id = %s
    """, (id_cliente,))

    conexao.commit()

    cursor.close()
    conexao.close()
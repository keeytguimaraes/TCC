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
    cursor.execute("SELECT * FROM cliente")

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
# Função responsável por excluir cliente
def excluir_cliente(id_cliente):

    # Conecta no banco
    conexao = conectar()

    # Cria cursor
    cursor = conexao.cursor()

    # Comando SQL
    sql = "DELETE FROM cliente WHERE id = %s"

    # Executa SQL
    cursor.execute(sql, (id_cliente,))

    # Salva alteração
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()
    # Função responsável por editar cliente
def editar_cliente(id_cliente, nome):

    # Conecta no banco
    conexao = conectar()

    # Cria cursor
    cursor = conexao.cursor()

    # Comando SQL
    sql = """
        UPDATE cliente
        SET nome = %s
        WHERE id = %s
    """

    # Executa SQL
    cursor.execute(sql, (nome, id_cliente))

    # Salva alteração
    conexao.commit()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()
    # Função responsável por buscar um cliente pelo ID
def buscar_cliente_por_id(id_cliente):

    # Conecta no banco
    conexao = conectar()

    # Cursor em formato dicionário
    cursor = conexao.cursor(dictionary=True)

    # SQL
    sql = "SELECT * FROM cliente WHERE id = %s"

    # Executa
    cursor.execute(sql, (id_cliente,))

    # Busca um único cliente
    cliente = cursor.fetchone()

    # Fecha cursor
    cursor.close()

    # Fecha conexão
    conexao.close()

    # Retorna cliente
    return cliente
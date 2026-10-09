# Importa a função responsável
# por criar conexão com o banco.
from app.database.conexao import conectar

# Permite que o resultado das consultas
# seja retornado como dicionário.
#
# Exemplo:
#
# resultado["nome"]
#
# ao invés de:
#
# resultado[0]
#
from psycopg2.extras import RealDictCursor


# ==================================================
# BUSCAR USUÁRIO PELO LOGIN
# ==================================================
#
# Esta função é utilizada durante
# o processo de autenticação.
#
# Recebe o nome de usuário digitado
# na tela de login e procura um
# usuário ativo no banco de dados.
#
# Apenas usuários ativos podem
# realizar login no sistema.
#
# Retorna:
#
# - Dados do usuário (dict)
# - None caso não encontre
#
# Fluxo:
#
# Controller → Model → Banco
#
# ==================================================

def buscar_usuario_por_login(usuario):

    # Cria conexão com o PostgreSQL
    conexao = conectar()

    # Cria cursor que retorna os dados
    # em formato de dicionário.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Executa consulta procurando
    # o usuário informado.
    #
    # O filtro ativo = 1 garante
    # que apenas usuários ativos
    # possam acessar o sistema.
    cursor.execute(
        """
        SELECT *
        FROM usuario
        WHERE usuario = %s
        AND ativo = 1
        """,
        (usuario,)
    )

    # Obtém apenas um resultado,
    # pois o login deve ser único.
    resultado = cursor.fetchone()

    # Fecha cursor.
    cursor.close()

    # Fecha conexão.
    conexao.close()

    # Retorna usuário encontrado
    # ou None.
    return resultado
from app.database.conexao import conectar
from psycopg2.extras import RealDictCursor


def buscar_usuario_por_login(usuario):

    conexao = conectar()

    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT *
        FROM usuario
        WHERE usuario = %s
        AND ativo = 1
        """,
        (usuario,)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado
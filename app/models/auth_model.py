from app.database.conexao import conectar


def buscar_usuario_por_login(usuario):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
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
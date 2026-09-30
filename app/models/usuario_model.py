from app.database.conexao import conectar

def listar_usuarios():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            id,
            nome,
            usuario,
            perfil,
            ativo
        FROM usuario
        ORDER BY nome
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados

def cadastrar_usuario(
    nome,
    usuario,
    senha,
    perfil
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO usuario
        (
            nome,
            usuario,
            senha,
            perfil,
            ativo
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            1
        )
        """,
        (
            nome,
            usuario,
            senha,
            perfil
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()

def buscar_usuario_por_nome_usuario(
    usuario
):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT id
        FROM usuario
        WHERE usuario = %s
        """,
        (usuario,)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado

def buscar_usuario_por_id(id_usuario):

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM usuario
        WHERE id = %s
        """,
        (id_usuario,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario

def editar_usuario(
    id_usuario,
    nome,
    usuario,
    perfil
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE usuario
        SET
            nome = %s,
            usuario = %s,
            perfil = %s
        WHERE id = %s
        """,
        (
            nome,
            usuario,
            perfil,
            id_usuario
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()

def desativar_usuario(
    id_usuario
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE usuario
        SET ativo = 0
        WHERE id = %s
        """,
        (id_usuario,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

def listar_usuarios_inativos():

    conexao = conectar()

    cursor = conexao.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM usuario
        WHERE ativo = 0
        ORDER BY nome
        """
    )

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados

def reativar_usuario(
    id_usuario
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE usuario
        SET ativo = 1
        WHERE id = %s
        """,
        (id_usuario,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

def alterar_senha_usuario(
    id_usuario,
    senha_hash
):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE usuario
        SET senha = %s
        WHERE id = %s
        """,
        (
            senha_hash,
            id_usuario
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()
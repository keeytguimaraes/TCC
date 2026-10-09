
# ============================================================
# MODELO DE USUÁRIOS
# ============================================================
# Este arquivo contém as funções responsáveis por consultar e
# modificar os usuários cadastrados no banco de dados do SIGC.
#
# As operações disponíveis são:
# - Listar usuários;
# - Cadastrar novos usuários;
# - Buscar usuários por nome de usuário ou ID;
# - Editar os dados de um usuário.
#
# Este arquivo trabalha somente com o banco de dados.
# As rotas e os controllers são responsáveis por receber as
# informações das telas e chamar as funções deste modelo.
# ============================================================


# Importa a função que estabelece a conexão com o PostgreSQL.
from app.database.conexao import conectar

# Importa RealDictCursor para retornar os registros como
# dicionários, permitindo acessar os campos pelo nome.
#
# Exemplo:
# usuario["nome"]
# usuario["perfil"]
from psycopg2.extras import RealDictCursor


def listar_usuarios():
    """
    Retorna todos os usuários cadastrados no sistema.

    A consulta seleciona apenas os campos necessários para
    a listagem principal de usuários. A senha não é retornada.

    Os registros são organizados alfabeticamente pelo nome.

    Retorno:
        Uma lista de dicionários contendo:
        id, nome, usuario, perfil e ativo.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que transforma cada registro retornado
    # pelo PostgreSQL em um dicionário.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Busca os campos necessários para exibir os usuários.
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

    # Recupera todos os registros encontrados.
    dados = cursor.fetchall()

    # Encerra o cursor e a conexão após a consulta.
    cursor.close()
    conexao.close()

    # Entrega a lista de usuários para quem chamou a função.
    return dados


def cadastrar_usuario(
    nome,
    usuario,
    senha,
    perfil
):
    """
    Cadastra um novo usuário no sistema.

    Parâmetros:
        nome: nome de exibição do usuário.
        usuario: nome de usuário utilizado para identificação.
        senha: valor da senha que será armazenado no banco.
        perfil: perfil de acesso atribuído ao usuário.

    O novo usuário é cadastrado com ativo = 1, preservando
    o comportamento da consulta original.
    """

    # Estabelece a conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar o comando SQL.
    cursor = conexao.cursor()

    # Insere o novo usuário.
    # Os valores são enviados separadamente para que o driver
    # trate os parâmetros corretamente, sem concatenar os
    # dados diretamente ao texto SQL.
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

    # Confirma a inclusão no banco de dados.
    conexao.commit()

    # Libera os recursos utilizados.
    cursor.close()
    conexao.close()


def buscar_usuario_por_nome_usuario(
    usuario
):
    """
    Busca um usuário pelo nome de usuário informado.

    Essa função retorna somente o ID, sendo útil, por exemplo,
    para verificar se determinado nome de usuário já existe.

    Parâmetros:
        usuario: nome de usuário que será pesquisado.

    Retorno:
        Um dicionário com o campo id, caso encontre o registro.
        Retorna None caso nenhum registro seja encontrado.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Utiliza RealDictCursor para acessar o resultado pelo nome
    # do campo, como resultado["id"].
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Pesquisa o usuário pelo campo usuario.
    cursor.execute(
        """
        SELECT id
        FROM usuario
        WHERE usuario = %s
        """,
        (usuario,)
    )

    # Recupera apenas o primeiro registro encontrado.
    resultado = cursor.fetchone()

    # Fecha os recursos da consulta.
    cursor.close()
    conexao.close()

    # Retorna o registro ou None.
    return resultado


def buscar_usuario_por_id(id_usuario):
    """
    Busca um usuário pelo seu identificador no banco.

    Parâmetros:
        id_usuario: ID do usuário que será pesquisado.

    Retorno:
        Um dicionário com os campos da tabela usuario,
        caso o registro exista; caso contrário, None.
    """

    # Estabelece a conexão com o banco.
    conexao = conectar()

    # Configura o cursor para retornar os dados como dicionário.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Busca todos os campos do usuário correspondente ao ID.
    cursor.execute(
        """
        SELECT *
        FROM usuario
        WHERE id = %s
        """,
        (id_usuario,)
    )

    # Recupera um único registro.
    usuario = cursor.fetchone()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Devolve os dados encontrados.
    return usuario


def editar_usuario(
    id_usuario,
    nome,
    usuario,
    perfil
):
    """
    Atualiza os dados básicos de um usuário existente.

    Parâmetros:
        id_usuario: ID do registro que será atualizado.
        nome: novo nome de exibição.
        usuario: novo nome de usuário.
        perfil: novo perfil de acesso.

    A senha não é alterada por esta função.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria o cursor para executar o UPDATE.
    cursor = conexao.cursor()

    # Atualiza somente nome, usuario e perfil.
    # O WHERE garante que a alteração seja direcionada
    # ao usuário cujo ID foi informado.
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

    # Confirma as alterações.
    conexao.commit()

    # Libera os recursos.
    cursor.close()
    conexao.close()


def desativar_usuario(
    id_usuario
):
    """
    Desativa um usuário sem excluir seu registro do banco.

    Parâmetros:
        id_usuario: ID do usuário que será desativado.

    A função altera o campo ativo para 0, preservando
    o registro e o histórico relacionado ao usuário.
    """

    # Estabelece a conexão com o banco.
    conexao = conectar()

    # Cria o cursor para executar a atualização.
    cursor = conexao.cursor()

    # Marca o usuário como inativo.
    cursor.execute(
        """
        UPDATE usuario
        SET ativo = 0
        WHERE id = %s
        """,
        (id_usuario,)
    )

    # Confirma a alteração no banco.
    conexao.commit()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()


def listar_usuarios_inativos():
    """
    Retorna os usuários que estão desativados.

    A consulta busca todos os campos dos registros cujo
    campo ativo possui valor 0.

    Os resultados são organizados pelo nome.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Utiliza um cursor que retorna cada registro como dicionário.
    cursor = conexao.cursor(
        cursor_factory=RealDictCursor
    )

    # Seleciona os usuários inativos.
    cursor.execute(
        """
        SELECT *
        FROM usuario
        WHERE ativo = 0
        ORDER BY nome
        """
    )

    # Recupera todos os usuários encontrados.
    dados = cursor.fetchall()

    # Fecha os recursos da consulta.
    cursor.close()
    conexao.close()

    # Retorna a lista de usuários inativos.
    return dados


def reativar_usuario(
    id_usuario
):
    """
    Reativa um usuário anteriormente desativado.

    Parâmetros:
        id_usuario: ID do usuário que será reativado.

    A função altera o campo ativo para 1.
    """

    # Abre a conexão com o banco.
    conexao = conectar()

    # Cria o cursor para executar o UPDATE.
    cursor = conexao.cursor()

    # Marca o usuário como ativo.
    cursor.execute(
        """
        UPDATE usuario
        SET ativo = 1
        WHERE id = %s
        """,
        (id_usuario,)
    )

    # Confirma a atualização.
    conexao.commit()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()


def alterar_senha_usuario(
    id_usuario,
    senha_hash
):
    """
    Altera a senha armazenada para um usuário específico.

    Parâmetros:
        id_usuario: ID do usuário cuja senha será alterada.
        senha_hash: valor da senha que será gravado no banco.

    IMPORTANTE:
        O parâmetro se chama senha_hash, mas esta função
        apenas grava o valor recebido. Ela não gera o hash.

        Portanto, o controller ou serviço que chamar esta
        função deve garantir que a senha já esteja protegida
        por um algoritmo de hash apropriado antes de armazená-la.
    """

    # Estabelece a conexão com o banco.
    conexao = conectar()

    # Cria o cursor para executar a atualização.
    cursor = conexao.cursor()

    # Atualiza a senha somente para o usuário informado.
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

    # Confirma a alteração no banco.
    conexao.commit()

    # Libera os recursos utilizados.
    cursor.close()
    conexao.close()
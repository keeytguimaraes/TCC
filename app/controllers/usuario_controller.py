from app.models.usuario_model import (
    listar_usuarios,
    cadastrar_usuario,
    buscar_usuario_por_nome_usuario,
    buscar_usuario_por_id,
    editar_usuario,
    desativar_usuario,
    listar_usuarios_inativos,
    reativar_usuario,
    alterar_senha_usuario
)

from werkzeug.security import (
    generate_password_hash
)

def pegar_usuarios():

    return listar_usuarios()

def cadastrar_usuario_controller(
    nome,
    usuario,
    senha,
    perfil
):

    senha_hash = generate_password_hash(
        senha
    )

    cadastrar_usuario(
        nome,
        usuario,
        senha_hash,
        perfil
    )

def usuario_existe(
    usuario
):

    return buscar_usuario_por_nome_usuario(
        usuario
    )

def buscar_usuario_controller(
    id_usuario
):

    return buscar_usuario_por_id(
        id_usuario
    )

def editar_usuario_controller(
    id_usuario,
    nome,
    usuario,
    perfil
):

    editar_usuario(
        id_usuario,
        nome,
        usuario,
        perfil
    )

def desativar_usuario_controller(
    id_usuario
):

    desativar_usuario(
        id_usuario
    )

def listar_usuarios_inativos_controller():

    return listar_usuarios_inativos()

def reativar_usuario_controller(
    id_usuario
):

    reativar_usuario(
        id_usuario
    )

def alterar_senha_usuario_controller(
    id_usuario,
    senha
):

    senha_hash = generate_password_hash(
        senha
    )

    alterar_senha_usuario(
        id_usuario,
        senha_hash
    )
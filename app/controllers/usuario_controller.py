# Importa as funções responsáveis
# pelas operações de usuários no banco.
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

# Importa função utilizada para
# criptografar senhas antes de salvar
# no banco de dados.
from werkzeug.security import (
    generate_password_hash
)


# ==================================================
# GERAR HASH DE SENHA
# ==================================================
#
# Centraliza a criação do hash das senhas.
#
# Isso evita repetição de código e garante
# que todas as senhas sejam armazenadas
# utilizando o mesmo padrão de segurança.
#
# ==================================================

def gerar_hash_senha(senha):

    return generate_password_hash(
        senha
    )


# ==================================================
# LISTAR USUÁRIOS
# ==================================================
#
# Retorna todos os usuários ativos
# cadastrados no sistema.
#
# ==================================================

def pegar_usuarios():

    return listar_usuarios()


# ==================================================
# CADASTRAR USUÁRIO
# ==================================================
#
# Recebe os dados do formulário,
# gera o hash da senha e envia
# as informações para o model.
#
# A senha nunca é salva em texto puro.
#
# ==================================================

def cadastrar_usuario_controller(

    nome,

    usuario,

    senha,

    perfil
):

    senha_hash = gerar_hash_senha(
        senha
    )

    cadastrar_usuario(

        nome,

        usuario,

        senha_hash,

        perfil
    )


# ==================================================
# VERIFICAR SE USUÁRIO EXISTE
# ==================================================
#
# Busca um usuário através do login.
#
# Utilizado para impedir cadastros
# duplicados.
#
# ==================================================

def usuario_existe(

    usuario
):

    return buscar_usuario_por_nome_usuario(
        usuario
    )


# ==================================================
# BUSCAR USUÁRIO POR ID
# ==================================================
#
# Retorna os dados completos de um
# usuário específico.
#
# ==================================================

def buscar_usuario_controller(

    id_usuario
):

    return buscar_usuario_por_id(
        id_usuario
    )


# ==================================================
# EDITAR USUÁRIO
# ==================================================
#
# Atualiza os dados básicos do usuário.
#
# Não altera a senha.
#
# ==================================================

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


# ==================================================
# DESATIVAR USUÁRIO
# ==================================================
#
# Realiza a desativação lógica do usuário.
#
# O registro permanece no banco,
# porém deixa de aparecer entre
# os usuários ativos.
#
# ==================================================

def desativar_usuario_controller(

    id_usuario
):

    desativar_usuario(
        id_usuario
    )


# ==================================================
# LISTAR USUÁRIOS INATIVOS
# ==================================================
#
# Retorna todos os usuários
# atualmente desativados.
#
# ==================================================

def listar_usuarios_inativos_controller():

    return listar_usuarios_inativos()


# ==================================================
# REATIVAR USUÁRIO
# ==================================================
#
# Torna um usuário desativado
# ativo novamente.
#
# ==================================================

def reativar_usuario_controller(

    id_usuario
):

    reativar_usuario(
        id_usuario
    )


# ==================================================
# ALTERAR SENHA
# ==================================================
#
# Gera um novo hash para a senha
# informada e atualiza o registro
# do usuário.
#
# A senha nunca é armazenada
# em texto puro.
#
# ==================================================

def alterar_senha_usuario_controller(

    id_usuario,

    senha
):

    senha_hash = gerar_hash_senha(
        senha
    )

    alterar_senha_usuario(

        id_usuario,

        senha_hash
    )
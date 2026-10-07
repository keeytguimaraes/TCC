# Importa model
from app.models.fornecedor_model import (

    listar_fornecedores,
    cadastrar_fornecedor,
    buscar_fornecedor_por_id,
    editar_fornecedor,
    listar_fornecedores_inativos,
    reativar_fornecedor,
    desativar_fornecedor
)


# ==========================
# PEGAR FORNECEDORES
# ==========================
def pegar_fornecedores():

    return listar_fornecedores()


# ==========================
# CADASTRAR FORNECEDOR
# ==========================
def cadastrar_fornecedor_controller(

    nome,
    telefone,
    observacao
):

    cadastrar_fornecedor(

        nome,
        telefone,
        observacao
    )
# ==========================
# PEGAR FORNECEDOR POR ID
# ==========================
def pegar_fornecedor_por_id(

    id_fornecedor
):

    return buscar_fornecedor_por_id(
        id_fornecedor
    )


# ==========================
# EDITAR FORNECEDOR
# ==========================
def editar_fornecedor_controller(

    id_fornecedor,

    nome,
    telefone,
    observacao
):

    editar_fornecedor(

        id_fornecedor,

        nome,
        telefone,
        observacao
    )

# ==========================
# LISTAR FORNECEDORES INATIVOS
# ==========================

def pegar_fornecedores_inativos():

    return listar_fornecedores_inativos()

# ==========================
# REATIVAR FORNECEDOR
# ==========================

def reativar_fornecedor_controller(
    id_fornecedor
):

    reativar_fornecedor(
        id_fornecedor
    )

# ==========================
# DESATIVAR FORNECEDOR
# ==========================
def desativar_fornecedor_controller(
    id_fornecedor
):

    desativar_fornecedor(
        id_fornecedor
    )
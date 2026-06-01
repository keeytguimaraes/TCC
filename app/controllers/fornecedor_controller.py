# Importa model
from app.models.fornecedor_model import (

    listar_fornecedores,
    cadastrar_fornecedor,
    buscar_fornecedor_por_id,
    editar_fornecedor
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
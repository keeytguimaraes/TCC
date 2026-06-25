# Importa funções do model
from app.models.produto_model import (
    listar_produtos,
    cadastrar_produto,
    listar_categorias,
    buscar_produto_por_id,
    editar_produto,
    inativar_produto,
    ativar_produto
)

# ==========================
# CONTROLLER:
# PEGAR CATEGORIAS
# ==========================
def pegar_categorias():

    return listar_categorias()
# ==========================
# CONTROLLER:
# LISTAR PRODUTOS
# ==========================
def pegar_produtos():

    # Busca produtos no model
    produtos = listar_produtos()

    # Retorna lista
    return produtos

# ==========================
# CONTROLLER:
# CADASTRAR PRODUTO
# ==========================
def cadastrar_produto_controller(

    nome,
    categoria,
    preco_venda,
    quantidade_por_caixa
):

    # Envia dados para model
    cadastrar_produto(
        nome,
        categoria,
        preco_venda,
        quantidade_por_caixa
    )
# ==========================
# CONTROLLER:
# BUSCAR PRODUTO POR ID
# ==========================
def pegar_produto_por_id(

    produto_id
):

    return buscar_produto_por_id(
        produto_id
    )


# ==========================
# CONTROLLER:
# EDITAR PRODUTO
# ==========================
def editar_produto_controller(

    produto_id,

    nome,

    categoria,

    preco_venda,

    quantidade_por_caixa
):

    editar_produto(

        produto_id,

        nome,

        categoria,

        preco_venda,

        quantidade_por_caixa
    )


# ==========================
# CONTROLLER:
# INATIVAR PRODUTO
# ==========================
def inativar_produto_controller(

    produto_id
):

    inativar_produto(
        produto_id
    )

# ==========================
# CONTROLLER:
# ATIVAR PRODUTO
# ==========================
def ativar_produto_controller(

    produto_id
):

    ativar_produto(
        produto_id
    )
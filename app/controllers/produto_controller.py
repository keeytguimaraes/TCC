# Importa funções do model
from app.models.produto_model import (
    listar_produtos,
    listar_produtos_ativos,
    listar_produtos_inativos,
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
# PRODUTOS ATIVOS
# ==========================
def pegar_produtos_ativos():

    return listar_produtos_ativos()


# ==========================
# PRODUTOS INATIVOS
# ==========================
def pegar_produtos_inativos():

    return listar_produtos_inativos()

# ==========================
# CONTROLLER:
# CADASTRAR PRODUTO
# ==========================
def cadastrar_produto_controller(

            nome,
            categoria,
            sabor,
            tipo_embalagem,
            volume,
            preco_venda,
            quantidade_por_caixa,
            vende_por_dose,
            volume_dose_ml,
            imagem
):

    # Envia dados para model
    cadastrar_produto(
            nome,
            categoria,
            sabor,
            tipo_embalagem,
            volume,
            preco_venda,
            quantidade_por_caixa,
            vende_por_dose,
            volume_dose_ml,
            imagem
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

    sabor,

    tipo_embalagem,

    volume,

    preco_venda,

    quantidade_por_caixa,

    vende_por_dose,

    volume_dose_ml
):

    editar_produto(

        produto_id,

    nome,

    categoria,

    sabor,

    tipo_embalagem,

    volume,

    preco_venda,

    quantidade_por_caixa,

    vende_por_dose,

    volume_dose_ml
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
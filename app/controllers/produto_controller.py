# Importa funções do model
from app.models.produto_model import (
    listar_produtos,
    cadastrar_produto,
    listar_categorias
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
    
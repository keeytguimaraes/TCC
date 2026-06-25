# Importa model
from app.models.estoque_model import (
    listar_estoque,
    cadastrar_estoque,
    baixar_estoque,
    buscar_estoque_atual
)


# ==========================
# CONTROLLER:
# PEGAR ESTOQUE
# ==========================
def pegar_estoque():

    return listar_estoque()


# ==========================
# CONTROLLER:
# CADASTRAR ESTOQUE
# ==========================
def cadastrar_estoque_controller(

    produto_id,

    origem_compra_id,
    nome_origem,

    fornecedor_id,
    tipo_entrada,

    quantidade_recebida_caixa,
    quantidade_recebida_unidade,

    preco_total_compra,
    data_entrada
):

    # Envia para model
    cadastrar_estoque(

        produto_id,

        origem_compra_id,
        nome_origem,

        fornecedor_id,
        tipo_entrada,

        quantidade_recebida_caixa,
        quantidade_recebida_unidade,

        preco_total_compra,
        data_entrada
    )

    # ==========================
# CONTROLLER:
# BAIXAR ESTOQUE
# ==========================
def baixar_estoque_controller(

    produto_id,

    quantidade,

    tipo_venda
):

    baixar_estoque(

        produto_id,

        quantidade,

        tipo_venda
    )

    # ==========================
# CONTROLLER:
# BUSCAR ESTOQUE ATUAL
# ==========================
def pegar_estoque_atual(

    produto_id
):

    return buscar_estoque_atual(

        produto_id
    )
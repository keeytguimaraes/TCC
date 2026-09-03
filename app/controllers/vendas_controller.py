# Importa model
from app.models.vendas_model import (

    listar_vendas,
    listar_historico_vendas,
    cadastrar_venda,
    buscar_produtos_venda,
    buscar_detalhes_venda
)


# ==========================
# PEGAR VENDAS
# ==========================
def pegar_vendas():

    vendas = listar_vendas()

    for venda in vendas:

        venda["produtos"] = (

            buscar_produtos_venda(
                venda["id"]
            )
        )

    return vendas
    # return listar_vendas()


# ==========================
# CADASTRAR VENDA
# ==========================
def cadastrar_venda_controller(

    produto_id,

    quantidade,

    tipo_venda,

    valor_recebido,

    status_pagamento
):

    cadastrar_venda(

        produto_id,

        quantidade,

        tipo_venda,

        valor_recebido,

        status_pagamento
    )

# ==========================
# HISTÓRICO DE VENDAS
# ==========================
def pegar_historico_vendas():

    vendas = listar_historico_vendas()

    for venda in vendas:

        venda["produtos"] = (

            buscar_produtos_venda(
                venda["id"]
            )
        )

    return vendas

# ==========================
# PEGAR DETALHES VENDA
# ==========================
def pegar_detalhes_venda(venda_id):

    return buscar_detalhes_venda(
        venda_id
    )
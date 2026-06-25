# Importa model
from app.models.vendas_model import (

    listar_vendas,
    cadastrar_venda,
    buscar_produtos_venda
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
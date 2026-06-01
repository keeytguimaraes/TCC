# Importa model
from app.models.vendas_model import (

    listar_vendas,
    cadastrar_venda
)


# ==========================
# PEGAR VENDAS
# ==========================
def pegar_vendas():

    return listar_vendas()


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
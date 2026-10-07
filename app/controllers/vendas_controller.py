# Importa model
from app.models.vendas_model import (

    listar_vendas,
    listar_historico_vendas,
    cadastrar_venda,
    buscar_produtos_venda,
    buscar_detalhes_venda,
    buscar_produtos_todas_vendas,
)


# ==========================
# PEGAR VENDAS
# ==========================
def pegar_vendas():

    vendas = listar_vendas()

    produtos = buscar_produtos_todas_vendas()

    produtos_por_venda = {}

    for produto in produtos:

        venda_id = produto["venda_id"]

        if venda_id not in produtos_por_venda:
            produtos_por_venda[venda_id] = []

        produtos_por_venda[venda_id].append(
            produto
        )

    for venda in vendas:

        venda["produtos"] = (
            produtos_por_venda.get(
                venda["id"],
                []
            )
        )

    return vendas

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

    produtos = buscar_produtos_todas_vendas()

    from collections import defaultdict

    produtos_por_venda = defaultdict(list)

    for produto in produtos:
        produtos_por_venda[
        produto["venda_id"]
    ].append(produto)

    for venda in vendas:

        venda["produtos"] = (
            produtos_por_venda.get(
                venda["id"],
                []
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
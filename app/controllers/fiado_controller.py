# Importa model
from app.models.fiado_model import (

    listar_fiados,

    buscar_produtos_fiado,

    buscar_fiado_por_id,

    atualizar_saldo_fiado,

    registrar_recebimento_fiado,

    buscar_recebimentos_fiado,

    buscar_conta_por_cliente,

    buscar_fichas_fiado
)


# ==========================
# LISTAR FIADOS
# ==========================
def pegar_fiados():

    fiados = listar_fiados()

    for fiado in fiados:

        produtos = buscar_produtos_fiado(
            fiado["id"]
        )

        agrupados = {}

        for produto in produtos:

            chave = (
                produto["nome"],
                produto["tipo_venda"]
            )

            if chave not in agrupados:

                agrupados[chave] = produto.copy()

            else:

                agrupados[chave]["quantidade"] += (
                    produto["quantidade"]
                )

        fiado["produtos"] = list(
            agrupados.values()
        )

        fiado["recebimentos"] = (
            buscar_recebimentos_fiado(
                fiado["id"]
            )
        )

    return fiados


# ==========================
# RECEBER PAGAMENTO FIADO
# ==========================
def receber_pagamento_fiado(

    conta_id,

    valor_recebido
):

    fiado = buscar_fiado_por_id(

        conta_id
    )

    saldo_atual = float(

        fiado["saldo_devedor"]
    )

    novo_saldo = (

        saldo_atual
        - float(valor_recebido)
    )

    registrar_recebimento_fiado(

        conta_id,

        valor_recebido
    )

    if novo_saldo <= 0:

        novo_saldo = 0

        status_conta = (
            "quitada"
        )

    else:

        status_conta = (
            "aberta"
        )

    atualizar_saldo_fiado(

        conta_id,

        novo_saldo,

        status_conta
    )


# ==========================
# DETALHES DO FIADO
# ==========================
def pegar_fiado_detalhes(conta_id):

    # Busca dados da conta
    fiado = buscar_fiado_por_id(
        conta_id
    )

    # Busca produtos
    produtos = buscar_produtos_fiado(
        conta_id
    )

    # Busca fichas da sinuca
    fichas = buscar_fichas_fiado(
        conta_id
    )

    # Adiciona fichas junto dos produtos
    for ficha in fichas:

        produtos.append({

            "nome": "Ficha",

            "quantidade": ficha[
                "quantidade_fichas"
            ],

            "tipo_venda": "Sinuca"
        })

    # Agrupa itens repetidos
    agrupados = {}

    for produto in produtos:

        chave = (
            produto["nome"],
            produto["tipo_venda"]
        )

        if chave not in agrupados:

            agrupados[chave] = (
                produto.copy()
            )

        else:

            agrupados[chave][
                "quantidade"
            ] += produto[
                "quantidade"
            ]

    fiado["produtos"] = list(
        agrupados.values()
    )

    # Busca recebimentos
    fiado["recebimentos"] = (
        buscar_recebimentos_fiado(
            conta_id
        )
    )

    return fiado


# ==========================
# BUSCAR CONTA PELO CLIENTE
# ==========================
def pegar_conta_cliente(

    cliente_id
):

    return buscar_conta_por_cliente(
        cliente_id
    )
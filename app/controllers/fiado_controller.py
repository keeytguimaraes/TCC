from app.models.fiado_model import (

    listar_fiados,

    buscar_produtos_fiado,

    buscar_fiado_por_id,

    atualizar_saldo_fiado,

    registrar_recebimento_fiado,

    buscar_recebimentos_fiado
)


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

                agrupados[chave]["quantidade"] += produto["quantidade"]

        fiado["produtos"] = list(
            agrupados.values()
        )

        fiado["recebimentos"] = buscar_recebimentos_fiado(
            fiado["id"]
        )

    return fiados

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
def pegar_fiado_detalhes(conta_id):

    fiado = buscar_fiado_por_id(
        conta_id
    )

    fiado["produtos"] = buscar_produtos_fiado(
        conta_id
    )

    fiado["recebimentos"] = buscar_recebimentos_fiado(
        conta_id
    )

    return fiado
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

     fiado["produtos"] = (

         buscar_produtos_fiado(
             fiado["id"]
         )
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

    venda_id,

    valor_recebido
):

    fiado = buscar_fiado_por_id(

        venda_id
    )

    saldo_atual = float(

        fiado["saldo_devedor"]
    )

    novo_saldo = (

        saldo_atual
        - float(valor_recebido)
    )
    registrar_recebimento_fiado(

    venda_id,

    valor_recebido
    )

    if novo_saldo <= 0:

        novo_saldo = 0

        status_pagamento = (
            "Pago"
        )

    else:

        status_pagamento = (
            "Pendente"
        )

    atualizar_saldo_fiado(

        venda_id,

        novo_saldo,

        status_pagamento
    )
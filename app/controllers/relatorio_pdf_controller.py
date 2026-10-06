from app.models.relatorio_pdf_model import (
    buscar_vendas_periodo,
    total_vendas_periodo,
    faturamento_periodo,
    ticket_medio_periodo,
    quantidade_pagas_periodo,
    quantidade_pendentes_periodo,
    total_recebido_periodo,
    total_pendente_periodo,
    buscar_vendas_dia,
    resumo_fechamento_dia
)

def pegar_vendas_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

    return buscar_vendas_periodo(
        data_inicial,
        data_final,
        tipo_vendas
    )

def pegar_resumo_periodo(
    data_inicial,
    data_final,
    tipo_vendas
):

    return {

        "total_vendas":
        total_vendas_periodo(
            data_inicial,
            data_final,
            tipo_vendas
        ),

        "faturamento":
        faturamento_periodo(
            data_inicial,
            data_final,
            tipo_vendas
        ),

        "ticket_medio":
        ticket_medio_periodo(
            data_inicial,
            data_final,
            tipo_vendas
        ),

        "pagas":
    quantidade_pagas_periodo(
        data_inicial,
        data_final,
        tipo_vendas
    ),

        "pendentes":
    quantidade_pendentes_periodo(
        data_inicial,
        data_final,
        tipo_vendas
    ),

        "recebido":
    total_recebido_periodo(
        data_inicial,
        data_final,
        tipo_vendas
    ),

    "pendente":
    total_pendente_periodo(
        data_inicial,
        data_final,
        tipo_vendas
    )
}

def pegar_fechamento_dia(
    data
):

    return buscar_vendas_dia(
        data
    )

def pegar_resumo_fechamento(
    data
):

    return resumo_fechamento_dia(
        data
    )
# Importa as funções do model responsáveis
# pela geração de relatórios PDF e cálculos
# estatísticos do período selecionado.
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


# ==================================================
# LISTAR VENDAS DO PERÍODO
# ==================================================
#
# Busca todas as vendas realizadas dentro
# do período informado pelo usuário.
#
# Também permite filtrar por tipo
# de venda.
#
# Os dados retornados são utilizados
# para geração dos relatórios PDF.
#
# ==================================================

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


# ==================================================
# RESUMO ESTATÍSTICO DO PERÍODO
# ==================================================
#
# Reúne os principais indicadores
# financeiros do período informado.
#
# Indicadores:
#
# - Quantidade de vendas
# - Faturamento total
# - Ticket médio
# - Vendas pagas
# - Vendas pendentes
# - Valor recebido
# - Valor pendente
#
# O resultado é retornado em formato
# de dicionário para facilitar o uso
# na geração do PDF.
#
# ==================================================

def pegar_resumo_periodo(

    data_inicial,

    data_final,

    tipo_vendas
):

    return {

        # Quantidade total de vendas
        "total_vendas":
        total_vendas_periodo(

            data_inicial,

            data_final,

            tipo_vendas
        ),

        # Soma do faturamento
        "faturamento":
        faturamento_periodo(

            data_inicial,

            data_final,

            tipo_vendas
        ),

        # Valor médio por venda
        "ticket_medio":
        ticket_medio_periodo(

            data_inicial,

            data_final,

            tipo_vendas
        ),

        # Quantidade de vendas pagas
        "pagas":
        quantidade_pagas_periodo(

            data_inicial,

            data_final,

            tipo_vendas
        ),

        # Quantidade de vendas pendentes
        "pendentes":
        quantidade_pendentes_periodo(

            data_inicial,

            data_final,

            tipo_vendas
        ),

        # Total efetivamente recebido
        "recebido":
        total_recebido_periodo(

            data_inicial,

            data_final,

            tipo_vendas
        ),

        # Total ainda pendente
        "pendente":
        total_pendente_periodo(

            data_inicial,

            data_final,

            tipo_vendas
        )
    }


# ==================================================
# BUSCAR VENDAS DE UM DIA
# ==================================================
#
# Retorna todas as vendas realizadas
# em uma data específica.
#
# Utilizado principalmente no relatório
# de fechamento diário.
#
# ==================================================

def pegar_fechamento_dia(

    data
):

    return buscar_vendas_dia(
        data
    )


# ==================================================
# RESUMO DO FECHAMENTO DIÁRIO
# ==================================================
#
# Calcula os indicadores do fechamento
# de uma data específica.
#
# Os dados retornados normalmente incluem
# totais de vendas, faturamento e demais
# informações utilizadas no PDF.
#
# ==================================================

def pegar_resumo_fechamento(

    data
):

    return resumo_fechamento_dia(
        data
    )
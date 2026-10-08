# Importa as funções do model responsáveis
# pelos cálculos e indicadores exibidos
# nos relatórios do sistema.
from app.models.relatorio_model import (

    total_vendido_hoje,

    total_vendido_mes,

    total_fiados,

    total_pendencias
)


# ==================================================
# GERAR RELATÓRIO GERAL
# ==================================================
#
# Esta função centraliza os principais
# indicadores utilizados na tela de
# relatórios do sistema.
#
# Para cada indicador é realizada uma
# consulta específica através do model.
#
# Indicadores retornados:
#
# - Total vendido hoje
# - Total vendido no mês
# - Total de fiados
# - Total de pendências
#
# O resultado é retornado em formato
# de dicionário para facilitar o uso
# nos templates HTML.
#
# Fluxo:
#
# Route → Controller → Model → Banco
#
# ==================================================

def pegar_relatorio():

    return {

        # Soma de todas as vendas realizadas
        # na data atual.
        "vendido_hoje":
        total_vendido_hoje(),

        # Soma de todas as vendas realizadas
        # durante o mês atual.
        "vendido_mes":
        total_vendido_mes(),

        # Valor total dos fiados registrados
        # no sistema.
        "fiados":
        total_fiados(),

        # Valor total das contas pendentes
        # registradas atualmente.
        "pendencias":
        total_pendencias()
    }
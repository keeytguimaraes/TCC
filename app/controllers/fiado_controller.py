# Importa as funções do model responsáveis
# pelas operações relacionadas aos fiados.
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


# ==================================================
# AGRUPAR PRODUTOS REPETIDOS
# ==================================================
#
# Esta função recebe uma lista de produtos
# e agrupa os itens que possuem o mesmo
# nome e o mesmo tipo de venda.
#
# Exemplo:
#
# Coca-Cola | Unidade | Quantidade 1
# Coca-Cola | Unidade | Quantidade 2
#
# Resultado:
#
# Coca-Cola | Unidade | Quantidade 3
#
# O objetivo é evitar que produtos iguais
# apareçam repetidos na tela.
#
# ==================================================

def agrupar_produtos(produtos):

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

    return list(
        agrupados.values()
    )


# ==================================================
# LISTAR FIADOS
# ==================================================
#
# Busca todas as contas fiadas cadastradas
# no sistema.
#
# Para cada conta encontrada:
#
# - Busca os produtos relacionados.
# - Agrupa produtos repetidos.
# - Busca o histórico de recebimentos.
#
# O resultado final é utilizado para
# preencher a tela principal de fiados.
#
# ==================================================

def pegar_fiados():

    fiados = listar_fiados()

    for fiado in fiados:

        produtos = buscar_produtos_fiado(
            fiado["id"]
        )

        fiado["produtos"] = (
            agrupar_produtos(produtos)
        )

        fiado["recebimentos"] = (
            buscar_recebimentos_fiado(
                fiado["id"]
            )
        )

    return fiados


# ==================================================
# RECEBER PAGAMENTO FIADO
# ==================================================
#
# Esta função registra um pagamento realizado
# em uma conta fiada.
#
# Fluxo:
#
# 1. Busca a conta.
# 2. Obtém o saldo atual.
# 3. Calcula o novo saldo.
# 4. Registra o recebimento.
# 5. Atualiza o saldo da conta.
# 6. Caso a dívida seja quitada,
#    altera o status para "Quitada".
#
# ==================================================

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
            "Quitada"
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


# ==================================================
# DETALHES DO FIADO
# ==================================================
#
# Monta todas as informações necessárias
# para exibir a tela de detalhes de uma
# conta fiada específica.
#
# Informações carregadas:
#
# - Dados da conta
# - Produtos comprados
# - Fichas de sinuca
# - Histórico de recebimentos
#
# Produtos e fichas são agrupados para
# evitar repetições na interface.
#
# ==================================================

def pegar_fiado_detalhes(conta_id):

    # Busca os dados principais da conta
    fiado = buscar_fiado_por_id(
        conta_id
    )

    # Busca todos os produtos associados
    # à conta fiada.
    produtos = buscar_produtos_fiado(
        conta_id
    )

    # Busca as fichas de sinuca associadas
    # à conta.
    fichas = buscar_fichas_fiado(
        conta_id
    )

    # Converte as fichas em itens para que
    # possam ser exibidas juntamente com
    # os demais produtos.
    for ficha in fichas:

        produtos.append({

            "nome": "Ficha",

            "quantidade": ficha[
                "quantidade_fichas"
            ],

            "tipo_venda": "Sinuca"
        })

    # Agrupa produtos repetidos.
    fiado["produtos"] = (
        agrupar_produtos(produtos)
    )

    # Busca todos os recebimentos já
    # registrados para esta conta.
    fiado["recebimentos"] = (
        buscar_recebimentos_fiado(
            conta_id
        )
    )

    return fiado


# ==================================================
# BUSCAR CONTA PELO CLIENTE
# ==================================================
#
# Localiza a conta fiada associada
# a um cliente específico.
#
# O cliente é identificado através
# do ID recebido pela rota.
#
# ==================================================

def pegar_conta_cliente(

    cliente_id
):

    return buscar_conta_por_cliente(
        cliente_id
    )
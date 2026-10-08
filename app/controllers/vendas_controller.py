# Importa funções do model relacionadas
# às vendas do sistema.
from app.models.vendas_model import (

    listar_vendas,

    listar_historico_vendas,

    cadastrar_venda,

    buscar_produtos_venda,

    buscar_detalhes_venda,

    buscar_produtos_todas_vendas,
)

from collections import defaultdict


# ==================================================
# ANEXAR PRODUTOS ÀS VENDAS
# ==================================================
#
# Recebe uma lista de vendas e adiciona
# em cada venda os respectivos produtos.
#
# Isso evita repetição de código entre
# as telas de vendas e histórico.
#
# ==================================================

def anexar_produtos_vendas(vendas):

    produtos = buscar_produtos_todas_vendas()

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


# ==================================================
# LISTAR VENDAS
# ==================================================
#
# Retorna as vendas atualmente abertas
# ou disponíveis na tela principal.
#
# Também adiciona os produtos de cada
# venda para facilitar a exibição.
#
# ==================================================

def pegar_vendas():

    vendas = listar_vendas()

    return anexar_produtos_vendas(
        vendas
    )


# ==================================================
# CADASTRAR VENDA
# ==================================================
#
# Envia os dados da venda para o model.
#
# O controller não realiza cálculos,
# apenas encaminha os dados.
#
# ==================================================

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


# ==================================================
# HISTÓRICO DE VENDAS
# ==================================================
#
# Retorna as vendas finalizadas
# registradas no sistema.
#
# Também adiciona os produtos
# relacionados a cada venda.
#
# ==================================================

def pegar_historico_vendas():

    vendas = listar_historico_vendas()

    return anexar_produtos_vendas(
        vendas
    )


# ==================================================
# DETALHES DA VENDA
# ==================================================
#
# Retorna todas as informações
# de uma venda específica.
#
# ==================================================

def pegar_detalhes_venda(

    venda_id
):

    return buscar_detalhes_venda(
        venda_id
    )
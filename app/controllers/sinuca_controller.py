# Importa as funções do model responsáveis
# pelas operações relacionadas à sinuca.
from app.models.sinuca_model import (

    buscar_config_sinuca,

    pegar_fichas_venda,

    atualizar_config_sinuca,

    pegar_relatorio_sinuca
)

# Importa a sessão do usuário
# utilizada para armazenar o carrinho.
from flask import session


# ==================================================
# BUSCAR CONFIGURAÇÃO DA SINUCA
# ==================================================
#
# Retorna a configuração atual da sinuca.
#
# Informações normalmente retornadas:
#
# - Nome da mesa
# - Valor da ficha
# - Percentual do comércio
#
# ==================================================

def pegar_config_sinuca():

    return buscar_config_sinuca()


# ==================================================
# ADICIONAR FICHA AO CARRINHO
# ==================================================
#
# Adiciona uma ficha de sinuca ao carrinho
# armazenado na sessão.
#
# Regras:
#
# - Se não existir configuração da sinuca,
#   a operação é interrompida.
#
# - Se a ficha já estiver no carrinho,
#   apenas aumenta a quantidade.
#
# - Caso contrário, cria um novo item.
#
# ==================================================

def adicionar_ficha_carrinho():

    # Busca a configuração atual
    # da sinuca.
    config = buscar_config_sinuca()

    # Se não existir configuração,
    # interrompe a operação.
    if not config:

        return

    # Obtém o valor unitário da ficha.
    valor_ficha = float(
        config["valor_ficha"]
    )

    # Cria o carrinho caso ele ainda
    # não exista na sessão.
    if "carrinho" not in session:

        session["carrinho"] = []

    carrinho = session["carrinho"]

    # Procura uma ficha já existente
    # dentro do carrinho.
    item_sinuca = None

    for item in carrinho:

        if item.get("tipo_item") == "sinuca":

            item_sinuca = item

            break

    # =================================
    # FICHA JÁ EXISTENTE
    # =================================

    if item_sinuca:

        item_sinuca["quantidade"] += 1

        item_sinuca["subtotal"] = (

            item_sinuca["quantidade"]

            * item_sinuca["preco_unitario"]
        )

    # =================================
    # NOVA FICHA
    # =================================

    else:

        carrinho.append({

            "tipo_item": "sinuca",

            "nome": "Ficha de Sinuca",

            "imagem": None,

            "quantidade": 1,

            "preco_original": valor_ficha,

            "preco_unitario": valor_ficha,

            "subtotal": valor_ficha
        })

    # Atualiza a sessão para que
    # as alterações sejam persistidas.
    session["carrinho"] = carrinho

    session.modified = True


# ==================================================
# BUSCAR FICHAS DE UMA VENDA
# ==================================================
#
# Retorna todas as fichas de sinuca
# registradas em uma venda específica.
#
# ==================================================

def buscar_fichas_venda(venda_id):

    return pegar_fichas_venda(
        venda_id
    )


# ==================================================
# SALVAR CONFIGURAÇÃO DA SINUCA
# ==================================================
#
# Atualiza as configurações da sinuca.
#
# Informações atualizadas:
#
# - Nome da mesa
# - Valor da ficha
# - Percentual do comércio
#
# ==================================================

def salvar_config_sinuca(

    nome,

    valor_ficha,

    percentual_comercio
):

    atualizar_config_sinuca(

        nome,

        valor_ficha,

        percentual_comercio
    )


# ==================================================
# RELATÓRIO DA SINUCA
# ==================================================
#
# Calcula os indicadores financeiros
# relacionados à sinuca.
#
# Retorna:
#
# - Quantidade total de fichas
# - Valor arrecadado
# - Valor destinado ao comércio
# - Valor destinado ao dono da mesa
#
# ==================================================

def pegar_dados_relatorio_sinuca():

    dados = pegar_relatorio_sinuca()

    config = buscar_config_sinuca()

    percentual = float(
        config["percentual_comercio"]
    )

    arrecadado = float(
        dados["valor_arrecadado"] or 0
    )

    # Calcula a parte do comércio.
    valor_comercio = (
        arrecadado * percentual
    ) / 100

    # Calcula a parte do dono
    # da mesa de sinuca.
    valor_dono = (
        arrecadado - valor_comercio
    )

    return {

        "total_fichas":
        dados["total_fichas"] or 0,

        "valor_arrecadado":
        arrecadado,

        "valor_comercio":
        valor_comercio,

        "valor_dono":
        valor_dono
    }
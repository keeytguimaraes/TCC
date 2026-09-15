# Importa model
from app.models.sinuca_model import (

    buscar_config_sinuca,

    pegar_fichas_venda,

    atualizar_config_sinuca,

    pegar_relatorio_sinuca
)

# Importa sessão
from flask import session


# ==========================
# PEGAR CONFIGURAÇÃO DA SINUCA
# ==========================
def pegar_config_sinuca():

    return buscar_config_sinuca()


# ==========================
# ADICIONAR FICHA AO CARRINHO
# ==========================
def adicionar_ficha_carrinho():

    # Busca configuração ativa
    config = buscar_config_sinuca()

    # Se não existir configuração
    if not config:

        return

    # Valor da ficha
    valor_ficha = float(
        config["valor_ficha"]
    )

    # Cria carrinho se não existir
    if "carrinho" not in session:

        session["carrinho"] = []

    carrinho = session["carrinho"]

    # Procura ficha já existente
    item_sinuca = None

    for item in carrinho:

        if item.get("tipo_item") == "sinuca":

            item_sinuca = item

            break

    # ==========================
    # SE JÁ EXISTE
    # ==========================
    if item_sinuca:

        item_sinuca["quantidade"] += 1

        item_sinuca["subtotal"] = (

            item_sinuca["quantidade"]

            * item_sinuca["preco_unitario"]
        )

    # ==========================
    # NOVO ITEM
    # ==========================
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

    # Atualiza sessão
    session["carrinho"] = carrinho

    session.modified = True

# ==========================
# BUSCAR FICHAS DA SINUCA PARA VENDA
# ==========================
def buscar_fichas_venda(venda_id):

    return pegar_fichas_venda(
        venda_id
    )

# ==========================
# SALVAR CONFIGURAÇÃO
# ==========================
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

# ==========================
# RELATÓRIO DA SINUCA
# ==========================
def pegar_dados_relatorio_sinuca():

    dados = pegar_relatorio_sinuca()

    config = buscar_config_sinuca()

    percentual = float(
        config["percentual_comercio"]
    )

    arrecadado = float(
        dados["valor_arrecadado"] or 0
    )

    valor_comercio = (
        arrecadado * percentual
    ) / 100

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
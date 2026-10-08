# Importa as funções do model responsáveis
# pelas operações relacionadas ao estoque.
from app.models.estoque_model import (
    listar_estoque,
    cadastrar_estoque,
    baixar_estoque,
    buscar_estoque_atual,
    listar_estoque_atual,
    buscar_detalhes_produto
)


# ==================================================
# LISTAR MOVIMENTAÇÕES DE ESTOQUE
# ==================================================
#
# Solicita ao model todas as entradas
# registradas no estoque.
#
# Os dados retornados serão utilizados
# para preencher a tabela principal
# da tela de estoque.
#
# ==================================================

def pegar_estoque():

    return listar_estoque()


# ==================================================
# CADASTRAR ENTRADA DE ESTOQUE
# ==================================================
#
# Recebe os dados informados no formulário
# de entrada de mercadorias e encaminha
# para o model realizar o cadastro.
#
# O controller não realiza cálculos
# nem acessa o banco diretamente.
#
# Fluxo:
#
# Route → Controller → Model → Banco
#
# ==================================================

def cadastrar_estoque_controller(

    produto_id,

    origem_compra_id,
    nome_origem,

    fornecedor_id,
    tipo_entrada,

    quantidade_recebida_caixa,
    quantidade_recebida_unidade,

    preco_total_compra,
    data_entrada
):

    cadastrar_estoque(

        produto_id,

        origem_compra_id,
        nome_origem,

        fornecedor_id,
        tipo_entrada,

        quantidade_recebida_caixa,
        quantidade_recebida_unidade,

        preco_total_compra,
        data_entrada
    )


# ==================================================
# BAIXAR ESTOQUE
# ==================================================
#
# Solicita ao model a redução da quantidade
# disponível de um produto.
#
# Essa função normalmente é utilizada
# durante o processo de venda.
#
# ==================================================

def baixar_estoque_controller(

    produto_id,

    quantidade,

    tipo_venda
):

    baixar_estoque(

        produto_id,

        quantidade,

        tipo_venda
    )


# ==================================================
# BUSCAR ESTOQUE DE UM PRODUTO
# ==================================================
#
# Retorna a quantidade atual disponível
# de um produto específico.
#
# O produto é identificado através
# do ID recebido pela rota.
#
# ==================================================

def pegar_estoque_atual(

    produto_id
):

    return buscar_estoque_atual(

        produto_id
    )


# ==================================================
# LISTAR ESTOQUE ATUAL COMPLETO
# ==================================================
#
# Retorna a situação atual de todos
# os produtos cadastrados.
#
# Utilizado principalmente na tela
# de estoque atual.
#
# ==================================================

def pegar_estoque_atual_completo():

    return listar_estoque_atual()


# ==================================================
# DETALHAR PRODUTO DO ESTOQUE
# ==================================================
#
# Busca todas as informações relacionadas
# a um produto específico.
#
# Essas informações são exibidas
# na tela de detalhes do estoque.
#
# ==================================================

def pegar_detalhes_produto_estoque(produto_id):

    return buscar_detalhes_produto(
        produto_id
    )
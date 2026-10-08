# Importa as funções do model responsáveis
# pelas operações relacionadas às movimentações
# de estoque.
from app.models.movimentacao_model import (

    listar_produtos_movimentacao,

    cadastrar_movimentacao,

    listar_movimentacoes
)


# ==================================================
# LISTAR PRODUTOS PARA MOVIMENTAÇÃO
# ==================================================
#
# Busca todos os produtos cadastrados
# que poderão ser utilizados no formulário
# de movimentação de estoque.
#
# Esses produtos serão exibidos no select
# da tela de movimentações.
#
# ==================================================

def pegar_produtos_movimentacao():

    return listar_produtos_movimentacao()


# ==================================================
# CADASTRAR MOVIMENTAÇÃO DE ESTOQUE
# ==================================================
#
# Recebe os dados informados no formulário
# de movimentação e encaminha para o model.
#
# Tipos comuns:
#
# - Entrada
# - Saída
# - Ajuste
# - Perda
#
# O controller não altera quantidades
# diretamente nem acessa o banco.
#
# Fluxo:
#
# Route → Controller → Model → Banco
#
# ==================================================

def cadastrar_movimentacao_controller(

    produto_id,

    tipo_movimentacao,

    quantidade_caixa,

    quantidade_unidade,

    quantidade_fracionada,

    motivo
):

    cadastrar_movimentacao(

        produto_id,

        tipo_movimentacao,

        quantidade_caixa,

        quantidade_unidade,

        quantidade_fracionada,

        motivo
    )


# ==================================================
# HISTÓRICO DE MOVIMENTAÇÕES
# ==================================================
#
# Busca todas as movimentações de estoque
# registradas no sistema.
#
# Os dados retornados são utilizados
# para preencher a tabela de histórico.
#
# ==================================================

def pegar_movimentacoes():

    return listar_movimentacoes()
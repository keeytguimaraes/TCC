from app.models.movimentacao_model import (

    listar_produtos_movimentacao,

    cadastrar_movimentacao
)

from app.models.movimentacao_model import (

    listar_produtos_movimentacao,

    cadastrar_movimentacao,

    listar_movimentacoes
)



def pegar_produtos_movimentacao():

    return listar_produtos_movimentacao()


# ==========================
# CADASTRAR MOVIMENTAÇÃO
# ==========================
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

# ==========================
# HISTÓRICO MOVIMENTAÇÃO
# ==========================
def pegar_movimentacoes():

    return listar_movimentacoes()
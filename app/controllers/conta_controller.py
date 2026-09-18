# Importa model
from app.models.conta_model import (
    listar_contas_pendentes,
    buscar_conta_pendente_por_id,
    buscar_vendas_conta_pendente,
    buscar_produtos_venda,
    buscar_fichas_pendentes
)

# ==========================
# PEGAR CONTAS
# ==========================
def pegar_contas():

    contas = listar_contas_pendentes()

    return contas

# ==========================
# DETALHES CONTA PENDENTE
# ==========================
def pegar_detalhes_conta(conta_id):

    conta = buscar_conta_pendente_por_id(
        conta_id
    )

    vendas = buscar_vendas_conta_pendente(
        conta_id
    )

    conta["valor_total"] = 0

    for venda in vendas:

        conta["valor_total"] += float(
            venda["valor_total"]
        )

        venda["produtos"] = buscar_produtos_venda(
            venda["id"]
        )

        venda["fichas"] = buscar_fichas_pendentes(
            venda["id"]
        )

    conta["vendas"] = vendas

    return conta
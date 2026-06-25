# Importa model
from app.models.conta_model import (
    listar_contas_pendentes,
    buscar_produtos_venda
)


# ==========================
# PEGAR CONTAS
# ==========================
def pegar_contas():

    contas = listar_contas_pendentes()

    for conta in contas:

        conta["produtos"] = (

            buscar_produtos_venda(
                conta["id"]
            )
        )

    return contas
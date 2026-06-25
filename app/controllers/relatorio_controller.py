from app.models.relatorio_model import (

    total_vendido_hoje,

    total_vendido_mes,

    total_fiados,

    total_pendencias
)


def pegar_relatorio():

    return {

        "vendido_hoje":
        total_vendido_hoje(),

        "vendido_mes":
        total_vendido_mes(),

        "fiados":
        total_fiados(),

        "pendencias":
        total_pendencias()
    }